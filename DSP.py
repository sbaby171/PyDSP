#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import numpy as np
import matplotlib.pyplot as plt


# TODOS:
# ======
# 
# Signal related: 
# =============
# (s001): dirac function
# (s002): unit step function 
# (s003): rect signal
# (s004): Distinction between 'name' and 'type' of a signal. 
#         We may want to determine what this distinction is between 
#         ourselves and ultimately create the self.Type field and methods.
# (s005): Should signal base classes have a fundamental-frequency of period? 
# 
# 
# Plotting Related: 
# =================
# Note to self: This should be kept to a very minimum. MatplotLib is too flexible (complicated and complex) 
#               to properly map all functionality. However, simple plotting functions should be consdiered. 
# 
# (p001): signal.tplot()
#         signal.fplot() (dft or fft must first be taken).
#         signal.tstem()
#         signal.fstem() 


__author__ = "Max Sbabo, GIT: sbaby171"
__version__ = "0.1"
    
class signal(object):
    
    
    def __init__(self, **kwargs):
        """ 
        Signal Constructor: 
   
        All attributes of the base class "signal" must be declared here. Child-classes are allowed to create new attributes 
        but not other functions held within this base class 'signal' is allowed to create new attributes. 

        """  
        self.A     = 1.0  # Note: Amplitude of signal. 
        self.Dc    = 0.0  # Note: DC offset of signal.
        self.Fs    = None # Note: The sampling frequency implies that we are only dealing with sampled signals. 
        self.Ts    = None # Note: Sampling period
        self.Fo    = None # Note: Fundamental frequency of signal. (TODO: signals typically have multple signals, so this the best to hold such info?)
        self.Per   = None # Note: Period of siganl (TODO: See note above.)
        self.N     = None # Note: Number of samples
        self.Ns    = None # Note: Sampling indices
        self.nTs   = None # Note: Ts*[0,1,2,3,..., N-1]
        self.Phase = 0.0  # Note: Phase of signal 

        self.NoiseSignal  = None # Note: Noise class object. To added to 'self.TimeSignal'. 
        self.TimeSignal   = None # Note: Time domain representation of signal.
        self.FreqSignal   = None # Note: Frequency domain representation of signal.

        self.__class__.name = "signal"
        

        # Initialize signal with all provided information
        self.init(**kwargs)

        # Sanity-Check: 
        # =============
        # Ensure no discrepancies in the signal settings. 
        #  

        # Check that users have provided a sampling frequency
        if self.Fs is None: 
            raise ValueError("Must provide sampling-frequency 'fs=<float>' to create signal.")

        # Check that user provided either a period or a fundamental frequency of there signal.
        # TODO: This is still debatable if freqiuency and/or period should be part of the base class 
        # ----- I think the answer should be yes and the answer may be in the fourier transform.
        if ( (self.Per is None) and (self.Fo is None) ): 
            raise ValueError("Must provide either frequency 'f=<float>' or the period 'p=<float>' to the create signal.")
        else: 
            self.__resolvePerAndFreq()

        if self.N is None: 
            raise ValueError("Must provide the number of samples 'n=<int>' to create signal.")
        
        # Set time-index
        self.nTs = np.linspace(start=0, stop=(float(1)/self.Fs)*self.N, num=self.N)
     
        
        
    def init(self, **kwargs):
        """ 
        Initializes the signal settings based on keyword arguements provided to signal constructor.

        Parameters: 
        -----------
        a : float, default: 1.0
            Amplitude of the signal

        dc : float, default: 0.0
            DC-level (offset) of the signal.

        phase : float, default: 0.0
            Phase-shift of signal (radians).

        per : float 
            Period of signal. (This should be the inverse of 'fo')

        fo : float 
            Fundamental cyclic frequency of signal (inverse of 'per'). 

        fs : float
            Sampling frequency. 

        n,N : int
            Number of samples. 

        noise : noise  
            Noise object to be linear combined (added) to signal. 
        """
        func = "signal.init"
        if "debug" in kwargs: 
            debug = kwargs["debug"]
        else: 
            debug = False 
        for kw in kwargs:
            if kw == "a":
                if (debug): print("DEBUG: (%s): Setting amplitude of signal to %s"%(func, str(kwargs[kw])))
                self.A = float(kwargs[kw]) # TODO: Special care to type errors from user? 
                continue
            if kw == "dc":
                if (debug): print("DEBUG: (%s): Setting dc-offset of signal to %s"%(func, str(kwargs[kw])))
                self.Dc = float(kwargs[kw]) # TODO: Special care to type errors from user? 
                continue  
            if kw == "n" or kw == "N":
                if (debug): print("DEBUG: (%s): Setting samples of signal to %s"%(func, str(kwargs[kw])))
                self.N   = int(kwargs[kw]) # TODO: Special care to type errors from user? 
                self.Ns  = np.arange(self.N)
                continue
            if kw == "per":
                if (debug): print("DEBUG: (%s): Setting period of signal to %s"%(func, str(kwargs[kw])))
                self.Per  = float(kwargs[kw]) # TODO: Special care to type errors from user? 
                # MSN: Only set the period. Dont also set the F because later we want to catch a discrepency if #s dont align
                continue 
            if kw == "fo":
                if (debug): print("DEBUG: (%s): Setting frequency of signal to %s"%(func, str(kwargs[kw])))
                self.Fo = float(kwargs[kw]) # TODO: Special care to type errors from user? 
                # MSN: Only set F. Dont also set the PER because later we want to catch a discrepency if #s dont aign
                continue   
            if kw == "fs":
                if (debug): print("DEBUG: (%s): Setting sampling-frequency of signal to %s"%(func, str(kwargs[kw])))
                self.Fs = float(kwargs[kw]) # TODO: Special care to type errors from user? 
                self.Ts = 1.0/self.Fs
                # MSN: Only set F. Dont also set the PER because later we want to catch a discrepency if #s dont aign
                continue 
            if kw == "phase":
                if (debug): print("DEBUG: (%s): Setting phase of signal to %s"%(func, str(kwargs[kw])))
                self.PHASE = float(kwargs[kw]) # TODO: Special care to type errors from user? 
                # MSN: Only set F. Dont also set the PER because later we want to catch a discrepency if #s dont aign
                continue 
            if kw == "noise":
                if (debug): print("DEBUG: (%s): Setting noise of signal to %s"%(func, str(kwargs[kw])))
                self.Noise = kwargs[kw] # MSN: This will alwasy be a noise object. Later could enfore that...
                continue 

    def __resolvePerAndFreq(self):
        func = "signal.__resolvePerAndFreq"
        if (self.Per is not None) and (self.Fo is not None): 
            per1 = self.Per
            per2 = float(1.0/self.Fo)
            if per1 != per2: 
                raise RuntimeError("ERROR: (%s): Both 'per' and 'fo' but they do not equal the inverses of each other (p=f^(-1))\n."\
                 " Period = %s\n. Fo = %s\n. Period = 1/Fo => %s ?= %s"%(func, str(self.Per), str(self.Fo), str(per1), str(per2)))
        if self.Per is None: 
            self.Per = float(1.0)/float(self.Fo)
        else: 
            self.Fo = float(1.0)/float(self.Per)
        return
  
    # TODO: There might be a confusion between the 'name' of a signal and the 'type' 
    def setName(self,string):
        self.__class__.__name__ = string
    def getName(self):
        return self.__class__.__name__
        
    
class sin(signal):
    def __init__(self, **kwargs):
        super(sin, self).__init__(**kwargs)
        
        if self.NoiseSignal is None:
            self.TimeSignal = ((self.A)*np.sin((self.Fo*2*np.pi)*self.nTs + self.Phase) + self.Dc)   
        else: 
            self.TimeSignal = self.NoiseSignal._noise + ((self.A)*np.sin((self.Fo*2*np.pi)*self.nTs + self.Phase) + self.Dc)
        
        self.freqRes = float(self.Fs)/float(self.N)
        #self.__class__.__name__ = "Sine"
        self.setName("sine")
        
class cos(signal):
    def __init__(self, **kwargs):
        super(cos, self).__init__(**kwargs)
        
        self.TimeSignal = ((self.A)*np.cos((self.Fo*2*np.pi)*self.nTs + self.Phase) + self.Dc)   
        
        if self.NoiseSignal is not None:
            self.TimeSignal = self.NoiseSignal._noise + self.TimeSignal

        self.freqRes = float(self.Fs)/float(self.N)
        #self.__class__.__name__ = "Cosine" 
        self.setName("cosine")

class noise(object):    
    def __init__(self, form, **kwargs):
        func = "noise.__init__"
        debug = False 
    
        forms = { "awg" : "Additive Gaussian White Noise"} 
    
        self.form = None
        self.mean = 0.0
        self.std  = 0.0
        self.size = 0
        self._noise = None 
    

        # MSN: Becasue 'form' is a named value without a default, python-interupter will handle error. 
        if form not in forms.keys(): 
            raise RuntimeError("Must provide 'form' of noise. Options: \n%s"%(str(forms)))
        if "debug" in kwargs: debug = kwargs["debug"]
        for kw in kwargs:    
            if kw == "mean":
                if (debug): print("DEBUG: (%s): Setting amplitude of signal to %s"%(func, str(kwargs[kw])))
                self.mean = float(kwargs[kw]) # TODO: Special care to type errors from user? 
                continue 
            if kw == "std":
                if (debug): print("DEBUG: (%s): Setting amplitude of signal to %s"%(func, str(kwargs[kw])))
                self.std = float(kwargs[kw]) # TODO: Special care to type errors from user? 
                continue            
            if kw == "size":
                if (debug): print("DEBUG: (%s): Setting amplitude of signal to %s"%(func, str(kwargs[kw])))
                self.size= int(kwargs[kw]) # TODO: Special care to type errors from user? 
                continue   

        if form == "awg": 
            self._noise = np.random.normal(self.mean, self.std, self.size) # Type = numpy.ndarray


if __name__ == "__main__":
    a=3.2
    dc=3.4
    phase=5.8
    fo = 5000
    per = 1.0/fo # Add a constant to throw error.
    fs = 12.34 * fo
    n = 1024
    _noise = noise(form = "awg", mean = 0, std = .5 , size = n)

    x = sin(a=a,dc=dc,phase=phase, fs=fs,fo=fo,per=per, n=n, noise = _noise , debug = True)
    print("Signal type = %s"%(type(x)))
    print("Signal name = %s"%(x.getName()))
    
    

    
      
