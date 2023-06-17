#!/usr/bin/env python3

# Standard Library
from math import log10, floor
from typing import Tuple
import json

# Library
import pint
import click


# Local
# from util_pint import pint_dict_to_pint, pint_to_pint_dict

APP_NAME = 'fuzzy_pint'
APP_VERSION = '0.0.1'
DEBUG_ENABLE = False

UREG = pint.UnitRegistry()


def main():
    """Fuzzy Pint demo."""
    indent = ' ' * 4

    v1 = FuzzyPint(2.73, 'volt', 0.13, -0.13)
    v2 = FuzzyPint(9.77, 'volt', 0.13, -0.13)
    i1 = FuzzyPint(21.97, 'ampere', 0.21, -0.21)
    w1 = FuzzyPint(1.23, 'ampere*volt', 0.01, -0.01)
    d1 = FuzzyPint(123.4)

    print('FuzzyPint.__repr__():')
    print(f'{indent}v1: {v1!r}')
    print('FuzzyPint.__str__():')
    print(f'{indent}v1: {v1}')
    print('FuzzyPint.pretty():')
    print(f'{indent}v1: {v1.pretty()}')
    print('FuzzyPint.significant():')
    print(f'{indent}v1: {v1.significant()}')
    print('Dimensionless:')
    print(f'{indent}d1: {d1!r}')
    print('Conversion:')
    print(f'{indent}{w1=}')
    print(f'{indent}{w1.to("watt")=}')

    print('Add:')
    print(f'{indent}{v1=}')
    print(f'{indent}{v2=}')
    print(f'{indent}{v1+v2=}')
    print(f'{indent}{(v1+v2).pretty()=}')
    print(f'{indent}{(v1+v2).significant()=}')

    print('Subtract:')
    print(f'{indent}{v1=}')
    print(f'{indent}{v2=}')
    print(f'{indent}{v1-v2=}')
    print(f'{indent}{(v1-v2).pretty()=}')
    print(f'{indent}{(v1-v2).significant()=}')

    print('Multiply:')
    v1 = FuzzyPint(2.73, 'volt', 0.1, -0.2)
    i1 = FuzzyPint(21.97, 'ampere', 0.3, -0.4)
    print(f'{indent}{v1=}')
    print(f'{indent}{i1=}')
    print(f'{indent}{v1*i1=}')
    print(f'{indent}{(v1*i1).pretty()=}')
    print(f'{indent}{(v1*i1).significant()=}')

    print('Divide:')
    v1 = FuzzyPint(12.73, 'volt', 0.1, -0.2)
    r1 = FuzzyPint(1234, 'ohm', 50, -50)
    print(f'{indent}{v1=}')
    print(f'{indent}{r1=}')
    print(f'{indent}{v1/r1=}')
    print(f'{indent}{(v1/r1).pretty()=}')
    print(f'{indent}{(v1/r1).significant()=}')

    print('Exponent:')
    v1 = FuzzyPint(12.73, 'volt', 0.1, -0.2)
    print(f'{indent}{v1=}')
    print(f'{indent}{v1**2=}')
    print(f'{indent}{(v1**2).pretty()=}')
    print(f'{indent}{(v1**2).significant()=}')

    print('Dimensionless Multiply:')
    v1 = FuzzyPint(2.73, 'volt', 0.1, -0.2)
    i1 = 2.0
    print(f'{indent}{v1=}')
    print(f'{indent}{i1=}')
    print(f'{indent}{v1*i1=}')
    print(f'{indent}{(v1*i1).pretty()=}')
    print(f'{indent}{(v1*i1).significant()=}')

    print('Prefix Scale Conversion: Example: 1.23456 from V -> mV:')
    v1 = FuzzyPint(1.23456, 'volt', 0.0001, -0.0001)
    print(f'{indent}{v1=}')
    print(f'{indent}{v1*1000=}')
    print(f'{indent}{(v1).to("millivolt")=}')
    print(f'{indent}{(v1).to("millivolt").pretty()=}')
    print(f'{indent}{(v1).to("millivolt").significant()=}')

    # print('Significance:')
    for v1 in (
        'Significance Precedence with Asymmetric Error:',
        FuzzyPint(1234.5678, 'volt', 0.1, -0.1),
        FuzzyPint(1234.5678, 'volt', 0.1, -0.01),
        FuzzyPint(1234.5678, 'volt', 0.1, -0.001),
        FuzzyPint(1234.5678, 'volt', 0.01, -0.1),
        FuzzyPint(1234.5678, 'volt', 0.001, -0.1),
        'Significance:',
        FuzzyPint(1234.5678, 'volt', 2000.0, -2000.0),
        FuzzyPint(1234.5678, 'volt', 200.0, -200.0),
        FuzzyPint(1234.5678, 'volt', 20.0, -0.2),
        FuzzyPint(1234.5678, 'volt', 2.0, -2.0),
        FuzzyPint(1234.5678, 'volt', 0.1, -0.1),
        FuzzyPint(1234.5678, 'volt', 0.12, -0.12),
        FuzzyPint(1234.5678, 'volt', 0.01, -0.01),
        FuzzyPint(1234.5678, 'volt', 0.009, -0.009),
        FuzzyPint(1234.5678, 'volt', 0.0009, -0.0009),
        FuzzyPint(1234.5678, 'volt', 0.00009, -0.00009),
        'Significance, Zero Padding:',
        FuzzyPint(1.0, 'volt', 0.1, -0.1),
        FuzzyPint(1.0, 'volt', 0.01, -0.01),
        FuzzyPint(1.0, 'volt', 0.001, -0.001),
    ):
        if isinstance(v1, str):
            # This is a heading
            print(v1)
            continue
        print(f'{indent}{v1=}')
        print(f'{indent}{v1.significant()=}')
        print()

    print('JSON serialization')
    v1 = FuzzyPint(2.551212121212, 'volt', 0.13, -0.13)
    print(f'{indent}v1: {v1!r}')
    print(f'{indent}v1: {v1}')
    print(f'{indent}{v1.significant()=}')
    print(f'{indent}{v1.to_serializable()=}')
    print(f'{indent}{json.dumps(v1.to_serializable())=}')
    v1_serialized = v1.to_serializable()
    print(f'{indent}{v1_serialized=}')
    print(f'{indent}{FuzzyPint.from_serializable(v1_serialized)=}')

class FuzzyPint:
    def __init__(self, magnitude: float, units: str = None, err_p: float = 0.0, err_n: float = 0.0):
        assert err_p >= 0
        assert err_n <= 0
        units = 'dimensionless' if units is None else units
        units = UREG(units) if isinstance(units, str) else units
        self._quantity = magnitude * units
        self._err_p = err_p
        self._err_n = err_n

    def clone(self):
        return FuzzyPint(self._quantity.m, self._quantity.units, self._err_p, self._err_n)

    def to(self, units: str):
        """Convert units.

        Some conversions (such as 'volts' to 'millivolts') may change the scale of the property's
        magnitude, in which case it is necessary for us to similarly scale the associated error.

        This conversion auto-detects such scale changes and scales the errors accordingly.
        """
        if isinstance(units, str):
            units = UREG(units)
        new_object = self.clone()
        new_object._quantity = self._quantity.to(units)
        if new_object._quantity.m != self._quantity.m:
            # The units change scaled the magnitude, so scale the errors similarly.
            scale = new_object._quantity.m / self._quantity.m
            new_object._err_p *= scale
            new_object._err_n *= scale
        return new_object
    
    def to_serializable(self, extended_precision=3):
        q_magnitude, _ = self.significant_magnitude(extended_precision=extended_precision)
        return {
            'value': q_magnitude,
            'units': f'{self._quantity.units:D}',
            'err_p': self._err_p,
            'err_n': self._err_n,
        }
    
    @classmethod
    def from_serializable(cls, object: dict) -> 'FuzzyPint':
        return FuzzyPint(
            object['value'],
            object['units'],
            object['err_p'],
            object['err_n'],
        )

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
            (a_m + a._err_n, b_m + b._err_n),
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
        return f'{self._quantity:g~P} [+{self._err_p:g}, {self._err_n:g}]'

    def significant(self):

        q_magnitude, decimal_rounding_digits = self.significant_magnitude()
        quantity = q_magnitude * self._quantity.units

        return f'{quantity:0.{decimal_rounding_digits}f~P}'
    
    def significant_magnitude(self, extended_precision: int = 0) -> Tuple[float, int]:
        """Return the significant part of the magnitude.

        The caller may request additional precision. This is typically used when
        storing values that will be used for future calculations (so that the
        precision is not prematurely truncated).

        Args:
            extended_precision (int, optional): Additional decimal digits of precision
            to use. Defaults to 0.

        Returns:
            Tuple[float, int]:
                ( The quantity (rounded to significant digits),
                  The number of decimal digits of precision )
        """
        q_magnitude = self._quantity.m
        q_significand, q_exponent, q_is_negative = self._float_to_scientific(q_magnitude)
        _debug_print(f'{q_significand=}, {q_exponent=}, {q_is_negative=}')

        err_p_significand, err_p_exponent, err_p_is_negative = self._float_to_scientific(
            self._err_p / (10 ** extended_precision)
        )
        _debug_print(f'{err_p_significand=}, {err_p_exponent=}, {err_p_is_negative=}')

        err_n_significand, err_n_exponent, err_n_is_negative = self._float_to_scientific(
            self._err_n / (10 ** extended_precision)
        )
        _debug_print(f'{err_n_significand=}, {err_n_exponent=}, {err_n_is_negative=}')

        err_exponent_max = max(err_p_exponent, err_n_exponent)
        _debug_print(f'{err_exponent_max=}')
        # print(f'🟠 {err_exponent_max=}')

        # Strip insignificant digits
        shift_exponent = q_exponent - err_exponent_max
        _debug_print(f'{shift_exponent=}')
        q_significand = round(q_significand * 10 ** (shift_exponent), 0) * 10 ** (-shift_exponent)
        _debug_print(f'{q_significand=}')
        q_magnitude = self._scientific_to_float(q_significand, q_exponent, q_is_negative)
        _debug_print(f'{q_magnitude=}')

        # Round any remaining insignificant "display digits"
        # (because we are working in floating point, there may be a very small epsilon in the
        # floating point representation of q_magnitude, so we will strip it)
        decimal_rounding_digits = abs(err_exponent_max) if err_exponent_max < 0 else 0

        _debug_print(f'{decimal_rounding_digits=}')
        # print(f'🟠 {decimal_rounding_digits=}')
        q_magnitude = round(q_magnitude, decimal_rounding_digits)
        _debug_print(f'{q_magnitude=}')

        return q_magnitude, decimal_rounding_digits

    @staticmethod
    def _float_to_scientific(value: float):
        is_negative = value < 0
        exponent = floor(log10(abs(value)))
        significand = value * 10 ** (-exponent)
        return significand, exponent, is_negative

    @staticmethod
    def _scientific_to_float(significand: float, exponent: int, is_negative: bool) -> float:
        value = significand * 10 ** exponent
        return -value if is_negative else value

    def __repr__(self):
        return (
            f'<FuzzyPint({self._quantity.m:g}, "{self._quantity.units}", err_p={self._err_p:g}, err_n={self._err_n:g})>'
        )

    def __str__(self):
        return f'{self._quantity} [+{self._err_p}, {self._err_n}]'


def _debug_print(text):
    if not DEBUG_ENABLE:
        return
    print(f'🟣  {text}')


if __name__ == "__main__":
    main()
