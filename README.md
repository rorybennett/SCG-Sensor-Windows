# SCG Sensor Windows

Monitor the accelerations produced by a Witmotion IMU. The accelerations are plotted in real-time
and can be logged for further analysis. The data stream from the IMU is plotted unaltered: accelerations in the
X, Y, and Z directions plotted in m/s^2. The acceleration norm is also plotted for reference.

## Hardware Considerations

This project was compiled with specific hardware in mind, but it is not entirely limited to the hardware
used. The hardware used when creating this project, beyond the computer running the software, is a BWT901CL
IMU from Witmotion: [BWT901CL 9-axis](https://www.wit-motion.com/9-axis/witmotion-bluetooth-2-0-mult.html).

Only the acceleration and the timestamp of the IMU is used, in both plotting and data logging, and as such all other
channels can be disabled using the Witmotion application: [Witmotion website](https://www.wit-motion.com/).

The Witmotion IMU should be setup to have a maximum bandwidth (256Hz) if a 200Hz return rate is required. If a lower
bandwidth is set with such a high return the IMU returns the same acceleration values multiple times (up to 5 or
6 repetitions), a higher bandwidth prevents this from happening.

## Overview of Program Functionality

### Basic Operation: IMU Connection

To connect to a WITMOTION IMU select menu 'IMU' -> 'Connect'.

A second window will pop up where you can choose the COM port and baud rate.

Take Note: It is possible for the program to 'connect' to a COM port that does not belong to the IMU.
Once a connection is successful ensure that there are IMU acceleration values appearing in the main
window. If you are sure that the correct COM port is being used and there is a problem with the plot,
ensure that the IMU has been set up to send acceleration data.

Once connected, the return rate of the IMU can be set and the accelerometer can be calibrated in the
'IMU' menu item.

### Basic Operation: Plotting

Once the IMU is connected the program will start plotting data immediately. Any of the acceleration values can
be removed, or shown, in the displayed plot by deselecting, or selecting, their relevant checkboxes respectively.
Even when deselected the plotting data is stored in memory,so when it is selected again there is no gap in the plot
between when it was deselected and reselected.

The plot can be reset: The plotting data is cleared before new data is added.

The total number of points to plot can be changed using the slider: At the moment the return rate of the IMU is not
accessible, so setting a plot size by time is a bit difficult. To calculate expected plot size time take the total
plot points and divide by the return rate of the IMU. E.g. 2000 points / 200 Hz = 10 seconds of plotting data.

### Basic Operation: Logging

Once the IMU is connected, you can log the data that is being sent by the IMU. Logging is independent of plotting,
so if an acceleration is disabled in the plot it will still be logged. All three acceleration values are logged,
X-, Y-, and Z-acceleration, but not the norm, as this can be calculated from the logged data. All logged data
is saved with a time stamp for future reference purposes.

The data is logged in a .txt file using a csv-type format: timestamp,Ax,Ay,Az.

# NB

- WITMOTION does not have any official Python support. The following library was used to enable
  communication with the IMU: [https://pypi.org/project/witmotion/](https://pypi.org/project/witmotion/).
- This project/program is run directly from PyCharm, and if any other libraries are required an error
  message will be shown.