#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 14:01:31 2018

@author: max.sbabo
"""

import DSP as dsp


sine_signal = dsp.sin("a=3.0; ft=50khz; n = 2048;") 
sine_signal.plot()