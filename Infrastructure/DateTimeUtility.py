import datetime


class DateTimeUtility:
    def get_timestamp(self):
        return datetime.datetime.now().timestamp()
