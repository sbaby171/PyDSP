#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import numpy as np
import matplotlib # Explicity to remove dep for tkinter
matplotlib.use("agg") # Use a different backend from tkinter
import matplotlib.pyplot as plt



__version__ = "001.o" # If t or c, then is temp or checkout. (same meanings)



SI_UNITS = {'ps' : 10**(-12), 'ns' : 10**(-9), 'us' : 10**(-6), 'ms' : 10**(-3), 
             'p' : 10**(-12), 'n' : 10**(-9), 'u' : 10**(-6), 'm' : 10**(-3),
            'Hz' : 1, 'hz': 1, 's' : 1,
           'THz' : 10**12, 'GHz' : 10**9, 'MHz' : 10**6, 'kHz' : 10**3, 'khz' : 10**3 ,
             'T' : 10**12, 'G' : 10**9, 'M' : 10**6, 'k' : 10**3} 

def SI_string_to_float(inStr, debug = False):
    """ Convert string, with or without SI-Units, into a float data type. 
    
        Syntax: <value>[.<decimals>]<SI-Unit>
        
        NOTE: All spaces will be removed from string prior to float conversion. 
        NOTE: Set 'debug' to 'True' to recieve console debug-print commands.
        
        - Ex.) inStr = str("200 kHz") -> str("200kHz") -> float(200*(10**3))
        - Ex.) inStr = str("30.0 us") -> str("30.0us") -> float(30*(10**(-6)))
    
        - Usage: 
            tmp = str("30.0 us")
            dsp.SI_string_to_float(tmp, debug = True)
            
        Return: float-type    

    """
    func_name = "SI_string_to_float"
    
    # Debug print incoming string. 
    if debug: print("DEBUG: (Func = %s): Input-str: %s" %( func_name, inStr ))
    
    #Remove all spaces from incoming string. 
    inStr  = inStr.replace(" ", ""); 
    if debug: print("DEBUG: (Func = %s): Removed spaces: %s" %( func_name, inStr ))
    
    # Allocate return value, and search in
    result = None
    letters = re.search( r'([\d\.]+)([a-z A-Z]+)', inStr)
    
    # Query if match was found. If not, print warning then try to directly convert incoming string.
    if letters:
        try:
           value = float(letters.group(1))
           scale = float(SI_UNITS[letters.group(2)])
           result = value * scale
           if debug: print("DEBUG: (Func = %s): Value: %f, scale: %f, result: %f"%(func_name, value,scale,result))
        except:
           print("ERROR: (Func = %s): Couldn't extract value and SI-Unit."%func_name)
           print("       Possible issue with seaching 'SI_UNITS for (%s)"% scale)
    else:
        print("WARNING: (Function = %s) Couldn't extract value and SI-Unit. Will attempt direct float conversion... "%func_name)
        #print("         Used the following regex: '([\d\.]+)([a-z A-Z]+)'")
        result = float(inStr) # TODO : Insert try catch 
         
    return result



    
class signal(object):
    
    
    # To be used when timing interval or sampling frequency is not determenined. 
    default_samples_per_cycle = int(16)
    
    def __init__(self, settings):
        
        debug = False
        func_name = "signal.__init__"
        
        # ------------------------------------------------------------------- #
        """ Objective: Intialize/Set all fundamental properties of signal """
        # ------------------------------------------------------------------- #
        self.A     = 1.0
        self.DC    = 0.0
        self.PER   = None
        self.FT    = None 
        self.PHASE = 0.0
        self.N     = int(16)
        self.FS    = None
        self.M     = 1
        self.nTs     = None
        self._signal = None
        
        
        

        #self.default_samples_per_cycle = 16
        
        # Parse the 'settings' input to set all the fields
        self.__signal_settings_handler__(settings, debug) 
        

        if debug: 
            print("self.A     (type)  = " + str( type(self.A) )  )
            print("           (value) = " + str( self.A ) )
            print("self.DC    (type)  = " + str( type(self.DC) ) )
            print("           (value) = " + str( self.DC ) )
            print("self.PER   (type)  = " + str( type(self.PER) ) )
            print("           (value) = " + str( self.PER ) )
            print("self.FT    (type)  = " + str( type(self.FT) ) )
            print("           (value) = " + str( self.FT ) )
            print("self.PHASE (type)  = " + str( type(self.PHASE) ) )
            print("           (value) = " + str( self.PHASE ) )
            print("self.N     (type)  = " + str(  type(self.N) ) )
            print("           (value) = " + str( self.N ) )
            print("self.FS    (type)  = " + str( type(self.FS) ) ) 
            print("           (value) = " + str( self.FS ) )

    # end of __init__ 
    
    
    def Print(self):
        """ Print content of signal object. This is merely a wrapper of pythons
        '__dict__' function which prints the namepsace as a dictionary object. 
        """
        print(self.__dict__)
        
        
    # *********************************************************************** #   
    """ Objective: Allocate process functions for each 'Fundament Property' of 
                   the signal  
    
        This section is partitioned into three sections:
          1. The defintions for a particular processing function. 
          2. The "__process_field_opts__" dictionary. Key is the string option 
             and the pair is the respective processing function call. 
          3. The funciton '__signal_settings_handler__' to parse the signal
                 'settings' and invoke proper processing functions.
              
    """    
    # *********************************************************************** #
    def __process_amplitude__(self, string, debug = False ):
        func_name = "__process_amplitude__"
        if debug: print(" -- DEBUG (%s) string: %s" %( func_name, string ))
        self.A = float(string)
        return
        
    def __process_sampling_freq__(self, string, debug = False ):
        func_name = "__process__sampling_freq__"
        if debug: print(" -- DEBUG (%s) string: %s" %( func_name, string ))
        self.FS = SI_string_to_float(string, debug)
        if debug: print(" -- DEBUG (%s) value: %s" %( func_name, self.FS ))
      
    def __process_signal_freq__(self, string, debug = False ):
        func_name = "__process__signal_freq__"
        if debug: print(" -- DEBUG (%s) string: %s" %( func_name, string ))
        self.FT = SI_string_to_float(string, debug)    
        
    def __process_signal_period__(self, string, debug = False ):
        func_name = "__process__signal_period__"
        if debug: print(" -- DEBUG (%s) string: %s" %( func_name, string ))
        self.PER = SI_string_to_float(string, debug)         

    def __process_samples__(self, string, debug = False ):
        func_name = "__process__samples__"
        if debug: print(" -- DEBUG (%s) string: %s" %( func_name, string ))
        self.N = int(string)
        
    def __process_phase__(self, string, debug = False ):
        func_name = "__process__phase__"
        if debug: print(" -- DEBUG (%s) string: %s" %( func_name, string ))   
    
    # Key = allowable string option, Pair = The repsective processing function. 
    __process_field_opts__ = { 'a' : __process_amplitude__ ,
                               'A' : __process_amplitude__ ,
                               'fs': __process_sampling_freq__,
                               'n' : __process_samples__,
                               'ft': __process_signal_freq__,
                               'per': __process_signal_period__,
                               "phase" : __process_phase__, }


    def __signal_settings_handler__(self, settings, debug):
        """ Parse incoming settings for signal-fields initialization 
           
            Algorithm: 
                1. Split incoming 'settings' string at delimiter: ";"
                2. Foreach item in settings
                   - Remove all whitespaces
                   - Split at field identifier delimiter
                   - If field-identifier is in '__process_field_opts__' then 
                     invoke respective function. 
                     
            Return: void (however, fields of the signal object will be set)
         
        """
        # Establish debug parameters...
        func_name = "__signal_settings_handler__";
        
        # Set up configurable parameters
        settings_delimiter = ";"
        fields_delimiter   = "="
        
        
        if debug: print(" -- DEBUG (%s) Incoming 'setting' string: %s" %( func_name, settings ) )
        
        # Split line at delimiters
        line_split = settings.split(settings_delimiter)
        
        for item in line_split:
            # Remove all spaces
            item  = item.replace(" ", ""); 
            if debug: print(" -- DEBUG (%s) Item: %s" %( func_name, item ) )
            
            # Split the field identifier and its value. 
            field_identifier = item.split(fields_delimiter) 
            if ( debug and len(field_identifier) is not 1 ): print(" -- DEBUG (%s) Field: %s, Value: %s" %( func_name, field_identifier[0], field_identifier[1] ) )
            
            """ Objective: Call processing function. 
               
                  - Check if the field is supported.
                  - If so, call the respective process function. 
            """
            if field_identifier[0] in self.__process_field_opts__:
                self.__process_field_opts__[field_identifier[0]](self, field_identifier[1], debug)
                
        # TODO: All fields should be checked here....
                
        # ERROR If FT (tramission frequency) and FS (sampling frequency) are not provided.
        if self.FT is None:
            sys.exit("ERROR: The transmission frequncy (ft) was not defined. Please added necessary information to 'settings' for signal construction...")


        # if FS not provided, base the interval on FT and cycles
        if self.FS is None: 
            print("WARNING: No sampling frequency provided. \n         Will provide default values for plotting...")
            if self.N is not (signal.default_samples_per_cycle * self.M):
                print("WARNING: Changing number of samples from %d to %d" %(self.N, (signal.default_samples_per_cycle * self.M)))
                self.N = (signal.default_samples_per_cycle * self.M)
            self.nTs    = np.linspace(start = 0, stop =  self.M * (1/self.FT), num = self.N )
            self.FS = self.nTs[1] - self.nTs[0]
            print("WARNING: Setting sampling frequency to: %f" %self.FS)
            self._signal = self.nTs
        else: 
            self.nTs    =  np.linspace(0, (float(1)/self.FS)*self.N, self.N) 
            self._signal =  self.nTs
                
                
    def plot (self):
        """ Plotting method of signal """
        
        plt.stem(self.nTs, self._signal)              


class sin(signal):
    def __init__(self, settings): 
        super(sin, self).__init__(settings)
        #self.sig =(self.ac)*np.sin((self.ft*2*np.pi)*self.nTs + self.phase) + self.dc
        
        self._signal =(self.A)*np.sin((self.FT*2*np.pi)*self.nTs + self.PHASE) + self.DC
        #if NOISE is not None:
            #self.sig = self.sig + NOISE.noise # If they arer different lengths..ERROR? 
            
        self.freqRes = float(self.FS)/float(self.N)
        
        
        
        
        
""" 
Revision Control (manual notes):
    
    001.o: July 4th 2018: 
        - Basic framework for dsp module. The main objective for inital version 
          is to be able to and plot sine signal from a list of input settings. 
          
        Module pieces: 
        --------------
        
        - Data type or structures: 
            1. 
        
        -  Functions: 
            1. SI_string_to_float
            
        - Classes: 
            
            1. Signal (parent):
                
              Data type or structures:
                  1.__process_field_opts__ (dictionary)
                  2. default_samples_per_cycle (int)
                  
                  condensed = [__process_field_opts__,default_samples_per_cycle]
                  
              Fields: 
                  1. A (float)
                  2. DC (float)
                  3. PER (float)
                  4. FT (float)
                  5. PHASE (float)
                  6. N (int)
                  7. FS (float)
                  8. M (int)
                  9. nTs (float-array)
                  10. _signal (float-array)
                  
                  condensed = [A,DC,PER,FT,PHASE,N,FS,M,nTs,_signal]
             
              Methods: 
                  1. __init__
                  2. Print
                  3.__process_amplitude__
                  4.__process_sampling_freq__
                  5.__process_signal_freq__
                  6.__process_signal_period__
                  7.__process_samples__
                  8.__process_phase__
                  9.__signal_settings_handler__
                  10.plot
                  
                  condensed = [ __init__,Print,__process_amplitude__,__process_sampling_freq__,__process_signal_freq__,__process_signal_period__,__process_samples__,__process_phase__,__signal_settings_handler__,plot]
                  
            2. Sin (child of 'signal')
            
              Data type or structures:
                   1. freqRes (float)
                   
                   condensed = [freqRes]
                   
               Fields: 
                   1.
                   
               Functions: 
                   1. 
                  
    
    Next Steps: 
        - Add cosine singnals 
        - Allow stem or line plots
            
    End of 001.o Revision Notes. 
                   


"""        
