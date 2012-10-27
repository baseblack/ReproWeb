from flask import Flask
import logging

logging.basicConfig()

logging.debug('Starting %s' % __name__)
app = Flask(__name__)

# PyReproWeb endpoints
import fileio
import views

