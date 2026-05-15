import smbus
import math
import sys

bus = smbus.SMBus(1) #i2c2 is used on the BBB

# check rev 

revF = False
try: 
    with open("/REV") as f:
       revF =  f.read() == "F"

except e:
    pass 

adr0 = 0x38
adr1 = 0x3f
#adr2 = 0x18 #tmp sensor

output_reg = 0x01
config_reg = 0x03

def write(i2c_address, register, cmd):
    '''
    8-bit code write, returns state of acknowledge bit (0=ack, 1=no ack)
    '''
    ack = bus.write_byte_data(i2c_address, register, cmd)

    return ack

def read(i2c_address, register):

    read_data = bus.read_byte_data(i2c_address, register)

    return read_data

def readBlock(i2c_address, register, num_bytes=2):

    read_block_data = bus.read_i2c_block_data(i2c_address, register, num_bytes)

    return read_block_data

def setup():
    '''
    on power-on, i2c expanders need to be config'ed as low and outputs
    '''
    write(adr1, output_reg, 0x00) #set output registers to 0
    write(adr0, output_reg, 0x00)
    write(adr1, config_reg, 0x00) #set as outputs
    write(adr0, config_reg, 0x00)

def getOutputRegisterValue():
    '''
    retrieves current setting of expander outputs
    '''
    val0 = read(adr0, output_reg)
    val1 = read(adr1, output_reg)

    return val0, val1
    
def select_waveform(wavetype):
    ret = getOutputRegisterValue()
    if wavetype == 0:
        write(adr1, output_reg, (ret[1] | 0x40) & (~0x02)) #Set sourceswitch to 1 for pulser and set sine_0_en to 0 for pulser
    elif wavetype == 1:
        write(adr1, output_reg, (ret[1] & (~0x40)) | (0x02)) #set sourceswitch to 0 for sine wave and set sine_0_en to 0 for pulser
        
    
def setOutput(select, bias = True):
    '''
    output select: 
    0 = rf0
    1 = rf1
    2 = rf2
    3 = rf3
    '''

    ret = getOutputRegisterValue()
    
    #turn all rfof biases off:
    write(adr1, output_reg, ret[1] & (~0x1d)) #biases are active high
    
    ret = getOutputRegisterValue()
    
    if select == 0:
        write(adr0, output_reg, ret[0] | (0x02)) #set out switch 0 to 1
        write(adr1, output_reg, ret[1] | (0x20)) #set out switch 1 to 1
        if bias:
            ret = getOutputRegisterValue()
            write(adr1, output_reg, ret[1] | (0x01)) #set en_bias0 to 1
            
    elif select == 1:
        write(adr0, output_reg, ret[0] | (0x02)) #set out switch 0 to 1
        write(adr1, output_reg, ret[1] & (~0x20)) #set out switch 1 to 0
        if bias:
            ret = getOutputRegisterValue()
            write(adr1, output_reg, ret[1] | (0x04)) #set en_bias1 to 1
    elif select == 2:
        write(adr0, output_reg, ret[0] & (~0x02)) #set out switch 0 to 0
        write(adr1, output_reg, ret[1] | (0x80)) #set out switch 2 to 1
        if bias:
            ret = getOutputRegisterValue()
            write(adr1, output_reg, ret[1] | (0x08)) #set en_bias2 to 1
    elif select == 3:
        write(adr0, output_reg, ret[0] & (~0x02)) #set out switch 0 to 0
        write(adr1, output_reg, ret[1] & (~0x80)) #set out switch 2 to 0   
        if bias:
            ret = getOutputRegisterValue()
            write(adr1, output_reg, ret[1] | (0x10)) #set en_bias3 to 1
    else:
        print(f'output {select} is not a valid output, please enter a number from 0-3')


def setAttenuation(atten_value=0):
    '''
    parallel loading into SKY12347: 6-bit step attenuator up to 31.5dB

    0 = most atten
    63 = least atten
    atten_value is bit-reversed before loading (to match schematic)
    '''
    
    ret = getOutputRegisterValue()

    atten_value_reversed = int('{:06b}'.format(atten_value)[::-1],2)
    
    atten_bits = (atten_value_reversed & 0x3F) << 2

    new_reg_value = atten_bits | (ret[0] & 0x02) #keeps outswitch 0 as is

    write(adr0, output_reg, new_reg_value)
    write(adr0, output_reg, new_reg_value | 0x01) #toggle load enable
    write(adr0, output_reg, new_reg_value)
        
if __name__=='__main__':
    '''
    att goes from 0 to 63, 0 is most attenuation and 63 is least attenuation
    output goes from 0 to 3 for rf0 to rf3
    wavetype is 0 for pulse, 1 for 156.25MHz sine wave
    
    example usage:
    python3 cal_revE

    To set up cal driver board to pulse:
    GPIO-SET CAL=EN=1  #To turn on the board
    GPIO-SET GPS_EN=1  #To turn on the GPS board
    GPIO-SET PPS_SELECT=1  #To select the GPS PPS as a trigger for the pulse
    '''
   
    att = int(sys.argv[1])
    output = int(sys.argv[2])
    wavetype = int(sys.argv[3])

    ##setup board
    setup() 

    bias = False #Set to false to turn off biases
    setOutput(output, bias = bias)
    
    select_waveform(wavetype)
    
    ##set attenuation level
    setAttenuation(att)
    
    
    
