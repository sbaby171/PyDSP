#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import DSP as dsp

from pydsp import PyDSP

x = PyDSP.SI_string_to_float("10")

print(x)

#x = dsp.sin("a=3.0; ft=50khz; n = 2048;") 
#x.plot()

