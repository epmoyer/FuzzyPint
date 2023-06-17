# FuzzyPint

Fuzzy Pint is a "wrapper" around [Pint](https://pint.readthedocs.io) objects which adds +/- error margins for the purpose of propagating "significant digits" through calculations.

## Demo
You can demo the functionality by executing the module:

```
$ ./fuzzy_pint.py             
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