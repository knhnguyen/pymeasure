import pyvisa
import unittest
from siglent1020 import IEEECommonCommands, MeasureSubsystemCommands, SourceCommonCommands

class TestInstrumentCommands(unittest.TestCase):

    def setUp(self):
        # Initialize a Resource Manager for Visa instruments
        rm = pyvisa.ResourceManager('@py')
        ip_addr = "169.254.245.175"
        self.instrument = rm.open_resource(f'TCPIP0::{ip_addr}')

        # Open a connection to the instrument using TCPIP protocol
        
        # Create instances of command classes
        self.ieee_commands = IEEECommonCommands(self.instrument)
        self.measure_commands = MeasureSubsystemCommands(self.instrument)
        self.source_commands = SourceCommonCommands(self.instrument)

        # self.ieee_commands.reset()
        # self.ieee_commands.clear_status()

    def tearDown(self):
        # print("closing connection")
        self.instrument.close()

    def test_ieee_common_commands(self):
        # Test IEEE Common Commands
        self.test_get_idn()
        self.test_set_event_status_enable()
        # self.test_query_and_clear_event_status()
        self.test_set_operation_complete()
        self.test_set_status_byte_enable()

    def test_measure_subsystem_commands(self):
        # Test Measure Subsystem Commands
        self.test_measure_voltage_dc()
        self.test_measure_current_dc()
        self.test_measure_power_dc()
        self.test_measure_resistance_dc()

#     def test_source_common_commands(self):
#         # Test Source Common Commands
        self.test_set_mode_transient_operation()
        self.test_set_mode_static_operation()
        self.test_set_current_IRange()
        self.test_set_voltage_VRange()
        self.test_set_voltage_CV_mode()
        self.test_set_time_measurement_switch()

    def test_get_idn(self):
        result = self.ieee_commands.get_idn()
        expected = "Siglent Technologies,SDL1020X-E,SDL13GCC7R0028,1.1.1.22\n"
        self.assertEqual(result, expected)


    def test_set_event_status_enable(self):
        self.ieee_commands.set_event_status_enable(16)
        result = self.ieee_commands.query_event_status_enable()
        self.assertEqual(result, 16)



    # def test_query_and_clear_event_status(self):
    #     result = self.ieee_commands.query_and_clear_event_status()
    #     self.ieee_commands.wait_until_operations_complete()
    #     self.assertEqual(result, 0)

    def test_set_operation_complete(self):
        self.ieee_commands.set_operation_complete()
        result = self.ieee_commands.query_operation_complete()
        self.assertEqual(result, 1)

    def test_set_status_byte_enable(self):
        self.ieee_commands.set_status_byte_enable(24)
        result = self.ieee_commands.query_status_byte_enable()
        self.assertEqual(result, 24)
        


    def test_measure_voltage_dc(self):
        result = self.measure_commands.measure_voltage_dc()
        self.assertEqual(result, 0)

    def test_measure_current_dc(self):
        result = self.measure_commands.measure_current_dc()
        self.assertEqual(result, 0)

    def test_measure_power_dc(self):
        result = self.measure_commands.measure_power_dc()
        self.assertEqual(result, 0)

    def test_measure_resistance_dc(self):
        result = self.measure_commands.measure_resistance_dc()
        self.assertEqual(result, 0)

    def test_measure_external(self):
        result = self.measure_commands.measure_external()
        self.assertEqual(result, 0)


    def test_set_mode_transient_operation(self):
        self.source_commands.set_mode_transient_operation("CURRent")
        result = self.source_commands.get_mode_transient_operation()
        self.assertEqual(result, "CURRENT\n")


    def test_set_mode_static_operation(self):
        self.source_commands.set_mode_static_operation("CURRent")
        result = self.source_commands.get_mode_static_operation()
        self.assertEqual(result, "CURRENT\n")

    #test this

    def test_set_current_IRange(self):
        
        self.source_commands.set_current_IRange("MINimum")
        # print(self.source_commands.query_current_IRange())
        # pass
        # IEEECommonCommands.wait_until_operations_complete()
        result = self.source_commands.query_current_IRange()
        self.assertEqual(result, 5)


    def test_set_voltage_VRange(self):
        self.source_commands.set_voltage_VRange("MAXimum")
        result = self.source_commands.query_voltage_VRange()
        self.assertEqual(result, 150)


    def test_set_voltage_CV_mode(self):
        self.source_commands.set_voltage_CV_mode("MAXimum")
        result = self.source_commands.get_voltage_CV_mode()
        self.assertEqual(result, "150.000000\n")
    


    def test_set_time_measurement_switch(self):
        self.source_commands.set_time_measurement_switch("ON")
        result = self.source_commands.get_time_measurement_switch_state()
        self.assertEqual(result, "1\n")

