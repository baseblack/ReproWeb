################################################################################
#
# Name: PyRepoWeb 
# Description: ...
# Date: 28th Oct 2012
# Author: Andrew Bunday <andrew.bunday@gmail.com>
#
################################################################################

import os

__version__ = "1.0.0"
__author__ = "andrew.bunday@gmail.com"
__website__ = "pyrepoweb.github.com"

# Initialze webapp
from flask import Flask
app = Flask(__name__)

# Read default settings and attempt to pick up settings overrides from 
# the environment.
app.config.from_object('repoweb.default_settings')

if os.getenv('PYREPROWEB_SETTINGS'):
    app.config.from_envvar('PYREPROWEB_SETTINGS')

# PyReproWeb endpoints
import views

# Make a first request to '/tests' to ensure the app is running correctly.
# ...


