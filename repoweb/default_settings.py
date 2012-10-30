################################################################################
#
# Name: default_settings.py
# Description: Default configuration settings for PyReproWeb. Either edit these,
#              or provide a file via PYREPROWEB_SETTINGS env var.
# Date: 28th Oct 2012
#
################################################################################

# Flask
DEBUG = False

# Application Settings
APP_NAME =  'ReproWeb'  # Lukas
APP_SETTINGSFILE = '/var/tmp/repoweb/settings.json'
APP_CACHEPATH = '/var/cache/repoweb'
APP_BASEDIR = '/mnt/tech/repositories/apt/auto-lucid'

# WSGI Settings
SERVER_PORT = 5000
