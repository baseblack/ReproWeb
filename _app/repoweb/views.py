from . import app
from flask import render_template, url_for, redirect, request
import flask

import repocheep
import logging
import json
import os


repository = repocheep.Repository('/mnt/tech/repositories/apt/auto-lucid')

class PackageCache(object):
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
    app.logger.debug(form)
    try:
        settings_dir = os.path.dirname(form['settingsfile'])
        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir)

        json.dump(form, open(form['settingsfile'], 'w'))

        return {'data': form, 'status': 'OK'}
    except Exception as e:
        app.logger.debug(e)
        return {'status': ''}

@app.route('/')
def index():
    if not os.path.exists('/var/tmp/repoweb/settings.json'):
        return redirect(url_for('get_settings'))

    return render_template('index.html')

@app.route('/settings', methods=['GET', 'POST'])
def get_settings():
    if request.method == 'POST':
        try:
            result = save_settings(request.form)
            return json.dumps(result)
        except:
            app.logger.warn('unable to save settings file')
            return json.dumps({})
    else:
        try:
            settings = json.load(open('/var/tmp/repoweb/settings.json', 'r'))
            return render_template('settings.html', settings=settings)
        except Exception as e:
            app.logger.debug(e)
            return render_template('settings.html', settings={})

@app.route('/about')
def get_about():
    return render_template('about.html')

@app.route('/api/packages/')
def get_packages():

    package_list = repository.list('auto-lucid')
    for package in package_list:
        if package:
            url = url_for('get_package_detail', codename = package.get('codename'),
                                                component = package.get('component'),
                                                architecture = package.get('architecture'),
                                                package = package.get('package'),
                                                version = package.get('version') )
            package['url'] = url
            #app.logger.debug(url)

    return render_template('packages.html', packages=sorted(package_list))

@app.route('/api/distributions/')
def get_codenames():
    codenames = repository.list_dists()
    for codename in codenames:
        if codename:
            url = url_for('get_codename_detail', codename=codename.get('Codename','#'))
            codename['url'] = url
            #app.logger.debug(url)

    return render_template('distributions.html', codenames=codenames)

@app.route('/api/<codename>/')
def get_codename_detail(codename):
    components = repository.list_components(codename)
    if components:
        print components
        for c in components:
            url = url_for('get_component_detail', codename=codename, component=c['component'])
            c['url'] = url
            app.logger.debug(url)
        return render_template('codename_detail.html', codename=codename, components=components)

    return render_template('codename_detail.html', codename=codename)

@app.route('/api/<codename>/<component>/')
def get_component_detail(codename, component):
    archs = repository.list_architectures(codename)
    if archs:
        for a in archs:
            url = url_for('get_architecture_detail', codename=codename, component=component, architecture=a['architecture'])
            a['url'] = url
            app.logger.debug(url)
        return render_template('component_detail.html', codename=codename, component=component, archs=archs)

    return render_template('component_detail.html', codename=codename, component=component)

@app.route('/api/<codename>/<component>/<architecture>/')
def get_architecture_detail(codename, component, architecture):

    repository.options.components = [str(component)]
    repository.options.architectures = [str(architecture)]
    package_list = repository.list('auto-lucid')
    repository.options.components = []
    repository.options.architectures = []

    for package in package_list:
        if package:
            url = url_for('get_package_detail', codename = package.get('codename'),
                                                component = package.get('component'),
                                                architecture = package.get('architecture'),
                                                package = package.get('package'),
                                                version = package.get('version') )
            package['url'] = url
            #app.logger.debug(url)

    return render_template('packages.html', packages=sorted(package_list), codename=codename, component=component, architecture=architecture)

@app.route('/api/<codename>/<component>/<architecture>/<package>/')
def get_package_versions(codename, component, architecture, package):

    try:
        ref = PackageCache().read(codename, component, architecture, package)
        all_versions = repository.list(codename, package)
        app.logger.debug('rendering from cache')
        return render_template('package_detail.html', package=package, reference=ref, versions=all_versions)
    except:
        app.logger.debug('gathering package info')
        references = repository.dumpreferences()
        all_versions = repository.list(codename, package)
        for ref in references:
            try:
                if ref['package'] == package:  # only 1 version of a package will be the current reference
                    ref['deb'] = os.path.join(repository.options.basedir, ref['deb'])
                    PackageCache().write(codename, component, architecture, package, version, ref)
                    return render_template('package_detail.html', package=package, reference=ref, versions=all_versions)
            except:
                print ref

    return render_template('package_versions.html', package=package)

@app.route('/api/<codename>/<component>/<architecture>/<package>/<version>')
@app.route('/api/<codename>/<component>/<architecture>/<package>/<version>.<format>')
def get_package_detail(codename, component, architecture, package, version, format=None):

    try:
        ref = PackageCache().read(codename, component, architecture, package, version)
        all_versions = repository.list(codename, package)
        app.logger.debug('rendering from cache')
        if format=='json':
            return json.dumps(ref)
        return render_template('package_detail.html', package=package, reference=ref, versions=all_versions)
    except:
        app.logger.debug('gathering package info')
        references = repository.dumpreferences()
        all_versions = repository.list(codename, package)
        for ref in references:
            try:
                if ref['package'] == package:  # only 1 version of a package will be the current reference
                    ref['deb'] = os.path.join(repository.options.basedir, ref['deb'])
                    PackageCache().write(codename, component, architecture, package, version, ref)
                    if format=='json':
                        return json.dumps(ref)
                    return render_template('package_detail.html', package=package, reference=ref, versions=all_versions)
            except:
                print ref

    return render_template('package_detail.html', package=package)

@app.route('/api/help')
def get_help():
    return render_template('help.html')
