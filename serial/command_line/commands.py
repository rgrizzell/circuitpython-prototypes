""" Opens a second serial connection and listens for commands """
import usb_cdc


class Commands(object):
    def __init__(self):
        self.not_found = lambda x: self.echo("Invalid command. See 'help' for usage.")
        self.serial = usb_cdc.data
        self.serial.timeout = 0.1

    def _cmd_list(self):
        for func in dir(self):
            if callable(getattr(self, func)) and not func.startswith("_"):
                yield func

    def _listen(self):
        # Process the serial interface for input.
        if self.serial.in_waiting > 0:
            line = self.serial.readline().decode()
            self.echo(line, raw=True)
            args = line.strip().split()
    
            if len(args) > 0:
                print(args)
                # Get the base command from the list of arguments
                cmd = args.pop(0)
                # Lookup the received command.
                func = getattr(self, cmd, self.not_found)
                # Execute the command and pass the rest of the arguments
                #func(*args)

    def echo(self, data, raw=False):
        b = bytearray(data.encode())
        if not raw:
            b = b + b"\n\r"
        self.serial.write(b)

    def help(self):
        self.echo("List of Commands")
        self.echo(", ".join(self._cmd_list()))
