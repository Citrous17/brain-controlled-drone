**Team Weekly Report**

**Team:** MegaMind  
**Week:** 5  
**Members:** Pravar Chetan, Samuel Huang, Greg Miller, Kyle Stallings

| Status Report |
| :---- |

The EEG prototype was further developed this week by implementing a noise filter within the preamplifier. The preamplifier circuit was adjusted to contain three main stages of a microvolt signal differential amplifier, noise filter, and adjustable gain stage. The microvolt signal differential amplifier is currently an AD620 module which is giving the most amount of problems due to the poor quality. The noise filter stage consists of an 8-pole ButterWorth filter at 50 Hz, which attenuates the signal at a rate of \-160 dB per decade. The final stage is an adjustable gain stage using a LM741CD operational amplifier and a 10K pot for an adjustable gain to maximize the input into the ADC (arduino nano). The visualization and Fast Fourier Transform of the data has been started and coded into the Arduino Nano allowing for initial data visualization and processing. 

The frontend code was completed, including a graph to visualize the different brainwave data.  
Control buttons were added for controlling the drone. Buttons to a different page lead the user to train off a user’s brainwaves and to train the model were added. Components were made in a DRY fashion so that they are easily maintainable and reusable.

| Current Status |
| :---- |

1. What did the team work on this past week?

| Task | Task Lead | Status | Notes |
| :---- | :---- | :---- | :---- |
| EEG Filter Configuration | Huang/Miller | Incomplete | Mostly done requires more testing and time to optimize design for signal fidelity |
| EEG prototype | Huang/Miller | Incomplete | Requires preamplifier to be complete before prototype is complete |
| EEG cap | Huang/Miller | Started | Prototype must be complete before this can be implemented |
| Created Frontend | Stallings | Completed | Frontend Design is mainly completed |
| Integrated Backend | Stallings / Chetan | Completed | Backend Schema is complete |
| Created Backedn | Chetan | Completed |  |

   

2. What feedback has the team received?

| From Whom | Feedback | Next Steps |
| :---- | :---- | :---- |
| NA | NA | NA |

   

3. Are any resources needed? If so, what?

No more resources at this time. Perhaps 

| Plans for Next Week |
| :---- |

What are your plans for this next week?

| Task | Task Lead | Notes |
| :---- | :---- | :---- |
| EEG Prototype | Huang/Miller | Worked on over the last couple weeks still not complete |
| EEG signal fidelity check | Huang/Miller | Need to better the design of the preamplifier circuit and signal processing. |
| EEG Prototype testing and part integration | Huang/Miller | Each stage of the pre-amplifier, the differential amplifier, noise filter, adjustable gain stage, ADC component, and microprocessor must be integrated together for a functional prototype.  |
| Update the Machine Learning model and compare results against research paper | Stallings / Chetan | The machine learning model is currently using ReLu on 5 data points |

