#==============================================================================
# node_powermeter.py
# SNAP Node code that monitors ADC inputs that are hooked up to current clamps
# Used as a wireless power monitoring node.
# Configured to work with Exosite's gateway and remote monitoring interfaces.
# This code expects there to be a master node somewhere in the mesh that
# implements the "publishNodeData" RPC (at minimum).
#==============================================================================
## Copyright (c) 2010, Exosite LLC
## All rights reserved.
##
## Redistribution and use in source and binary forms, with or without 
## modification, are permitted provided that the following conditions are met:
##
##    * Redistributions of source code must retain the above copyright notice,
##      this list of conditions and the following disclaimer.
##    * Redistributions in binary form must reproduce the above copyright 
##      notice, this list of conditions and the following disclaimer in the
##      documentation and/or other materials provided with the distribution.
##    * Neither the name of Exosite LLC nor the names of its contributors may
##      be used to endorse or promote products derived from this software 
##      without specific prior written permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
## ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
## LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
## SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
## INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
## CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
## ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
## POSSIBILITY OF SUCH DAMAGE.

# Use Synapse Evaluation Board definitions
from synapse.evalBase import *

NV_DEVICE_NAME_ID = 8       # The device name is stored at this location
DEVICE_NAME = 'NODECIKHEREFROMEXOSITEPLATFORM'        # Device name is its client interface key
LOOP_PERIOD = 10            # Adjust this to report/take action faster or slower
NV_DEVICE_GROUP_ID = 5
DEVICE_GROUP = 0x0003       # set to groups 0x0001 and 0x0002 (bit OR)

#==============================================================================
# Custom Node Code
#==============================================================================
#------------------------------------------------------------------------------
def initCustomCode():
# Function called at startup to initialize any custom items
#------------------------------------------------------------------------------
    global sequence
    sequence = 0

#------------------------------------------------------------------------------
def runCustomCode():
# Function called periodically to run custom code - add function calls/code
# here that are specific to this node
#------------------------------------------------------------------------------
    global sequence
    #note - if name of publish source does not exactly match the data source
    #name in Exosite Portals, a new data source will need to be created  to 
    #match.  some gateways will be able to auto-create the data source, while
    #other simpler gateways will need the data source to be manually created
    
    if 0 == sequence:
      #we are using dumb clamps that output about 1 step = 0.23A.  Max reading
      #is around 100 so we can safely multiply by up to 327.  ADC0 is 110V, so we
      #multiply by 25 per step to get watts.  ADC1 is 220V, so we multiply by 50 
      #to get Watts
      value = 25 * getPowerValue(0) # Read Adc on GPIO 18
      name = "1"
    elif 1 == sequence:
      value = 50 * getPowerValue(1) # Read Adc on GPIO 17
      name = "2"
    elif 2 == sequence:
      #our new test clamp outputs about 3.67 steps per amp (1 step = 0.27A).  it 
      #hooked to a 220v line, so watts = reading * 0.27 * 220 = reading * 60
      value = 60 * getPowerValue(2) # Read Adc on GPIO 16
      name = "3"
    elif 3 == sequence:
      value = 30 * getPowerValue(3) # Read Adc on GPIO 15
      name = "4"
    elif 4 == sequence:
      #CT248-M clamp is 33.3mA at 100A across a 100 ohm resistor.  Means it will
      #generate 3.3v (1024 ADC value) at 100A usage.  So, each count equals
      #0.0976 amps.  Since CT248-M are big hosses, they are typically used on
      #220V 3-phase power.  So, we can calculate wattage by ADCValue*0.0976*220,
      #or ADCValue * 21.48.
      value = 21.48 * getPowerValue(4) # Read Adc on GPIO 14
      name = "5"
      
    publishNodeData(name,value)
    
    sequence += 1
    if sequence > 4: sequence = 0

#------------------------------------------------------------------------------
def getPowerValue(adcPin):
#------------------------------------------------------------------------------
    #Get adc values
    minval = 1024
    maxval = 0
    sample = readAdc(adcPin) #pre-read
    # nodes can read up to 5000 samples per second (one sample every 0.2mS). A
    # single 60Hz waveform spans 16.7mS, and we have to read at least 1/2 of
    # it to get a peak (min or max).  so we have to sample at least 42 times.
    # 10 bit adc can return a value of up to 1024
    # snappy ints can be up to 32767, so we are safe summing up to 30 times
    adcReads = 0
    total = 0
    while adcReads < 25:
      adcReads += 1
      sample = readAdc(adcPin)
      if minval > sample: minval = sample
      if maxval < sample: maxval = sample
      total += sample
    average1 = total / adcReads
    adcReads = 0
    total = 0
    while adcReads < 25:
      adcReads += 1
      sample = readAdc(adcPin)
      if minval > sample: minval = sample
      if maxval < sample: maxval = sample
      total += sample
    average2 = total / adcReads
    sample = (average1 + average2) / 2
    return getAbsDiff(minval,maxval,sample)

#------------------------------------------------------------------------------
def getAbsDiff(minVal,maxVal,avgVal):
#------------------------------------------------------------------------------
    if (avgVal - minVal) > (maxVal - avgVal): return avgVal - minVal
    else: return maxVal - avgVal

#==============================================================================
# Standard Node Code
#==============================================================================
#------------------------------------------------------------------------------
def startupEvent():
# This is hooked into the HOOK_STARTUP event - called at power up or reset
#------------------------------------------------------------------------------
    global secondCounter, timerCounter, node_name
    secondCounter = 0 # Used by the system for one second count
    timerCounter = 0 # Used by the system for 100mS count
    node_name = loadNvParam(NV_DEVICE_NAME_ID)
    if node_name != DEVICE_NAME: 
      saveNvParam(NV_DEVICE_NAME_ID,DEVICE_NAME)
    group = loadNvParam(NV_DEVICE_GROUP_ID)
    if group != DEVICE_GROUP:
      saveNvParam(NV_DEVICE_GROUP_ID,DEVICE_GROUP)
    initProtoHw() # Intialize the proto board
    initCustomCode() # Initialize custom code

#------------------------------------------------------------------------------
def doEverySecond():
# Things to be done every second
#------------------------------------------------------------------------------
    global secondCounter
    secondCounter += 1
    if secondCounter >= LOOP_PERIOD:
      runCustomCode()
      secondCounter = 0

#------------------------------------------------------------------------------
def timer100msEvent(currentMs):
# Hooked into the HOOK_100MS event. Called every 100ms
#------------------------------------------------------------------------------
    global timerCounter
    timerCounter += 1
    if timerCounter >= 10:
        doEverySecond()
        timerCounter = 0

#------------------------------------------------------------------------------
def publishNodeData(resource_name, resource_value):
# Sends node data into the ether for a master node to pick up and transmit
# onto the gateway for remote monitoring
#------------------------------------------------------------------------------
    global node_name
    mcastRpc(DEVICE_GROUP, 10, "publishData",node_name,resource_name,resource_value)

#==============================================================================
# SnappyGen Hooks
# Hook up event handlers
#==============================================================================
snappyGen.setHook(SnapConstants.HOOK_STARTUP, startupEvent)
snappyGen.setHook(SnapConstants.HOOK_100MS, timer100msEvent)

