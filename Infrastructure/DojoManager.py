import _thread
import random

import paho.mqtt.publish as mqtt_pub
import paho.mqtt.client as mqtt
import json

RANDOM_TOPIC_BID = "RandomTopicBid"

START_RANDOM_DRIVER_BID = "StartRandomDriverBid"

MOBBER_LIST = "MobberList"

TIME_CHANGE = "TimeChange"


class DojoManager(object):
    def __init__(self, controller):
        if not controller.settings_manager.get_dojo_enabled():
            return
        self.switch_dictionary = {
            MOBBER_LIST: self.sub_mobber_list,
            TIME_CHANGE: self.sub_time_change,
            START_RANDOM_DRIVER_BID: self.sub_start_random_driver_bid,
            RANDOM_TOPIC_BID: self.sub_random_topic_bid
        }
        self.station_drivers = {}
        self.controller = controller
        self.dojo_broker = self.controller.settings_manager.get_dojo_broker()
        self.dojo_port = self.controller.settings_manager.get_dojo_port()
        self.dojo_mob_station_name = self.controller.settings_manager.get_dojo_mob_station_name()
        self.dojo_session_id = self.controller.settings_manager.get_dojo_session_id()
        self.dojo_topic_root = self.controller.settings_manager.get_dojo_topic_root()
        self.controller.mobber_manager.subscribe_to_mobber_list_change(self.publish_mobber_list_changes)
        self.controller.time_options_manager.subscribe_to_timechange(self.publish_time_change)
        self.subscribe_to_time_change()

    def publish_time_change(self, time_string, minutes, seconds):
        topic = self.generate_topic(TIME_CHANGE)
        payload_dictionary = {
            "minutes": minutes,
            "seconds": seconds
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
        self.switch_statement_dictionary_trick(station_name, message_type, msg.payload)

    def switch_statement_dictionary_trick(self, station_name, message_type, payload):
        self.switch_dictionary[message_type](station_name, message_type, payload)

    def sub_mobber_list(self, station_name, message_type, payload):
        if not station_name == self.dojo_mob_station_name:
            payload_dictionary = json.loads(payload.decode("utf-8"))
            for mobber in payload_dictionary["mobber_list"]:
                self.controller.mobber_manager.add_mobber(mobber)
        topic = self.generate_topic(START_RANDOM_DRIVER_BID)
        self.publish(topic, "")

    def generate_topic(self, message_type):
        topic = "{}/{}/{}/{}".format(self.dojo_topic_root, self.dojo_session_id, self.dojo_mob_station_name,
                                     message_type)
        return topic

    def sub_time_change(self, station_name, message_type, payload):
        if not station_name == self.dojo_mob_station_name:
            payload_dictionary = json.loads(payload.decode("utf-8"))
            minutes = payload_dictionary["minutes"]
            seconds = payload_dictionary["seconds"]
            if not (
                            self.controller.time_options_manager.minutes == minutes and self.controller.time_options_manager.seconds == seconds):
                self.controller.time_options_manager.set_countdown_time(minutes, seconds)

    def sub_start_random_driver_bid(self, station_name, message_type, payload):
        print(message_type)
        # topic = self.generate_topic(RANDOM_TOPIC_BID)
        # if self.controller.mobber_manager.mobber_list.__len__() > 1:
        #     payload_dictionary = {"bid": random.randint(0, 100),
        #                           "mobber": random.choice(self.controller.mobber_manager.mobber_list)}
        #     self.publish(topic, json.dumps(payload_dictionary))

    def sub_random_topic_bid(self, station_name, message_type, payload):
        print(payload)
        # payload_dictionary = json.loads(payload.decode("utf-8"))
        # self.station_drivers[payload_dictionary["mobber"]] = station_name
        # print(self.station_drivers)
        # self.controller.mobber_manager.fire_time_change_callbacks()

    def subscribe_to_dojo(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.dojo_broker, self.dojo_port, 60)
        client.loop_forever()
