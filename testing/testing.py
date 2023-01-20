from autohue.userIn import Schedule
from autohue.timeVal import TimeCalc
from autohue.lightCalc import Temperature

a = Temperature()

b = a.wake1()

print(b)




z = Schedule()
y = z.waketime()
x = z.daylength()
w = z.sundownlength()

a = TimeCalc(y,x,w)

print(a.wakestart())
print(a.wakeend1())
print(a.wakeend2())
print(a.dayend())
print(a.downend1())
print(a.downend2())
