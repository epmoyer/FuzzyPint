#!/usr/bin/env python3

# Standard Library
import json

# Library
import pint
import click


# Local
# from util_pint import pint_dict_to_pint, pint_to_pint_dict

APP_NAME = 'fuzzy_pint'
APP_VERSION = '0.0.1'

UREG = pint.UnitRegistry()


def main():
    """Fuzzy Pint demo."""
    indent = ' ' * 4

    v1 = FuzzyPint(2.73, 'volts', 0.13, -0.13)
    print('Object __repr__():')
    print(f'{indent}{v1!r}')
    print('Object __str__():')
    print(f'{indent}{v1}')

    v2 = FuzzyPint(9.77, 'volts', 0.13, -0.13)
    print(f'\n{v1=}\n{v2=}\n{v1+v2=}')



class FuzzyPint:
    def __init__(self, magnitude: float, units: str = None, err_p: float = 0.0, err_n: float = 0.0):
        assert err_p > 0
        assert err_n <= 0
        self._quantity = magnitude * UREG(units)
        self._err_p = err_p
        self._err_n = err_n
    
    # def __sum__(self, b):
    #     quantity = self._quantity + b._quantity
    #     err_p = self._err_p + b._err_p
    #     err_n = self._err_n + b._err_n
    #     return FuzzyPint(quantity.m, quantity.units, err_p, err_n)

    def __repr__(self):
        return f'<FuzzyPint({self._quantity.m}, {self._quantity.units}, {self._err_p}, {self._err_n})>'
    
    def __str__(self):
        return f'{self._quantity} [+{self._err_p}, {self._err_n}]'


if __name__ == "__main__":
    main()
