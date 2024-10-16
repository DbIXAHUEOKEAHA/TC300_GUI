"""
This example shows how to communicate with Thorlabs
KST101, KCube Stepper Motor.
"""
import os
import time

from msl.equipment import (
    EquipmentRecord,
    ConnectionRecord,
    Backend,
)
from msl.equipment.resources.thorlabs import MotionControl
from msl.equipment.resources.thorlabs.kinesis.kcube_stepper_motor import KCubeStepperMotor
from ctypes import byref
from ctypes import c_double
from ctypes import c_int
from ctypes import c_int16
from ctypes import c_int32
from ctypes import c_int64
from ctypes import c_short
from ctypes import c_uint
from ctypes import create_string_buffer

class KST201():
    def __init__(self, record):
        
        self.record = record
        self.device = KCubeStepperMotor(self.record)
        self.device.start_polling(250)
        self.device.enable_channel()
        self.device.load_settings()
    
    def restart(self):
        self.close()
        
        
        MotionControl.build_device_list()
        
        self.device = KCubeStepperMotor(self.record)
        self.device.start_polling(250)
        self.device.enable_channel()
        self.device.load_settings()
        
    
    def velocity(self):
        velocity, _ = self.device.get_vel_params()
        velocity = self.device.get_real_value_from_device_unit(velocity, 'VELOCITY')
        return velocity
    
    def acceleration(self):
        _, acc = self.device.get_vel_params()
        acc = self.device.get_real_value_from_device_unit(acc, 'ACCELERATION')
        return acc
    
    def set_velocity(self, value):
        velocity = value
        acc = max(velocity * 2, 0.0001)
        velocity = self.device.get_device_unit_from_real_value(velocity, 'VELOCITY')
        acc = self.device.get_device_unit_from_real_value(acc, 'ACCELERATION')
        
        self.device.set_vel_params(velocity, acc)
        
        
    def set_persistent_velocity(self, value): #on-device velocity
    
        def go():
            velocity = value
            acc = max(velocity * 10, 0.0001)
            backlash = min(velocity * 2, 0.02)
            velocity = self.device.get_device_unit_from_real_value(velocity, 'VELOCITY')
            acc = self.device.get_device_unit_from_real_value(acc, 'ACCELERATION')
            
            self.KCube_params = list(self.device.get_mmi_params()) #velocity_control_mode, velocity, acceleration etc.
            self.KCube_params[1] = velocity
            self.KCube_params[2] = acc
            self.KCube_params = tuple(self.KCube_params[:-2])
            self.device.set_mmi_params(*self.KCube_params)
            
            self.set_backlash(backlash)
    
        if self.device.check_connection():
    
            go()
        
        else:
            self.restart()
            time.sleep(0.1)
            go()
            
        
    def backlash(self):
        backlash = self.device.get_backlash()
        backlash = self.device.get_real_value_from_device_unit(backlash, 'DISTANCE')
        return backlash
    
    def set_backlash(self, value):
        backlash = value
        backlash = self.device.get_device_unit_from_real_value(backlash, 'DISTANCE')
        self.device.set_backlash(backlash)
        
    def position(self):
        position = self.device.get_position()
        position = self.device.get_real_value_from_device_unit(position, 'DISTANCE')
        return position
        
    def set_position(self, value):
        position_target = value
        position_target = self.device.get_device_unit_from_real_value(position_target, 'DISTANCE')
        
        self.device.set_move_absolute_position(position_target)
        self.device.move_absolute()
        
    def shift_up(self, value):
        """
        Parameters
        ----------
        value : float. Real units (mm).
            The shift in distance. Going up.

        Send a move absolute command to a target position = current position + value
        """
        
        def go():
            current_position = self.position()
            target_position = current_position + value
            self.set_position(target_position)
        
        if self.device.check_connection():
        
            go()
            
        else:
            
            self.restart()
            time.sleep(0.1)
            
            go()
        
    def shift_down(self, value):
        """
        Parameters
        ----------
        value : float. Real units (mm).
            The shift in distance. Going down.

        Send a move absolute command to a target position = current position - value
        """
        def go():
            current_position = self.position()
            target_position = current_position - value
            self.set_position(target_position)
        
        if self.device.check_connection():
        
            go()
            
        else:
            
            self.restart()
            time.sleep(0.1)
            
            go()
        
    def close(self):
        self.device.stop_polling()
        self.device.close()
        

def main():
    try:
        device = KST201()
        device.set_persistent_velocity(0.0001)
        device.set_persistent_velocity(0.001) 
    except Exception as ex:
        print(f'Exception hapened in executing KCube: {ex}')
    finally:
        pass
        
if __name__ == '__main__':
    main()
