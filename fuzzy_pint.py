#!/usr/bin/env python3

# Standard Library
import json

# Library
import pint
import click


# Local
from util_pint import pint_dict_to_pint, pint_to_pint_dict

APP_NAME = 'fuzzy_pint'
APP_VERSION = '0.0.1'

UREG = pint.UnitRegistry()


def main():
    """Fuzzy Pint demo."""
    fp = FuzzyPint(2.73, 'volts', 0.13, -0.13)
    print(fp)


class FuzzyPint:
    def __init__(self, magnitude: float, units: str = None, err_p: float = 0.0, err_n: float = 0.0):
        assert err_p > 0
        assert err_n <= 0
        self._quantity = magnitude * UREG(units)
        self._err_p = err_p
        self._err_n = err_n
    
    def __repr__(self):
        print(f'FuzzyPint({self._quantity.m}, {self._quantity.units}, {self._err_p}, {self._err_n})')


if __name__ == "__main__":
    main()
