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
# (p002): Related to (p001), Shoule we offer an keyword arg for the user to select the x-axis to be shown
#         as time-stamps (Ts*[0,1,2,...,N-1]) or sample indices ([0,1,2,..., N-1])
# (p003): Consider mergeing signal.__plot and signal.__stem into a single location (only do so when you move to 
#         managing Figure objects).
# (p004): ** Add docs to makeFigure, subplot, and makeGridSpec, showFigures() 
#

__author__ = "Max Sbabo, GIT: sbaby171"
__version__ = "0.1"


# Add signal.qFT to check if the fourier transform of the signal was taken.


# TODO: Look at all plt.figure() input vars + look into FIgure.supt()
# Default Figure settings. 
FIGSIZEW = 10.0 # matplotlib default = 6.4
FIGSIZEH =  8.0 # matplotlib default = 4.8
FIGSIZE  = [FIGSIZEW, FIGSIZEH]
DPI = 100       # matplotlib default = 100
FACECOLOR = 'w' # matplotlib default = 'w'
EDGECOLOR = 'w' # matplotlib default = 'w'
FIGI = 0 
def makeFigure(grid=True, t=None, figsize=None, dpi=None, facecolor=None, edgecolor=None, num=None, frameon=True, debug=False):
    func = "makeFigure" 

    global FIGI 
    FIGI += 1
    if (debug): print("DEBUG: (%s): FIGI = %d"%(func, FIGI))

    # Set default values: 
    if grid: 
        plt.rcParams['axes.grid'] = True 
    if not figsize:
        figsize = FIGSIZE
    if not dpi:
        dpi = DPI
    if not facecolor:
        facecolor = FACECOLOR
    if not edgecolor:
        edgecolor = EDGECOLOR
    # Create 'Figure' object
    if not num: 
        figure = plt.figure(num=FIGI, figsize=figsize, dpi=dpi, facecolor=facecolor, edgecolor=edgecolor, frameon=frameon)
    else: 
        figure = plt.figure(num=num, figsize=figsize, dpi=dpi, facecolor=facecolor, edgecolor=edgecolor, frameon=frameon)
    if (debug): print("DEBUG: (%s): Figure = %s"%(func, figure))

    # Add title to figure. (TODO: other args. See source for figure.suptitle())
    if t: 
        figure.suptitle(t=t)
  
    # Return 'Figure' object
    return figure

def makeGridSpec(figure, nrows=1, ncols=1, wspace=None, hspace=None, debug=False):
    func = "makeGridspec"
    GS = figure.add_gridspec(nrows=nrows, ncols=ncols, hspace=hspace, wspace=wspace)
    return GS

def hello_world():
    print("Hello world from DSP module.")




# TODO: Track the keyword arg 'show'. I want to remove it but not sure yet. So just set to 'true' for now
def subplot(signals, dim, show=True, debug=False):
    """ 
    Produce a subplot of signals using matplotlib.pyplot.stem function

    Parameters: 
    ----------
    signals : list
    	A list of signals to be plotted. 
    
    dim : list or tuple 
    	Number of rows and columns in grid. 
        Ex.) (2,3) -> 2 rows, 3 columns

    """
    func = "subplot"
    _signals = len(signals)
    
    nrows = dim[0]
    ncols = dim[1]

    # Create GridSpec: 
    hspace = .5
    wspace = None 
    figure = makeFigure() #  figure : Figure (matplotlib.figure.Figure)
    gridspec = makeGridSpec(figure, nrows=nrows, ncols=ncols, wspace=wspace, hspace=hspace)



    i = 0 
    for ir in range(nrows):
        for ic in range(ncols): 
            # TODO: Here there is potential to extract nameing out the signal objects and place them on the labels.
            ax = figure.add_subplot(gridspec[ir,ic], xlabel = "Signal:%d"%i)

            # Signal type: signal OR numpy.ndarray
            signalType = str(type(signals[i]))
            if debug: print("DEBUG: (%s): Signal-type = %s"%(func,signalType))   
            if "ndarray" in signalType:
                ax.stem(signals[i])
            else: 
                ax.stem(signals[i].nTs, signals[i].TimeSignal)
            i+=1
    if show:
        plt.show()
    
    return


def showFigures():
    plt.show(); 
    return;
    


def dSignal(a=1.0, dc=0.0, fo=5000.0, n=256, phase=0.0, per=None, fs=None, noise = False):
    if not per: 
        per = 1.0/fo # Add a constant to throw error.
    if not fs:
        fs = 25.89 * fo
    
    _noise = Noise(form = "awg", mean = 0, std = .5 , size = n)

    ret = None 

    if not noise: 
        ret  = sin(a=a,dc=dc,phase=phase, fs=fs,fo=fo,per=per, n=n, debug = True)
    else: 
        ret = sin(a=a,dc=dc,phase=phase, fs=fs,fo=fo,per=per, n=n, noise = _noise , debug = True)

    return ret 

def printArray(arr, attrs = False):
    """ 
    Print the numpy.ndarray contents. If optional keyword arguement 'attrs'
    is 'True', the the attributes of the array will be printed.
    
    Parameters:
    -----------
    arr : numpy.ndarray, 
        ndarray to be printed (if not proper type error will be thrown)
    attrs : bool, default: False
        If True, attributes of input array will be printed.   
    
    """
    if "numpy.ndarray" not in str(type(arr)): 
        raise ValueError("(%s): input %s must be of type numpy.ndarray"
                        %("printArray","arr"))
    # Print type and attributes
    if attrs: 
        print("Printing the type and attributes of input numpy.ndarray:")
        print("--------------------------------------------------------")
        print("  - type(ndarray) = %s"%(str(type(arr))))
        print("  - ndarray.ndim = %d"%(arr.ndim))
        print("  - ndarray.shape = %s"%(str(arr.shape)))
        print("  - ndarray.size = %d"%(arr.size))
        print("  - ndarray.dtype = %s"%(arr.dtype))
        print("  - ndarray.itemsize = %d"%(arr.itemsize))
        print("  - ndarray.data = %s"%(str(arr.data)))
    print("ndarray = %s"%(str(arr)))
    
    return    


class signal(object):
    
    
    def __init__(self, **kwargs):
        """ 
        Signal Constructor: 
   
        All attributes of the base class "signal" must be declared here.

        Child-classes are allowed to create new attributes.

        However, no other methods associated with this 'signal' base class is allowed to create new attributes that are not first initialized here. 

        """  
        self.debug = False 
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

        self.noise        = None  # Note: Noise class object. To added to 'self.TimeSignal'. 
        self.TimeSignal   = None  # Note: Time domain representation of signal.
        self.FreqSignal   = None  # Note: Frequency domain representation of signal.
        self.qFT          = False # Note: Query-Fourier transform. Set to true once the DFT of FFT of the signal was taken.
       


         
        self.focusDomain = "time"     # TODO: Allow users to place focus variable on onthe particular object to easily control plots, len, etc.? 
        self.__setFocusDomain = False # TODO: This may not be needed

        self.__class__.name = "DSP.signal"
        

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
                self.noise = kwargs[kw] # MSN: This will alwasy be a noise object. Later could enfore that...
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


    def setFocus(domain): 
        func = "signal.setFocus"

    
        if domain == "time": 
            self.focusDomain = "time"
        elif domain == "freq":
            self.focusDomain = "freq"
        else: 
            raise ValueError("ERROR: (%s): Arguement (%s) only takes the following options = %s"%(func,"domain",str(["time","freq"])))

        self.__setFocusDomain = True


    
    def getTime(self):
        """ 
        Return time domain signal (numpy.ndarray type)
        """
        return self.TimeSignal 
    def getFreq(self): 
        """ 
        Return frequency domain signal (numpy.ndarray type)
        """
        return self.FreqSignal
    def getNoise(self):
        """ 
        Return the DSP.Noise object 
        NOTE: for numpy.ndarray signal call 'getNoise()' on the returned Noise object.
        """
        return self.noise

    # Overloaded operators:
    # ====================

    def __len__(self, domain = "time"): 
        func = "len"
        ret = None

        if domain == "time": 
            ret = len(self.TimeSignal)
        elif domain == "freq":
            ret = len(self.FreqSignal)
        else: 
            raise ValueError("ERROR: (%s): Arguement (%s) only takes the following options = %s"%(func,"domain",str(["time","freq"])))

        return ret

    # TODO: It doesnt really make sense to have an input arguement for 'domain' when the funciton is an operator [],
    # ----- example, the following will error
    def __getitem__(self, index, domain = "time"):
        func = "signal.__getitem__"
        ret = None 

        if domain == "time": 
            ret = self.TimeSignal[index]
        elif domain == "freq":
            ret = self.FreqSignal[index]
        else: 
            raise ValueError("ERROR: (%s): Arguement (%s) only takes the following options = %s"%(func,"domain",str(["time","freq"])))

        return ret


  
    # Plotting functions: 
    # ===================


    # TODO: __plot and __stem need to come from the same centeral function. If they continue to be separate functions, maintenance will
    #       be tidious, inefficient, and ultimately it is unncessary. 

    def __Plot(self, Type, index = "time", domain="time", title="", **kwargs):
        """ 
        Base plotting function for signals wrapping matplotlib.pyplot.plot and .stem. 

        Paramters: 
        ----------
        index : str, optional, default: "time"
            X-axis markers. 
            Options: 
                - "time" : Time-stamp indices x,[n], where n = Ts*[0,1,2,3,...,N-1]
                - "samples" : Samples indices x[n], where n = [0,1,2,3,...N-1]
                TODO: Need to handle index options for the frequency domain ()

        domaim : str, optional, default: "time"
            Domain for signal to be plotted in. 
            Options: 
                - "time": Time domain representation.
                - "freq": Frequency domain representation.

        **kwargs : matplotlib.pyplot.plot keyword arguments, optional
            See URL: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot
            NOTE: matplotlib.pyplot functions 'stem' and 'plot' contains different **kwargs
           
         **kwargs : matplotlib.pyplot.stem keyword arguments, optional
            See URL: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.stem.html#matplotlib.pyplot.stem    
            NOTE: matplotlib.pyplot functions 'stem' and 'plot' contains different **kwargs

        """
        func = "signal.__plot"

        # for kw in kwargs: 
        # other checks 

        plt.figure()
        plt.grid(True)

        # Check domain
        if (domain == "time"):  
            # Check index: 
            if (index == "time"): 
                # Check Type: 
                if (Type == "plot"):
                    # Plot signal
                    plt.plot(self.nTs, self.TimeSignal, **kwargs)
                else: 
                    plt.stem(self.nTs, self.TimeSignal, **kwargs)
            else: 
                # Check Type: 
                if (Type == "plot"):
                    # Plot signal
                    plt.plot(self.Ns, self.TimeSignal, **kwargs)
                else: 
                    plt.stem(self.Ns, self.TimeSignal, **kwargs)
            
        # Check domain:
        elif (domain == "freq"): 
            if not self.qFT: 
                raise RuntimeError("ERROR: (%s): The Fourier transform of the signal must be taken becomce plotting the frequency domain representation."%(func))
            # Check index:
            if (index == "freq"):  # self.nFs = freRes * [0,1,2,3, ... , N/2-1]
                print("TODO: (%s):"%(func)) #plt.plot(self.freqRes*self.Ns[0:len(self.Ns)], self.FreqSignal, **kwargs)
            else: # self.Ns -> [0,1,2,...N/2-1]
                print("TODO: (%s)"%(func))

        else: 
            raise ValueError("ERROR: (%s): Arg(%s) only has the following options: %s"%(func,"index",str(["time","samples"])))
 

        if title:
            plt.title(title) 
 
        plt.show()

        return;
       



    
   
    def tstem(self, index = "time", title="", **kwargs):
        #self.__stem(index=index, domain="time", title=title, **kwargs)
        self.__Plot(Type="stem", index=index, domain="time", title=title, **kwargs)

    def tplot(self, index = "time", title="", **kwargs):
        #self.__plot(index=index, domain="time", title = title, **kwargs)
        self.__Plot(Type="plot", index=index, domain="time", title=title, **kwargs)


    # TODO: There might be a confusion between the 'name' of a signal and the 'type' 
    def setName(self,string):
        self.__class__.__name__ = string
    def getName(self):
        return self.__class__.__name__
        
    
class sin(signal):
    def __init__(self, **kwargs):
        super(sin, self).__init__(**kwargs)
        
        if self.noise is None:
            self.TimeSignal = ((self.A)*np.sin((self.Fo*2*np.pi)*self.nTs + self.Phase) + self.Dc)   
        else: 
            self.TimeSignal = self.noise._noise + ((self.A)*np.sin((self.Fo*2*np.pi)*self.nTs + self.Phase) + self.Dc)
        
        self.freqRes = float(self.Fs)/float(self.N)
        #self.__class__.__name__ = "Sine"
        self.setName("DSP.sine")
        
class cos(signal):
    def __init__(self, **kwargs):
        super(cos, self).__init__(**kwargs)
        
        self.TimeSignal = ((self.A)*np.cos((self.Fo*2*np.pi)*self.nTs + self.Phase) + self.Dc)   
        
        if self.noise is not None:
            self.TimeSignal = self.noise._noise + self.TimeSignal

        self.freqRes = float(self.Fs)/float(self.N)
        #self.__class__.__name__ = "Cosine" 
        self.setName("DSP.cosine")

class Noise(object):    
    def __init__(self, form, **kwargs):
        func = "Noise.__init__"
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
    def getNoise(self):
        """ 
        Return the noise signal. (numpy.ndarrary type) 
        """
        return self._noise

if __name__ == "__main__":
    a=3.2
    dc=0.45
    phase=5.8
    fo = 5000
    per = 1.0/fo # Add a constant to throw error.
    fs = 25.89 * fo
    n = 256
    _noise = Noise(form = "awg", mean = 0, std = .5 , size = n)

    x  = sin(a=a,dc=dc,phase=phase, fs=fs,fo=fo,per=per, n=n, debug = True)
    xn = sin(a=a,dc=dc,phase=phase, fs=fs,fo=fo,per=per, n=n, noise = _noise , debug = True)
    print("Signal type = %s"%(type(x)))
    print("Signal name = %s"%(x.getName()))
    x.tstem(index="samples", label="mlabel")
    #x.tplot()
    subplot([x,xn], dim=(2,1), debug=True)
    
    showFigures() 

    
      
