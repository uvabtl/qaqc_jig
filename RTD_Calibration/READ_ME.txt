So you need to find the scale factors again huh. No need to worry. Here is a guide to get you started!

First, delete all .log files. If you don't do this, the previous data will still be there, and a new line of ten temperature reads will be added. This will cause confusion. No need to worry, all the current scale factors and their uncert are in "combined.json", so all previous data will not be lost :)

Next, place the resistor in one of the slots. You will do this for all  24. For each slot, you need to execute a command line in the terminal that will poll the temperature 10 times. Slides made by Alexander Mayanka Albert explain this deeper. The line to execute is...

python3 temp_calibration_read_RTDs.py <board name> <slot> <front or back> # just to be clear, front="right", back="left"


The board name will be CIT_prod_(insert number 0-7 here). You can do just a number instead of CIT_prod_(number), but then the names of your files will be different. Later down the line I list things to copy and paste, so it might make life a little harder later.  

The slot will just be a number 0-11. Enter this accordingly for where the resistor is. This reminds me, if the resistor has not changed since August 23 2024, the value is 1100 ohms. If you redo this with so much as 100 ohms less, you will get weird answers. Your log files should read values between 20 and 30 degrees C.  

front will be a and back will be b

Again, do this for all 24 slots.

Once you have all the .log files, you then need to make a .json file for all 24 .log files you made. To do this, this line should be executed for all 24 .log files...

python3 temp_calibration_compute_factors.py <path to log file> <value of resistance in ohms>

More information is found in the slides created by Alex.

An example of what this line may look like may be...

python3 temp_calibration_compute_factors.py CIT_prod_0_0_a.log 1100

Once you have all 24 .json files, run this line to combine all 24 .json into one (this will remove all old data)...

jq -s . scale_factor_CIT_prod_0_0_a.json scale_factor_CIT_prod_0_1_a.json scale_factor_CIT_prod_0_2_a.json scale_factor_CIT_prod_1_0_b.json scale_factor_CIT_prod_1_1_b.json scale_factor_CIT_prod_1_2_b.json scale_factor_CIT_prod_2_3_a.json scale_factor_CIT_prod_2_4_a.json scale_factor_CIT_prod_2_5_a.json scale_factor_CIT_prod_3_3_b.json scale_factor_CIT_prod_3_4_b.json scale_factor_CIT_prod_3_5_b.json scale_factor_CIT_prod_4_6_a.json scale_factor_CIT_prod_4_7_a.json scale_factor_CIT_prod_4_8_a.json scale_factor_CIT_prod_5_6_b.json scale_factor_CIT_prod_5_7_b.json scale_factor_CIT_prod_5_8_b.json scale_factor_CIT_prod_6_10_a.json scale_factor_CIT_prod_6_11_a.json scale_factor_CIT_prod_6_9_a.json scale_factor_CIT_prod_7_10_b.json scale_factor_CIT_prod_7_11_b.json scale_factor_CIT_prod_7_9_b.json > combined.json

One last thing, this .json combined file will add brackets at the start and end. As of right now, we use vim magic to fix this. In the future this should be fixed. 

And there you have it. Happy scale factors!

-Sarah Waldych
