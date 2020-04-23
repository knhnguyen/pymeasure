#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2020 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from time import sleep

import pytest
from pymeasure.instruments.agilent.agilent34450A import Agilent34450A
from pyvisa.errors import VisaIOError


class TestAgilent34450A:
    """
    Unit tests for Agilent34450A class.

    An Agilent34450A device should be connected to the computer.
    Indicate the resource address below.
    """

    # Resource address goes here:
    resource = "USB0::10893::45848::MY56511723::0::INSTR" # EQ0017

    # Fixtures
    @pytest.fixture
    def make_reseted_dmm(self):
        dmm = Agilent34450A(self.resource)
        dmm.reset()
        return dmm

    # Parametrizations
    pBooleans = [False, True]
    pResolution = [[3.00E-5, 3.00E-5], [2.00E-5, 2.00E-5], [1.50E-6, 1.50E-6],
                                ["MIN", 1.50E-6], ["MAX", 3.00E-5], ["DEF", 1.50E-6]]
    pModes = ['current', 'ac current', 'voltage', 'ac voltage', 'resistance',
              '4w resistance', 'current frequency', 'voltage frequency',
              'continuity', 'diode', 'temperature', 'capacitance']
    pCurrentRanges = [[100E-6, 100E-6], [1E-3, 1E-3], [10E-3, 10E-3], [100E-3, 100E-3],
                      [1, 1], ["MIN", 100E-6], ["MAX", 10], ["DEF", 100E-3]]
    pCurrentAcRanges = [[10E-3, 10E-3], [100E-3, 100E-3], [1, 1], ["MIN", 10E-3],
                        ["MAX", 10], ["DEF", 100E-3]]
    pVoltageRanges = [[100E-3, 100E-3], [1, 1], [10, 10], [100, 100], [1000, 1000],
                      ["MIN", 100E-3], ["MAX", 1000], ["DEF", 10]]
    pVoltageAcRanges = [[100E-3, 100E-3], [1, 1], [10, 10], [100, 100], [750, 750],
                        ["MIN", 100E-3], ["MAX", 750], ["DEF", 10]]
    pResistanceRanges = [[1E2, 1E2], [1E3, 1E3], [1E4, 1E4], [1E5, 1E5], [1E6, 1E6],
                         [1E7, 1E7], [1E8, 1E8], ["MIN", 1E2], ["MAX", 1E8], ["DEF", 1E3]]
    pResistance4wRanges = [[1E2, 1E2], [1E3, 1E3], [1E4, 1E4], [1E5, 1E5], [1E6, 1E6],
                           [1E7, 1E7], [1E8, 1E8], ["MIN", 1E2], ["MAX", 1E8], ["DEF", 1E3]]
    pFrequencyApertures = [[100E-3, 100E-3], [1, 1], ["MIN", 100E-3], ["MAX", 1], ["DEF", 1]]
    pCapacitanceRanges = [[1E-9, 1E-9], [1E-8, 1E-8], [1E-7, 1E-7], [1E-6, 1E-6], [1E-5, 1E-5],
                          [1E-4, 1E-4], [1E-3, 1E-3], [1E-2, 1E-2], ["MIN", 1E-9], ["MAX", 1E-2],
                          ["DEF", 1E-6]]

    def test_dmm_initialization_bad(self):
        bad_resource = "USB0::10893::45848::MY12345678::0::INSTR"
        with pytest.raises(VisaIOError):
            dmm = Agilent34450A(bad_resource)

    def test_good_address(self):
        dmm = Agilent34450A(self.resource)

    def test_reset(self):
        dmm = Agilent34450A(self.resource)
        dmm.reset()

    def test_beep(self, make_reseted_dmm):
        dmm = Agilent34450A(self.resource)
        # Assert that a beep is audible
        dmm.beep()

    @pytest.mark.parametrize("case", pModes)
    def test_modes(self, make_reseted_dmm, case):
        dmm = make_reseted_dmm
        dmm.mode = case
        assert dmm.mode == case

    @pytest.mark.parametrize("case, expected", pCurrentRanges)
    def test_current_range(self, make_reseted_dmm, case, expected):
        dmm = make_reseted_dmm
        dmm.current_range = case
        assert dmm.current_range == expected

    @pytest.mark.parametrize("case", pBooleans)
    def test_current_auto_range(self, make_reseted_dmm, case):
        dmm = make_reseted_dmm
        dmm.current_auto_range = case
        assert dmm.current_auto_range == case

    @pytest.mark.parametrize("case, expected", pResolution)
    def test_current_resolution(self, make_reseted_dmm, case, expected):
        dmm = make_reseted_dmm
        dmm.current_resolution = case
        assert dmm.current_resolution == expected

    @pytest.mark.parametrize("case, expected", pCurrentAcRanges)
    def test_current_ac_range(self, make_reseted_dmm, case, expected):
        dmm = make_reseted_dmm
        dmm.current_ac_range = case
        assert dmm.current_ac_range == expected

    @pytest.mark.parametrize("case", pBooleans)
    def test_current_ac_auto_range(self, make_reseted_dmm, case):
        dmm = make_reseted_dmm
        dmm.current_ac_auto_range = case
        assert dmm.current_ac_auto_range == case

    @pytest.mark.parametrize("case, expected", pResolution)
    def test_current_ac_resolution(self, make_reseted_dmm, case, expected):
        dmm = make_reseted_dmm
        dmm.current_ac_resolution = case
        assert dmm.current_ac_resolution == expected

    def test_configure_current(self, make_reseted_dmm):
        dmm = make_reseted_dmm

        # No parameters specified
        dmm.configure_current()
        assert dmm.mode == "current"
        assert dmm.current_auto_range == 1
        assert dmm.current_resolution == 1.50E-6

        # Four possible paths
        dmm.configure_current(current_range=1, ac=True, resolution="MAX")
        assert dmm.mode == "ac current"
        assert dmm.current_ac_range == 1
        assert dmm.current_ac_auto_range == 0
        assert dmm.current_ac_resolution == 3.00E-5
        dmm.configure_current(current_range="AUTO", ac=True, resolution="MIN")
        assert dmm.mode == "ac current"
        assert dmm.current_ac_auto_range == 1
        assert dmm.current_ac_resolution == 1.50E-6
        dmm.configure_current(current_range=1, ac=False, resolution="MAX")
        assert dmm.mode == "current"
        assert dmm.current_range == 1
        assert dmm.current_auto_range == 0
        assert dmm.current_resolution == 3.00E-5
        dmm.configure_current(current_range="AUTO", ac=False, resolution="MIN")
        assert dmm.mode == "current"
        assert dmm.current_auto_range == 1
        assert dmm.current_resolution == 1.50E-6

    def test_current_reading(self, make_reseted_dmm):
        dmm = make_reseted_dmm
        dmm.mode = "current"
        value = dmm.current
        assert type(value) is float

    def test_current_ac_reading(self, make_reseted_dmm):
        dmm = make_reseted_dmm
        dmm.mode = "ac current"
        value = dmm.current_ac
        assert type(value) is float

    @pytest.mark.parametrize("case, expected", pVoltageRanges)
    def test_voltage_range(self, make_reseted_dmm, case, expected):
        dmm = make_reseted_dmm
        dmm.voltage_range = case
        assert dmm.voltage_range == expected

    @pytest.mark.parametrize("case", pBooleans)
    def test_voltage_auto_range(self, make_reseted_dmm, case):
        dmm = make_reseted_dmm
        dmm.voltage_auto_range = case
        assert dmm.voltage_auto_range == case

    @pytest.mark.parametrize("case, expected", pResolution)
    def test_voltage_resolution(self, make_reseted_dmm, case, expected):
        dmm = make_reseted_dmm
        dmm.voltage_resolution = case
        assert dmm.voltage_resolution == expected

    @pytest.mark.parametrize("case, expected", pVoltageAcRanges)
    def test_voltage_ac_range(self, make_reseted_dmm, case, expected):
        dmm = make_reseted_dmm
        dmm.voltage_ac_range = case
        assert dmm.voltage_ac_range == expected

    @pytest.mark.parametrize("case", pBooleans)
    def test_voltage_ac_auto_range(self, make_reseted_dmm, case):
        dmm = make_reseted_dmm
        dmm.voltage_ac_auto_range = case
        assert dmm.voltage_ac_auto_range == case

    @pytest.mark.parametrize("case, expected", pResolution)
    def test_voltage_ac_resolution(self, make_reseted_dmm, case, expected):
        dmm = make_reseted_dmm
        dmm.voltage_ac_resolution = case
        assert dmm.voltage_ac_resolution == expected

    def test_configure_voltage(self, make_reseted_dmm):
        dmm = make_reseted_dmm

        # No parameters specified
        dmm.configure_voltage()
        assert dmm.mode == "voltage"
        assert dmm.voltage_auto_range == 1
        assert dmm.voltage_resolution == 1.50E-6

        # Four possible paths
        dmm.configure_voltage(voltage_range=100, ac=True, resolution="MAX")
        assert dmm.mode == "ac voltage"
        assert dmm.voltage_ac_range == 100
        assert dmm.voltage_ac_auto_range == 0
        assert dmm.voltage_ac_resolution == 3.00E-5
        dmm.configure_voltage(voltage_range="AUTO", ac=True, resolution="MIN")
        assert dmm.mode == "ac voltage"
        assert dmm.voltage_ac_auto_range == 1
        assert dmm.voltage_ac_resolution == 1.50E-6
        dmm.configure_voltage(voltage_range=100, ac=False, resolution="MAX")
        assert dmm.mode == "voltage"
        assert dmm.voltage_range == 100
        assert dmm.voltage_auto_range == 0
        assert dmm.voltage_resolution == 3.00E-5
        dmm.configure_voltage(voltage_range="AUTO", ac=False, resolution="MIN")
        assert dmm.mode == "voltage"
        assert dmm.voltage_auto_range == 1
        assert dmm.voltage_resolution == 1.50E-6

    def test_voltage_reading(self, make_reseted_dmm):
        dmm = make_reseted_dmm
        dmm.mode = "voltage"
        value = dmm.voltage
        assert type(value) is float

    def test_voltage_ac_reading(self, make_reseted_dmm):
        dmm = make_reseted_dmm
        dmm.mode = "ac voltage"
        value = dmm.voltage_ac
        assert type(value) is float

    @pytest.mark.parametrize("case, expected", pResistanceRanges)
    def test_resistance_range(self, make_reseted_dmm, case, expected):
        dmm = make_reseted_dmm
        dmm.resistance_range = case
        assert dmm.resistance_range == expected

    @pytest.mark.parametrize("case", pBooleans)
    def test_resistance_auto_range(self, make_reseted_dmm, case):
        dmm = make_reseted_dmm
        dmm.resistance_auto_range = case
        assert dmm.resistance_auto_range == case

    @pytest.mark.parametrize("case, expected", pResolution)
    def test_resistance_resolution(self, make_reseted_dmm, case, expected):
        dmm = make_reseted_dmm
        dmm.resistance_resolution = case
        assert dmm.resistance_resolution == expected

    @pytest.mark.parametrize("case, expected", pResistance4wRanges)
    def test_resistance_4w_range(self, make_reseted_dmm, case, expected):
        dmm = make_reseted_dmm
        dmm.resistance_4w_range = case
        assert dmm.resistance_4w_range == expected

    @pytest.mark.parametrize("case", pBooleans)
    def test_resistance_4w_auto_range(self, make_reseted_dmm, case):
        dmm = make_reseted_dmm
        dmm.resistance_4w_auto_range = case
        assert dmm.resistance_4w_auto_range == case

    @pytest.mark.parametrize("case, expected", pResolution)
    def test_resistance_4w_resolution(self, make_reseted_dmm, case, expected):
        dmm = make_reseted_dmm
        dmm.resistance_4w_resolution = case
        assert dmm.resistance_4w_resolution == expected

    def test_configure_resistance(self, make_reseted_dmm):
        dmm = make_reseted_dmm

        # No parameters specified
        dmm.configure_resistance()
        assert dmm.mode == "resistance"
        assert dmm.resistance_auto_range == 1
        assert dmm.resistance_resolution == 1.50E-6

        # Four possible paths
        dmm.configure_resistance(resistance_range=10E3, wires=2, resolution="MAX")
        assert dmm.mode == "resistance"
        assert dmm.resistance_range == 10E3
        assert dmm.resistance_auto_range == 0
        assert dmm.resistance_resolution == 3.00E-5
        dmm.configure_resistance(resistance_range="AUTO", wires=2, resolution="MIN")
        assert dmm.mode == "resistance"
        assert dmm.resistance_auto_range == 1
        assert dmm.resistance_resolution == 1.50E-6
        dmm.configure_resistance(resistance_range=10E3, wires=4, resolution="MAX")
        assert dmm.mode == "4w resistance"
        assert dmm.resistance_4w_range == 10E3
        assert dmm.resistance_4w_auto_range == 0
        assert dmm.resistance_4w_resolution == 3.00E-5
        dmm.configure_resistance(resistance_range="AUTO", wires=4, resolution="MIN")
        assert dmm.mode == "4w resistance"
        assert dmm.resistance_4w_auto_range == 1
        assert dmm.resistance_4w_resolution == 1.50E-6

        # Should raise ValueError
        with pytest.raises(ValueError):
            dmm.configure_resistance(wires=3)

    def test_resistance_reading(self, make_reseted_dmm):
        dmm = make_reseted_dmm
        dmm.mode = "resistance"
        value = dmm.resistance
        assert type(value) is float

    def test_resistance_4w_reading(self, make_reseted_dmm):
        dmm = make_reseted_dmm
        dmm.mode = "4w resistance"
        value = dmm.resistance_4w
        assert type(value) is float

    @pytest.mark.parametrize("case, expected", pCurrentAcRanges)
    def test_frequency_current_range(self, make_reseted_dmm, case, expected):
        dmm = make_reseted_dmm
        dmm.frequency_current_range = case
        assert dmm.frequency_current_range == expected

    @pytest.mark.parametrize("case", pBooleans)
    def test_frequency_current_auto_range(self, make_reseted_dmm, case):
        dmm = make_reseted_dmm
        dmm.frequency_current_auto_range = case
        assert dmm.frequency_current_auto_range == case

    @pytest.mark.parametrize("case, expected", pVoltageAcRanges)
    def test_frequency_voltage_range(self, make_reseted_dmm, case, expected):
        dmm = make_reseted_dmm
        dmm.frequency_voltage_range = case
        assert dmm.frequency_voltage_range == expected

    @pytest.mark.parametrize("case", pBooleans)
    def test_frequency_voltage_auto_range(self, make_reseted_dmm, case):
        dmm = make_reseted_dmm
        dmm.frequency_voltage_auto_range = case
        assert dmm.frequency_voltage_auto_range == case

    @pytest.mark.parametrize("case, expected", pFrequencyApertures)
    def test_frequency_aperture(self, make_reseted_dmm, case, expected):
        dmm = make_reseted_dmm
        dmm.frequency_aperture = case
        assert dmm.frequency_aperture == expected

    def test_configure_frequency(self, make_reseted_dmm):
        dmm = make_reseted_dmm

        # No parameters specified
        dmm.configure_frequency()
        assert dmm.mode == "voltage frequency"
        assert dmm.frequency_voltage_auto_range == 1
        assert dmm.frequency_aperture == 1

        # Four possible paths
        dmm.configure_frequency(measured_from="voltage_ac", measured_from_range=1,
                                aperture=1E-1)
        assert dmm.mode == "voltage frequency"
        assert dmm.frequency_voltage_range == 1
        assert dmm.frequency_voltage_auto_range == 0
        assert dmm.frequency_aperture == 1E-1
        dmm.configure_frequency(measured_from="voltage_ac",
                                measured_from_range="AUTO", aperture=1)
        assert dmm.mode == "voltage frequency"
        assert dmm.frequency_voltage_auto_range == 1
        assert dmm.frequency_aperture == 1
        dmm.configure_frequency(measured_from="current_ac", measured_from_range=1E-1,
                                aperture=1E-1)
        assert dmm.mode == "current frequency"
        assert dmm.frequency_current_range == 1E-1
        assert dmm.frequency_current_auto_range == 0
        assert dmm.frequency_aperture == 1E-1
        dmm.configure_frequency(measured_from="current_ac",
                                measured_from_range="AUTO", aperture=1)
        assert dmm.mode == "current frequency"
        assert dmm.frequency_current_auto_range == 1
        assert dmm.frequency_aperture == 1

        # Should raise ValueError
        with pytest.raises(ValueError):
            dmm.configure_frequency(measured_from="")

    def test_frequency_reading(self, make_reseted_dmm):
        dmm = make_reseted_dmm
        dmm.mode = "voltage frequency"
        value = dmm.frequency
        assert type(value) is float

    def test_configure_temperature(self, make_reseted_dmm):
        dmm = make_reseted_dmm
        dmm.configure_temperature()
        assert dmm.mode == "temperature"

    def test_temperature_reading(self, make_reseted_dmm):
        dmm = make_reseted_dmm
        dmm.mode = "temperature"
        value = dmm.temperature
        assert type(value) is float

    def test_configure_diode(self, make_reseted_dmm):
        dmm = make_reseted_dmm
        dmm.configure_diode()
        assert dmm.mode == "diode"

    def test_diode_reading(self, make_reseted_dmm):
        dmm = make_reseted_dmm
        dmm.mode = "diode"
        value = dmm.diode
        assert type(value) is float

    @pytest.mark.parametrize("case, expected", pCapacitanceRanges)
    def test_capacitance_range(self, make_reseted_dmm, case, expected):
        dmm = make_reseted_dmm
        dmm.capacitance_range = case
        assert dmm.capacitance_range == expected

    @pytest.mark.parametrize("case", pBooleans)
    def test_capacitance_auto_range(self, make_reseted_dmm, case):
        dmm = make_reseted_dmm
        dmm.capacitance_auto_range = case
        assert dmm.capacitance_auto_range == case

    def test_configure_capacitance(self, make_reseted_dmm):
        dmm = make_reseted_dmm

        # No parameters specified
        dmm.configure_capacitance()
        assert dmm.mode == "capacitance"
        assert dmm.capacitance_auto_range == 1

        # Two possible paths
        dmm.configure_capacitance(capacitance_range=1E-2)
        assert dmm.mode == "capacitance"
        assert dmm.capacitance_range == 1E-2
        assert dmm.capacitance_auto_range == 0
        dmm.configure_capacitance(capacitance_range="AUTO")
        assert dmm.mode == "capacitance"
        assert dmm.capacitance_auto_range == 1

    def test_capacitance_reading(self, make_reseted_dmm):
        dmm = make_reseted_dmm
        dmm.mode = "capacitance"
        value = dmm.capacitance
        assert type(value) is float

    def test_configure_continuity(self, make_reseted_dmm):
        dmm = make_reseted_dmm
        dmm.configure_continuity()
        assert dmm.mode == "continuity"

    def test_continuity_reading(self, make_reseted_dmm):
        dmm = make_reseted_dmm
        dmm.mode = "continuity"
        value = dmm.continuity
        assert type(value) is float
