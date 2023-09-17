import unittest
# from pymeasure.instruments.instrument import Instrument
from pymeasure.adapters import VISAAdapter
from pymeasure.instruments.siglenttechnologies.siglent_sdl10xx import SDLbase

# TEST FILE OF FUNCTIONALTIES FOR SIGLENT_SDL1020.py
# TO RUN TEST EXECUTE "python -m unittest siglent_sdl10xx_test.py"
# TO-DO: INITIATE CONNECTION BEFORE TESTING, ADD TO setUp()

class TestInstrumentCommands(unittest.TestCase):

    def setUp(self):


        # Open a connection to the instrument using TCPIP protocol
        # Create an instance of the command class (SDLbase)

        # EXAMPLE
        # self.adapter = VISAAdapter('TCPIP0::169.254.245.175::inst0::INSTR')
        # self.siglentObject = SDLbase(self.adapter)

        pass

    # Test for the get_idn() method
    def test_get_idn(self):
        self.siglentObject.wait_until_operations_complete()
        result = self.siglentObject.get_idn()
        expected = "Siglent Technologies,SDL1020X-E,SDL13GCC7R0028,1.1.1.22\n"
        self.assertEqual(result, expected)

    # Test for setting event status enable
    def test_set_event_status_enable(self):
        self.siglentObject.wait_until_operations_complete()
        self.siglentObject.event_status = 16
        result = self.siglentObject.event_status
        self.assertEqual(result, 16)

    # Test for setting status byte enable
    def test_set_status_byte_enable(self):
        self.siglentObject.wait_until_operations_complete()
        self.siglentObject.status_byte_enable = 24
        result = self.siglentObject.status_byte_enable
        self.assertEqual(result, 24)

    # Test for measuring DC voltage
    def test_measure_voltage_dc(self):
        self.siglentObject.wait_until_operations_complete()
        result = self.siglentObject.measure_voltage_dc
        self.assertEqual(result, 0)

    # Test for measuring DC current
    def test_measure_current_dc(self):
        self.siglentObject.wait_until_operations_complete()
        result = self.siglentObject.measure_current_dc
        self.assertEqual(result, 0)

    # Test for measuring DC power
    def test_measure_power_dc(self):
        self.siglentObject.wait_until_operations_complete()
        result = self.siglentObject.measure_power_dc
        self.assertEqual(result, 0)

    # Test for measuring DC resistance
    def test_measure_resistance_dc(self):
        self.siglentObject.wait_until_operations_complete()
        result = self.siglentObject.measure_resistance_dc
        self.assertEqual(result, 0)

    # Test for measuring external values
    def test_measure_external(self):
        self.siglentObject.wait_until_operations_complete()
        result = self.siglentObject.measure_external
        self.assertEqual(result, 0)
        # print(self.siglentObject.measure_external(), "test")
        # pass

    # Test for setting transient operation mode
    def test_set_mode_transient_operation(self):
        self.siglentObject.wait_until_operations_complete()
        self.siglentObject.mode_transient_operation = "CURRent"
        result = self.siglentObject.mode_transient_operation
        self.assertEqual(result, "CURRENT")

    # Test for setting static operation mode
    def test_set_mode_static_operation(self):
        self.siglentObject.wait_until_operations_complete()
        self.siglentObject.mode_static_operation = "CURRent"
        result = self.siglentObject.mode_static_operation
        self.assertEqual(result, "CURRENT")

    # Test for setting current range in CC static operation
    def test_set_current_IRange(self):
        self.siglentObject.wait_until_operations_complete()
        self.siglentObject.current_range_CC_static_operation = "MINimum"
        result = self.siglentObject.current_range_CC_static_operation
        self.assertEqual(result, 5)

    # Test for setting voltage range in CC static operation
    def test_set_voltage_VRange(self):
        self.siglentObject.wait_until_operations_complete()
        self.siglentObject.voltage_range_CC_static_operation = "MAXimum"
        result = self.siglentObject.voltage_range_CC_static_operation
        self.assertEqual(result, 150)

    # # Test for setting voltage value in CV static operation
    def test_set_voltage_CV_mode(self):
        self.siglentObject.wait_until_operations_complete()
        self.siglentObject.voltage_value_CV_static_operation = "MAXimum"
        result = self.siglentObject.voltage_value_CV_static_operation
        self.assertEqual(result, 150)

    # Test for setting time measurement switch
    def test_set_time_measurement_switch(self):
        self.siglentObject.wait_until_operations_complete()
        self.siglentObject.time_measurement_switch = "ON"
        result = self.siglentObject.time_measurement_switch
        self.assertEqual(result, 1.0)