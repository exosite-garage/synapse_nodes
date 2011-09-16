========================================
About synapse_nodes
========================================
The synapse_nodes project is a collection of example SNAPPY scripts meant for
deployment on wirelesss nodes using the Synapse Wireless SNAP communications
stack.  The nodes are setup to communicate on a specific channel and each
node, including the master node, has its own Client Interface Key (CIK) 
identifier.  CIKs for the nodes must be obtained from Exosite's data platform
via the API or manually via the online Exosite Portals web dashboards.  The
master node aggregates remote node data and passes the remote node data through
to a gateway connected to the master node's serial port.

License is BSD, Copyright 2011, Exosite LLC (see LICENSE file)

--) Tested deployment of scripts with Synapse PORTAL version 2.4.17<br>
--) Tested functionality on Synapse wireless node model RF100 (FW version 2.4.9)<br>
--) Verified master node with gateways:<br>
  (1) https://github.com/exosite-garage/pc_serial_gateway v2011-09-15<br>
  (2) Fluid Gateway, firmware "fluid_synapse_gateway" v2011-06-08<br>

For more information on Exosite API and examples, reference Exosite online 
documentation at http://exosite.com/developers/documentation.

========================================
Quick Start
========================================
(1) Get a node CIK for each node from your Exosite account.  Go to your Exosite
account in Portals (https://portals.exosite.com) and add a new device using the
following information:<br>
  Device Type: Generic<br>
  Device Timezone: ---> Select your timezone<br>
  Device Location: ---> Provide any descriptive location<br>
  Device Name: ---> Any name you want to provide<br>

For additional documentation on adding a new device:<br>
http://exosite.com/developers/documentation?cid=1009

(2) Open the SNAP script in this project that you want to program to a SNAP
node and modify the NODECIKHEREFROMEXOSITEPLATFORM to be the 40 character CIK 
your new device was given in Exosite Portals.

(3) Open Synapse Portal on a PC and connect to a SNAP Stick USB module.

IMPORTANT: Ensure the SNAP node in the SNAP stick USB module is configured
to use the same group as the remote nodes

(4) Power on remote nodes and execute a "Broadcast PING" in the Synapse Portal.
This will "find" all active nodes and list them in the Node Views box.

(5) In Synapse Portal, select the remote node to be programmed in the Node
Views box.

(6) Click "Upload SNAPPy Image" button in the Node Info box and select the 
node image in this project that the node will be programmed with.

(7) Attach a node with the "node_master.py" script to a supported gateway and
ensure power is on for the master node, the gateway and the remote nodes.

(8) Login to Exosite Portals and verify the "new device" you created in step 1
is receiving data

========================================
Release History
========================================
----------------------------------------
2011-07-24
----------------------------------------
--) updated comments regarding alias creation<br>

----------------------------------------
2011-01-11
----------------------------------------
--) updated nodes to use NV param for group-based communications<br>

----------------------------------------
2011-01-01
----------------------------------------
--) initial release<br>

----------------------------------------
