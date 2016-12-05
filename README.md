# hueautotemp
Automation of Philips Hue eco to help adjust circadian rhythm.


Melanopsin(subfamily of the Opsin proteins) is a photosensitive protein found in mammalian retina. When light contacts the human eyes, melonopsin reacts according to the presence of blue light, with peak light absorption at 480nm. As light absorption of melonopsin is increased, a negative correlative relationship with melatonin is exhibited. In other words: the closer we get to 480nm blue light, the brain releases less melatonin, while a decrease from 480nm increases the release of melatonin in the mammalian brain.

As we can see, melanopsin can be partially responsible for the control of circadian rhythm.

By adjusting the amount of blue/red light in cyclical/phasic fashion during the day, we can potentially manipulate our own circadian rhythm. This could be beneficial for anyone hoping to potentially more productive, or to maybe feel better. Those with seasonal depression may find great benefit from such a system.

https://en.wikipedia.org/wiki/Melanopsin
http://s3.amazonaws.com/academia.edu.documents/42833859/Panda_S._et_al._Melanopsin_Opn4_requir20160219-25833-1vm1a2f.pdf?AWSAccessKeyId=AKIAJ56TQJRTWSMTNPEA&Expires=1480642008&Signature=TyDbajhAcqepGK76sTWrANoJ3v4%3D&response-content-disposition=inline%3B%20filename%3DMelanopsin_Opn4_Requirement_for_Normal_L.pdf
http://science.sciencemag.org/content/298/5601/2211

The application constantly signals the Hue bridge by use of the Hue API. For this to work, something needs to be constantly running the program, and having a personal computer or cell phone do that is inconvenient since they are occasionally turned off. A good solution is to a buy a Raspberry Pi Zero for $5, pull out your light switch, and pop the Pi in its place. Raspberry Pi can be powered by the same wires that were being used by the power switch(don't forget to switch breakers off first).


At current the program is very rudimentary:

1.	Simply use linear point approximations with known light temperatures of each phase(start temp and end temp are set) as a dependent values, and times input by user(wake time, length of the day, and how long sundown should be). Program generates simple linear function that can be cycled through its phase, checking the time and setting the according light temperature.

      Method of function call is class based: 
            
            1. Instance of `hueautotemp.lightCalc.LinCalc` is created at the start of each phase
            
            2. `LinCalc.linfunct` is called as an instace variable of the given phase. 
            Recieves the current time (the independent value) as a timedelta vallue
            
            3. Garbage collector end of phase clears the LinCalc object out of memory
            
            4. Repeat until program terminates(bedtime)
            

2.	Make the lights nice!


To use: (assuming RPi talking to router)

1.	in terminal, `arp -a` to find the pi and hue

2.	follow API instructions to create new user and get generated key: http://www.developers.meethue.com/documentation/configuration-api#71_create_user

3.	edit the JSON code in main module to use your new user
      in `autohue.emmiter.SendJSON`
      ```python 
      address = 'http://ADDRESS/api/USER_KEY/lights/3/state/'
      ```

4.	SSH into pi and transfer the script

5.	run it, `~./main.py` and answer the questions. the program will wait until your set waking time and begin its first cycle


cycle = length, starting to ending temp in kelvin

1.	gentle wake = 45min, 2000K to 4500K

2.	transition to day = 15min, 4500K to 6000K

3.	day = length set by user, 6000K to 6000K

4.	first sundown = (3/4)*length set by user, 6000K to 3000K

5.	night phase = (1/4)*length set by user, 3000K to 2000K


future improvements:

-a linear function does an okay job to mimic daylight, but it could be improved. numerical techniques, specifically a cubic polynomial spline interpolation (https://en.wikipedia.org/wiki/Spline_interpolation) would give a nice smooth curve that would better mimic real life temperature change in light. we can use three known points to get our curve: `a(start time, start temp)`, `b(end time/n, some temp)`, `c(end time, end temp)`. 
point b is the point that would decide the curviness of our curve.

-at current, the function itself is computed on a per use basis. it would computationally more efficient to set a function and simply treat it as a scalar

-setting up python celery to manage tasking and not always having to worry whether the system was set

-web functionality: flask framework since this is so simple, and a front end because we like it pretty

-make the lights mimic daylight even more by adding some occasion flutter as if there were clouds passing by

--
//MDorfman
