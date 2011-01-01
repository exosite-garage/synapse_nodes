#==============================================================================
# ot_masternode.py
# SNAP Master Node code that interacts with other nodes on the SNAP network
# to receive their data and forward it onto a serial-to-Internet gateway for
# remote monitoring purposes.  This is part of an Exosite-compatible SNAP
# network configuration.
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

from synapse.evalBase import *
from synapse.switchboard import *
from synapse.sysInfo import *

NV_DEVICE_NAME_ID = 8       # The decice name is stored at this location
DEVICE_NAME = 'MSTR'
HEADER = '12345678'
FOOTER = '87654321'
NODE_PASSPHRASE = 'exositemasternode'
GW_PASSPHRASE = 'exositegateway'

#------------------------------------------------------------------------------
def startupEvent():
# Ran on power-up and reset, hooked into the HOOK_STARTUP event
#------------------------------------------------------------------------------
    node_name = loadNvParam(NV_DEVICE_NAME_ID)
    if node_name != DEVICE_NAME: 
      saveNvParam(NV_DEVICE_NAME_ID,DEVICE_NAME)
    initUart(0, 38400)
    flowControl(0,False)
    stdinMode(1, False) # Char Mode, Echo Off
    crossConnect(DS_STDIO, DS_UART0) # Hook UART to STDIO (print out/Event in)

#------------------------------------------------------------------------------
def publishData(node,resource,message):
# Invoked when a node publishes a message
#------------------------------------------------------------------------------
    # Due to crossConnect call above, all print messages sent out UART to GW
    print HEADER
    print node
    print resource
    print message
    print FOOTER
    return

#------------------------------------------------------------------------------
def stdinEvent(data_buff): 
# Invoked when the gateway sends us data via UART.
#------------------------------------------------------------------------------
    processCommands(data_buff)

#------------------------------------------------------------------------------
def processCommands(data_buff): 
# Process commands received from the gateway
#------------------------------------------------------------------------------
    if GW_PASSPHRASE == data_buff: # check for gateway 'ping'
      print NODE_PASSPHRASE  # just echo rx'd characters back
    else:
      print 'error: unavailable'

#==============================================================================
# SnappyGen Hooks
# Hook up event handlers
#==============================================================================
snappyGen.setHook(SnapConstants.HOOK_STARTUP, startupEvent)
snappyGen.setHook(SnapConstants.HOOK_STDIN, stdinEvent)

