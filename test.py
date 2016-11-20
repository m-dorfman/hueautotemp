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
from _datetime import datetime

print (datetime.now())
print (datetime.now().hour)
print (datetime.now().minute)

print(datetime.now().strftime("%H %M %S"))