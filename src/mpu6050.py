#!/usr/bin/env python

import smbus
from time import sleep

# select the correct i2c bus for this revision of Raspberry Pi
revision = ([l[12:-1] for l in open('/proc/cpuinfo', 'r').readlines() if l[:8] == "Revision"] + ['0000'])[0]
bus = smbus.SMBus(1 if int(revision, 16) >= 4 else 0)

# MPU6050 constants

XG_OFFS_TC = 0x00  # [7] PWR_MODE, [6:1] XG_OFFS_TC, [0] OTP_BNK_VLD
YG_OFFS_TC = 0x01  # [7] PWR_MODE, [6:1] YG_OFFS_TC, [0] OTP_BNK_VLD
ZG_OFFS_TC = 0x02  # [7] PWR_MODE, [6:1] ZG_OFFS_TC, [0] OTP_BNK_VLD
X_FINE_GAIN = 0x03  # [7:0] X_FINE_GAIN
Y_FINE_GAIN = 0x04  # [7:0] Y_FINE_GAIN
Z_FINE_GAIN = 0x05  # [7:0] Z_FINE_GAIN
XA_OFFS_H = 0x06  # [15:0] XA_OFFS
XA_OFFS_L_TC = 0x07
YA_OFFS_H = 0x08  # [15:0] YA_OFFS
YA_OFFS_L_TC = 0x09
ZA_OFFS_H = 0x0A  # [15:0] ZA_OFFS
ZA_OFFS_L_TC = 0x0B
XG_OFFS_USRH = 0x13  # [15:0] XG_OFFS_USR
XG_OFFS_USRL = 0x14
YG_OFFS_USRH = 0x15  # [15:0] YG_OFFS_USR
YG_OFFS_USRL = 0x16
ZG_OFFS_USRH = 0x17  # [15:0] ZG_OFFS_USR
ZG_OFFS_USRL = 0x18
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
FF_THR = 0x1D
FF_DUR = 0x1E
MOT_THR = 0x1F
MOT_DUR = 0x20
ZRMOT_THR = 0x21
ZRMOT_DUR = 0x22
FIFO_EN = 0x23
I2C_MST_CTRL = 0x24
I2C_SLV0_ADDR = 0x25
I2C_SLV0_REG = 0x26
I2C_SLV0_CTRL = 0x27
I2C_SLV1_ADDR = 0x28
I2C_SLV1_REG = 0x29
I2C_SLV1_CTRL = 0x2A
I2C_SLV2_ADDR = 0x2B
I2C_SLV2_REG = 0x2C
I2C_SLV2_CTRL = 0x2D
I2C_SLV3_ADDR = 0x2E
I2C_SLV3_REG = 0x2F
I2C_SLV3_CTRL = 0x30
I2C_SLV4_ADDR = 0x31
I2C_SLV4_REG = 0x32
I2C_SLV4_DO = 0x33
I2C_SLV4_CTRL = 0x34
I2C_SLV4_DI = 0x35
I2C_MST_STATUS = 0x36
INT_PIN_CFG = 0x37
INT_ENABLE = 0x38
DMP_INT_STATUS = 0x39
INT_STATUS = 0x3A
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40
TEMP_OUT_H = 0x41
TEMP_OUT_L = 0x42
GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44
GYRO_YOUT_H = 0x45
GYRO_YOUT_L = 0x46
GYRO_ZOUT_H = 0x47
GYRO_ZOUT_L = 0x48
EXT_SENS_DATA_00 = 0x49
EXT_SENS_DATA_01 = 0x4A
EXT_SENS_DATA_02 = 0x4B
EXT_SENS_DATA_03 = 0x4C
EXT_SENS_DATA_04 = 0x4D
EXT_SENS_DATA_05 = 0x4E
EXT_SENS_DATA_06 = 0x4F
EXT_SENS_DATA_07 = 0x50
EXT_SENS_DATA_08 = 0x51
EXT_SENS_DATA_09 = 0x52
EXT_SENS_DATA_10 = 0x53
EXT_SENS_DATA_11 = 0x54
EXT_SENS_DATA_12 = 0x55
EXT_SENS_DATA_13 = 0x56
EXT_SENS_DATA_14 = 0x57
EXT_SENS_DATA_15 = 0x58
EXT_SENS_DATA_16 = 0x59
EXT_SENS_DATA_17 = 0x5A
EXT_SENS_DATA_18 = 0x5B
EXT_SENS_DATA_19 = 0x5C
EXT_SENS_DATA_20 = 0x5D
EXT_SENS_DATA_21 = 0x5E
EXT_SENS_DATA_22 = 0x5F
EXT_SENS_DATA_23 = 0x60
MOT_DETECT_STATUS = 0x61
I2C_SLV0_DO = 0x63
I2C_SLV1_DO = 0x64
I2C_SLV2_DO = 0x65
I2C_SLV3_DO = 0x66
I2C_MST_DELAY_CTRL = 0x67
SIGNAL_PATH_RESET = 0x68
MOT_DETECT_CTRL = 0x69
USER_CTRL = 0x6A
PWR_MGMT_1 = 0x6B
PWR_MGMT_2 = 0x6C
BANK_SEL = 0x6D
MEM_START_ADDR = 0x6E
MEM_R_W = 0x6F
DMP_CFG_1 = 0x70
DMP_CFG_2 = 0x71
FIFO_COUNTH = 0x72
FIFO_COUNTL = 0x73
FIFO_R_W = 0x74
WHO_AM_I = 0x75

SCALE = 1.0 / 16384.0
G_SCALE = 1.0 / 65.5

class MPU6050:

    address = None

    def __init__(self, address=0x68):
        # 0x68 is the default address        
        self.address = address
        
        # check that this is the right sensor
        whoami = bus.read_byte_data(self.address, WHO_AM_I)
        if 0x68 != whoami:
            raise("expected to read 0x68, but received {}".format(whoami))
        
        # setup the sensor
        # Sets sample rate to 8000/1+7 = 1000Hz
        bus.write_byte_data(self.address, SMPLRT_DIV, 0x07);
        # Disable FSync, 256Hz DLPF
        bus.write_byte_data(self.address, CONFIG, 0x00);
        # Disable gyro self tests, scale of 500 degrees/s
        bus.write_byte_data(self.address, GYRO_CONFIG, 0b00001000);
        # Sets clock source to gyro reference w/ PLL
        bus.write_byte_data(self.address, PWR_MGMT_1, 0b00000010);

    def norm(self, value):
        # is it something with the sign?
        if(value & (1 << 16 - 1)):
            value = value - (1 << 16)
        return value

    def getAccelValuesRaw(self):
        # read all at once:
        # 6 bytes accelerometer
        # 2 bytes temperature
        # 6 bytes gyroscope
        bytes = bus.read_i2c_block_data(self.address, ACCEL_XOUT_H, 6 + 2 + 6)

        # accelerometer
        x = self.norm((bytes[0] << 8) | bytes[1]) 
        y = self.norm((bytes[2] << 8) | bytes[3])
        z = self.norm((bytes[4] << 8) | bytes[5])

        # gyroscope
        gx = self.norm((bytes[8] << 8) | bytes[9])
        gy = self.norm((bytes[10] << 8) | bytes[11])
        gz = self.norm((bytes[12] << 8) | bytes[13])
        return {'x': x, 'y': y, 'z': z, 'gx': gx, 'gy': gy, 'gz': gz}

    def getAccelValuesScaled(self):
        axes = self.getAccelValuesRaw()
        axes['x'] = axes['x'] * SCALE
        axes['y'] = axes['y'] * SCALE
        axes['z'] = axes['z'] * SCALE
        
        axes['gx'] = axes['gx'] * G_SCALE
        axes['gy'] = axes['gy'] * G_SCALE
        axes['gz'] = axes['gz'] * G_SCALE
        
        return axes

    def getAxes(self, gforce = False):
        return self.getAccelValuesScaled()

if __name__ == "__main__":
    # if run directly we'll just create an instance of the class and output 
    # the current readings
    mpu6050 = MPU6050()
    
    axes = mpu6050.getAccelValuesRaw()
    print axes

    axes = mpu6050.getAccelValuesScaled()
    print axes
