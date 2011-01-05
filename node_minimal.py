#==============================================================================
# node_minimal.py
# Minimal SNAP Node code that allows the node to interact with SNAP network that
# is configured to work with Exosite's gateway and remote monitoring interfaces.
# This code expects there to be a master node somewhere in the mesh that
# implements the "publishNodeData" RPC (at minimum).
#
# Use this code as the starting point for custom node creation.
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
DEVICE_NAME = '[NODE CIK HERE FROM EXOSITE]' # Device name is its client interface key
LOOP_PERIOD = 10            # Adjust this to report/take action faster or slower
NV_DEVICE_GROUP_ID = 5
DEVICE_GROUP = 0x0003       # set to group 0x0002 (bit OR)

#==============================================================================
# Custom Node Code
#==============================================================================
#------------------------------------------------------------------------------
def initCustomCode():
# Function called at startup to initialize any custom items
#------------------------------------------------------------------------------
	return

#------------------------------------------------------------------------------
def runCustomCode():
# Function called periodically to run custom code - add function calls/code
# here that are specific to this node
#------------------------------------------------------------------------------
    #publish the data "hello" as resource "1"
	#note: some gateways can only handle 6 character names and values
    publishNodeData("1","hello")

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

