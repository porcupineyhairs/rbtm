#!/usr/bin/env python
# -*- coding:utf-8 -*- 


##############################################################################
## license :
##============================================================================
##
## File :        XRaySource.py
## 
## Project :     XRaySource
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

"""It is a class for XRay sourse, which is used for setting operating mode (voltage)"""

__all__ = ["XRaySource", "XRaySourceClass", "main"]

__docformat__ = 'restructuredtext'

import PyTango
import sys
# Add additional import
#----- PROTECTED REGION ID(XRaySource.additionnal_import) ENABLED START -----#
import ConfigParser
from driver_source import Source
#----- PROTECTED REGION END -----#  //  XRaySource.additionnal_import

## Device States Description
## ON : The state in which the source is active
## OFF : The state in which the source is not active
## FAULT : The state in which the source is fault
## STANDBY : 

class XRaySource (PyTango.Device_4Impl):

    #--------- Add you global variables here --------------------------
    #----- PROTECTED REGION ID(XRaySource.global_variables) ENABLED START -----#

    CONFIG_PATH = 'tango_ds.cfg'

    def get_port_from_config(self):
        config = ConfigParser.RawConfigParser()
        config.read(XRaySource.CONFIG_PATH)
        source_port = config.get("x-ray source", "port")
        return source_port

    def _read_voltage(self):
        try:
            voltage = self.source_driver.get_actual_voltage()
            self.debug_stream("Got voltage = {}".format(voltage))
        except PyTango.DevFailed as df:
            self.error_stream(str(df))
            raise
        except Exception as e:
            self.error_stream(str(e))
            raise

        return voltage

    def _write_voltage(self, new_voltage):
        try:
            self.debug_stream("Setting voltage: {}".format(new_voltage))
            self.source_driver.set_voltage(new_voltage)
            self.debug_stream("Voltage has been set")
        except PyTango.DevFailed as df:
            self.error_stream(str(df))
            raise
        except Exception as e:
            self.error_stream(str(e))
            raise

    def _read_current(self):
        try:
            current = self.source_driver.get_actual_current()
            self.debug_stream("Got current = {}".format(current))
        except PyTango.DevFailed as df:
            self.error_stream(str(df))
            raise
        except Exception as e:
            self.error_stream(str(e))
            raise

        return current

    def _write_current(self, new_current):
        try:
            self.debug_stream("Setting current: {}".format(new_current))
            self.source_driver.set_current(new_current)
            self.debug_stream("Current has been set")
        except PyTango.DevFailed as df:
            self.error_stream(str(df))
            raise
        except Exception as e:
            self.error_stream(str(e))
            raise

    #----- PROTECTED REGION END -----#  //  XRaySource.global_variables

    def __init__(self,cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        self.debug_stream("In __init__()")
        XRaySource.init_device(self)
        #----- PROTECTED REGION ID(XRaySource.__init__) ENABLED START -----#
        #----- PROTECTED REGION END -----#  //  XRaySource.__init__
        
    def delete_device(self):
        self.debug_stream("In delete_device()")
        #----- PROTECTED REGION ID(XRaySource.delete_device) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#  //  XRaySource.delete_device

    def init_device(self):
        self.debug_stream("In init_device()")
        self.get_device_properties(self.get_device_class())
        self.attr_voltage_read = 0.0
        self.attr_current_read = 0.0
        #----- PROTECTED REGION ID(XRaySource.init_device) ENABLED START -----#

        source_port = self.get_port_from_config()

        try:
            self.source_driver = Source(source_port)
        except PyTango.DevFailed as df:
            self.error_stream(str(df))
            raise
        except Exception as e:
            self.error_stream(str(e))
            raise

        print(self.source_driver.get_tube_name())

        self.attr_voltage_read = self._read_voltage()
        self.attr_current_read = self._read_current()

        self.voltage_reads_counter = 0
        self.current_reads_counter = 0
        
        if self.source_driver.is_on_high_volatge():
            self.set_state(PyTango.DevState.ON)
        else:
            self.set_state(PyTango.DevState.OFF)

        # read actual values from source

        #----- PROTECTED REGION END -----#  //  XRaySource.init_device

    def always_executed_hook(self):
        self.debug_stream("In always_excuted_hook()")
        #----- PROTECTED REGION ID(XRaySource.always_executed_hook) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#  //  XRaySource.always_executed_hook

    #-----------------------------------------------------------------------------
    #    XRaySource read/write attribute methods
    #-----------------------------------------------------------------------------
    
    def read_voltage(self, attr):
        self.debug_stream("In read_voltage()")
        #----- PROTECTED REGION ID(XRaySource.voltage_read) ENABLED START -----#
        if self.voltage_reads_counter % 5 == 0:
            self.attr_voltage_read = self._read_voltage()
        self.voltage_reads_counter = (self.voltage_reads_counter + 1) % 5
        attr.set_value(self.attr_voltage_read / 10.)
        #----- PROTECTED REGION END -----#  //  XRaySource.voltage_read
        
    def write_voltage(self, attr):
        self.debug_stream("In write_voltage()")
        data=attr.get_write_value()
        # ----- PROTECTED REGION ID(XRaySource.voltage_write) ENABLED START -----#
        new_voltage = int(round(data * 10))
        self._write_voltage(new_voltage)
        self.attr_voltage_read = self._read_voltage()
        #----- PROTECTED REGION END -----#  //  XRaySource.voltage_write
        
    def read_current(self, attr):
        self.debug_stream("In read_current()")
        # ----- PROTECTED REGION ID(XRaySource.current_read) ENABLED START -----#
        if self.current_reads_counter % 5 == 0:
            self.attr_current_read = self._read_current()
        self.current_reads_counter = (self.current_reads_counter + 1) % 5
        attr.set_value(self.attr_current_read / 10.)
        # ----- PROTECTED REGION END -----# //  XRaySource.current_read
        
    def write_current(self, attr):
        self.debug_stream("In write_current()")
        data=attr.get_write_value()
        # ----- PROTECTED REGION ID(XRaySource.current_write) ENABLED START -----#
        new_current = int(round(data * 10))
        self._write_current(new_current)
        self.attr_current_read = self._read_current()
        # ----- PROTECTED REGION END -----# //  XRaySource.current_write
        
    
    
        #----- PROTECTED REGION ID(XRaySource.initialize_dynamic_attributes) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#  //  XRaySource.initialize_dynamic_attributes
            
    def read_attr_hardware(self, data):
        self.debug_stream("In read_attr_hardware()")
        #----- PROTECTED REGION ID(XRaySource.read_attr_hardware) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#  //  XRaySource.read_attr_hardware


    #-----------------------------------------------------------------------------
    #    XRaySource command methods
    #-----------------------------------------------------------------------------
    
    def Off(self):
        """ Turns off the X-Ray source
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In Off()")
        #----- PROTECTED REGION ID(XRaySource.Off) ENABLED START -----#
        try:
            self.debug_stream("Turn off high voltage")
            self.source_driver.off_high_voltage()
            self.debug_stream("High voltage has been turned off")
        except PyTango.DevFailed as df:
            self.debug_stream(str(df))
            raise
        except Exception as e:
            self.debug_stream(str(e))
            raise

        self.voltage_reads_counter = 0
        self.current_reads_counter = 0

        self.set_state(PyTango.DevState.OFF)

        #----- PROTECTED REGION END -----#  //  XRaySource.Off
        
    def On(self):
        """ Turns on the X-Ray source
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In On()")
        #----- PROTECTED REGION ID(XRaySource.On) ENABLED START -----#
        try:
            self.debug_stream("Setting high voltage")       
            self.source_driver.on_high_voltage()
            self.debug_stream("High voltage has been set")
        except PyTango.DevFailed as df:
            self.debug_stream(str(df))
            raise
        except Exception as e:
            self.debug_stream(str(e))
            raise

        self.voltage_reads_counter = 0
        self.current_reads_counter = 0

        self.set_state(PyTango.DevState.ON)

        #----- PROTECTED REGION END -----#  //  XRaySource.On
        

class XRaySourceClass(PyTango.DeviceClass):
    #--------- Add you global class variables here --------------------------
    #----- PROTECTED REGION ID(XRaySource.global_class_variables) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#  //  XRaySource.global_class_variables

    def dyn_attr(self, dev_list):
        """Invoked to create dynamic attributes for the given devices.
        Default implementation calls
        :meth:`XRaySource.initialize_dynamic_attributes` for each device
    
        :param dev_list: list of devices
        :type dev_list: :class:`PyTango.DeviceImpl`"""
    
        for dev in dev_list:
            try:
                dev.initialize_dynamic_attributes()
            except:
                import traceback
                dev.warn_stream("Failed to initialize dynamic attributes")
                dev.debug_stream("Details: " + traceback.format_exc())
        #----- PROTECTED REGION ID(XRaySource.dyn_attr) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#  //  XRaySource.dyn_attr

    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        }


    #    Command definitions
    cmd_list = {
        'Off':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        'On':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        }


    #    Attribute definitions
    attr_list = {
        'voltage':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "voltage",
                'unit': "kV",
                'standard unit': "10E+3",
                'format': "%3.1f",
                'max value': "60",
                'min value': "2",
                'description': "voltage of the X-Ray source",
            } ],
        'current':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "current",
                'unit': "mA",
                'standard unit': "10E-3",
                'format': "%3.1f",
                'max value': "80",
                'min value': "2",
                'description': "current of the X-Ray source",
            } ],
        }


def main():
    try:
        py = PyTango.Util(sys.argv)
        py.add_class(XRaySourceClass,XRaySource,'XRaySource')

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed,e:
        print '-------> Received a DevFailed exception:',e
    except Exception,e:
        print '-------> An unforeseen exception occured....',e

if __name__ == '__main__':
    main()
