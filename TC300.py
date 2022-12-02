import re
import numpy as np
import pyvisa as visa
from pyvisa import constants

rm = visa.ResourceManager()

# Write command to a device and get it's output
def get(device, command):
    '''device = rm.open_resource() where this function gets all devices initiaals such as adress, baud_rate, data_bits and so on; 
    command = string Standart Commands for Programmable Instruments (SCPI)'''
    #return device.query(command)
    return np.random.random(1)

class TC300():

    def __init__(self, adress='ASRL3::INSTR'):
        '''
        self.tc = rm.open_resource(adress, baud_rate=115200,
                                   data_bits=8, parity=constants.VI_ASRL_PAR_NONE,
                                   stop_bits=constants.VI_ASRL_STOP_ONE,
                                   flow_control=constants.VI_ASRL_FLOW_NONE,
                                   write_termination='\r', read_termination='\r')
        
        '''
        self.tc = 0

        self.set_options = {'T1', 'T2'}

        self.get_options = {'t1', 't2'}
        
    def IDN(self):
        return(get(self.tc, 'IDN?')[2:])

    def t1(self):
        # Get the CH1 target temperature; returned value is the actual temperature in °C
        value_str = get(self.tc, 'TACT1?')
        value_float = re.findall(r'\d*\.\d+|\d+', value_str)
        try:
            value_float = [float(i) for i in value_float][0]
        except IndexError:
            try:
                value_str = get(self.tc, 'TACT1?')
                value_float = re.findall(r'\d*\.\d+|\d+', value_str)
                value_float = [float(i) for i in value_float][0]
            except IndexError:
                value_float = np.nan
        return value_float

    def set_T1(self, value=20):
        # Set the CH1 target temperature to value/10 °C, the range is defined by
        # TMIN1 and TMAX1, the setting resolution of value is 1.
        self.tc.write('EN1=1')
        self.tc.write('TSET1=' + str(int(value * 10)))

    def set_T1_MIN(self, t1_from=0):
        # Set the CH1 Target Temperature Min value,
        # (Range: -200 to TMAX1°C, with a resolution of 1°C).
        self.tc.write('TMIN1=' + str(t1_from))

    def set_T1_MAX(self, t1_to=30):
        # Set the CH1 Target Temperature Max value, n equals value
        # TMIN1 to 400°C, with a resolution of 1°C).
        self.tc.write('T1MAX=' + str(t1_to))

    def t2(self):
        # Get the CH2 target temperature; returned value is the actual temperature in °C
        value_str = get(self.tc, 'TACT2?')
        if value_str == '':
            value_str = get(self.tc, 'TACT2?')
        value_float = re.findall(r'\d*\.\d+|\d+', value_str)
        value_float = [float(i) for i in value_float]
        return(value_float[0])

    def set_T2(self, value=20):
        # Set the CH2 target temperature to value/10 °C, the range is defined by
        # TMIN1 and TMAX1, the setting resolution of value is 1.
        self.tc.write('EN2=1')
        self.tc.write('TSET2=' + str(int(value * 10)))

    def set_T2_MIN(self, t2_from=0):
        # Set the CH2 Target Temperature Min value,
        # (Range: -200 to TMAX2°C, with a resolution of 1°C).
        self.tc.write('TMIN1=' + str(t2_from))

    def set_T2_MAX(self, t2_to=20):
        # Set the CH2 Target Temperature Max value, n equals value
        # TMIN1 to 400°C, with a resolution of 1°C).
        self.tc.write('T1MAX=' + str(t2_to))
    