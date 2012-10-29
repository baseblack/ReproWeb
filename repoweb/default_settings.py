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
APP_NAME =  'PyReproWeb'  # Lukas
REPO_SETTINGS_FILE = '/var/tmp/repoweb/settings.json'
CACHE_DIR = '/var/cache/repoweb'
REPO_BASEDIR = ''

# WSGI Settings
SERVER_PORT = 5000
