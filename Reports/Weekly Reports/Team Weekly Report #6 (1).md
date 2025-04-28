**Team Weekly Report**

**Team:** MegaMind  
**Week:** 6  
**Members:** Pravar Chetan, Samuel Huang, Greg Miller, Kyle Stallings

| Status Report |
| :---- |

The previous circuit consisted of an AD620 for an amplifier gain stage, a 8-pole butter worth filter for a 55 Hz cutoff point, and a final adjustable gain stage leading to an arduino nano. To make the circuit functional, we have to create a final offset stage to bring the voltage range of the signal to be between 0 and 9V. To do this we had to order a different amplifier that allowed for higher voltage supply, OPA192, we also ordered AD620 chips to see if it alleviates problems with the modules we have been using, such as the gain sensitivity and voltage supply limitations. When testing the chips themselves we found that they were more difficult to work with, but are still trying to get them to work. We have also been looking for a way to convert a 9V battery supply to be used as the 5V and  \-5V.. 

The communication between the Arduino and the Raspberry Pi, and the communication between the Raspberry Pi and the client laptop are working as intended. It is able to transfer information from the EEG headset and add the data collected into a database through socket connections.

| Current Status |
| :---- |

1. What did the team work on this past week?

| Task | Task Lead | Status | Notes |
| :---- | :---- | :---- | :---- |
| Added to capstone report, updating relevant information to the required section for submission | Chetan | Halfway complete | Still need to update necessary system design materials |
| Communication Protocols | Kyle Stallings | Complete | Transfer Speeds are able to transfer close to 20kB / s |

   

2. What feedback has the team received?

| From Whom | Feedback | Next Steps |
| :---- | :---- | :---- |
| NA | NA | NA |

   

3. Are any resources needed? If so, what?

Hardware segments are being tested and integrated within the system. If one segment is able to be completed, then the remaining hardware segments can be ordered / built.

| Plans for Next Week |
| :---- |

What are your plans for this next week?

| Task | Task Lead | Notes |
| :---- | :---- | :---- |
| Design an inverter, AD620 diff amp, offset, adjustable amp, and feedback reducer segment. | Sam Huang/ Gerg | With these four components combined with the buttersworth segments should hopefully give us viable |
| Normalize data collected into proper data formats | Kyle Stallings / Pravar  | Will work direct with hardware side to make modifications |

