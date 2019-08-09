#!/usr/bin/env python
#===============================================================================
#> \file factory.py
## \brief
## \b Class factory in Python
## \author
## Marc Joos <marc.joos@gmail.com>
## \copyright
## Copyrights 2019, Marc Joos
## This file is distributed under the CeCILL-A & GNU/GPL licenses, see
## <http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html> and
## <http://www.gnu.org/licenses/>
#<
#===============================================================================

# Factory class
class DataFactory(object):
    data_maker = {}

    # Decorator to register a new class
    @classmethod
    def register_data(cls, typ):
        def wrapper(maker):
            cls.data_maker[typ] = maker
            return cls
        return wrapper

    # Class maker for new classes with explicit error message if the class does not exist
    @classmethod
    def make_data(cls, typ, *args, **kwargs):
        try:
            return cls.data_maker[typ](*args, **kwargs)
        except KeyError:
            print("TypeError\n'" + typ + "' extension does not exist!")

# User Interface class: generic class the user will use
class UIClass(object):
    """Generic User class:
    Use this class to do stuff on dummy files.

    Usage:
      myobj = UIClass(fname)
      myobj.load()
    With:
      fname: dummy file name
    """
    def __init__(self, fname):
        self.fname = fname
        # List of data we will retrieve from ad hoc classes
        self._data = ['n', 'x', 'y', 'str']

    # Some method that is calling the method that is calling the class maker
    def load(self):
        ext = self.fname.split('.')[-1]
        self.ext = ext
        self._get_data(self.fname, ext)

    # Method that calls the class maker
    def _get_data(self, fname, ext):
        data_reader = DataFactory.make_data(ext)
        data_reader.load(fname=fname)
        # We transparently load attributes from the created class; we get only the ones defined in _data
        for attr in self._data:
            self.__setattr__(attr, data_reader.__getattribute__(attr))
        # Get extra methods if defined -- note that the same could be used to discover attributes
        # instead of explicitely defining them in __init__
        for attr in dir(data_reader):
            if callable(getattr(data_reader, attr)) and not attr in dir(self):
                self.__setattr__(attr, data_reader.__getattribute__(attr))

# Generic class to build the ad hoc classes; we will inherit from this class
class DataReader(object):
    def __init__(self):
        self.n = 0

    # Hidden empty method that will be defined in the ad hoc class
    def _load(self, *args, **kwargs):
        pass

    # Method used to call the hidden method that will be defined in the ad hoc class
    def load(self, fname):
        self.str = "If defined, then it was loaded"
        self._load(fname)

# Ad hoc class for extension 'a'
@DataFactory.register_data('a')
class ADataReader(DataReader):
    def __init__(self):
        DataReader.__init__(self)
        self.x = 42
        self.y = 42

    # Actual definition of the previously empty method to do stuff
    def _load(self, fname):
        print("fname: {}".format(fname))

# Ad hoc class for extension 'b'
@DataFactory.register_data('b')
class BDataReader(DataReader):
    def __init__(self):
        DataReader.__init__(self)
        self.x = 'test'
        self.y = [i for i in range(10)]

    # Actual definition of the previously empty method to do stuff
    def _load(self, fname):
        print("fname extension: {}".format(fname.split('.')[-1]))

    def do_smthg(self):
        print("Specific method only for BDataReader")

