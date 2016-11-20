'''
this module employs modules lightCalc
calculates time values for the time of day
'''

from lightCalc import LinCalc, Temperature
from userin import Schedule

from datetime import datetime

class TimeCalc:
    def __init__(self, wake_time, day_length):
        self.wake_time = wake_time
        self.day_length = day_length

    def wakestart(self):
        wake_time = str(self.wake_time)





