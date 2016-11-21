# import datetime
# print(datetime.hour)
#
# time = input('\n what time? ')
#
# print('at', time)
#
#
# # import datetime, time
# #
# #
# # count = 0
# #
# # while count < 20:
# #
# #     print(datetime.datetime.now().second)
# #
# #     time.sleep(3)
# #
# #     count +=1
# #
#
#
# class Dothing:
#
#     def __init__(self):
#         Dothing.a = 1
#         b = 2
#
#     def thing(self):
#
#         print(Dothing.a)
#
#
#
# c = Dothing()
# c.thing()
#
# from _datetime import datetime, timedelta
#
# print (datetime.now())
# print (datetime.now().hour)
# print (datetime.now().minute)
#
# print(datetime.now().strftime("%H %M %S"))
#
# #a = 8.0
#
# #print(datetime.fromtimestamp(a * 600))
#
# b = "8:00"
#
# print(datetime.strptime(b, '%H:%M').strftime("%H %M %S"))
#
# class DoIt:
#     def __init__(self, inputter):
#         self.inputter = inputter
#
#     def returnit(self):
#         print(self.inputter)
#
# z = DoIt('hello')

from datetime import datetime, timedelta
a = '8:00'
b = '0:45'


c = [a, b]
sumit = timedelta()

for i in c:
    (h,m) = i.split(':')
    d = timedelta(hours=int(h), minutes=int(m))

    sumit = sumit + d

print(sumit)

a = timedelta(hours=1, minutes=30).__str__()

print(a)

# a = datetime(hour=1, minute=20)
# b = timedelta(hours=1)
#
# c = a + b
# print(c)

a = timedelta(hours=12, minutes=3, seconds=10)
b = timedelta(hours=2, minutes=3)
d = timedelta(hours=1)

c = a + b
print(c)

e = c + d
print(e)

def do():
    a = True
    while a == True:
        b = input()
        if b == "b":
            a = False
        else:
            print('again')

do()
