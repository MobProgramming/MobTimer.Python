class TimeSettingsManager(object):
    def __init__(self):
        self.minutes = 10
        self.seconds = 0
        self.time_change_callbacks = []

    def get_time_string(self):
        return "{0:0>2}:{1:0>2}".format(self.minutes, self.seconds)

    def increment_minutes(self):
        self.minutes += 1
        self.fire_time_change_callbacks()

    def decrement_minutes(self):
        self.minutes -= 1
        if self.minutes < 0:
            self.minutes = 0
        self.fire_time_change_callbacks()

    def increment_seconds(self, increment = 15):
        self.seconds = (self.seconds + increment) % 60
        self.fire_time_change_callbacks()

    def decrement_seconds(self, decriment=60):
        self.seconds = ((self.seconds + decriment) - 15) % 60
        self.fire_time_change_callbacks()

    def subscribe_to_timechange(self, time_change_callback):
        self.time_change_callbacks.append(time_change_callback)
        self.fire_time_change_callbacks()

    def fire_time_change_callbacks(self):
        for time_change_callback in self.time_change_callbacks:
            if time_change_callback:
                time_change_callback(self.get_time_string(), self.minutes, self.seconds)

    def set_countdown_time(self, minutes, seconds):
        self.minutes = minutes
        self.seconds = seconds
        self.fire_time_change_callbacks()