'''
this module employs modules lightCalc
calculates time values for the time of day
'''

from lightCalc import LinCalc, Temperature
from userin import Schedule

from datetime import datetime, timedelta


class TimeCalc:
    def __init__(self, wake_time, day_length):
        self.wake_time = self.timeconvert(wake_time)
        self.day_length = self.timeconvert(day_length)
        # both received as str

    def timeconvert(self, time_in):
        time_in = str(time_in)
        try:
            (h,m) = time_in.split(':')
        except ValueError:
            (h,m,s) = time_in.split(':')
        time_out = timedelta(hours=int(h), minutes=int(m))

        return time_out

    def wakestart(self): # first waking phase start
        wake_time = self.wake_time

        return wake_time

    def wakeend1(self): # first waking phase end and second start
        wake_time = self.wakestart()
        phase_a = timedelta(minutes=45) # first waking phase is 45min long
        phase_a += wake_time

        return phase_a

    def wakeend2(self): # second waking phase end and daytime phase starts
        phase_a = self.wakeend1()
        phase_b = timedelta(minutes=15) # second waking phase is 15min long
        phase_b += phase_a

        return phase_b

    def dayend(self): # end of daylight phase and start of first sundown phase
        day_start = self.wakeend2()
        day_end = day_start + self.day_length

        return day_end



