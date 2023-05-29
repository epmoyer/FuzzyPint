#!/usr/bin/env python3

# Standard Library
from math import log10, floor
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
    d1 = FuzzyPint(123.4)

    print('FuzzyPint.__repr__():')
    print(f'{indent}v1: {v1!r}')
    print('FuzzyPint.__str__():')
    print(f'{indent}v1: {v1}')
    print('FuzzyPint.pretty():')
    print(f'{indent}v1: {v1.pretty()}')
    print('FuzzyPint.significant():')
    print(f'{indent}v1: {v1.significant()}')
    return
    print('Dimensionless:')
    print(f'{indent}d1: {d1!r}')

    print('Add:')
    print(f'{indent}{v1=}')
    print(f'{indent}{v2=}')
    print(f'{indent}{v1+v2=}')

    print('Subtract:')
    print(f'{indent}{v1=}')
    print(f'{indent}{v2=}')
    print(f'{indent}{v1-v2=}')

    print('Multiply:')
    v1 = FuzzyPint(2.73, 'volt', 0.1, -0.2)
    i1 = FuzzyPint(21.97, 'ampere', 0.3, -0.4)
    print(f'{indent}{v1=}')
    print(f'{indent}{i1=}')
    print(f'{indent}{v1*i1=}')

    print('Divide:')
    v1 = FuzzyPint(12.73, 'volt', 0.1, -0.2)
    r1 = FuzzyPint(1234, 'ohm', 50, -50)
    print(f'{indent}{v1=}')
    print(f'{indent}{r1=}')
    print(f'{indent}{v1/r1=}')

    print('Exponent:')
    v1 = FuzzyPint(12.73, 'volt', 0.1, -0.2)
    print(f'{indent}{v1=}')
    print(f'{indent}{v1**2=}')

    print('Dimensionless Multiply:')
    v1 = FuzzyPint(2.73, 'volt', 0.1, -0.2)
    i1 = 2.0
    print(f'{indent}{v1=}')
    print(f'{indent}{i1=}')
    print(f'{indent}{v1*i1=}')


class FuzzyPint:
    def __init__(self, magnitude: float, units: str = None, err_p: float = 0.0, err_n: float = 0.0):
        assert err_p >= 0
        assert err_n <= 0
        units = 'dimensionless' if units is None else units
        units = UREG(units) if isinstance(units, str) else units
        self._quantity = magnitude * units
        self._err_p = err_p
        self._err_n = err_n

    def __add__(self, b):
        return FuzzyPint._apply_function(self, b, FuzzyPint._add)

    def __sub__(self, b):
        return FuzzyPint._apply_function(self, b, FuzzyPint._sub)

    def __mul__(self, b):
        return FuzzyPint._apply_function(self, b, FuzzyPint._multiply)

    def __truediv__(self, b):
        return FuzzyPint._apply_function(self, b, FuzzyPint._divide)
    
    def __pow__(self, b):
        return FuzzyPint._apply_function(self, b, FuzzyPint._pow)
    
    @staticmethod
    def _apply_function(a: 'FuzzyPint', b: 'FuzzyPint', function):
        # Convert dimensionless quantities to FuzzyPint objects if supplied
        if isinstance(a, (float, int)):
            a = FuzzyPint(a)
        if isinstance(b, (float, int)):
            b = FuzzyPint(b)

        quantity = function(a._quantity, b._quantity)
        err_p, err_n = FuzzyPint._get_error(a, b, function)
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
    def _add(a, b):
        return a + b

    @staticmethod
    def _sub(a, b):
        return a - b

    @staticmethod
    def _multiply(a, b):
        return a * b

    @staticmethod
    def _divide(a, b):
        return a / b

    @staticmethod
    def _pow(a, b):
        return a ** b
    
    def pretty(self):
        return f'{self._quantity:~P} [+{self._err_p}, {self._err_n}]'

    def significant(self):
        # err_p_exp = floor(log10(abs(self._err_p)))
        # err_n_exp = floor(log10(abs(self._err_n)))
        q_magnitude = self._quantity.m
        q_significand, q_exponent, q_is_negative = self._to_scientific(q_magnitude)
        print(f'{q_significand=}, {q_exponent=}, {q_is_negative=}')

        err_p_significand, err_p_exponent, err_p_is_negative = self._to_scientific(self._err_p)
        print(f'{err_p_significand=}, {err_p_exponent=}, {err_p_is_negative=}')

        err_n_significand, err_n_exponent, err_n_is_negative = self._to_scientific(self._err_n)
        print(f'{err_n_significand=}, {err_n_exponent=}, {err_n_is_negative=}')

        # magnitude_exp = floor(log10(abs(q_magnitude)))

        return f'{self._quantity:~P} [+{self._err_p}, {self._err_n}]'
    
    @staticmethod
    def _to_scientific(value: float):
        is_negative = value < 0
        # log = log10(abs(value))
        # exponent = floor(log)
        exponent = floor(log10(abs(value)))
        significand = value * 10**(-exponent)
        return significand, exponent, is_negative
        

    def __repr__(self):
        return (
            f'<FuzzyPint({self._quantity.m}, {self._quantity.units}, {self._err_p}, {self._err_n})>'
        )

    def __str__(self):
        return f'{self._quantity} [+{self._err_p}, {self._err_n}]'


if __name__ == "__main__":
    main()
