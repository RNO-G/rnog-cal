import smbus
import math

bus = smbus.SMBus(2) #i2c2 is used on the BBB

adr0 = 0x38
adr1 = 0x3f

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

    else:
        print 'Nothing was changed'

    ##TODO, finish this function


def setAttenuation(atten_value=0):
    '''
    0 = most atten
    63 = least atten
    needs some re-arranging to be monotonic in these units
    '''
    
    ret = getOutputRegisterValue()

    atten_bits = (atten_value & 0x3F) << 2

    new_reg_value = atten_bits | (ret[0] & 0x02)

    write(adr0, output_reg, new_reg_value)
    write(adr0, output_reg, new_reg_value | 0x01) #toggle load enable
    write(adr0, output_reg, new_reg_value)
    
        
if __name__=='__main__':
    '''
    example usage
    '''
    
    ##setup board
    setup() 

    ##set coax output
    setOutput(1)

    ##enable VCO 
    #enableVCO(True)

    ##set pulser option
    selectPulser()

    
    ##set attenuation level
    setAttenuation(63)
    
    
    
