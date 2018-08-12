#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import numpy as np
import matplotlib.pyplot as plt



__version__ = "004.c" # If t or c, then is temp or checkout. (same meanings)


""" Major Concepts to be addressed:
    
    1. Discussion on handling error outs. 
    2. Relation between Plotter and Signal.
    3. Handling 'settings'...
    4. Wokring with FFT
    5. Working with modulation/demodulation schemes
    
    TODO: I need to consult with grant and chris about how simulation is done for amplitude modulation
    
    My thought is that everyone in the space usually has some home brewed methods and scripts for 
    developing thier simulation. My goal is to create a standard paskage that can be used. 
    

"""



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
    
    #p = re.compile(r'((?P<value>)[\d\.]+)((?P<SIUnit>)[a-zA-Z]+)')
    p = re.compile(r'([\d\.]+)([a-zA-Z]+)')
    letters = p.search(inStr)
    
    # Query if match was found. If not, print warning then try to directly convert incoming string.
    if debug: print("DEBUG: (Func = %s): Search Success?: %s" %( func_name,  str(letters) ) )
    if letters:
        try:
           value = float(letters.group(1))           # letters.group("value")
           scale = float(SI_UNITS[letters.group(2)]) # letters.group("SIUnit")
           # Error should occur if: result = float * None
           result = value * scale
           if debug: print("DEBUG: (Func = %s): Value: %f, scale: %f, result: %f"%(func_name, value,scale,result))
        except:
           print("ERROR: (Func = %s): Couldn't extract value and SI-Unit."%func_name)
           print("       Possible issue with seaching 'SI_UNITS for (%s)"% letters.group(2))
    else:
        print("WARNING: (Function = %s) Couldn't extract value and SI-Unit. Will attempt direct float conversion... "%func_name)
        #print("         Used the following regex: '([\d\.]+)([a-z A-Z]+)'")
        result = float(inStr) # TODO : Insert try catch 
         
    return result



    
class signal(object):
    
    
    # To be used when timing interval or sampling frequency is not determenined. 
    default_samples_per_cycle = int(16)
    
    def __init__(self, settings, debug = False):
        
        func_name = "signal.__init__"

        # Objective: Intialize/Set all fundamental properties of signal 
        self.A     = 1.0
        self.DC    = 0.0
        self.PER   = None
        self.FT    = None 
        self.PHASE = 0.0
        self.N     = int(16)
        self.FS    = None
        self.M     = 1
        self.nTs     = None
        self.Ns      = None 
        self._signal = None
        
        # amplitude modulation feilds
        self.AM = None
        self.FC = None
        self.AC = None
        self.FM = None
        self.modulation_signal = False 
        
        self.freqRes = None 
        
        # Parse the 'settings' input to set all the fields
        self.__signal_settings_handler__(settings, debug) 
        
 
        # Create singleton plotter object: They should all refer to the same plotter...
        #self.plotter = _plotter_()

        if debug: 
            print("DEBUG: (Func = %s): self.A      (type)  = %s" %(func_name, str( type(self.A) )  ) )
            print("DEBUG: (Func = %s):             (value) = %s" %(func_name, str( self.A ) ) )
            print("DEBUG: (Func = %s): self.DC     (type)  = %s" %(func_name, str( type(self.DC) ) ) )
            print("DEBUG: (Func = %s):             (value) = %s" %(func_name, str( self.DC ) ) )
            print("DEBUG: (Func = %s): self.PER    (type)  = %s" %(func_name, str( type(self.PER) ) ) )
            print("DEBUG: (Func = %s):             (value) = %s" %(func_name, str( self.PER ) ) )
            print("DEBUG: (Func = %s): self.FT     (type)  = %s" %(func_name, str( type(self.FT) ) ) )
            print("DEBUG: (Func = %s):             (value) = %s" %(func_name, str( self.FT ) ) )
            print("DEBUG: (Func = %s): self.PHASE  (type)  = %s" %(func_name, str( type(self.PHASE) ) ) )
            print("DEBUG: (Func = %s):             (value) = %s" %(func_name, str( self.PHASE ) ) )
            print("DEBUG: (Func = %s): self.N      (type)  = %s" %(func_name, str(  type(self.N) ) ) )
            print("DEBUG: (Func = %s):             (value) = %s" %(func_name, str( self.N ) ) )
            print("DEBUG: (Func = %s): self.FS     (type)  = %s" %(func_name, str( type(self.FS) ) ) )
            print("DEBUG: (Func = %s):             (value) = %s" %(func_name, str( self.FS ) ) )
            print("DEBUG: (Func = %s): self.nTs    (type)  = %s" %(func_name, str( type(self.nTs) ) ) )
            print("DEBUG: (Func = %s):             (size)  = %s" %(func_name, str( len(self.nTs) ) ) )
            print("DEBUG: (Func = %s):             (first) = %s" %(func_name, str( self.nTs[0]) ) ) 
            print("DEBUG: (Func = %s):             (last)  = %s" %(func_name, str( self.nTs[-1]) ) ) 
            
            print("DEBUG: (Func = %s): self.modulation_signal      (type)  = %s" %(func_name, str( type(self.modulation_signal) )  ) )
            print("DEBUG: (Func = %s):              (value) = %s" %(func_name, str( self.modulation_signal ) ) )           
            print("DEBUG: (Func = %s): self.AC      (type)  = %s" %(func_name, str( type(self.AC) )  ) )
            print("DEBUG: (Func = %s):              (value) = %s" %(func_name, str( self.AC ) ) )
            print("DEBUG: (Func = %s): self.AM      (type)  = %s" %(func_name, str( type(self.AM) )  ) )
            print("DEBUG: (Func = %s):              (value) = %s" %(func_name, str( self.AM ) ) )
            print("DEBUG: (Func = %s): self.FC      (type)  = %s" %(func_name, str( type(self.FC) )  ) )
            print("DEBUG: (Func = %s):              (value) = %s" %(func_name, str( self.FC ) ) )
            print("DEBUG: (Func = %s): self.FM      (type)  = %s" %(func_name, str( type(self.FM) )  ) )
            print("DEBUG: (Func = %s):              (value) = %s" %(func_name, str( self.FM ) ) )
            
    # end of __init__ 
    
    def type_signal(self):
        return True
    
    
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
        if debug: print("DEBUG: (Func = %s): string: %s" %( func_name, string ))
        self.A = float(string)
        return
        
    def __process_sampling_freq__(self, string, debug = False ):
        func_name = "__process__sampling_freq__"
        if debug: print("DEBUG: (Func = %s): string: %s" %( func_name, string ))
        self.FS = SI_string_to_float(string, debug)
        if debug: print("DEBUG: (Func = %s): value: %s" %( func_name, self.FS ))
      
    def __process_signal_freq__(self, string, debug = False ):
        func_name = "__process__signal_freq__"
        if debug: print("DEBUG: (Func = %s): string: %s" %( func_name, string ))
        self.FT = SI_string_to_float(string, debug)    
        
    def __process_signal_period__(self, string, debug = False ):
        func_name = "__process__signal_period__"
        if debug: print("DEBUG: (Func = %s): string: %s" %( func_name, string ))
        self.PER = SI_string_to_float(string, debug)         

    def __process_samples__(self, string, debug = False ):
        func_name = "__process__samples__"
        if debug: print("DEBUG: (Func = %s): string: %s" %( func_name, string ))
        self.N = int(string)
        
    def __process_phase__(self, string, debug = False ):
        func_name = "__process__phase__"
        if debug: print("DEBUG: (Func = %s): string: %s" %( func_name, string ))  
        # TODO: adjust from input: (2*np.pi/3) OR 2pi/3
        
    # Modulation processing funcitons...    
    def __process_message_frequency__(self, string, debug = False ):
        func_name = "__process_message_frequency__"
        if debug: print("DEBUG: (Func = %s): string: %s" %( func_name, string ))
        self.FM = float(string)
        self.modulation_signal = True # TODO: Reconsider 
        return        
        
    def __process_carrier_frequency__(self, string, debug = False ):
        func_name = "__process_carrier_frequency__"
        if debug: print("DEBUG: (Func = %s): string: %s" %( func_name, string ))
        self.FC = float(string)
        self.modulation_signal = True # TODO: Reconsider 
        return   

    def __process_message_amplitude__(self, string, debug = False ):
        func_name = "__process_message_amplitude__"
        if debug: print("DEBUG: (Func = %s): string: %s" %( func_name, string ))
        self.AM = float(string)
        self.modulation_signal = True # TODO: Reconsider 
        return 
    
    def __process_carrier_amplitude__(self, string, debug = False ):
        func_name = "__process_carrier_amplitude__"
        if debug: print("DEBUG: (Func = %s): string: %s" %( func_name, string ))
        self.AC = float(string)
        self.modulation_signal = True # TODO: Reconsider 
        return    
      
    
    # Key = allowable string option, Pair = The repsective processing function. 
    __process_field_opts__ = { 'a' : __process_amplitude__ ,
                               'A' : __process_amplitude__ ,
                               'fs': __process_sampling_freq__,
                               'n' : __process_samples__,
                               'ft': __process_signal_freq__,
                               'per': __process_signal_period__,
                               "phase" : __process_phase__, 
                               "fm" : __process_message_frequency__,
                               "fc" : __process_carrier_frequency__,
                               "am" : __process_message_amplitude__,
                               "ac" : __process_carrier_amplitude__,
                               }


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
        
        
        if debug: print("DEBUG: (Func = %s): Incoming 'setting' string: %s" %( func_name, settings ) )
        
        # Split line at delimiters
        line_split = settings.split(settings_delimiter)
        
        for item in line_split:
            # Remove all spaces
            item  = item.replace(" ", ""); 
            if debug: print("DEBUG: (Func = %s): Item: %s" %( func_name, item ) )
            
            # Split the field identifier and its value. 
            field_identifier = item.split(fields_delimiter) 
            if ( debug and len(field_identifier) is not 1 ): print("DEBUG: (Func = %s): Field: %s, Value: %s" %( func_name, field_identifier[0], field_identifier[1] ) )
            
            """ Objective: Call processing function. 
               
                  - Check if the field is supported.
                  - If so, call the respective process function. 
            """
            if field_identifier[0] in self.__process_field_opts__:
                self.__process_field_opts__[field_identifier[0]](self, field_identifier[1], debug)
                
        # TODO: All fields should be checked here....
                
        # ERROR If FT (tramission frequency) and FS (sampling frequency) are not provided.
        if self.FT is None and self.modulation_signal is False:
            sys.exit("ERROR: The transmission frequncy (ft) was not defined. Please added necessary information to 'settings' for signal construction...")


        ## Start: Build signal samples (nTs Ns)
        # if FS not provided, base the interval on FT and cycles
        if self.FS is None: 
            print("WARNING: No sampling frequency provided. Will provide default values for plotting...")
            if self.N is not (signal.default_samples_per_cycle * self.M):
                print("WARNING: Changing number of samples from %d to %d" %(self.N, (signal.default_samples_per_cycle * self.M)))
                self.N = (signal.default_samples_per_cycle * self.M)
            self.nTs    = np.linspace(start = 0, stop =  self.M * (1/self.FT), num = self.N )
            self.FS = self.nTs[1] - self.nTs[0]
            print("WARNING: Setting sampling frequency to: %f" %self.FS)
        else: # If sampling frequency was provided...
            self.nTs    =  np.linspace(0, (float(1)/self.FS)*self.N, self.N)  # time-indexed

            
        self.Ns     = range(self.N) # sample-indexed 
        self._signal = self.nTs
        ## End:   Build signal samples (nTs Ns)      
                
            
            
    # TODO: I want the '*plot*' functions in 'signal' to be linked to one
    #       plotter object. 
    #  
    #       I want this plotter object to have memory of all signals it needs 
    #       to plot. 
    #     
    #       An example I would like to see is the subplot easy linked to a 
    #       previously plotted signal in the script. 
    #       Ex) x = dsp.sin()
    #           x.plot() # A new figure and single plot is generated
    #           y = dsp.cos()
    #           y.subplot(x) # a new figure is plotted with both signals plotted.
    #           
    
    """ Note: Subplotting
    
    There are two ways to subplot. 
      - signal.subplot(other_signal)
      - dsp.subplot(signal1, signal2, [dims = [rows,columns]])
    """
   
    # TODO: Perhaps remove debug options in official check-in. 
    def plot(self, *args, settings = None, debug = False):
        func_name = "signal.plot"
        
        # These are signals that are to be plotted.... 
        # NOTE: dictionary with id() as key may be overkill, a simple list should do. 
        signals = {id(self):self}

        # Iterate through unspecified arguements. # Only Non kwargs allowed are signalObjs and 'settings'.
        for arg in args:          
            if (debug): print("DEBUG: (Func = %s): arg = %s"%(func_name, arg))

            # String type is only allowed for 'settings'
            if type(arg) is type(str()):
                if (debug): print("DEBUG: (Func = %s): string type arg was found: %s"%(func_name, str(arg)) ) # this would be for settings
                print("TODO: (Func = %s): Need to add parser to check if this arg is really for settings..."%(func_name))
                #settings = arg
                continue
            
            if type(arg) is type(bool):
                if (debug): print("DEBUG: (Func = %s): bool type arg was found: %s"%(func_name, str(arg))) 
                debug = arg
                continue
                
            #if type(arg) is type(self):
            try:
                if (arg.type_signal()):
                    if (debug): print("DEBUG: (Func = %s): signal type arg was found: %s"%(func_name, str(arg)))
                    signals[id(arg)] = arg
                    continue
            except:
                continue # Do nothing...
                
    
        # Boolean controlling how we plot in the light of multiple signals
        multi_plot = False
        
        # Default structures holding how signals wil be printed....
        # TODO: make these work within the context of 
        line_style = ["-", "--", "-."]
        markers    = ["o"]
        colors     = ["green", "red", "blue"] # TODO: this may need to grow AND be combined with functionality with 'settings'
        

        # If multiple signals were provided, set 'multi_plot' and check all signals for correct sample size
        if len(signals) > 1:
            if (debug): print("DEBUG: (Func = %s): 'signals' size = %d" %(func_name, len(signals)))
            multi_plot = True
            samples = self.N # Bootstrap the samples with the first signal 'self'
            for signal in signals:
                if (debug): print("DEBUG: (Func = %s): signal-id = %d, signal-obj = %s" %(func_name, signal, str(signals[signal])))
                if signals[signal].N != samples:
                    sys.exit("ERROR: (Func = %s): Signal samples size are not consistent. Main signal %s samples = %d, %s signal samples = %d"%(func_name,str(self),samples,str(signals[signal]),signals[signal].N))
        else:
            if (debug): print("DEBUG: (Func = %s): 'signals' size = %d" %(func_name, len(signals)))    
        
        # TODO: Confirm is this is needed? What happens if removed? 
        default_figure_size = [10.0, 8.0]
        plt.rcParams['figure.figsize'] = default_figure_size
        
        # Parse 'settings' and build the setup file....
        xaxis = 0 # {0:"samples", 1:"time" } # TODO: These should be moved into DS for setting up the setups for plotting
        gridon = True # TODO: These should be moved into DS for setting up the setups for plotting
        xlabel = None # TODO: These should be moved into DS for setting up the setups for plotting
        
        # Create new figure 
        figure = plt.figure()
        
        # Plot axis points..
        left_plot_axes    = 0.1
        bottom_plot_axes  = 0.4
        width_plot_axes   = 0.5
        height_plot_axes  = 0.5
        plot_edge = left_plot_axes   + width_plot_axes
        plot_top  = bottom_plot_axes + height_plot_axes
        plot_axes = [left_plot_axes,bottom_plot_axes, width_plot_axes,height_plot_axes]
        
        # Create Axes class (this make techincally be incorrect but suffice for understanding)
        axes   =  figure.add_axes(plot_axes)
        
        if multi_plot:
            if (debug): print("DEBUG: (Func = %s): Multiple plots. Ignore 'Signal Traits'..." %(func_name))
            
            for i, sig in enumerate(signals):
                if xaxis == 0: # samples
                    axes.plot(signals[sig].Ns, signals[sig]._signal, color = colors[i], linestyle = line_style[i], marker = markers[0] )
                    xlabel = "Sample Indexed"
                else: 
                    axes.plot(signals[sig].nTs, signals[sig]._signal, color = colors[i], linestyle = line_style[i], marker = markers[0])
                    xlabel = "Time Indexed" # TODO: Within the context of multi-plot how do I want to do this...
        
        else:  
            if (debug): print("DEBUG: (Func = %s): Not multiple plots. will print 'Signal Traits'..." %(func_name))
            # Determine how the signal x-axis should be? Samples or time-stamps
            if xaxis == 0: # samples
                axes.plot(self.Ns, self._signal) # TODO: Find out why generating stem plots take significantly longer to create than plot (or line) plots...
                xlabel = "Sample Indexed"
            else: 
                axes.stem(self.nTs, self._signal)
                xlabel = "Time Indexed"
        
            # Place grid if needed...
            plt.grid(gridon)    
            axes.set_xlabel(xlabel) #plt.xlabel(xlabel)
            #plt.ylabel('voltage (mV)')
            
            
            # Print title of the figure. 
            axes.set_title(self.__class__.__name__ + " signal")
            
            # Title of the right hand side, signal traits
            text_title = "Signal Traits"
            
            
            # All sections to be reported in the "Signal Traits"
            text_data = [ 
                          "Samples: " + str(self.N),
                          "Sampling-Freq: " + str(self.FS),
                          "Freq-resolution: " + str(self.freqRes),
                          "Signal-amplitude: " + str(self.A), 
                          "Signal-freq: " + str(self.FT),
                          "Signal-period: " + str(self.PER),
                          "Signal-Phase: " + str(self.PHASE),
                          ]
    
            step_size = 0.05
            # Set the text box coordinates...
            x_text_coor = plot_edge + step_size
            y_text_coor = plot_top 
            figure.text(x_text_coor, y_text_coor, text_title, fontsize = 12)
            

            offset = .05
            # Step through the text-data and print all fields...
            for line in text_data: 
                figure.text(x_text_coor, y_text_coor - offset, line, wrap = True) 
                offset = offset + step_size
            
            
        # Print signal...
        plt.show()
            

class sin(signal):
    def __init__(self, settings, debug = False): 
        super(sin, self).__init__(settings, debug)
        self._signal =(self.A)*np.sin((self.FT*2*np.pi)*self.nTs + self.PHASE) + self.DC
        self.freqRes = float(self.FS)/float(self.N)

        self.__class__.__name__ = "Sine"
        
class cos(signal):
    def __init__(self, settings,debug = False): 
        super(cos, self).__init__(settings,debug)
        self._signal =(self.A)*np.cos((self.FT*2*np.pi)*self.nTs + self.PHASE) + self.DC
        self.freqRes = float(self.FS)/float(self.N)      
        
        self.__class__.__name__ = "Cosine"
        
# There should be two ways of generating the am signal
#   1. passing in two signal objects and simply multiplying them. 
#   2. passing in the 'settings' which descrips all the characteristics necessary
#      parameters of an am signal (i.e. Ac, Am, fm, fc, ....)
# TODO: Need a way to distingush between DSB-SC, AM, SSB and VSB signals
# TODO: The init of signal should have another input arugement that takes in the modulation type which is default to None, 
#       Then we pass the modulation type from the am.__init__ to the signal.__init__
class am(signal):
    
    def __init__(self, message = None, carrier = None,  settings = None, debug = False):
        func_name = "am.__init__"
        
        # Ensure that is settings was provide, the message or carrier signals were also not set...
        if ( (settings is not None) and (message is not None or carrier is not None) ):
            sys.exit("ERROR: (func = %s): Can not create amplitude modulated signal if 'settings' is provided AND either 'message' or 'carrier' is provided. "%(func_name))
         
        # Ensure that is the message or carrier signals are provided...    
        if ( message is not None and carrier is None ) or (carrier is not None and message is None):
            sys.exit("ERROR: (func = %s): Both 'message' and 'carrier' signals need to be define to create an amplitudue modulation signal." %(func_name))
        
        # All sanity checks are above...
        
        if settings:
            super(am, self).__init__(settings,debug) # Simply pass the settings to signal base class...            
            self._signal = self.AC*np.sin(2*np.pi*self.FC*self.nTs) + ((self.AC*self.AM)/(2.0))*(np.sin(2*np.pi*(self.FC + self.FM)*self.nTs + self.PHASE) + np.sin(2*np.pi*(self.FC - self.FM)*self.nTs - self.PHASE))     
               #             Ac*np.sin(2*np.pi*fc*nTs) + ((Ac*Am)/(2.0))*                    (np.sin(2*np.pi*(fc + fm)*nTs + phase) +                     np.sin(2*np.pi*(fc - fm)*nTs - phase))
            self.freqRes = float(self.FS)/float(self.N) 
        
        
       
        
#sine_signal = sin("a=3.0; ft=50khz; n = 2048;", debug = True) 
##sine_signal.plot( debug = True )
#       
#cosine_signal = cos("a = 4.5; ft = 50khz; 2048;")
##cosine_signal.plot(sine_signal, debug = True )
#cosine_signal.plot( sine_signal,debug = True )
#cosine_signal.subplot(sine_signal, settings = "this would be some settings", sharex = True)  


# Plotting samples ...
#x.plot(y)          # GOOD: This will aim to put all the plots on a signal plot
#x.subplot(y,z)     # Good: this will create three distinct plots
#dsp.subplot(x,y,z) # ERROR: For now...





 
""" 
Revision Control (manual notes):
    
    
    005.t1: 2018-07-24:
      - Note: With this revision I want to implement a basic strucutre for FFT 
              work with modulation schemes
              These two schemes will take alot of reworking....
      - I removed singleton plotter...
      - I have implemented a basic working strucutre for am signals. However,
        view notes becasue I need to change the init from both am and signal classes. 
        As of now, it is too hacky
    
    004.o: 2018-07-23
      - Added 'multi_plot' to control signal.plot for a single signal or many. 
      - Create 'colors', 'line_style' and 'markers' to how default values for plotting. These 
        sholud be expanded and aimed to work i conjusction with 'settings' parsing. 
      - TODO: Need to added title to multi-plot
      - TODO: Add x azix to multi-plot
      - TODO: Refactor the size of figure for multi-plot.
      - Removed **kwargs from signal.plot. Everything handled through x or y 
      - Removed '__plotter__' from signal.plot to be added at later time. 
      - TODO: Need to establish better system for handling errors. Currently, anaconda or spyder will
              report 'An exception has occurred, use %tb to see the full traceback.

SystemExit: ERROR: (Func = signal.plot): Keyword (X) is not supported!! Exitting...

/anaconda3/lib/python3.6/site-packages/IPython/core/interactiveshell.py:2918: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.
  warn("To exit: use 'exit', 'quit', or Ctrl-D.", stacklevel=1)'
              It should only report what I have stated. 
      
    
    


"""        