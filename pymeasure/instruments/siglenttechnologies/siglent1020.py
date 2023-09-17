# Import necessary libraries
# from pymeasure.instruments.resources import list_resources
import pyvisa

from pymeasure.instruments.instrument import Instrument

from pymeasure.instruments.validators import strict_discrete_set

# Initialize a Resource Manager for Visa instruments
# rm = pyvisa.ResourceManager('@py')
# ip_addr = "169.254.245.175"

# # # Open a connection to the instrument using TCPIP protocol
# instrument = rm.open_resource(f'TCPIP0::{ip_addr}')


class IEEECommonCommands:
    """
    A class that provides common IEEE488.2 commands for the instrument.

    Args:
        instrument (pyvisa.resources.Resource): The instrument resource to communicate with.

    Attributes:
        instrument (pyvisa.resources.Resource): The instrument resource to communicate with.
    """

    def __init__(self, instrument):
        self.instrument = instrument

    def get_idn(self):
        """
        Query SDL1020X-e instrument identification information.

        Returns:
            str: The instrument identification information.
        """
        return self.instrument.query("*IDN?")

    def reset(self):
        """
        Restore the equipment state to the initial state.
        """
        self.instrument.write("*RST")

    def clear_status(self):
        """
        Clears all bits in all of the event registers and the error list.
        """
        self.instrument.write("*CLS")

    def set_event_status_enable(self, value):
        """
        Set the bits in the standard event status enable register.

        Args:
            value (int): The value to set in the register.
        """
        self.instrument.write(f'*ESE {value}')

    def query_event_status_enable(self):
        """
        Query the standard event status enable register.

        Returns:
            int: The value in the register.
        """
        return int(self.instrument.query("*ESE?"))

    def query_and_clear_event_status(self):
        """
        Query and clear the standard event status register.

        Returns:
            int: The value in the register.
        """
        return int(self.instrument.query("*ESR?"))

    def set_operation_complete(self):
        """
        Set bit 0 in the standard event status register to "1" when all operations have finished.
        """
        self.instrument.write("*OPC")

    def query_operation_complete(self):
        """
        Query whether the current operation has been finished.

        Returns:
            int: "1" if the operation is complete, otherwise "0".
        """
        return int(self.instrument.query("*OPC?"))

    def set_status_byte_enable(self, value):
        """
        Set the bits in the status byte enable register.

        Args:
            value (int): The value to set in the register.
        """
        self.instrument.write(f"*SRE {value}")

    def query_status_byte_enable(self):
        """
        Query the status byte enable register. 

        Returns:
            int: The value in the register.
        """
        return int(self.instrument.query("*SRE?"))

    def query_status_byte_event(self):
        """
        Query the status byte event register.

        Returns:
            int: The value in the register.
        """
        return int(self.instrument.query("*STB?"))

    def run_self_test(self):
        """
        Perform a self-test.

        Returns:
            int: The result of the self-test.
        """
        return int(self.instrument.query("*TST?"))

    def wait_until_operations_complete(self):
        """
        Cause the instrument to wait until all pending commands are completed before executing any additional commands.
        """
        self.instrument.write("*WAI")


class MeasureSubsystemCommands:
    """
    A class that provides measurement commands for the instrument.

    Args:
        instrument (pyvisa.resources.Resource): The instrument resource to communicate with.

    Attributes:
        instrument (pyvisa.resources.Resource): The instrument resource to communicate with.
    """

    def __init__(self, instrument):
        self.instrument = instrument

    def measure_voltage_dc(self):
        """
        Gets the real-time voltage measurement value.

        Returns:
            float: The voltage measurement value.
        """
        return float(self.instrument.query("MEASure:VOLTage:DC?"))

    def measure_current_dc(self):
        """
        Gets the real-time current measurement value.

        Returns:
            float: The current measurement value.
        """
        return float(self.instrument.query("MEASure:CURRent:DC?"))

    def measure_power_dc(self):
        """
        Gets the real-time power measurement value.

        Returns:
            float: The power measurement value.
        """
        return float(self.instrument.query("MEASure:POWer:DC?"))

    def measure_resistance_dc(self):
        """
        Gets the real-time resistance measurement value.

        Returns:
            float: The resistance measurement value.
        """
        return float(self.instrument.query("MEASure:RESistance:DC?"))

    def measure_external(self):
        """
        Gets the real-time external measurement value in external sink mode.

        Returns:
            float: The external measurement value.
        """
        return float(self.instrument.query("MEASure:EXT?"))

    def measure_waveform_data(self, measurement_type):
        """
        Gets the waveform data of the waveform display interface in CC/CV/CP/CR mode.

        Args:
            measurement_type (str): The type of measurement ("CURRent", "VOLTage", "POWer", or "RESistance").

        Returns:
            str: The waveform data as a comma-separated string.
        """
        valid_list = ["CURRent", "VOLTage", "POWer", "RESistance"]
        if measurement_type not in valid_list:
            raise ValueError(
                "Invalid measurement type. Use the following: 'CURRent' or 'VOLTage' or 'POWer' or 'RESistance'")

        command = f'MEASure:WAVEdata? {measurement_type}'
        return self.instrument.query(command)


class SourceCommonCommands:
    """
    A class that provides common source commands for the instrument.

    Args:
        instrument (pyvisa.resources.Resource): The instrument resource to communicate with.

    Attributes:
        instrument (pyvisa.resources.Resource): The instrument resource to communicate with.
        optionalBoolParams (list): List of optional boolean parameters ("ON", "OFF", "1", "0").
        optionalModeParams (list): List of optional mode parameters ("CURRent", "VOLTage", "POWer", "RESistance").
        optionalValueParams (list): List of optional mode parameters ("MINimum", "MAXimum", "DEFault").
    """

    def __init__(self, instrument):
        self.instrument = instrument
        self.optionalBoolParams = ["ON", "OFF", "1", "0"]
        self.optionalModeParams = ["CURRent", "VOLTage", "POWer", "RESistance"]
        self.optionalModeParamsWithLED = [
            "CURRent", "VOLTage", "POWer", "RESistance", "LED"]
        self.optionalValueParams = ["MINimum", "MAXimum", "DEFault"]

        self.invalidValueErrorMsg = "Invalid parameter. Please provide 'MINimum', 'MAXimum', 'DEFault', or a numeric value."
        self.invalidModeErrorMsg = "Invalid parameter. Please provide 'CURRent', 'VOLTage', 'POWer', or 'RESistance'"
        self.invalidModeErrorMsgWithLED = "Invalid parameter. Please provide 'CURRent', 'VOLTage', 'POWer', or 'RESistance'"
        self.invalidBoolParamsMsg = "Invalid parameter. Please provide 'ON', 'OFF', '1', or '0'"

    # 3.3.1 Source Common Subsystem Command

    def set_mode_transient_operation(self, mode="CURRent"):
        """
        Sets mode in transient operation (CC/CV/CP/CR).

        Args:
            mode (str): The mode to set ("CURRent", "VOLTage", "POWer", or "RESistance").
        """
        if mode not in self.optionalModeParams:
            raise ValueError(self.invalidModeErrorMsg)

        self.instrument.write(f':SOURce:FUNCtion:TRANsient {mode}')

    def get_mode_transient_operation(self):
        """
        get mode in transient operation (CC/CV/CP/CR).

        Returns:
            mode (str): The mode to set ("CURRent", "VOLTage", "POWer", or "RESistance").
        """
        return self.instrument.query(":SOURce:FUNCtion:TRANsient?")

    # 3.3.1
    def set_mode_static_operation(self, mode="CURRent"):
        """
        Sets mode in static operation (CC/CV/CP/CR/LED)

        Args:
            mode (str): The mode to set ("CURRent", "VOLTage", "POWer", "RESistance", or "LED").
        """
        if mode not in self.optionalModeParamsWithLED:
            raise ValueError(self.invalidModeErrorMsgWithLED)

        self.instrument.write(f':SOURce:FUNCtion {mode}')

    def get_mode_static_operation(self):
        """
        Get mode in static operation (CC/CV/CP/CR/LED)

        Returns:
            mode (str): The mode to set ("CURRent", "VOLTage", "POWer", "RESistance", or "LED").
        """
        return self.instrument.query(":SOURce:FUNCtion?")

    # 3.3.2 Source Current Subsystem Command
    # def set_sink_current_cc_mode_static(self):
    #     """
    #     Set the sink current CC mode to static (Not implemented).
    #     """
    #     pass
    # set current range
    # get current range
    # set voltage range
    # get voltage range

    def set_current_IRange(self, value="DEFault"):
        """
        Set the current range of CC mode in static operation.

        Args:
            value (str): The current range value to set. It can be any setting value, "MINimum", "MAXimum", or "DEFault".
                         If <value> is greater than 5, the current range will be set to 30A; if <value> is less than 5,
                         the current range will be set to 5A.
        """

        if not (value in self.optionalValueParams or isinstance(value, int)):
            raise ValueError(self.invalidValueErrorMsg)
        self.instrument.write(f':SOURce:CURRent:IRANGe {value}')

    def query_current_IRange(self):
        """
        Query the current range of CC mode in static operation.

        Returns:
            int: The current range value (in Amperes).
        """
        return int(self.instrument.query(':SOURce:CURRent:IRANGe?'))

    def set_voltage_VRange(self, value="DEFault"):
        """
        Set the voltage range of CC mode in static operation.

        Args:
            value (str): The voltage range value to set. It can be any setting value, "MINimum", "MAXimum", or "DEFault".
                         If <value> is greater than 36, the voltage range will be set to 150V; if <value> is less than 36,
                         the voltage range will be set to 36V.
        """

        if not (value in self.optionalValueParams or isinstance(value, (float, int))):
            raise ValueError(self.invalidValueErrorMsg)
        self.instrument.write(f':SOURce:CURRent:VRANGe {value}')

    def query_voltage_VRange(self):
        """
        Query the voltage range of CC mode in static operation.

        Returns:
            int: The voltage range value (in Volts).
        """
        # Add logic here to query the voltage range and return the result as an integer.
        return int(self.instrument.query(':SOURce:CURRent:VRANGe?'))

    # TO BE ADDED
    '''
        Set voltage/current/power etc for (CC,CV,CP,CR, etc..) mode for static/transient 
        Query voltage/current/power etc for (CC,CV,CP,CR, etc..) mode for static/transient 
        ETC ... 
        https://int.siglent.com/upload_file/user/SDL1000X/SDL1000X_Programming_Guide_V1.0.pdf

    '''

    # 3.3.3 Source Voltage Subsystem Command
    def set_voltage_CV_mode(self, value="DEFault"):
        """
        Sets the preset voltage value of CV mode in static operation.

        Args:
            value (str): The voltage level to set (default is "DEFault").
        """
        if not (value in self.optionalValueParams or isinstance(value, (float, int))):
            raise ValueError(
                self.invalidValueErrorMsg)
        self.instrument.write(f"SOURce:VOLTage:LEVel:IMMediate {value}")

    def get_voltage_CV_mode(self):
        """
        Query the preset voltage value of CV mode in static operation.

        Returns:
            value (str): The voltage level of CV mode.
        """
        return self.instrument.query(":SOURce:VOLTage:LEVel:IMMediate?")

    # 3.4 Subsystem Command

    def set_time_measurement_switch(self, state="OFF"):
        """
        Sets whether enable the time measurement switch.

        Args:
            state (str): The state to set ("ON", "OFF", "1", or "0").
        """
        if state not in self.optionalBoolParams:
            raise ValueError(
                self.invalidBoolParamsMsg)

        self.instrument.write(f'TIME:TEST:STATe {state}')

    def get_time_measurement_switch_state(self):
        """
        Get the time measurement switch state.

        Returns:
            state (str): The state  0 or 1.
        """
        return self.instrument.query("TIME:TEST:STATe?")


rm = pyvisa.ResourceManager()
ip_addr = "169.254.245.175"
instrument = rm.open_resource(f'TCPIP0::{ip_addr}')


class siglent1020:
    def __init__(self, instrument):
        self.instrument = instrument

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

    def test_get(self):
        return self.source_input

siglentObject = siglent1020(instrument)
print(siglentObject.source_input())
# print(siglent1020.source_input.fget(instrument))

# print("Test")

# source_common_commands = SourceCommonCommands(instrument)
# source_common_commands.set_voltage_VRange("MINimum")
# print(source_common_commands.query_voltage_VRange())
# print(source_common_commands.get_mode_static_operation())
# source_common_commands.set_current_IRange("MAXimum")
# print(source_common_commands.query_current_IRange())
# source_common_commands.set_voltage_CV_mode("MAXimum")
# print(source_common_commands.get_voltage_CV_mode())
# source_common_commands.set_current_IRange("MINimum")
# iee_common_commands = IEEECommonCommands(instrument)
# print(iee_common_commands.query_and_clear_event_status())
# print(iee_common_commands.query_operation_complete())
