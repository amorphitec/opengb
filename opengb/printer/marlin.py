from opengb.printer import IPrinter


class Marlin(IPrinter):
    """
    Marlin firmware printer.
    """

    def __init__(self, to_addr, from_addr):
        super().__init__(to_addr, from_addr)
