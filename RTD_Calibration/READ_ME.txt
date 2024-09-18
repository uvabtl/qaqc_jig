So you need to find the scale factors again huh. No need to worry. Here is a guide to get you started!

First, delete the temp .log file. If you don't do this, the previous data will still be there, and a new line of ten temperature reads will be added. This will cause confusion. 

Next, place the resistor in one of the slots. You will do this for all  24. For each slot, you need to execute a command line in the terminal that will poll the temperature 10 times. Slides made by Alexander Mayanka Albert explain this deeper. The line to execute is...

python3 temp_calibration_read_RTDs.py <board name> <slot> <front or back> # just to be clear, front="right", back="left"


The board name will be ( 0-7 here).   

The slot will just be a number 0-11. Enter this accordingly for where the resistor is. This reminds me, if the resistor has not changed since August 23 2024, the value is 1100 ohms. If you redo this with so much as 100 ohms less, you will get weird answers. Your log files should read values between 20 and 30 degrees C.  

front will be a and back will be b

Again, do this for all 24 slots.

For each run of the previous command it will store the information into temp.log file. 
To find the scale factors we do the following command:
python3 temp_calibration_compute_factors.py <name of the log file>  <value of resistance in ohms>

More information is found in the slides created by Alex.

An example of what this line may look like may be...

python3 temp_calibration_compute_factors.py temp.log 1100
It will create a json file called scale_factor.log

One last thing, this .json combined file will add brackets at the start and end. As of right now, we use vim magic to fix this. In the future this should be fixed. 

And there you have it. Happy scale factors!

-Sarah Waldych
