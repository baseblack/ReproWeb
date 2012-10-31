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
#
# repocheep can be replaced by any library you like. requirements are:
#
# * the library must provide a Repository class on which to perform actions.
# * any replacement must return lists of dictionaries containing the contents of
#   an action.
# * actions should be in the form Repository.<Action> ie, repository.dumpreferences()
# * options such as `-C`, `-T`, or `-A` are set on the repository
#   as respository.options.X

from repocheep import Repository

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

    def cache_path(self, repository, codename, component, arch, package, version):
        return os.path.join(self.cachedir, repository.name, codename, component, arch, package, '%s.json' % version)

    def write(self, repository, codename, component, arch, package, version, data):
        cache_file_path = self.cache_path(repository, codename, component, arch, package, version)
        try:
            if not os.path.exists(os.path.dirname(cache_file_path)):
                os.makedirs(os.path.dirname(cache_file_path))

            json.dump(data, open(cache_file_path, 'w'))
        except Exception as e:
            app.logger.warn('Unable to write cache %s to disk' % cache_file_path)
            app.logger.warn(e)
            raise

    def read(self, repository, codename, component, arch, package, version):
        path = self.cache_path(repository, codename, component, arch, package, version)
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

        except Exception as e:
            app.logger.debug(e)
            self.loaded = False

    def load(self, config_file):
        """Load the settings file. Accessed via its own method to allow reloads."""
        data = json.load(open(config_file, 'r'))
        self.__dict__.update(data)

        # if the attrs were set and not empty strings set the config as loaded.
        if self.settingsfile and self.basedir:
            self.loaded = True

    def reload(self):
        """Try to re-initialize ourself"""
        try:
            self.load(self.settingsfile)
        except Exception as e:
            app.logger.debug(e)
            self.loaded = False

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
        except Exception as e:
            app.logger.debug(e)
            return {'data': {}, 'status': 'WRITE_FAIL'}

        try:
            # try to apply the settings back onto self.
            self.load(form['settingsfile'])
        except:
            return {'data': {}, 'status': 'LOAD_FAIL'}

        # all is good, return OK
        return {'data': form, 'status': 'OK'}


