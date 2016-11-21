from autohue.userIn import Schedule
from autohue.timeVal import TimeCalc

z = Schedule()
y = z.waketime()
print(y)

wake = 10
daylength = 14
endlength = "3:00"
a = TimeCalc(wake, daylength, endlength)

b = a.wakestart()
print(b)

c = a.wakeend1()
print(c)

d = a.wakeend2()
print(d)

e = a.dayend()
print(e)

f = a.downend1()
print(f)