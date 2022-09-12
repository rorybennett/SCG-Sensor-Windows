"""
Constants used throughout the application.
"""
# Available return rates for the IMU. The Witmotion library limits the number of return rates that are available.
IMU_RATE_OPTIONS = [
    "0.2Hz",
    "0.5Hz",
    "1Hz",
    "2Hz",
    "5Hz",
    "10Hz",
    "20Hz",
    "50Hz",
    "100Hz",
    "200Hz"
]

# Commonly used baud rates for bluetooth communication.
COMMON_BAUD_RATES = [
    2400,
    4800,
    9600,
    19200,
    38400,
    57600,
    115200,
    230400,
    460800,
    576000
]

# Available bandwidths for the IMU. Higher bandwidths should be used with higher return rates.
IMU_BANDWIDTH_OPTIONS = [
    "256Hz",
    "188Hz",
    "98Hz",
    "42Hz",
    "20Hz",
    "10Hz",
    "5Hz"
]

# Available algorithms for the IMU, either 6-axis (without magnetometer) or 9-axis.
IMU_ALGORITHM_OPTIONS = [
    '6-Axis (without magnetometer)',
    '9-Axis (with magnetometer)'
]
