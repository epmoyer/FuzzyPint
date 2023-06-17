![](docs/img/fuzz_pint_logo.jpg)
# FuzzyPint

FuzzyPint is a "wrapper" around [Pint](https://pint.readthedocs.io) objects that adds +/- error margins (which can be asymmetric) for the purpose of propagating "significant digits" through calculations.

## TL;DR
- Create a bunch of values with **units** and **error margin**.
- Do a bunch of math on them.
- Get a result with a (propagated) error margin.
- Display the result, with units, with the number of **significant digits** reflected by that result's error margin.

## Overview
FuzzyPint values correctness and simplicity over performance. Every math operation on (a pair of) FuzzyPint objects performs 5 calculations: A nominal calculation on the nominal magnitudes, and all 4 possible combinations of worst-case min/max error propagations.  FuzzyPint does not try to be "smart" about how errors propagate; instead it brute-forces all calculations to see what the resulting worst-case min/max error would be, then includes that (worst case) error margin in the result.


## Installation
There is no pip release (yet). FuzzyPint is a single file with a single external dependency (the [`pint`](https://pint.readthedocs.io) package), so for now you can just download `fuzzy_pint.py` to use it in a project.

To use FuzzyPint, import the FuzzyPint object like this:
```python
from fuzzy_pint import FuzzyPint
```

## Example
### Basic Calculations
Let's say you measure a resistor in the lab as "1000.2345 Ohms", and you know that the error of your multimeter (for resistance measurements) is +/- 0.01 ohms. You would enter that value like this:

```
>>> from fuzzy_pint import FuzzyPint
>>> r = FuzzyPint(1000.2345, "ohm", 0.01, -0.01)
>>> r
<FuzzyPint(1000.23, "ohm", err_p=0.01, err_n=-0.01)>
>>>
```

Now let's say you measure the voltage across that resistor as 5.4321 V, and you know that the error of your multimeter (for voltage measurements) is +/- 0.001 V. You would enter that value like this:

```
>>> v=FuzzyPint(5.4321, "volt", 0.001, -0.001)
>>> v
<FuzzyPint(5.4321, "volt", err_p=0.001, err_n=-0.001)>
>>>
```

You could then calculate the power dissipation in the resistor (P = V²/R) like this:

```
>>> p = v**2 / r
>>> p
<FuzzyPint(0.0295008, "volt ** 2 / ohm", err_p=1.11577e-05, err_n=-1.11555e-05)>
>>> 
```

Notice that FuzzyPint has calculated the resulting (propagated) error margin. The units are in "volt / ohms" so let's convert that to milliwatts...

```
>>> p
<FuzzyPint(29.5008, "milliwatt", err_p=0.0111577, err_n=-0.0111555)>
>>>
```

[Pint](https://pint.readthedocs.io) does the heavy lifting here (units conversion, including SI prefix scaling of the nominal magnitude), and FuzzyPint scales the errors to match the new (scaled) magnitude.

Now we can render the final result showing only the "significant" digits like this...

```
>>> p.significant()
'29.50 mW'
>>>
```
### JSON Serialization
If we wish to store this result in a JSON file for later use we can serialize the FuzzyPint object like this:

```
>>> d = p.to_serializable()
>>> d
{'value': 29.50079, 'units': 'milliwatt', 'err_p': 0.011157703020417409, 'err_n': -0.011155480409783675}
>>>
```

The `.to_serializable()` method returns a (JSON Serializable) dict:

```
>>> import json
>>> j = json.dumps(d, indent=4)
>>> print(j)
{
    "value": 29.50079,
    "units": "milliwatt",
    "err_p": 0.011157703020417409,
    "err_n": -0.011155480409783675
}
>>>
```

And we can recover a serialized FuzzyPint object like this:
```
>>> v_recovered = FuzzyPint.from_serializable(d)
>>> v_recovered
<FuzzyPint(29.5008, "milliwatt", err_p=0.0111577, err_n=-0.0111555)>
>>>
```

## Demo
You can demo the functionality by executing the module:

```
$ ./fuzzy_pint.py
fuzzy_pint 0.0.2
FuzzyPint.__repr__():
    v1: <FuzzyPint(2.73, "volt", err_p=0.13, err_n=-0.13)>
FuzzyPint.__str__():
    v1: 2.73 volt [+0.13, -0.13]
FuzzyPint.pretty():
    v1: 2.73 V [+0.13, -0.13]
FuzzyPint.significant():
    v1: 2.7 V
Dimensionless:
    d1: <FuzzyPint(123.4, "dimensionless", err_p=0, err_n=0)>
Conversion:
    w1=<FuzzyPint(1.23, "ampere * volt", err_p=0.01, err_n=-0.01)>
    w1.to("watt")=<FuzzyPint(1.23, "watt", err_p=0.01, err_n=-0.01)>
Add:
    v1=<FuzzyPint(2.73, "volt", err_p=0.13, err_n=-0.13)>
    v2=<FuzzyPint(9.77, "volt", err_p=0.13, err_n=-0.13)>
    v1+v2=<FuzzyPint(12.5, "volt", err_p=0.26, err_n=-0.26)>
    (v1+v2).pretty()='12.5 V [+0.26, -0.26]'
    (v1+v2).significant()='12.5 V'
Subtract:
    v1=<FuzzyPint(2.73, "volt", err_p=0.13, err_n=-0.13)>
    v2=<FuzzyPint(9.77, "volt", err_p=0.13, err_n=-0.13)>
    v1-v2=<FuzzyPint(-7.04, "volt", err_p=0.26, err_n=-0.26)>
    (v1-v2).pretty()='-7.04 V [+0.26, -0.26]'
    (v1-v2).significant()='7.0 V'
Multiply:
    v1=<FuzzyPint(2.73, "volt", err_p=0.1, err_n=-0.2)>
    i1=<FuzzyPint(21.97, "ampere", err_p=0.3, err_n=-0.4)>
    v1*i1=<FuzzyPint(59.9781, "ampere * volt", err_p=3.046, err_n=-5.406)>
    (v1*i1).pretty()='59.9781 A·V [+3.046, -5.406]'
    (v1*i1).significant()='60 A·V'
Divide:
    v1=<FuzzyPint(12.73, "volt", err_p=0.1, err_n=-0.2)>
    r1=<FuzzyPint(1234, "ohm", err_p=50, err_n=-50)>
    v1/r1=<FuzzyPint(0.010316, "volt / ohm", err_p=0.000520103, err_n=-0.000557478)>
    (v1/r1).pretty()='0.010316 V/Ω [+0.000520103, -0.000557478]'
    (v1/r1).significant()='0.0103 V/Ω'
Exponent:
    v1=<FuzzyPint(12.73, "volt", err_p=0.1, err_n=-0.2)>
    v1**2=<FuzzyPint(162.053, "volt ** 2", err_p=2.556, err_n=-5.052)>
    (v1**2).pretty()='162.053 V² [+2.556, -5.052]'
    (v1**2).significant()='162 V²'
Dimensionless Multiply:
    v1=<FuzzyPint(2.73, "volt", err_p=0.1, err_n=-0.2)>
    i1=2.0
    v1*i1=<FuzzyPint(5.46, "volt", err_p=0.2, err_n=-0.4)>
    (v1*i1).pretty()='5.46 V [+0.2, -0.4]'
    (v1*i1).significant()='5.5 V'
Prefix Scale Conversion: Example: 1.23456 from V -> mV:
    v1=<FuzzyPint(1.23456, "volt", err_p=0.0001, err_n=-0.0001)>
    v1*1000=<FuzzyPint(1234.56, "volt", err_p=0.1, err_n=-0.1)>
    (v1).to("millivolt")=<FuzzyPint(1234.56, "millivolt", err_p=0.1, err_n=-0.1)>
    (v1).to("millivolt").pretty()='1234.56 mV [+0.1, -0.1]'
    (v1).to("millivolt").significant()='1234.6 mV'
Significance Precedence with Asymmetric Error:
    v1=<FuzzyPint(1234.57, "volt", err_p=0.1, err_n=-0.1)>
    v1.significant()='1234.6 V'

    v1=<FuzzyPint(1234.57, "volt", err_p=0.1, err_n=-0.01)>
    v1.significant()='1234.6 V'

    v1=<FuzzyPint(1234.57, "volt", err_p=0.1, err_n=-0.001)>
    v1.significant()='1234.6 V'

    v1=<FuzzyPint(1234.57, "volt", err_p=0.01, err_n=-0.1)>
    v1.significant()='1234.6 V'

    v1=<FuzzyPint(1234.57, "volt", err_p=0.001, err_n=-0.1)>
    v1.significant()='1234.6 V'

Significance:
    v1=<FuzzyPint(1234.57, "volt", err_p=2000, err_n=-2000)>
    v1.significant()='1000 V'

    v1=<FuzzyPint(1234.57, "volt", err_p=200, err_n=-200)>
    v1.significant()='1200 V'

    v1=<FuzzyPint(1234.57, "volt", err_p=20, err_n=-0.2)>
    v1.significant()='1230 V'

    v1=<FuzzyPint(1234.57, "volt", err_p=2, err_n=-2)>
    v1.significant()='1235 V'

    v1=<FuzzyPint(1234.57, "volt", err_p=0.1, err_n=-0.1)>
    v1.significant()='1234.6 V'

    v1=<FuzzyPint(1234.57, "volt", err_p=0.12, err_n=-0.12)>
    v1.significant()='1234.6 V'

    v1=<FuzzyPint(1234.57, "volt", err_p=0.01, err_n=-0.01)>
    v1.significant()='1234.57 V'

    v1=<FuzzyPint(1234.57, "volt", err_p=0.009, err_n=-0.009)>
    v1.significant()='1234.568 V'

    v1=<FuzzyPint(1234.57, "volt", err_p=0.0009, err_n=-0.0009)>
    v1.significant()='1234.5678 V'

    v1=<FuzzyPint(1234.57, "volt", err_p=9e-05, err_n=-9e-05)>
    v1.significant()='1234.56780 V'

Significance, Zero Padding:
    v1=<FuzzyPint(1, "volt", err_p=0.1, err_n=-0.1)>
    v1.significant()='1.0 V'

    v1=<FuzzyPint(1, "volt", err_p=0.01, err_n=-0.01)>
    v1.significant()='1.00 V'

    v1=<FuzzyPint(1, "volt", err_p=0.001, err_n=-0.001)>
    v1.significant()='1.000 V'

JSON serialization
    v1: <FuzzyPint(2.55121, "volt", err_p=0.13, err_n=-0.13)>
    v1: 2.551212121212 volt [+0.13, -0.13]
    v1.significant()='2.6 V'
    v1.to_serializable()={'value': 2.5512, 'units': 'volt', 'err_p': 0.13, 'err_n': -0.13}
    json.dumps(v1.to_serializable())='{"value": 2.5512, "units": "volt", "err_p": 0.13, "err_n": -0.13}'
    v1_serialized={'value': 2.5512, 'units': 'volt', 'err_p': 0.13, 'err_n': -0.13}
    FuzzyPint.from_serializable(v1_serialized)=<FuzzyPint(2.5512, "volt", err_p=0.13, err_n=-0.13)>
$ 
```

## Why not use Pint's `Measurement` object?
Pint has a native `Measurement` object which can represent measurement error in a manner similar to FuzzyPint, but it has three significant limitations:

- It does not propagate errors properly for non-linear operations
    - This is a known issue. Pint's [Measurement](https://pint.readthedocs.io/en/stable/advanced/measurement.html) documentation says "Only linear combinations are currently supported."
- It does not support asymmetric error margins (e.g. `10 V +1/-2`)
- It does not natively support rendering a value's significant figures based on that value's error margin.

### An example of the non-linear issue with Pint's `Measurement` object

If we square a voltage of 10 V +/- 1 V using Pint's native `Measurement` object we get:

```
>>> from pint import UnitRegistry
>>> ureg = UnitRegistry()
>>> v = (10 * ureg.volt).plus_minus(1)
>>> print(v)
(10.0 +/- 1.0) volt
>>> print(v**2)
(100 +/- 20) volt ** 2
>>>
```

Pint's native `Measurement` object incorrectly reports the resulting error as `+/- 20`, but the error should be `+21 / -19` (because the worst case positive error would occur at `(10+1) * (10+1) == 121 == 100 + 21` and the worst case negative error would occur at `(10-1) * (10-1) == 81 == 100 - 19`).

For the same calculation FuzzyPint correctly reports the expected error of `+21 / -19`:

```
>>> from fuzzy_pint import FuzzyPint
>>> v = FuzzyPint(10, "volt", 1, -1)
>>> print(v)
10 volt [+1, -1]
>>> print(v**2)
100 volt ** 2 [+21.0, -19.0]
>>>
```


## Development Status
As of version `0.0.2`:

- Supported operations:
    - Add
    - Subtract
    - Multiply
    - Divide
    - Power (i.e. Exponentiation)
- There are no tests (yet); just a demonstration of functionality.
- There are no (known) bugs.
- I am plumbing this into a "real" data analysis project.  Once that project has successfully "kicked the tires" in a real-world application I will consider the API "stable" and I will add proper test cases.
