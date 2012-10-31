#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.join( os.path.dirname(os.path.abspath(__file__)), '3rdParty/python') )

import fapws._evwsgi as evwsgi
from fapws import base

from reproweb import app

evwsgi.start('0.0.0.0', str(app.config['SERVER_PORT']))
evwsgi.set_base_module(base)

evwsgi.wsgi_cb(('/', app))
evwsgi.set_debug(0)
evwsgi.run()
