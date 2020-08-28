from datetime import datetime, timedelta

from custom_components.doorman.yale.exceptions import DataNotValidException

"""
Expiration data container,
 - If the container is valid it will return the data, else returns None
"""
class Expireable():

    """
    Input:
    data - The contaied data
    timestamp - timestamp of creation, if timestamp is None the current time will be used
    time_valid - how long time is the data valid
    buffer - seconds prior to the expiraton time that the container will expire
    """
    def __init__(self, data, time_valid, timestamp=None, buffer=0.0):
        self._data = data
        self.time_valid = time_valid
        self.set_timestamp(timestamp)
        self.buffer = buffer

    def set_timestamp(self, timestamp):
        if timestamp is None:
            self.timestamp = self.get_timestamp_now()
        else:
            self.timestamp = timestamp

    def get_timestamp_now(self):
        return datetime.timestamp(datetime.now())

    """Returns the timestamp that the container expires"""
    @property
    def expiration_time(self):
        return self.timestamp + self.time_valid - self.buffer

    """Returns True if active, false if not"""
    @property
    def is_active(self):
        if self._data == None:
            return False

        if self.expiration_time >= self.get_timestamp_now():
            return True
        else:
            return False

    """ Returns the data if active, else return None"""
    def get_data(self):
        if self.is_active:
            return self._data
        else:
            return None
