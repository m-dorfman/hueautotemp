from autohue import lightCalc, timeVal, userIn

# ask user for times
q = userIn.Schedule()

wake_time = q.waketime()
day_length = q.daylength()
sundown_length = q.sundownlength()

calc = timeVal.TimeCalc(wake_time, day_length, sundown_length)

wake_start = calc.wakestart()  # time to wake
end_wake_1 = calc.wakeend1()   # time to end first waking phase/start of second wake
end_wake_2 = calc.wakeend2()   # time to end second waking phase, end of wake/start of day
end_day = calc.dayend()        # time to end day/start first sundown
down_1_end = calc.downend1()   # time to end first sundown phase/start second waking phase
down_2_end = calc.downend2()   # time to end second sundown phase/night time

(t_wake_up1_start, t_wake_up1_end) = (wake_start, end_wake_1)
(t_wake_up2_start, t_wake_up2_end) = (end_wake_1, end_wake_2)
(t_day_start, t_day_end) = (end_wake_2, end_day)
(t_night_down1_start, t_night_down1_end) = (end_day, down_1_end)
(t_night_down2_start, t_night_down2_end) = (down_1_end, down_2_end)

(k_wake_up1_start, k_wake_up1_end) = (lightCalc.Temperature.wake1())
(k_wake_up2_start, k_wake_up2_end) = (lightCalc.Temperature.wake2())
(k_day_start, k_day_end) = (lightCalc.Temperature.day())
(k_night_down1_start, k_night_down1_end) = (lightCalc.Temperature.down1())
(k_night_down2_start, k_night_down2_end) = (lightCalc.Temperature.down2())

iter_val = [
    ((t_wake_up1_start, t_wake_up1_end), (k_wake_up1_start, k_wake_up1_end)),
            ((t_wake_up2_start, t_wake_up2_end), (k_wake_up2_start, k_wake_up2_end)),
            ((t_day_start, t_day_end), (k_day_start, k_day_end)),
            ((t_night_down1_start, t_night_down1_end), (k_night_down1_start, k_night_down1_end)),
            ((t_night_down2_start, t_night_down2_end), (k_night_down2_start, k_night_down2_end))
            ]

for (t_start, t_end, k_start, k_end) in iter_val:
