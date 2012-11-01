#!/usr/bin/env python
################################################################################
#
# Name: runserver.py
# Description: Starts up a development instance of the app.
# Date: 28th Oct 2012
# Author: Andrew Bunday <andrew.bunday@gmail.com>
#
################################################################################

import os
import sys
sys.path.insert(0, os.path.join( os.path.dirname(os.path.abspath(__file__)), '3rdParty/python') )

from reproweb import app
app.run(host='0.0.0.0', port= app.config['SERVER_PORT'])
