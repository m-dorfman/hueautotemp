'''
this module will calculate the color of temperature
as a function of time
seperated into multiple linear function for initial implementation
'''

from datetime import datetime, time
from math import ceil

current_time = datetime.now()


# class to generate a lin function using point slope
class LinCalc(object):

    def __init__(self, time_start, time_end, temp_start, temp_end):
        self.time_start = time_start
        self.time_end = time_end
        self.temp_start = temp_start
        self.temp_end = temp_end

        self.slope = (temp_end - temp_start)/(time_end-time_start)
        self.y_int = self.slope * time_start - temp_start

    def linfunct(self, time_point):
        tk = self.slope * time_point - self.y_int

        return tk  # tk=light temp in kelvin


class Temperature(object):

    @staticmethod
    def mired(temp_kelvin):
        m = ceil(1000000.0/temp_kelvin)

        return int(m)

    @staticmethod
    def wake1():
        (temp1, temp2) = (Temperature.mired(2000), Temperature.mired(4500))
        return (temp1, temp2)

    @staticmethod
    def wake2():
        (temp1, temp2) = (Temperature.mired(4500), Temperature.mired(6000))
        return (temp1, temp2)

    @staticmethod
    def day():
        temp = Temperature.mired(6000)
        return temp

    @staticmethod
    def down1():
        (temp1, temp2) = (Temperature.mired(6000), Temperature.mired(3000))
        return (temp1, temp2)

    @staticmethod
    def down2():
        (temp1, temp2) = (Temperature.mired(3000), Temperature.mired(2000))
        return (temp1, temp2)