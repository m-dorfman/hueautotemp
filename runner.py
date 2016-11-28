from autohue import lightCalc, timeVal, userIn

from datetime import datetime, timedelta, time

question = userIn.Schedule()

a1 = question.waketime()
a2 = question.daylength()
a3 = question.sundownlength()


sched = timeVal.TimeCalc(a1, a2, a3)

b1 = sched.wakestart()
b2 = sched.wakeend2()
b3 = sched.wakeend2()
b4 = sched.dayend()
b5 = sched.downend1()
b6 = sched.downend2().total_seconds()

print(b6)



# def formatter1(time_in):
#     time_in = str(time_in)
#
#     (a, b) = time_in.split(" day, ")
#     (c, d, e) = b.split(":")
#
#     print(a, b, c, d, e)
#
#     a = int(a) *24
#     c = int(c) +a
#     return(c,d,e)
#
# def formatter2(time_in):
#     time_in = str(time_in)
#     (a,b,c) = time_in.split(":")
#
#     return(a,b,c)
#
# if b6 >= timedelta(days=1):
#     print(formatter1(b6))
# else:
#     print(formatter2(b6))

