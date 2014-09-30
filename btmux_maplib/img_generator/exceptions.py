
class BasicImagingException(Exception):
    """
    Basic exception for others to inherit or use.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
    

class InvalidImageMode(BasicImagingException):
    """
    Raised when someone tries to set an invalid map imaging mode.
    """

    def __str__(self):
        return repr("Invalid imaging mode: %s" % self.value)
