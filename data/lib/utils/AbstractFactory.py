#----------------------------------------------------------------------------------------------------

    # Libraries
from .Singleton import Singleton
#----------------------------------------------------------------------------------------------------

    # Class
class AbstractFactory(metaclass = Singleton):
    '''Abstract Factory class.'''

    def __init__(self) -> None:
        self._data = {}


    @classmethod
    def register(cls_, key: str, cls: type) -> None:
        '''Register a class to the factory.

        Args:
            key (str): The key to register the class.
            cls (type): The class to register.
        '''
        AbstractFactory()._data[key] = cls


    @classmethod
    def create(cls, key: str, *args, **kwargs) -> object:
        '''Create an instance of a class.

        Args:
            key (str): The key to create the class.
            *args: The arguments to pass to the class.
            **kwargs: The keyword arguments to pass to the class.

        Returns:
            object: The instance of the class.
        '''
        cls = AbstractFactory()._data.get(key, None)
        if cls:
            return cls(*args, **kwargs)
        return None


    @classmethod
    def get(cls, key: str) -> object:
        '''Get the class.

        Args:
            key (str): The key to get the class.

        Returns:
            object: The class.
        '''
        return AbstractFactory()._data.get(key, None)


    def __contains__(self, key: str) -> bool:
        '''Check if the key is in the factory.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key is in the factory, otherwise False.
        '''
        return key in AbstractFactory()._data
    

    def __delitem__(self, key: str) -> None:
        '''Delete the class from the factory.

        Args:
            key (str): The key to delete.
        '''
        del AbstractFactory()._data[key]
#----------------------------------------------------------------------------------------------------
