################################################################################
#
# Name: backend.py
# Description: Functions used by the web view which are not direct endpoints.
# Date: 28th Oct 2012
# Author: Andrew Bunday <andrew.bunday@gmail.com>
#
################################################################################

import os

from . import app
from flask import json

################################################################################
# Repository access module. Updated at http://github.com/andrewbunday/repocheep

from repocheep import Repository
repository = Repository('/mnt/tech/repositories/apt/auto-lucid')

################################################################################
# Functions

def cache(settings):
    return PackageCache(settings.cachepath)

################################################################################
# Classes

class PackageCache(object):
    """
    Cache class. Provides performance enhancement for accessing package deb info.
                 Reprepro only provides handles to packages/versions and their
                 associated codename/component/arch. It handles debs for you and
                 does not provide an easy way to associate a deb file in the
                 repository with a package.

                 We use `reprepro.Repository.dumpreferences()` to extract the
                 current deb list in the repository. Then we use dpkg-deb to read
                 the deb file's package and associate the two.

                 For large repositories this can get slow. Once an association has
                 been generated it is stored as a json file in the cache.
    """

    def __init__(self, path):
        self.cachedir = path

    def cache_path(self, codename, component, arch, package, version):
        return os.path.join(self.cachedir, repository.name, codename, component, arch, package, '%s.json' % version)

    def write(self, codename, component, arch, package, version, data):
        cache_file_path = self.cache_path(codename, component, arch, package, version)
        try:
            if not os.path.exists(os.path.dirname(cache_file_path)):
                os.makedirs(os.path.dirname(cache_file_path))

            json.dump(data, open(cache_file_path, 'w'))
        except Exception as e:
            app.logger.warn('Unable to write cache %s to disk' % cache_file_path)
            app.logger.warn(e)
            raise e

    def read(self, codename, component, arch, package, version):
        path = self.cache_path(codename, component, arch, package, version)
        try:
            return json.load(open(path, 'r'))
        except:
            raise  # raises an exception if the cache file it wants to read cannot be.

class Settings(object):
    """Settings used by the webapp. Provides an object which reads configuration
       from disk and ingests it into its __dict__ making it available as attributes
       on the object."""

    loaded = False

    def __init__(self):
        """Reads the default/environment set configuration and attempts to load
           the specified settings file."""
        try:
            # attempt to read in the settings from a stored file on disk
            self.load(app.config['APP_SETTINGSFILE'])
            # if the attrs were set and not empty strings set the config as loaded.
            if self.settingsfile and self.basedir:
                self.loaded = True

        except Exception as e:
            app.logger.debug(e)
            self.loaded = False

    def load(self, config_file):
        """Load the settings file. Accessed via its own method to allow reloads."""
        data = json.load(open(config_file, 'r'))
        self.__dict__.update(data)

    def reload(self):
        """Try to re-initialize ourself"""
        self.__init__()

    def save(self, form):
        """Accepts a web input form from a request. Attmpts to store the content of
           the form within the file specified by 'settingsfile'.

           Returns: dict('status': 'OK') if app was able to write out the settings
                    file.
                    dict('status': '') if the app was not able to write out the
                    settings."""

        app.logger.debug(form)

        try:
            settings_dir = os.path.dirname(form['settingsfile'])
            if not os.path.exists(settings_dir):
                os.makedirs(settings_dir)

            # overwrite any previous settings.
            json.dump(form, open(form['settingsfile'], 'w'))

            return {'data': form, 'status': 'OK'}
        except Exception as e:
            app.logger.debug(e)
            return {'data': {}, 'status': 'FAIL'}



