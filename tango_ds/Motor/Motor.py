#!/usr/bin/env python
# -*- coding:utf-8 -*- 


##############################################################################
## license :
##============================================================================
##
## File :        Motor.py
## 
## Project :     Motor
##
## This file is part of Tango device class.
## 
## Tango is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Tango is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with Tango.  If not, see <http://www.gnu.org/licenses/>.
## 
##
## $Author :      mariya.ryabova$
##
## $Revision :    $
##
## $Date :        $
##
## $HeadUrl :     $
##============================================================================
##            This file is generated by POGO
##    (Program Obviously used to Generate tango Object)
##
##        (c) - Software Engineering Group - ESRF
##############################################################################

"""Class for motors and its commands

http://sourceforge.net/p/tango-ds/code/HEAD/tree/DeviceClasses/Simulators/SimuMotor/trunk/src/SimuMotor.py
http://sourceforge.net/p/tango-ds/code/HEAD/tree/DeviceClasses/Simulators/SimMotor/trunk/SimMotor.cpp"""

__all__ = ["Motor", "MotorClass", "main"]

__docformat__ = 'restructuredtext'

import PyTango
import sys
# Add additional import
# ----- PROTECTED REGION ID(Motor.additionnal_import) ENABLED START -----#
import ximc
#----- PROTECTED REGION END -----#  //  Motor.additionnal_import

## Device States Description
## ON : The motor is powered on
## OFF : The motor is powered off
## MOVING : The motor is moving

class Motor (PyTango.Device_4Impl):

    #--------- Add you global variables here --------------------------
    #----- PROTECTED REGION ID(Motor.global_variables) ENABLED START -----#

    def _read_position(self, motor):
        self.debug_stream("In _read_position()")

        self.debug_stream("Reading position...")
        try:
            steps = motor.get_position()["Position"]
        except PyTango.DevFailed as df:
            self.error_stream(str(df))
            raise
        except Exception as e:
            self.error_stream(str(e))
            raise
        self.debug_stream("Position = {}".format(steps))
        print steps
        return steps

    def _write_position(self, motor, steps):
        self.debug_stream("In _write_position()")

        try:
            self.debug_stream("Setting position = {}".format(steps))
            motor.move_to_position(steps, 0)
            self.debug_stream("Position has been set")
        except PyTango.DevFailed as df:
            self.error_stream(str(df))
            raise
        except Exception as e:
            self.error_stream(str(e))
            raise

    #----- PROTECTED REGION END -----#  //  Motor.global_variables

    def __init__(self,cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        self.debug_stream("In __init__()")
        Motor.init_device(self)
        #----- PROTECTED REGION ID(Motor.__init__) ENABLED START -----#

        #----- PROTECTED REGION END -----#  //  Motor.__init__
        
    def delete_device(self):
        self.debug_stream("In delete_device()")
        #----- PROTECTED REGION ID(Motor.delete_device) ENABLED START -----#
        self.angle_motor.close()
        #----- PROTECTED REGION END -----#  //  Motor.delete_device

    def init_device(self):
        self.debug_stream("In init_device()")
        self.get_device_properties(self.get_device_class())
        self.attr_angle_position_read = 0.0
        self.attr_vertical_position_read = 0
        self.attr_horizontal_position_read = 0
        #----- PROTECTED REGION ID(Motor.init_device) ENABLED START -----#

        self.set_state(PyTango.DevState.OFF)

        try:
            self.debug_stream("Creating link to motor drivers...")
            self.angle_motor = ximc.Motor("COM5")
            self.horizontal_motor = ximc.Motor("COM3")
            self.debug_stream("Links were created")
        except PyTango.DevFailed as df:
            self.error_stream(str(df))
            raise
        except Exception as e:
            self.error_stream(str(e))
            raise

        self.angle_motor.open()
        self.angle_motor.set_move_settings(500, 500)
        steps = self._read_position(self.angle_motor)
        self.attr_angle_position_read = steps

        self.horizontal_motor.open()
        self.horizontal_motor.set_move_settings(500, 500)
        steps = self._read_position(self.horizontal_motor)
        self.attr_horizontal_position_read = steps

        self.set_state(PyTango.DevState.ON)


        #----- PROTECTED REGION END -----#  //  Motor.init_device

    def always_executed_hook(self):
        self.debug_stream("In always_excuted_hook()")
        #----- PROTECTED REGION ID(Motor.always_executed_hook) ENABLED START -----#

        #----- PROTECTED REGION END -----#  //  Motor.always_executed_hook

    #-----------------------------------------------------------------------------
    #    Motor read/write attribute methods
    #-----------------------------------------------------------------------------
    
    def read_angle_position(self, attr):
        self.debug_stream("In read_angle_position()")
        #----- PROTECTED REGION ID(Motor.angle_position_read) ENABLED START -----#

        self.attr_angle_position_read = self._read_position(self.angle_motor) * 360. / 32300
        attr.set_value(self.attr_angle_position_read)

        #----- PROTECTED REGION END -----#  //  Motor.angle_position_read
        
    def write_angle_position(self, attr):
        self.debug_stream("In write_angle_position()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Motor.angle_position_write) ENABLED START -----#

        angle = data
        steps = int(angle * 32300 / 360.)
        self._write_position(self.angle_motor, steps)

        #----- PROTECTED REGION END -----#  //  Motor.angle_position_write 
        
    def is_angle_position_allowed(self, attr):
        self.debug_stream("In is_angle_position_allowed()")
        state_ok = not(self.get_state() in [PyTango.DevState.OFF])
        #----- PROTECTED REGION ID(Motor.is_angle_position_allowed) ENABLED START -----#

        #----- PROTECTED REGION END -----#  //  Motor.is_angle_position_allowed
        return state_ok
        
    def read_vertical_position(self, attr):
        self.debug_stream("In read_vertical_position()")
        #----- PROTECTED REGION ID(Motor.vertical_position_read) ENABLED START -----#

        attr.set_value(self.attr_vertical_position_read)

        #----- PROTECTED REGION END -----#  //  Motor.vertical_position_read
        
    def write_vertical_position(self, attr):
        self.debug_stream("In write_vertical_position()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Motor.vertical_position_write) ENABLED START -----#

        self.attr_vertical_position_read = data

        #----- PROTECTED REGION END -----#  //  Motor.vertical_position_write
        
    def is_vertical_position_allowed(self, attr):
        self.debug_stream("In is_vertical_position_allowed()")
        state_ok = not(self.get_state() in [PyTango.DevState.OFF])
        #----- PROTECTED REGION ID(Motor.is_vertical_position_allowed) ENABLED START -----#

        #----- PROTECTED REGION END -----#  //  Motor.is_vertical_position_allowed
        return state_ok
        
    def read_horizontal_position(self, attr):
        self.debug_stream("In read_horizontal_position()")
        #----- PROTECTED REGION ID(Motor.horizontal_position_read) ENABLED START -----#

        self.attr_horizontal_position_read = self._read_position(self.horizontal_motor)
        attr.set_value(self.attr_horizontal_position_read)

        #----- PROTECTED REGION END -----#  //  Motor.horizontal_position_read
        
    def write_horizontal_position(self, attr):
        self.debug_stream("In write_horizontal_position()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Motor.horizontal_position_write) ENABLED START -----#

        steps = data
        self._write_position(self.horizontal_motor, steps)

        #----- PROTECTED REGION END -----#  //  Motor.horizontal_position_write
        
    def is_horizontal_position_allowed(self, attr):
        self.debug_stream("In is_horizontal_position_allowed()")
        state_ok = not(self.get_state() in [PyTango.DevState.OFF])
        #----- PROTECTED REGION ID(Motor.is_horizontal_position_allowed) ENABLED START -----#

        #----- PROTECTED REGION END -----#  //  Motor.is_horizontal_position_allowed
        return state_ok
        
    
    
        #----- PROTECTED REGION ID(Motor.initialize_dynamic_attributes) ENABLED START -----#

        #----- PROTECTED REGION END -----#  //  Motor.initialize_dynamic_attributes
            
    def read_attr_hardware(self, data):
        self.debug_stream("In read_attr_hardware()")
        #----- PROTECTED REGION ID(Motor.read_attr_hardware) ENABLED START -----#

        #----- PROTECTED REGION END -----#  //  Motor.read_attr_hardware


    #-----------------------------------------------------------------------------
    #    Motor command methods
    #-----------------------------------------------------------------------------
    
    def ResetAnglePosition(self):
        """ Resets the device to the initial position
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In ResetAnglePosition()")
        #----- PROTECTED REGION ID(Motor.ResetAnglePosition) ENABLED START -----#
        self.debug_stream("Setting current angle position as new zero")
        self.angle_motor.set_zero()
        self.debug_stream("New zero has been set")
        #----- PROTECTED REGION END -----#  //  Motor.ResetAnglePosition
        
    def is_ResetAnglePosition_allowed(self):
        self.debug_stream("In is_ResetAnglePosition_allowed()")
        state_ok = not(self.get_state() in [PyTango.DevState.OFF])
        #----- PROTECTED REGION ID(Motor.is_ResetAnglePosition_allowed) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#  //  Motor.is_ResetAnglePosition_allowed
        return state_ok
        

class MotorClass(PyTango.DeviceClass):
    #--------- Add you global class variables here --------------------------
    #----- PROTECTED REGION ID(Motor.global_class_variables) ENABLED START -----#

    #----- PROTECTED REGION END -----#  //  Motor.global_class_variables

    def dyn_attr(self, dev_list):
        """Invoked to create dynamic attributes for the given devices.
        Default implementation calls
        :meth:`Motor.initialize_dynamic_attributes` for each device
    
        :param dev_list: list of devices
        :type dev_list: :class:`PyTango.DeviceImpl`"""
    
        for dev in dev_list:
            try:
                dev.initialize_dynamic_attributes()
            except:
                import traceback
                dev.warn_stream("Failed to initialize dynamic attributes")
                dev.debug_stream("Details: " + traceback.format_exc())
        #----- PROTECTED REGION ID(Motor.dyn_attr) ENABLED START -----#

                #----- PROTECTED REGION END -----#  //  Motor.dyn_attr

    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        }


    #    Command definitions
    cmd_list = {
        'ResetAnglePosition':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        }


    #    Attribute definitions
    attr_list = {
        'angle_position':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "angle position",
                'format': "%4.1f",
            } ],
        'vertical_position':
            [[PyTango.DevShort,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "vertical position",
                'unit': "mm",
                'standard unit': "10E-3",
                'max value': "500",
                'min value': "0",
            } ],
        'horizontal_position':
            [[PyTango.DevLong,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "horizontal position",
                'format': "%5d",
            } ],
        }


def main():
    try:
        py = PyTango.Util(sys.argv)
        py.add_class(MotorClass,Motor,'Motor')

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed,e:
        print '-------> Received a DevFailed exception:',e
    except Exception,e:
        print '-------> An unforeseen exception occured....',e

if __name__ == '__main__':
    main()
