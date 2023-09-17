from pymeasure.instruments.instrument import Instrument
import pyvisa
from pymeasure.instruments.validators import strict_discrete_set
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

    def getIDN(self):
        self.write("*IDN?")
        return self.adapter.read()

print(instrument, adapter)
    
siglentObject = SDLbase(adapter)
print(siglentObject.getIDN())
# siglentObject.get_input_status()
# siglentObject.source_input


