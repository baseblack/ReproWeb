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

import repocheep
repository = repocheep.Repository('/mnt/tech/repositories/apt/auto-lucid')

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

    def __init__(self):
        self.cachedir = '/var/cache/repoweb'

    def cache_path(self, codename, component, arch, package, version):
        return os.path.join(self.cachedir, repository.name, codename, component, arch, package, '%s.json' % version)

    def write(self, codename, component, arch, package, version, data):
        path = self.cache_path(codename, component, arch, package, version)
        try:
            os.makedirs(os.path.dirname(path))
            json.dump(data, open(path, 'w'))
        except:
            app.logger.warn('Unable to write cache %s to disk' % path)

    def read(self, codename, component, arch, package, version):
        path = self.cache_path(codename, component, arch, package, version)
        if os.access(path, os.R_OK):
            return json.load(open(path, 'r'))

def save_settings(form):
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
        # if _anything_ goes wrong, return unsuccessfull.

        app.logger.debug(e)
        return {'status': ''}


