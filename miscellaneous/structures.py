"""
This module provides data structures/patterns (classes or decorators).
"""


from typing import Set, Any
from types import MethodType
from miscellaneous import constants as const
import tools.param_validators as param_val


class Singleton:
    """
    Represents singleton data pattern applicable on class / function / method . When applied on a class,
    only one instance of the class is allowed for whole program lifespan. When applied on a function / method , only
    one call is allowed for whole program lifespan. The decorator can be applied on more classes / functions / methods,
    not only on one object of the program. It does not change decorated object.

    Attributes:
        _called (Set[Any]): Set data structure which keeps one use across classes / functions / methods.
        _function (Any): Class / function / method on which the decorator is applied.
    """

    _called: Set[Any] = set()

    def __init__(self, decorated_object: Any):
        """
        Saves decorated object as attribute, for later lookup.

        Args:
            decorated_object (Any): Decorated object.
        """
        self._decorated_object = decorated_object

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        It checks if decorated object was not already instantiated or called.
        If does not, it allows to create / call it. The method is called when decorator
        is applied on class / function / method.

        Args:
            *args (Any): Positional arguments.
            **kwargs (Any): Key-worded arguments.

        Returns (Any): Decorated object itself without change.

        Exceptions:
            Exception: Violence of singleton paradigm of decorated object.
        """
        if self._decorated_object not in self._called:
            self._called.add(self._decorated_object)
        else:
            raise Exception(
                f"Decorated {self._decorated_object} as `Singleton` can be called " f"/ instantiated only once!"
            )

        return self._decorated_object(*args, **kwargs)

    def __get__(self, instance: Any, owner: Any) -> Any:
        """
        The method is needed to work with class method.

        Args:
            instance (Any): Class instance.
            owner (Any): Instance class owner.

        Returns (Any):

        Exceptions:
            Exception: Violence of singleton paradigm of decorated object.
        """
        if instance is None:
            return self

        if owner not in self._called:
            self._called.add(owner)
        else:
            raise Exception(
                f"Decorated {self._decorated_object} as `Singleton` can be called " f"/ instantiated only once!"
            )

        return self.__class__(MethodType(self._decorated_object, instance))


class Resolution:
    """
    Class for storing resolution information.

    Attributes:
        width (int): Resolution width.
        height (int): Resolution height.
        channels (int): Resolution's number of channels. It can be set to `1` (grayscale), `3` (RGB), `4` (RGBA) or
            `-1` for unknown/not set.
    """

    @property
    def width(self) -> None:
        """
        N/A
        """
        return self._width

    @width.setter
    def width(self, res_width: int):
        """
        N/A
        """
        param_val.check_type(res_width, int)
        param_val.check_parameter_value_in_range(res_width, 1, const.MAX_RESOLUTION_WIDTH)
        self._width = res_width

    @property
    def height(self):
        """
        N/A
        """
        return self._height

    @height.setter
    def height(self, res_height: int):
        """
        N/A
        """
        param_val.check_type(res_height, int)
        param_val.check_parameter_value_in_range(res_height, 1, const.MAX_RESOLUTION_WIDTH)
        self._height = res_height

    @property
    def channels(self):
        """
        N/A
        """
        return self._channels

    @channels.setter
    def channels(self, res_channels: int):
        """
        N/A
        """
        param_val.check_type(res_channels, int)
        param_val.check_parameter_value_in_list(res_channels, [-1, 1, 3, 4])   # `-1` stands for unknown channel.
        self._channels = res_channels

    def __init__(self, res_width: int, res_height: int, res_channels: int = -1) -> None:
        """
        N/A

        Args:
            res_width (int): Resolution width.
            res_height (int): Resolution height.
            res_channels (int): Resolution's number of channels. By default it sets `res_channels` to unknown symbolic
                value.
        """
        self.width = res_width
        self.height = res_height
        self.channels = res_channels

    def get_pixels_count(self) -> int:
        """
        Computes pixels count of the resolution.

        Returns:
            int: Pixels count.
        """
        return self.height * self.width
