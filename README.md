# haemoplot
This is a repository for estimating blood loss volume from photographs. The goal is to promote tracking of disease progression in haemophilia and a range of haematological disorders. The main code is ```haemotrack.py``` and uses OpenCV and python to output a simple CSV file from blood volume extracted from uploaded images. 

Right now, datestamps are calculated directly from the image name. The format is ```YYYYMMDD_HHMMSS``` but this can be edited to suit whatever is needed. You can use ```test_plot.py``` to create a basic plot and output the first few rows of the CSV file to help debugging. If there are NaNs in the date column it means that the date has not been able to be extracted from the filename. 

It is assumed that all images to be analysed will be stored in the /images folder. OpenCV does not require any specific layout for photographs but does best at a similar scale and under similar lighting. It calculates the absorbancy of surrounding materials (currently in a limited way) and tries to calculate both unabsorbed and absorbed blood volume. 

Future development will focus on improving and standardising the algorithm and adding pattern segmentation functionality, if possible. The goal will be to help support diagnostics and tracking for bleeding disorders in general. Right now the main disadvantage is threshold recalculation per image which results in inaccuracies -- ```debug_mask.py``` can be used to visualise contours and decide on next steps for more robust development. 

```.gitignore``` is currently set to exclude all input and reference images, extracted data and plots for reassurance and security of health information.
