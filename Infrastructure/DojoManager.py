import _thread
import random
import uuid

import paho.mqtt.publish as mqtt_pub
import paho.mqtt.client as mqtt
import json

MOBBER_LIST = "MobberList"

TIME_CHANGE = "TimeChange"

SAY_HELLO = "SayHello"

START_TIMER = "StartTimer"


class DojoManager(object):
    def __init__(self, controller):
        if not controller.settings_manager.get_dojo_enabled():
            return

        self.time_change_increment = 0
        self.mobber_change_increment = 0
        self.session_id = uuid.uuid4().__str__()


        self.switch_dictionary = {
            MOBBER_LIST: self.sub_mobber_list,
            TIME_CHANGE: self.sub_time_change,
            SAY_HELLO: self.sub_say_hello,
            START_TIMER: self.sub_start_timer,
        }
        self.station_drivers = {}
        self.other_stations = []
        self.controller = controller
        self.dojo_broker = self.controller.settings_manager.get_dojo_broker()
        self.dojo_port = self.controller.settings_manager.get_dojo_port()
        self.dojo_mob_station_name = self.controller.settings_manager.get_dojo_mob_station_name() + uuid.uuid4().__str__()
        self.dojo_session_id = self.controller.settings_manager.get_dojo_session_id()
        self.dojo_topic_root = self.controller.settings_manager.get_dojo_topic_root()
        self.controller.mobber_manager.subscribe_to_mobber_list_change(self.publish_mobber_list_changes)
        self.controller.time_options_manager.subscribe_to_timechange(self.publish_time_change)
        self.subscribe_to_time_change()
        self.say_hello()

    def say_hello(self):
        topic = self.generate_topic(SAY_HELLO)
        self.publish(topic, "")

    def publish_time_change(self, time_string, minutes, seconds, origin_station_name=None):
        topic = self.generate_topic(TIME_CHANGE)
        station_name = self.dojo_mob_station_name
        if origin_station_name is not None:
            return
        payload_dictionary = {
            "minutes": minutes,
            "seconds": seconds,
            "station_name": station_name
        }
        payload = json.dumps(payload_dictionary)
        self.publish(topic, payload)

    def publish_mobber_list_changes(self, mobber_list, driver_index, next_driver_index):
        topic = self.generate_topic(MOBBER_LIST)
        payload_object = {
            "driver_index": driver_index,
            "next_driver_index": next_driver_index,
            "mobber_list": mobber_list
        }
        payload = json.dumps(payload_object)
        self.publish(topic, payload)

    def publish(self, topic, payload):
        _thread.start_new_thread(self.thread_publish, (topic, payload))

    def thread_publish(self, topic, payload):
        mqtt_pub.single(topic, hostname=self.dojo_broker, port=self.dojo_port, payload=payload)

    def subscribe_to_time_change(self):
        _thread.start_new_thread(self.subscribe_to_dojo, ())

    def on_connect(self, client, userdata, flags, rc):
        topic = "{}/{}/#".format(self.dojo_topic_root, self.dojo_session_id)
        client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        topic_parts = msg.topic.split('/')
        topic_root = topic_parts[0]
        session_id = topic_parts[1]
        station_name = topic_parts[2]
        message_type = topic_parts[3]
        print("on_message",msg.topic)
        self.switch_statement_dictionary_trick(station_name, message_type, msg.payload)

    def switch_statement_dictionary_trick(self, station_name, message_type, payload):
        self.switch_dictionary[message_type](station_name, message_type, payload)

    def sub_mobber_list(self, station_name, message_type, payload):
        if not station_name == self.dojo_mob_station_name:
            payload_dictionary = json.loads(payload.decode("utf-8"))
            mobber_list = payload_dictionary["mobber_list"]
            print("sub_mobber_list",mobber_list)
            self.controller.mobber_manager.set_mobber_list(mobber_list)

    def generate_topic(self, message_type):
        topic = "{}/{}/{}/{}".format(self.dojo_topic_root, self.dojo_session_id, self.dojo_mob_station_name,
                                     message_type)
        print("generate_topic",topic)
        return topic

    def sub_time_change(self, station_name, message_type, payload):
        print(payload)
        if not station_name == self.dojo_mob_station_name:
            payload_dictionary = json.loads(payload.decode("utf-8"))
            minutes = payload_dictionary["minutes"]
            seconds = payload_dictionary["seconds"]
            origin_station_name = payload_dictionary["station_name"]
            if not (
                            self.controller.time_options_manager.minutes == minutes and self.controller.time_options_manager.seconds == seconds):
                self.controller.time_options_manager.set_countdown_time(minutes, seconds, origin_station_name)

    def sub_say_hello(self, station_name, message_type, payload):
        if not station_name == self.dojo_mob_station_name:
            if not self.other_stations.__contains__(station_name):
                self.other_stations.append(station_name)
                topic = self.generate_topic(SAY_HELLO)
                self.publish(topic, "")

    def sub_start_timer(self, station_name, message_type, payload):
        if not station_name == self.dojo_mob_station_name:
            self.controller.launch_transparent_countdown_if_blocking()

    def subscribe_to_dojo(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.dojo_broker, self.dojo_port, 60)
        client.loop_forever()

