import smbus
import math

bus = smbus.SMBus(2) #i2c2 is used on the BBB

adr0 = 0x38
adr1 = 0x3f
adr2 = 0x18 #tmp sensor

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
    
def enableVCO(enable=True):
    '''
    sets VCO as output
    '''
    ret = getOutputRegisterValue()
    
    if enable:
        write(adr1, output_reg, ret[1] | 0x08) #turns on vco power rail
        ret = getOutputRegisterValue()
        write(adr1, output_reg, ret[1] & (~0x40)) #selects vco
        
    else:
        write(adr1, output_reg, ret[1] & (~0x08)) #turns off vco power rail
        selectPulser() #re-selects pulser output


def selectPulser():

    ret = getOutputRegisterValue()
    write(adr1, output_reg, ret[1] | 0x40)
    
def setOutput(select):
    '''
    output select: 
    0 = all off
    1 = coax
    2 = rfof1
    3 = rfof2
    '''

    ret = getOutputRegisterValue()
    
    if select == 1:
        write(adr0, output_reg, ret[0] & (~0x02)) #set out switch 0 to 0
        write(adr1, output_reg, ret[1] & (~0x80)) #set out switch 2 to 0

    elif select == 2:
        write(adr0, output_reg, ret[0] & (~0x02)) #set out switch 0 to 0
        write(adr1, output_reg, ret[1] | (0x80)) #set out switch 2 to 1

    elif select == 3:
        write(adr0, output_reg, ret[0] | (0x02)) #set out switch 0 to 1
        write(adr1, output_reg, ret[1] & (0x20)) #set out switch 1 to 0        
        
    else:
        print 'Nothing was changed'


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

    new_reg_value = atten_bits | (ret[0] & 0x02)

    write(adr0, output_reg, new_reg_value)
    write(adr0, output_reg, new_reg_value | 0x01) #toggle load enable
    write(adr0, output_reg, new_reg_value)

def getTemp(verbose=True):
    '''
    read local temperature sensor (MCP9804)
    probably could be more complicated, but seems to work..
    see datasheet for more information
    '''
    raw = readBlock(adr2, 0x05) #2-byte read
    temp_sign = raw[0] & 0x10

    temp = (raw[0] & 0xF) * 2**4 + raw[1] * 2**(-4)

    ##greater than 0degC-->
    if temp_sign < 1:
        temp = temp
    ##less than 0degC-->
    else:
        #temp = 256.-temp    
        temp = temp-256.
        
    if verbose:
        print 'Board temp:', temp, 'degC'

    return temp
        
if __name__=='__main__':
    '''
    example usage
    '''
    
    ##setup board
    setup() 

    ##read temperature
    getTemp()
    
    ##set coax output
    #setOutput(1)

    ##set RFoF 2 output
    setOutput(3)
    
    ##enable VCO 
    #enableVCO(True)

    ##set pulser option
    selectPulser()

    
    ##set attenuation level
    setAttenuation(48)
    
    
    
