'''
this module employs modules lightCalc
calculates time values for the time of day
'''

from datetime import timedelta


class TimeCalc:
    def __init__(self, wake_time, day_length, down_length):
        self.wake_time = self.timeconvert(wake_time)
        self.day_length = self.timeconvert(day_length)
        self.down_length = self.timeconvert(down_length)
        # both received as str

    def timeconvert(self, time_in):
        time_in = str(time_in)
        (h,m,s) = (0,0,0)
        try:
            (h,m,s) = time_in.split(':')
        except ValueError:
            try:
                (h,m) = time_in.split(':')
            except ValueError:
                h = time_in

        time_out = timedelta(hours=int(h), minutes=int(m))

        return time_out

    def wakestart(self): # first waking phase start
        wake_time = self.wake_time

        return wake_time

    def wakeend1(self): # first waking phase end and second start
        wake_time = self.wakestart()
        phaseup_a = timedelta(minutes=45) # first waking phase is 45min long
        phaseup_a += wake_time

        return phaseup_a

    def wakeend2(self): # second waking phase end and daytime phase starts
        phaseup_a = self.wakeend1()
        phaseup_b = timedelta(minutes=15) # second waking phase is 15min long
        phaseup_b += phaseup_a

        return phaseup_b

    def dayend(self): # end of daylight phase and start of first sundown phase
        day_start = self.wakeend2()
        day_end = day_start + self.day_length

        return day_end

    def downend1(self):
        day_end = self.dayend()
        phasedown_a = (self.down_length/2)

        phasedown_a += day_end

        return phasedown_a





