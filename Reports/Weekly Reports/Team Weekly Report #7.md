**Team Weekly Report**

**Team:** MegaMind  
**Week:** 7  
**Members:** Pravar Chetan, Samuel Huang, Greg Miller, Kyle Stallings

| Status Report |
| :---- |

The first four stages of the EEG prototype have been completed. The ad620 module has been replaced with a single ad620 chip, allowing us to better control the gain and increase our supply voltage. The improved second stage has allowed for better gain in the pass band and higher attenuation rate. The 3rd stage allows for precise gain boost up to the optimal voltage swing. The final stage creates the offset and maximizes the output voltage swing. Each stage was tested for its frequency response and functionality, and integrated into the entire system. Original design schematics used parts that did not work as well in comparison to the simulation. Many problems arose when trying to create the offset for the final stage, with the original OD172 chip used in design did not work so switching the chip to TL071 worked well. Better data visualization and processing has also been started. The program has been able to recreate input signal and frequency but will be improved on to handle the full output signal.

| Current Status |
| :---- |

1. What did the team work on this past week?

| Task | Task Lead | Status | Notes |
| :---- | :---- | :---- | :---- |
| Improved Stage 1 Differential Amplifier Implementation | Sam Huang | Halfway complete |  |
| Improved Stage 2 Low Pass Filter | Sam Huang | Halfway complete | Created a 12th order Butterworth filter to achieve a band pass gain of around 26 DB, with 15dB at 60Hz |
| Improved Stage 3 Adjustable Gain | Sam Huang | Halfway complete | Created an adjustable gain stage allowing for the signal to reach an amplitude of 1.5 V |
| Stage 4 Offset Amplifier | Sam Huang | Complete | Created an amplifier which causes a 1.5V 0-peak signal to maximise the positive voltage range. Create an offset and gain which allows for a voltage swing from 0 to 7.5 (9V \-Headroom voltage). |
| Combine all stages and check for functionality. | Sam Huang | Complete |  |
| Simulate Stage 1 Multisim | Gerg | Complete | Simulated the AD620 AN, and measure associated gain |
| Simulate Stage 2 Multisim | Gerg | Complete | Simulated the band pass filter, and work with values to maximize bandpass gain and minimize gain at 60Hz |
| Simulate Stage 3 Multisim | Gerg | Complete | Simulated adjustable gain stage, to allow for an input of at least .5 to 1.5 V to produce an output of 1.5V 0-to-peak |
| Simulate Stage 4 Multisim | Gerg | Complete | Simulated the offset amplifier, ensure it takes in a value of around 1.5 V and produces an output with maximum swim in the positive voltage range, from o to 7.5. |
| Wave Recreation | Kyle | Complete | Created a program to determine the original input wave magnitude at each frequency. |
| FFT Accuracy Improvement | Kyle | Complete | Improved and tested the FFT program to ensure accuracy. |
| CSV Parser Function | Kyle | Complete | Created a function to Parse and Process a CSV file to get the gain at each frequency, to be later used in the Wave Recreation function |
| Engineering Standards, Regulations, and Considerations | Pravar | Complete | Updated the Engineering Standards, Regulations, and Considerations |
| System Design | Gerg | Complete | Updated the system Design in the Report. |

   

2. What feedback has the team received?

| From Whom | Feedback | Next Steps |
| :---- | :---- | :---- |
| NA | NA | NA |

   

3. Are any resources needed? If so, what?

Hardware segments are being tested and integrated within the system.  The next step is integration of a power supply for the circuit.  WIth the prototype complete, we will need to get more parts to create  multiple nodes.

| Plans for Next Week |
| :---- |

What are your plans for this next week?

| Task | Task Lead | Notes |
| :---- | :---- | :---- |
| Replicate and consolidate Circuit Prototype, using soldered resistors and capacitors to reduce space. | Sam Huang/ Gerg |  |
| Test Neural Case | Kyle Stallings / Pravar  | When connected to the user and the user is not thinking about anything see what the system is showing. |
| Test Wrong Connection Case | Kyle Stallings / Pravar  | If only one node is touching then there will be clipping and as such we should give an error or warning. |
| Test When no one is wearing the system | Kyle Stallings / Pravar  | Make sure that the system is showing a flatline that is not the same as clipping from only having a node on. IE make sure that the value is 0\. |
| Test Signal Fidelity | Kyle Stallings / Pravar | Input signal amplitudes through filter stages 2-4 into the arduino, starting from 10 mA up to 50 mA incrementing by 5 mA each time with frequencies varying from 10 \- 50 Hz incrementing by 5 Hz. Ensure the system does not clip with a 50mA 40 Hz signal beforehand and adjust the adjustable gain if necessary. |
| Update Butterworth | Gerg | Update the sixth stage of the Butterworth system to have a 61k resistor instead of a 100k. |
| Create a CSV function that takes in two files | Kyle Stallings / Pravar | Create a CSV file that takes in the CSV Frequency Response file of the stage 1, and the file of stage 2-4 to get the associated gain magnitude (not in DB) at each frequency. |
| Update the second Twin T | Gerg | Update the values of all resistors and capacitors to be as accurate to what is simulated as possible as the closer the numbers are to each other the deeper the notch. Also consider changing the values in the R3 and R4 setup. |
| Wave Visualizer | Kyle Stallings / Pravar | Create a wave visualization function to display the four wave categories in real time. |

