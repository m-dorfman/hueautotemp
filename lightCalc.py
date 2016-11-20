'''
this module will calculate the color of temperature
as a function of time
seperated into multiple linear function for initial implementation
'''

from datetime import datetime, time

current_time = datetime.datetime.now()


# class to generate a lin function using point slope
class LinCalc:

    def __init__(self, time_start, time_end, temp_start, temp_end):
        self.time_start = time_start
        self.time_end = time_end
        self.temp_start = temp_start
        self.temp_end = temp_end

        self.slope = (temp_end - temp_start)/(time_end-time_start)
        self.y_int = self.slope * time_start - temp_start

    def linfunct(self, time_point):
        tk = self.slope * time_point - self.y_int

        return tk # tk=light temp in kelvin


class Temperature:

    def __init__(self, time_start):
        self.time_start = time_start

    # def funcgen(self, time_start, time_end, temp_start, temp_end):
    #     func_instance = Calcer(time_start, time_end, temp_start, temp_end)

    def wakeup1(self, time_start, time_end):
        pass

    def wakeup2(self):
        pass

    def day(self):
        pass

    def evedown(self):
        pass

    def nightdown(self):
        pass

