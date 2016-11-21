# from .lightCalc import Temperature


class Schedule:

    # def __init__(self):

    def waketime(self):
        wake = input('\nwhen will you wake? ')
        wake = int(wake)

        return wake

    def daylength(self):
        length = input('\nhow long is daylight? ')
        length = int(length)
        if length <= 12:
            return length
        else:
            return 11

