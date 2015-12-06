import datetime
import time


class CountdownManager(object):
    def __init__(self, root_tk_app):
        self.start_time = time.time()
        self.minutes = 0
        self.seconds = 0
        self.time_change_callbacks = []
        self.count_down_total = datetime.timedelta(minutes=10, seconds=0)

        self.root_tk_app = root_tk_app
        self.refresh_timer()

    def set_countdown_duration(self, minutes, seconds):
        self.start_time = time.time()
        self.minutes = minutes
        self.seconds = seconds
        self.count_down_total = datetime.timedelta(minutes=minutes, seconds=seconds)
        self.fire_time_change_callbacks()

    def subscribe_to_time_changes(self, time_change_callback):
        self.time_change_callbacks.append(time_change_callback)

    def fire_time_change_callbacks(self):
        end_time = time.time()
        up_time = end_time - self.start_time
        remaining_time = self.count_down_total - datetime.timedelta(seconds=(int(up_time)))
        print(remaining_time.days)
        for callback in self.time_change_callbacks:
            if callback:
                callback(remaining_time.days, (remaining_time.seconds // 60) % 60, remaining_time.seconds % 60)

    def refresh_timer(self):
        if self.root_tk_app:
            self.fire_time_change_callbacks()
            self.root_tk_app.after(500, self.refresh_timer)