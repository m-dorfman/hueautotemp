# hueautotemp
Automation of Philips Hue eco to help adjust circadian rhythm. 


Melanopsin(subfamily of the Opsin proteins) is a photosensitive prortein found in mammalian retina.
When light contacts the huma eyes, melonopsin reacts according to the presence of blue light, with peak light absorption at 480nm. As light absorption of melonopson is increased, a negative correlative relationship with melatonin is exhibited.
In other words: the closer we get to 480nm blue light, the brain releases less melatonin, while a decrease from 480nm increases the release of melatonin in the mammalian brain.

As we can see, melanopsin can be partially responsible for the control of circadian rhythm.

By adjusting the amount of blue/red light in cyclical/phasic fashion during the day, we can potentially manipulate our own circadian rhythm. This could be beneficial for anyone hoping to potetnitally more productive, or to maybe feel better. Those with seasonal depression may find great benefit from such a system. 

The application constantly signals the Hue bridge by use of the Hue API. For this to work, something needs to be constantly running the program, and having a personal computer or cell phone do that is inconvenient since they are occasionally turned off. A good solution is to a buy a Raspberry Pi Zero for $5, pull out your light switch, and pop the Pi in it's place. Raspberry Pi can be powered by the same wires that were being used by the power switch. 

At current the program is very rudimentary:

1. Simply use linear point approximations with known light temperatures of each pahse(start temp and end temp are set) as a dependent values, and times input by user(wake time, length of the day, and how long sundown should be). Program generates simple linear function that can be cycled through it's phase, checking the time and setting the according light temperature. 

2. make the lights nice!

To use: (assuming RPi talking to router)

1. in terminal 
