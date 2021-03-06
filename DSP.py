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












SI_UNITS = {'ps' : 10**(-12), 'ns' : 10**(-9), 'us' : 10**(-6), 'ms' : 10**(-3), 
             'p' : 10**(-12), 'n' : 10**(-9), 'u' : 10**(-6), 'm' : 10**(-3),
            'Hz' : 1, 'hz': 1, 's' : 1,
           'THz' : 10**12, 'GHz' : 10**9, 'MHz' : 10**6, 'kHz' : 10**3, 'khz' : 10**3 ,
             'T' : 10**12, 'G' : 10**9, 'M' : 10**6, 'k' : 10**3} 

def SItoString(inStr):
    """ 
    Convert string, with or without SI-Units, into a float data type. 
    
    Syntax: <value>[.<decimals>]<SI-Unit>
        
    Concept examples: 
    -----------------
      Ex.) inStr = str("200 kHz") -> str("200kHz") -> float(200*(10**3))
      Ex.) inStr = str("30.0 us") -> str("30.0us") -> float(30*(10**(-6)))
    
    Useage example:
    ---------------
      >> tmp = str("30.0 us")
      >> dsp.SI_string_to_float(tmp, debug = True)
            
    Return: 
    -------
      ret : Float variable representing input-string.    

    """
    func = "SItoString"

    result = None

    p = re.compile(r'([\d\.]+)([a-zA-Z]+)')
    letters = p.search(inStr)

    if letters:
        try:
           value = float(letters.group(1))           
           scale = float(SI_UNITS[letters.group(2)]) 
           result = value * scale
        except:
           raise RuntimeError("(%s): Input string is not compatiable"%(func))
    else:
        try: 
            result = float(inStr)  
        except: 
            raise RuntimeError("(%s): Input string is not compatiable"%(func))
         
    return result



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
    
    
def resolve_freq_and_period(f,p):
    """ 
    Resolve the period and frequency, and return the repective values. 
    
    If both value are given, it checks to ensure they are the inverses of each 
    other. Otherwise, the frequency and period are provided
    
    Parameters: 
    -----------
      x1 : Freq or period
      x2 : Period or frequency 
    Returns: 
        freq : 
    """
    if (f is not None) and (p is not None): 
        per1 = p
        per2 = float(1.0/f)
        if per1 != per2: 
            raise RuntimeError("Period and frequecny values do not match")
    elif f is None: 
        f = float(1.0)/float(p)
    else: 
        p= float(1.0)/float(f)
    return f,p



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


#TODO: How to embed latex into python source code. 
def decay(a, b=1, start=0, stop=1, steps=1000, debug = False):
    """ 
    This function returns a numpy.ndarray representing an 'exponential decay' function. This function is of the form. 

     x(t) = \beta\cdot e^{-\alpha\cdot t}


    """
    func = "decay"
    ts = np.linspace(0,1,1000)
    x = b * np.exp(a*(-ts))

    return x 


class signal(object):
    
    
    def __init__(self, **kwargs):
        """ 
        Signal constructor: 
        """  
        self.debug = False 
        self.A     = 1.0   
        self.DC    = 0.0  
        self.Fs    = None 
        self.Ts    = None 
        self.Fo    = None 
        self.To    = None 
        self.N     = None 
        self.M     = None 
        self.Ns    = None 
        self.nTs   = None 
        self.Phase = 0.0  

        self.Noise        = None  # Note: Noise class object. To added to 'self.TimeSignal'. 
        self.TimeSignal   = None  # Note: Time domain representation of signal.
        self.FreqSignal   = None  # Note: Frequency domain representation of signal.
        self.qFT          = False # Note: Query-Fourier transform. Set to true once the DFT of FFT of the signal was taken.
       
        self.focusDomain = "time"     # TODO: Allow users to place focus variable on onthe particular object to easily control plots, len, etc.? 
        self.__setFocusDomain = False # TODO: This may not be needed
        self.__class__.name = "DSP.signal"
        
        self.init(**kwargs)
        self.sanity_checks()
        
        if self.debug: self.debug_print()
            

        return 
    
 

    def cycle_based(self):
        """ 
        Resolve setting for signal based on cycle calculation.
        """
        if not self.Fo and not self.To: 
            raise RuntimeError("Must provide fundamental period or frequency")
            
            
        # If ther only provide the number of cycles
        if self.M and not self.N and not self.Fs: 
            self.N = 2048
            
            

        if self.M and self.N: 
            self.Fs = ( self.N / self.M) * self.Fo
        elif self.M and self.Fs: 
            self.N = ( self.Fs / self.Fo ) * self.M
        else:
            raise RuntimeError("Must at least provide  either number of samples" \
                               "or sampling frequency.")
        return self.N, self.Fs
            
     
        
    def sanity_checks(self): 
        """ 
        Check all the setting of the signal.
        
        Logic of checks: 
        ----------------
          - Fundmental period or frequency was provided. 
          - If M, the number of cycles, was provided, re-calculation of N and Fs. 
          
          
          Exiting checks and sets: 
          - Check that the sampling frequency and period are set.  
          - Check the N, the number of samples, are set.
          - Set nTs: the time-index array.
          
        
        """
 
        # - Fundmental period or frequency was provided. 
        if not self.Fo and not self.To: 
            raise RuntimeError("Must provide fundamental period or frequency")
        else: 
            self.Fo, self.To = resolve_freq_and_period(f=self.Fo,p=self.To)

        # - If M, the number of cycles, was provided, re-calculation of N and Fs. 
        if self.M: 
            self.N,self.Fs = self.cycle_based()
        
        # - Check that the sampling frequency and period are set. 
        if not self.Fs and not self.Ts: 
            raise ValueError("No values for the sampling frequency or period.")
        else: 
            self.Fs, self.Ts = resolve_freq_and_period(f=self.Fs,p=self.Ts)
            
        # - Check the N, the number of samples, are set.
        if self.N is None: 
            raise ValueError("Must provide the number of samples 'n=<int>' to create signal.")
        else: 
            self.Ns = np.arange(self.N)
        
        # - Set nTs: the time-index array.
        self.nTs = np.linspace(start=0, stop=(float(1)/self.Fs)*self.N, num=self.N)
        
        return 
        
        

     
    def init(self, **kwargs):
        """ 
        Initializes the signal settings based on keyword arguements provided to signal constructor.
        
        The sole job of this function is set the values. It will be job of another function 
        to ensrue that things are 'sane'. 

        Parameters: 
        -----------
        A : float, default: 1.0
            Amplitude of the signal

        DC : float, default: 0.0
            DC-level (offset) of the signal.

        Phase : float, default: 0.0
            Phase-shift of signal (radians).

        To : float 
            Period of signal. (This should be the inverse of 'fo')

        Fo : float 
            Fundamental cyclic frequency of signal (inverse of 'per'). 

        Fs : float
            Sampling frequency. 
            
        Ts : float
            Sampling period.             

        N : int
            Number of samples. 
            
        M : int
            Number of samples.             

        noise : noise  
            Noise object to be linear combined (added) to signal. 
        """
        for kw in kwargs:
            if kw == "A":
                self.A = float(kwargs[kw]); continue
            if kw == "DC":
                self.DC = float(kwargs[kw]); continue  
            if kw == "N":
                self.N   = int(kwargs[kw]); continue
            if kw == "M":
                self.M   = int(kwargs[kw]); continue
            if kw == "To":
                self.To  = float(kwargs[kw]); continue 
            if kw == "Fo":
                try:
                    self.Fo = float(kwargs[kw]); continue  
                except:
                    self.Fo = SItoString(kwargs[kw]); continue 
            if kw == "Fs":
                self.Fs = float(kwargs[kw]); continue 
            if kw == "Fs":
                self.Fs = float(kwargs[kw]); continue 
            if kw == "Phase":
                self.PHASE = float(kwargs[kw]); continue 
            if kw == "Noise":
                self.noise = kwargs[kw]; continue 
            if kw == "debug":
                self.debug = True;continue
        return 
                
    def debug_print(self):
        print("%s: id = %s"%(self.__class__.name, str(id(self))))
        print(" - A.......: %s"%(str(self.A)))
        print(" - DC......: %s"%(str(self.DC)))
        print(" - Phase...: %s"%(str(self.Phase)))
        print(" - N.......: %s"%(str(self.N)))
        print(" - Fo......: %s"%(str(self.Fo)))
        print(" - To......: %s"%(str(self.To)))
        print(" - Fs......: %s"%(str(self.Fs)))
        print(" - Ts......: %s"%(str(self.Ts)))
        print("")
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
        
        self.TimeSignal = ((self.A)*np.sin((self.Fo*2*np.pi)*self.nTs + self.Phase) + self.DC)   
        
        if self.Noise is not None:
            self.TimeSignal = self.Noise._noise + self.TimeSignal
            
        self.freqRes = float(self.Fs)/float(self.N)
        #self.__class__.__name__ = "Sine"
        self.setName("DSP.sine")
        
class cos(signal):
    def __init__(self, **kwargs):
        super(cos, self).__init__(**kwargs)
        
        self.TimeSignal = ((self.A)*np.cos((self.Fo*2*np.pi)*self.nTs + self.Phase) + self.DC)   
        
        if self.Noise is not None:
            self.TimeSignal = self.Noise._noise + self.TimeSignal

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
    to = 1.0/fo 
    fs = 25.89 * fo
    n = 256
    _noise = Noise(form = "awg", mean = 0, std = .5 , size = n)

    x  = sin(A=a,Dc=dc,Fo=fo,To=to,Fs=fs,N=n,phase=phase,debug=True)
    x  = sin(A=a,Dc=dc,Fo=fo,To=to,Fs=fs,N=n,phase=phase,Noise = _noise,debug=True)
    
    """
    print("Signal type = %s"%(type(x)))
    print("Signal name = %s"%(x.getName()))
    #x.tstem(index="samples", label="mlabel")
    #x.tplot()
    #subplot([x,xn], dim=(2,1), debug=True)

    # Decay function:
    x = decay(a=9.8,b=1.02)
    plt.plot(x)
    
    plt.grid()
    
    showFigures() 
    """

    
      
