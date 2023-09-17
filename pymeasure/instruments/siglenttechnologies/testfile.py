from pymeasure.instruments.instrument import Instrument
import pyvisa
from pymeasure.instruments.validators import strict_discrete_set, custom_voltage_range_validator
from pymeasure.adapters import VISAAdapter


rm = pyvisa.ResourceManager()
ip_addr = "169.254.245.175"
instrument = rm.open_resource(f'TCPIP0::{ip_addr}')

adapter = VISAAdapter('TCPIP0::169.254.245.175::inst0::INSTR')

class SDLbase(Instrument):
    def __init__(self, adapter, name="Siglent SDL10xx instrument Base Class", **kwargs):
        super().__init__(
            adapter,
            name,
            usb=dict(write_termination='\n',
                     read_termination='\n'),
            tcpip=dict(write_termination='\n',
                       read_termination='\n'),
            **kwargs
        )

    source_input = Instrument.control(
        ":SOURce:INPut:STATe?", ":SOURce:INPut:STATe %s",
        """Query the input status of the load. Return “1” if input status is ON. 
        Otherwise, return “0”.

        :type : string
        """,
        validator=strict_discrete_set,
        values=["0", "1", "OFF", "ON"],
        dynamic=True
    )

    event_status = Instrument.control(
        "*ESE?", "*ESE %d",
        """ 
        Query the standard event status enable register.
        Returns:
        int: The value returned reflects the current state of all the bits in the register..
        """,
        dynamic=True
    )

    status_byte_enable = Instrument.control(
        "*SRE?", "*SRE %i",
        """
        Query the status byte enable register. 

        Returns:
            int: The value in the register.
        """,
        dynamic=True

    )

    mode_transient_operation = Instrument.control(
        ':SOURce:FUNCtion:TRANsient?', ':SOURce:FUNCtion:TRANsient %s',
        """
        get mode in transient operation (CC/CV/CP/CR).

        Returns:
            mode (str): The mode to set ("CURRent", "VOLTage", "POWer", or "RESistance").
        """,
        validator=strict_discrete_set,
        values=["CURRent", "VOLTage", "POWer", "RESistance"],
        dynamic=True

    )

    mode_static_operation = Instrument.control(
        ":SOURce:FUNCtion?", ":SOURce:FUNCtion %s",
        """
        Sets mode in static operation (CC/CV/CP/CR/LED)

        Args:
            mode (str): The mode to set ("CURRent", "VOLTage", "POWer", "RESistance", or "LED").        
        """,
        validator=strict_discrete_set,
        values=["CURRent", "VOLTage", "POWer", "RESistance", "LED"],
        dynamic=True
    )

    current_range_CC_static_operation = Instrument.control(
        ":SOURce:CURRent:IRANGe?", ":SOURce:CURRent:IRANGe %s",
        """
        Set the current range of CC mode in static operation.

        Args:
            value (str): The current range value to set. It can be any setting value, "MINimum", "MAXimum", or "DEFault".
                         If <value> is greater than 5, the current range will be set to 30A; if <value> is less than 5,
                         the current range will be set to 5A.
        """,
        validator=custom_voltage_range_validator,
        values=["MINimum", "MAXimum", "DEFault"] ,
        dynamic=True
    )

    voltage_range_CC_static_operation = Instrument.control(
        ':SOURce:CURRent:VRANGe?', ':SOURce:CURRent:VRANGe %s',
        """
        Set the voltage range of CC mode in static operation.

        Args:
            value (str): The voltage range value to set. It can be any setting value, "MINimum", "MAXimum", or "DEFault".
                         If <value> is greater than 36, the voltage range will be set to 150V; if <value> is less than 36,
                         the voltage range will be set to 36V.
        """,
        validator=custom_voltage_range_validator,
        values=["MINimum", "MAXimum", "DEFault"],
        dynamic=True
    )

    voltage_value_CV_static_operation = Instrument.control(
        ':SOURce:VOLTage:LEVel:IMMediate?', 'SOURce:VOLTage:LEVel:IMMediate %s',
        """
        Sets the preset voltage value of CV mode in static operation.

        Args:
            value (str): The voltage level to set (default is "DEFault").
        """,
        validator=custom_voltage_range_validator,
        values=["MINimum", "MAXimum", "DEFault"],
        dynamic=True
    )

    time_measurement_switch = Instrument.control(
        'TIME:TEST:STATe?', 'TIME:TEST:STATe %s',
        """
        Sets whether enable the time measurement switch.

        Args:
            state (str): The state to set ("ON", "OFF", "1", or "0").
        """,
        validator=strict_discrete_set,
        values=["ON", "OFF", "1",  "0"] ,
        dynamic=True

    )

    def getIDN(self):
        self.write("*IDN?")
        return self.adapter.read()

    
siglentObject = SDLbase(adapter)

print(siglentObject.event_status)
siglentObject.event_status = -1
print(siglentObject.event_status)
siglentObject.status_byte_enable = 15
print(siglentObject.status_byte_enable)
siglentObject.mode_static_operation = "CURRent"
print(siglentObject.mode_static_operation)

siglentObject.current_range_CC_static_operation = "DEFault"
print(siglentObject.current_range_CC_static_operation)

siglentObject.voltage_range_CC_static_operation = "MINimum"
print(siglentObject.voltage_range_CC_static_operation)

siglentObject.voltage_value_CV_static_operation = "MINimum"
print(siglentObject.voltage_value_CV_static_operation)

siglentObject.time_measurement_switch = "OFF"
print(siglentObject.time_measurement_switch)
# siglentObject.mode_transient_operation = "CURRent"
# print(siglentObject.mode_transient_operation)
print(siglentObject.getIDN())
# siglentObject.get_input_status()
# siglentObject.source_input


