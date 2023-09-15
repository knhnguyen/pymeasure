from pymeasure.instruments.resources import list_resources
import pyvisa

rm = pyvisa.ResourceManager('@py')
ip_addr = "169.254.245.175"
instrument = rm.open_resource(f'TCPIP0::{ip_addr}')


class IEEECommonCommands:
    def __init__(self, instrument):
        self.instrument = instrument
        pass

    def get_idn(self):
        """
            Query SDL1020X-e instrument identification information

            :param instrument: Instance of the instrument class
            "rtype: str
        """
        return self.instrument.query("*IDN?")

    def reset(self):
        self.instrument.write("*RST")

    def clear_status(self):
        self.instrument.write("*CLS")

    def set_event_status_enable(self, value):
        self.instruemt.write(f'*ESE {value}')

    def query_event_status_enable(self):
        return int(self.instrument.query("*ESE?"))

    def query_and_clear_event_status(self):
        return int(self.instrument.query("*ESR?"))

    def set_operation_complete(self):
        self.instrument.write("OPC")

    def query_operation_complete(self):
        return int(self.instrument.query("OPC?"))

    def set_status_byte_enable(self, value):
        self.instrument.write(f"*SRE {value}")

    def query_status_byte_enable(self):
        return int(self.instrument.query("*SRE?"))

    def query_status_byte_event(self):
        return int(self.instrument.query("*STB?"))
        

    def run_self_test(self):
        return int(self.instrument.query("*TST?"))
        

    def wait_until_operations_complete(self):
        self.instrument.write("*WAI")

class MeasureSubsystemCommands:
    def __init__(self, instrument):
        self.instrument = instrument

    def measure_voltage_dc(self):
        return self.instrument.query("MEASure:VOLTage:DC?")
    
    def measure_current_dc(self):
        return self.instrument.query("MEASure:CURRent:DC?")
    
    def measure_power_dc(self):
        return self.instrument.query("MEASure:POWer:DC?")
    
    def measure_resistance_dc(self):
        return self.instrument.query("MEASure:RESistance:DC?")
    
    def measure_external(self):
        return self.instrument.query("MEASure:EXT?")
    
    def measure_waveform_data(self, measurement_type):
        valid_list = ["CURRent", "VOLTage", "POWer", "RESistance"]
        if measurement_type not in valid_list:
            raise ValueError("Invalid measurement type. Use the following: 'CURRent' or 'VOLTage' or 'POWer' or 'RESistance'")
        
        command = f'MEASure:WAVEdata? {measurement_type}'
        return self.instrument.write(command)
       
    
#CORE FUNCTIONALITIES TO DO
#set voltage, current, power levels
# enabling, disabling load
# reading measurement - done
# configure output state( CC,CV,CP, CR)
# enabling/disabling protection features

class SourceCommonCommands:
    def __init__(self,instrument):
        self.instrument = instrument
        self.optionalBoolParams = ["ON", "OFF", "1", "0"]
        self.optionalModeParams = ["CURRent", "VOLTage", "POWer", "RESistance"]

    def set_sink_current_cc_mode_static(self):
        pass

    def set_voltage_CV_mode(self, value = "DEFault" ):
        self.instrument.write(f"SOURce:VOLTage:LEVel:IMMediate {value}")

    def set_time_measurement_switch(self, state="OFF"):
        if state not in self.optionalBoolParams:
            raise ValueError("Invalid state. Please provide 'ON', 'OFF', '1', or '0")
        
        self.instrument.write(f'TIME:TEST:STATe {state}')

    def set_mode_transient_operation(self, mode = "CURRent"):
        if mode not in self.optionalModeParams:
            raise ValueError("Invalid state. Please provide 'CURRent', 'VOLTage', 'POWer', or 'RESistance")
        
        self.instrument.write(f':SOURce:FUNCtion:TRANsient {mode}')
    
    def set_mode_static_operation(self, mode = "CURRent"):
        if mode not in self.optionalModeParams:
            raise ValueError("Invalid state. Please provide 'CURRent', 'VOLTage', 'POWer', or 'RESistance")
        
        self.instrument.write(f':SOURce:FUNCtion:TRANsient {mode}')
# pyvisa.log_to_screen()

# instrument.write('*IDN?')
# response = instrument.read()
# print(response)
ieee_commands = IEEECommonCommands(instrument)
measure_subsystem_commands = MeasureSubsystemCommands(instrument)
source_common_commands = SourceCommonCommands(instrument)
source_common_commands.set_mode_static_operation("VOLTage")
# print(measure_subsystem_commands.measure_voltage_dc())
# print(measure_subsystem_commands.measure_current_dc())
# print(measure_subsystem_commands.measure_external())
# print(measure_subsystem_commands.measure_waveform_data("RESistance"))
# print(ieee_commands.run_self_test())
# print(ieee_commands.get_idn())
