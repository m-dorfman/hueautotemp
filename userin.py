class Schedule:
    # def __init__(self):

    def waketime(self):
        wake = input('\nwhen will you wake? ')
        wake = int(wake)

        return wake

    def daylength(self):
        a = True
        while (a == True):
            b = True
            while (b == True):
                try:
                    day_length = input('\nhow long is daylight? ')
                    (h,m) = day_length.split(':')
                    b = False
                except ValueError:
                    print('format must be hh:mm, for example 00:00')
                    b = True

            if (int(h) <12) and (int(m) <60):
                day_length = '{}:{}'.format(h,m)
                return day_length
            else:
                print('day can\'t be more than 12hrs')


    #def sundownlength(self):

