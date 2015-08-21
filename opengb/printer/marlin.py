from opengb.printer import IPrinter
from opengb.printer import State 


class Marlin(IPrinter):
    """
    Marlin firmware printer.
    """

    def __init__(self, to_addr, from_addr):
        super().__init__(to_addr, from_addr)

    def _process_message_from_printer(self):
        """
        Process a message from the printer.
        """
        '''
        TODO:
        if temp_message:
            update local
            temp callback
        if error_message:
            log error callback
        if position_message:
            update local
            if z change: zchange callback
        '''
