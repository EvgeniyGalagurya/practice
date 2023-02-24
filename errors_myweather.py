class MyweatherErrorBase(Exception):
    """Common demominator for all exceptions raised by myweather module."""
    pass


class CityNameError(MyweatherErrorBase):

    error_text = ('Incorrect City name: (name can contains only '
                  'letters a-z, A-Z).\nTry again.')

    def __init__(self):
        super().__init__()
        self.msg = self.error_text

    def __str__(self):
        return self.msg


class CityNotFoundError(MyweatherErrorBase):

    error_text = 'City name is not found.\nTry again.'

    def __init__(self):
        super().__init__()
        self.msg = self.error_text

    def __str__(self):
        return self.msg
