from pymeasure.instruments.instrument import Instrument
from pymeasure.instruments.validators import strict_discrete_set

# SAMPLE CODE USAGE 
##########################################################################################
#INITIALIZE CONNTECTION
# ip_addr = "169.254.245.175"   
# adapter = VISAAdapter('TCPIP0::169.254.245.175::inst0::INSTR')

# CREATE an object with the SDLbase class 
# siglentObject = SDLbase(adapter)


# SAMPLE COMMANDS
# SETTING MODE IN STATIC OPERATION
# siglentObject.mode_static_operation = "CURRent"

# QUERY CURRENT MODE IN STATIC OPERATION.
# print(siglentObject.mode_static_operation)

# GET REAL TIME VOLTAGE MEASUREMENT 
# print(siglentObject.measure_voltage_dc)
##########################################################################################

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
        """
        Setter: Sets the input status of the load (ON or OFF)

        Getter: Query the input status of the load. Return “1” if input status is ON. 
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
        Setter: Set the bits in the standard event status enable register.
        
        Getter: Query the standard event status enable register.
        Returns:
        int: The value returned reflects the current state of all the bits in the register..
        """,
        dynamic=True
    )

    status_byte_enable = Instrument.control(
        "*SRE?", "*SRE %i",
        """
        Setter: Set the bits in the status byte enable register.

        Getter: Query the status byte enable register. The value returned reflects
        the current state of all the bits in the register.
 

        Returns:
            int: The value in the register.
        """,
        dynamic=True

    )

    mode_transient_operation = Instrument.control(
        ':SOURce:FUNCtion:TRANsient?', ':SOURce:FUNCtion:TRANsient %s',
        """
        Setter: Sets mode in transient operation (CC/CV/CP/CR)
        
        Getter: Query current mode in transient operation.

        Returns:
            mode (str): The mode ("CURRent", "VOLTage", "POWer", or "RESistance").
        """,
        validator=strict_discrete_set,
        values=["CURRent", "VOLTage", "POWer", "RESistance"],
        dynamic=True

    )

    mode_static_operation = Instrument.control(
        ":SOURce:FUNCtion?", ":SOURce:FUNCtion %s",
        """
        Setter: Sets mode in static operation (CC/CV/CP/CR/LED)

        Args:
            mode (str): The mode to set ("CURRent", "VOLTage", "POWer", "RESistance", or "LED").        
        
        Getter:  Query current mode in static operation.
        Returns:
            mode (str): The mode ("CURRent", "VOLTage", "POWer", or "RESistance", "LED").
        """,
        validator=strict_discrete_set,
        values=["CURRent", "VOLTage", "POWer", "RESistance", "LED"],
        dynamic=True
    )

    current_range_CC_static_operation = Instrument.control(
        ":SOURce:CURRent:IRANGe?", ":SOURce:CURRent:IRANGe %s",
        """
        Setter: Sets the current range of CC mode in static operation.


        Args:
            value (str): The current range value to set. It can be any setting value, "MINimum", "MAXimum", or "DEFault".
                         If <value> is greater than 5, the current range will be set to 30A; if <value> is less than 5,
                         the current range will be set to 5A.

        Getter: Query the current range of CC mode in static operation.
            Returns: int
        """,
        validator=custom_current_range_validator,
        values=["MINimum", "MAXimum", "DEFault"],
        dynamic=True
    )

    voltage_range_CC_static_operation = Instrument.control(
        ':SOURce:CURRent:VRANGe?', ':SOURce:CURRent:VRANGe %s',
        """
        Setter: Set the voltage range of CC mode in static operation.

        Args:
            value (str): The voltage range value to set. It can be any setting value, "MINimum", "MAXimum", or "DEFault".
                         If <value> is greater than 36, the voltage range will be set to 150V; if <value> is less than 36,
                         the voltage range will be set to 36V.
        
        Getter: Query the voltage range of CC mode in static operation.
        Returns: int
        """,
        validator=custom_voltage_range_validator,
        values=["MINimum", "MAXimum", "DEFault"],
        dynamic=True
    )

    voltage_value_CV_static_operation = Instrument.control(
        ':SOURce:VOLTage:LEVel:IMMediate?', 'SOURce:VOLTage:LEVel:IMMediate %s',
        """
        Setter: Sets the preset voltage value of CV mode in static operation.

        Getter: Query the preset voltage value of CV mode in static operation.
        Return: int
        """,
        validator=custom_voltage_range_validator,
        values=["MINimum", "MAXimum", "DEFault"],
        dynamic=True
    )

    time_measurement_switch = Instrument.control(
        'TIME:TEST:STATe?', 'TIME:TEST:STATe %s',
        """
        Setter: Sets whether enable the time measurement switch.

        Args:
            state (str): The state to set ("ON", "OFF", "1", or "0").
        
        Getter: Query whether the time measurement switch is enabled
        Return: int
        """,
        validator=strict_discrete_set,
        values=["ON", "OFF", "1",  "0"],
        dynamic=True

    )

    measure_voltage_dc = Instrument.measurement(
        "MEASure:VOLTage:DC?",
        """
        Gets the real-time voltage measurement value.

        Returns:
            float: The voltage measurement value.
        """
    )

    measure_current_dc = Instrument.measurement(
        "MEASure:CURRent:DC?",
        """
        Gets the real-time current measurement value.

        Returns:
            float: The current measurement value.
        """
    )

    measure_power_dc = Instrument.measurement(
        "MEASure:POWer:DC?",
        """
        Gets the real-time power measurement value.

        Returns:
            float: The power measurement value.
        """
    )

    measure_resistance_dc = Instrument.measurement(
        "MEASure:RESistance:DC?",
        """
        Gets the real-time resistance measurement value.

        Returns:
            float: The resistance measurement value.
        """
    )

    measure_external = Instrument.measurement(
        "MEASure:EXT?",
        """
        Gets the real-time external measurement value in external sink mode.

        Returns:
            float: The external measurement value.
        """

    )

    def wait_until_operations_complete(self):
        """
        Cause the instrument to wait until all pending commands are completed before executing any additional commands.
        """
        self.write("*WAI")
    
    def get_idn(self):
        """
        Query SDL1020X-e instrument identification information.

        Returns:
            str: The instrument identification information.
        """
        self.write("*IDN?")
        return self.adapter.read()
