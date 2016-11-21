from datetime import timedelta

class Schedule:
    # def __init__(self):

    def timecheck(self, lim, question):
        a = True
        while a == True:
            length = input(question)
            try:
                (h, m, s) = length.split(':')
                try:
                    if (int(h) < lim >= 0) and (int(m) < 60 >= 0) and (int(s) < 60 >= 0):
                        length = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                        return length
                    else:
                        print('some time val is out of range')
                except ValueError:
                    print('some time val is out of range')
            except ValueError:
                try:
                    (h, m) = length.split(':')
                    try:
                        if (int(h) < lim >= 0) and (int(m) < 60 >= 0):
                            length = timedelta(hours=int(h), minutes=int(m))
                            return length
                        else:
                            print('some time val is out of range')
                    except ValueError:
                        print('some time val is out of range')
                except ValueError:
                    try:
                        if int(length) < lim >= 0:
                            h = int(length)
                            return timedelta(hours=h)
                        else:
                            print('some time val is out of range')
                    except ValueError:
                        print('some time val is out of range')

    def waketime(self):
        question = "when will you wake? "
        lim = 24
        wake = self.timecheck(lim, question)
        return wake

    def daylength(self):
        question = "length of daylight? "
        lim = 12
        day_length = self.timecheck(lim, question)
        return day_length

    def sundownlength(self):
        question = "length of sundown? "
        lim = 12
        down_length = self.timecheck(lim, question)
        return down_length