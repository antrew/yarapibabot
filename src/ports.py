import wiringpi2

#wiringpi2.wiringPiSetup() # For sequential pin numbering, one of these MUST be called before using IO functions
#wiringpi2.wiringPiSetupSys() # For /sys/class/gpio with GPIO pin numbering
#wiringpi2.wiringPiSetupGpio() # For GPIO pin numbering

wiringpi2.wiringPiSetupGpio() # For GPIO pin numbering


led_output_port=1

# MOTOR DRIVER PORTS

# input 1 of the driver
motor_left_backward=6

# input 2 of the driver
motor_left_forward=13

# input 3 of the driver
motor_right_backward=19

# input 4 of the driver
motor_right_forward=26
