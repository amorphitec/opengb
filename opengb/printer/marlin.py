from opengb.printer import IPrinter
from opengb.printer import States 


class Marlin(IPrinter):
    """
    Marlin firmware printer.
    """

    def __init__(self, to_addr, from_addr):
        self._state = States.READY
        super().__init__(to_addr, from_addr)

    def run(self):
        '''
        # look for incoming serial data
        if (self.sp.inWaiting() > 0):
            result = self.sp.readline().replace("\n", "")

            # send it back to tornado
            self.resultQ.put(result)
        '''
        pass
