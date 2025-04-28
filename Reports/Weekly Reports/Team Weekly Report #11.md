**Team Weekly Report 11**

**Team:** MegaMind  
**Week:** 11  
**Members:** Pravar Chetan, Samuel Huang, Greg Miller, Kyle Stallings

| Status Report |
| :---- |

The project is almost complete. We simplified our preamplifier circuit configuration, making debugging much easier. The prototype still needs to be finalized and soldered, and verified on the software side for data collection. The current preamplifier circuit now uses the AD620 amplifier with a gain 106, the first 3 out of a 5 stage butterworth, two Twin-T notch filters centered at 60 Hz, and a final adjustable gain and offset stage. The current frequency response of this system provides better performance in keeping a maximally flat bandpass with a minimal peak around 50 Hz, and \-6 Db gain at 60Hz.

The software system is almost near completion. The last things that have to be implemented are functions for handling a baseline input and those for testing active for inactive focus. Currently, keypresses are being used to handle these functionalities in the Pong game, but this can be cumbersome to work with. Functions are being made to make this more user friendly.

| Current Status |
| :---- |

1. What did the team work on this past week?  
   

| Task | Task Lead | Status | Notes |
| :---- | :---- | :---- | :---- |
| Final Software System | Kyle Stallings | Near Completion | The software is being refined for a threshold algorithm instead of a machine learning model, which has already been implemented before |
| Final Hardware System | Sam Huang | Nearly Complete | Simplified prototype is complete, just needs to be verified with software before its soldered |

   

2. What feedback has the team received?

| From Whom | Feedback | Next Steps |
| :---- | :---- | :---- |
| NA | NA | NA |

   

3. Are any resources needed? If so, what?

The hardware components are still being swapped in and out as the reliability of the components get tested. We are in the final stages of the project and have all the parts necessary to complete our prototype.

| Plans for Next Week |
| :---- |

What are your plans for this next week?

| Task | Task Lead | Notes |
| :---- | :---- | :---- |
| Finish getting working data  | Kyle/Pravar | While we have some data, ideally more data would allow for a better model |
| Get proper readings with the current hardware. | Kyle/Pravar | The finalized hardware system currently outputs data, but current software processing does not output significant data. |
| Move the circuit to a protoboard | Greg/Sam | To ensure portability and no issues with loose wires |

