import wiringpi2

#wiringpi2.wiringPiSetup() # For sequential pin numbering, one of these MUST be called before using IO functions
#wiringpi2.wiringPiSetupSys() # For /sys/class/gpio with GPIO pin numbering
#wiringpi2.wiringPiSetupGpio() # For GPIO pin numbering

wiringpi2.wiringPiSetupGpio() # For GPIO pin numbering


led_output_port=1

# MOTOR DRIVER PORTS

# enable A of the H-bridge
port_motor_left_pwm = 18

# input 1 of the H-bridge
port_motor_left_backward=6

# input 2 of the H-bridge
port_motor_left_forward=16

# enable B of the H-bridge
port_motor_right_pwm = 13

# input 3 of the H-bridge
port_motor_right_backward=20

# input 4 of the H-bridge
port_motor_right_forward=26
