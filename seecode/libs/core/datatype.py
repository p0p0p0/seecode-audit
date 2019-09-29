# coding: utf-8

import copy
import types
import re


class AttribDict(dict):
    """
    This class defines the config object, inheriting from Python data
    type dictionary.
    >>> foo = AttribDict()
    >>> foo.bar = 1
    >>> foo.bar
    1
    """

    def __init__(self, indict=None, attribute=None):
        if indict is None:
            indict = {}

        # Set any attributes here - before initialisation
        # these remain as normal attributes
        self.attribute = attribute
        dict.__init__(self, indict)
        self.__initialised = True

        # After initialisation, setting attributes
        # is the same as setting an item

    def __getattr__(self, item):
        """
        Maps values to attributes
        Only called if there *is NOT* an attribute with this name
        """

        try:
            return self.__getitem__(item)
        except KeyError:
            raise Exception("unable to access item '%s'" % item)

    def __setattr__(self, item, value):
        """
        Maps attributes to values
        Only if we are initialised
        """

        # This test allows attributes to be set in the __init__ method
        if "_AttribDict__initialised" not in self.__dict__:
            return dict.__setattr__(self, item, value)

        # Any normal attributes are handled normally
        elif item in self.__dict__:
            dict.__setattr__(self, item, value)

        else:
            self.__setitem__(item, value)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, dict):
        self.__dict__ = dict

    def __deepcopy__(self, memo):
        retVal = self.__class__()
        memo[id(self)] = retVal

        for attr in dir(self):
            if not attr.startswith('_'):
                value = getattr(self, attr)
                if not isinstance(value, (types.BuiltinFunctionType, types.FunctionType, types.MethodType)):
                    setattr(retVal, attr, copy.deepcopy(value, memo))

        for key, value in self.items():
            retVal.__setitem__(key, copy.deepcopy(value, memo))

        return retVal


class ReVerify(object):

    def __init__(self, expression, flag_str, name=None):
        """

        :param expression: 正则表弟
        :param flag_str: 标志位
        :param name: 检测名称
        """
        if flag_str == 'I':
            flag = re.I
        elif flag_str == 'M':
            flag = re.M
        elif 'I' in flag_str and 'M' in flag_str:
            flag = re.I | re.M

        if flag:
            self.regex = re.compile(expression, flag)
        else:
            self.regex = re.compile(expression)

        self.__name = name or expression

    @property
    def name(self):
        return self.__name

    def verify(self, target_str):
        """

        :param target_str: 目标字符串
        :return:
        """
        status = False
        match_str = None

        if target_str:
            result = self.regex.search(target_str)
            if result:
                status = True
                match_str = result.group()

        return status, match_str
