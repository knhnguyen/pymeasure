# Instrument Control with PyMeasure
This repository contains Python code for controlling instruments using PyMeasure, a Python package that simplifies scientific measurements. The code provided here is tailored for managing the SDL1020X-E, a high-performance DC electronic load manufactured by SIGLENT. The SDL1020X-E offers precise load control with adjustable current slew rates ranging from 0.001 A/μs to 2.5 A/μs. This instrument features a user-friendly 3.5-inch TFT-LCD display, integrated communication interfaces (RS232, USB, LAN), support for various operating modes (CC, CV, CP, CR, LED), and robust protection functions (OCP, OPP, OTP, LRV). Its versatility makes it ideal for applications in industries such as power, battery, LED lighting, automotive electronics, and aerospace. Engineers and technicians can conveniently control and monitor the SDL1020X-E remotely via a PC, making it an indispensable tool.

Please note that this document provides only a fragment of the information available in the complete Programming Guide for the SDL1000X series. The guide offers comprehensive details on programming and utilizing this instrument to its full potential.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Supported Commands](#supported-commands)
- [Supplementary Documentation](#supplementary-documentation)

## Prerequisites

Before using this code, make sure you have the following:

- Python installed (Python 3.8 or higher)
- PyMeasure package installed
- Access to the instrument with its IP address

## Installation

To install the required packages, you can use pip:

```bash
pip install pymeasure
```

## Usage
1. Import the necessary libraries and initialize connection:
```python
  import pyvisa
  from pymeasure.instruments.siglenttechnologies.siglent_sdl10xx import SDLbase
```
2. Create instances of SDLbase class:
```python
  #INITIALIZE CONNTECTION SAMPLE
  ip_addr = "169.254.245.175"   
  adapter = VISAAdapter('TCPIP0::169.254.245.175::inst0::INSTR')

  # Create instances of command classes
  siglentObject = SDLbase(adapter)
```
3. Use the provided commands to control and query the instrument. See the Supported Commands section for details on available commands.
```python
  # SAMPLE COMMANDS
  # SETTING MODE IN STATIC OPERATION
  siglentObject.mode_static_operation = "CURRent"

  # QUERY CURRENT MODE IN STATIC OPERATION.
  print(siglentObject.mode_static_operation)

  # GET REAL TIME VOLTAGE MEASUREMENT 
  print(siglentObject.measure_voltage_dc)
```

## Supported Commands
  - source_input: Getter and setter for the input status of the load in the form of "ON" or "OFF".
  - event_status: Getter and setter for the bits in the standard event status enable register.
  - status_byte_enable: Getter and setter for the bits in the status byte enable register.
  - mode_transient_operation: Getter and setter for the mode in transient operation, which can be "CURRent," "VOLTage," "POWer," or "RESistance."
  - mode_static_operation: Getter and setter for the mode in static operation, which can be "CURRent," "VOLTage," "POWer," "RESistance," or "LED."
  - current_range_CC_static_operation: Getter and setter for the current range in CC mode in static operation, with options "MINimum," "MAXimum," or "DEFault."
  - voltage_range_CC_static_operation: Getter and setter for the voltage range in CC mode in static operation, with options "MINimum," "MAXimum," or "DEFault."
  - voltage_value_CV_static_operation: Getter and setter for the preset voltage value in CV mode in static operation, with options "MINimum," "MAXimum," or "DEFault."
  - time_measurement_switch: Getter and setter for enabling or disabling the time measurement switch, with options "ON," "OFF," "1," or "0."
  - measure_voltage_dc: Measurement command to get the real-time voltage measurement value.
  - measure_current_dc: Measurement command to get the real-time current measurement value.
  - measure_power_dc: Measurement command to get the real-time power measurement value.
  - measure_resistance_dc: Measurement command to get the real-time resistance measurement value.
  - measure_external: Measurement command to get the real-time external measurement value in external sink mode.
  - wait_until_operations_complete(): A method to make the instrument wait until all pending commands are completed before executing additional commands.
  - get_idn(): A method to query the instrument's identification information using "*IDN?".

## Supplementary Documentation
For comprehensive programming and utilization information, please refer to the complete Programming Guide for the SDL1000X series: https://www.siglenteu.com/wp-content/uploads/dlm_uploads/2019/05/SDL1000X-Programming_Guide-V1.0.pdf.

