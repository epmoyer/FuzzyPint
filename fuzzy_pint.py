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

    v1 = FuzzyPint(2.73, 'volt', 0.13, -0.13)
    v2 = FuzzyPint(9.77, 'volt', 0.13, -0.13)
    i1 = FuzzyPint(21.97, 'ampere', 0.21, -0.21)

    print('Object __repr__():')
    print(f'{indent}{v1!r}')
    print('Object __str__():')
    print(f'{indent}{v1}')

    print('\Add:')
    print(f'{indent}{v1=}')
    print(f'{indent}{v2=}')
    print(f'{indent}{v1+v2=}')

    print('\Subtract:')
    print(f'{indent}{v1=}')
    print(f'{indent}{v2=}')
    print(f'{indent}{v1-v2=}')

    print('Multiply:')
    v1 = FuzzyPint(2.73, 'volt', 0.1, -0.2)
    i1 = FuzzyPint(21.97, 'ampere', 0.3, -0.4)
    print(f'{indent}{v1=}')
    print(f'{indent}{i1=}')
    print(f'{indent}{v1*i1=}')


class FuzzyPint:
    def __init__(self, magnitude: float, units: str = None, err_p: float = 0.0, err_n: float = 0.0):
        assert err_p >= 0
        assert err_n <= 0
        units = UREG(units) if isinstance(units, str) else units
        self._quantity = magnitude * units
        self._err_p = err_p
        self._err_n = err_n

    def __add__(self, b):
        quantity = self._quantity + b._quantity
        err_p, err_n = FuzzyPint._get_error(self, b, FuzzyPint._add)
        return FuzzyPint(quantity.m, quantity.units, err_p, err_n)

    def __sub__(self, b):
        quantity = self._quantity + b._quantity
        err_p, err_n = FuzzyPint._get_error(self, b, FuzzyPint._sub)
        return FuzzyPint(quantity.m, quantity.units, err_p, err_n)

    def __mul__(self, b):
        quantity = self._quantity * b._quantity
        err_p, err_n = FuzzyPint._get_error(self, b, FuzzyPint._multiply)
        return FuzzyPint(quantity.m, quantity.units, err_p, err_n)
    
    @staticmethod
    def _get_error(a: 'FuzzyPint', b: 'FuzzyPint', function):
        a_m = a._quantity.m
        b_m = b._quantity.m
        nominal_m = function(a_m, b_m)

        errors = []
        for a_m_speculative, b_m_speculative in (
            (a_m + a._err_p, b_m + b._err_p),
            (a_m + a._err_n, b_m + b._err_p),
            (a_m + a._err_p, b_m + b._err_n),
            (a_m + a._err_n, b_m + b._err_n)
        ):
            result = function(a_m_speculative, b_m_speculative)
            error = result - nominal_m
            errors.append(error)
        err_p = max(errors)
        err_n = min(errors)
        assert err_p >= 0
        assert err_n <= 0

        return err_p, err_n

    @staticmethod
    def _multiply(a, b):
        return a * b

    @staticmethod
    def _add(a, b):
        return a + b

    @staticmethod
    def _sub(a, b):
        return a - b

    def __repr__(self):
        return (
            f'<FuzzyPint({self._quantity.m}, {self._quantity.units}, {self._err_p}, {self._err_n})>'
        )

    def __str__(self):
        return f'{self._quantity} [+{self._err_p}, {self._err_n}]'


if __name__ == "__main__":
    main()
