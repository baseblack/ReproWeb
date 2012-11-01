################################################################################
#
# Name: PyRepoWeb
# Description: ...
# Date: 28th Oct 2012
# Author: Andrew Bunday <andrew.bunday@gmail.com>
#
################################################################################

import os
from logging import Formatter, FileHandler
from logging.handlers import SysLogHandler
import logging

from flask import Flask

__version__ = "1.0.0"
__author__ = "andrew.bunday@gmail.com"
__website__ = "reproweb.github.com"

# Initialze webapp
app = Flask(__name__)

# Read default settings and attempt to pick up settings overrides from
# the environment.
app.config.from_object('reproweb.default_settings')

if os.getenv('REPROWEB_SETTINGS'):
    app.config.from_envvar('REPROWEB_SETTINGS')

# Setup logging. Base logfile on configuration
logfile = app.config['LOGFILE']
file_handler = FileHandler(logfile)
file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

syslog_handler = SysLogHandler()
syslog_handler.setLevel(logging.WARN)
app.logger.addHandler(syslog_handler)


# PyReproWeb endpoints
import views

# Make a first request to '/tests' to ensure the app is running correctly.
# ...


