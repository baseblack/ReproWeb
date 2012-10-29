################################################################################
#
# Name: views.py
# Description: Defines the visible endpoints available from the webapp.
# Date: 29th Oct 2012
# Author: Andrew Bunday <andrew.bunday@gmail.com>
#
################################################################################

import os
from functools import wraps

# Application framework imports
from flask import render_template
from flask import send_file
from flask import redirect
from flask import url_for
from flask import request
from flask import json
from flask import g

# Application setup/configuration etc.
from . import app
from backend import cache, Settings, repository

settings = Settings()

@app.route('/')
def index():
    """Displays a welcome splash screen and redirects to settings page
       on first run."""

    if not settings.loaded:
        return redirect(url_for('get_settings'))

    return render_template('index.html')

@app.route('/settings', methods=['GET', 'POST'])
def get_settings():
    """Settings view.
        * If a GET request is made the settings page is returned.
        * If a POST request is made, then the content of the request' form is
          loaded into the settings and saved to disk."""

    g.breadcrumb = [ {'name': 'settings', 'url': url_for('get_settings')}, ]

    if request.method == 'POST':
        return json.dumps(settings.save(request.form))

    if request.method == 'GET':
        settings.reload()
        g.settings = settings
        return render_template('settings.html')

@app.route('/about')
def get_about():
    g.breadcrumb = [ {'name': 'about', 'url': url_for('get_about')}, ]
    return render_template('about.html')

@app.route('/help')
def get_help():
    g.breadcrumb = [ {'name': 'help', 'url': url_for('get_help')}, ]
    return render_template('help.html')

@app.route('/api/packages/')
def get_packages():
    """Render a view listing _all_ of the packages within the repository."""
    g.breadcrumb = [ {'name': 'search', 'url': request.path}, ]

    package_list = repository.list('auto-lucid')
    for package in package_list:
        package['url'] = url_for('get_package_detail', codename = package.get('codename'),
                                                       component = package.get('component'),
                                                       architecture = package.get('architecture'),
                                                       package = package.get('package'),
                                                       version = package.get('version') )

    return render_template('api/packages.html', packages=sorted(package_list))

@app.route('/api/repository/')
def get_repository_detail():
    """Render a view listing all of the distributions configured in the repository"""
    g.breadcrumb = [ {'name': 'browse', 'url': url_for('get_repository_detail')}, ]

    codenames = repository.list_dists()
    for codename in codenames:
        codename['url'] = url_for('get_codename_detail', codename=codename.get('Codename','#'))

    return render_template('api/detail/repository.html', codenames=codenames)

@app.route('/api/<codename>/')
def get_codename_detail(codename):
    """Render a view listing all of the components of the selected distribution"""
    g.breadcrumb = [{'name': 'browse', 'url': url_for('get_repository_detail')},
                    {'name': codename, 'url': request.path},]

    components = repository.list_components(codename)
    if components:
        for c in components:
            c['url'] = url_for('get_component_detail', codename=codename, component=c['component'])
        return render_template('api/detail/codename.html', codename=codename, components=components)

    return render_template('api/detail/codename.html', codename=codename)

@app.route('/api/<codename>/<component>/')
def get_component_detail(codename, component):
    """Render a view listing all of the architectures of the selected component"""
    g.breadcrumb = [{'name': 'browse', 'url': url_for('get_repository_detail')},
                    {'name': codename, 'url': url_for('get_codename_detail', codename=codename)},
                    {'name': component, 'url': request.path},]

    archs = repository.list_architectures(codename)
    if archs:
        for a in archs:
            a['url'] = url_for('get_architecture_detail', codename=codename, component=component, architecture=a['architecture'])
        return render_template('api/detail/component.html', codename=codename, component=component, archs=archs)

    return render_template('api/detail/component.html', codename=codename, component=component)

@app.route('/api/<codename>/<component>/<architecture>/')
def get_architecture_detail(codename, component, architecture):
    """Render a view listing all of the packages referenced by the selected architecture"""
    g.breadcrumb = [{'name': 'browse', 'url': url_for('get_repository_detail')},
                    {'name': codename, 'url': url_for('get_codename_detail', codename=codename)},
                    {'name': component, 'url': url_for('get_component_detail', codename=codename, component=component)},
                    {'name': architecture, 'url': request.path},]

    # setup filters on component/architecture, str() cast is required for
    # subprocess. unicode is unsupported.
    repository.options.components = [str(component)]
    repository.options.architectures = [str(architecture)]
    package_list = repository.list(str(codename))
    repository.options.components = []
    repository.options.architectures = []

    for package in package_list:
        package['version_url'] = url_for('get_package_detail', codename = package.get('codename'),
                                                    component = package.get('component'),
                                                    architecture = package.get('architecture'),
                                                    package = package.get('package'),
                                                    version = package.get('version'))

        package['package_url'] = url_for('get_package_versions', codename = package.get('codename'),
                                                      component = package.get('component'),
                                                      architecture = package.get('architecture'),
                                                      package = package.get('package'))

    return render_template('api/packages.html', packages=sorted(package_list), codename=codename, component=component, architecture=architecture)

@app.route('/api/<codename>/<component>/<architecture>/<package>/')
def get_package_versions(codename, component, architecture, package):
    g.breadcrumb = [{'name': 'browse', 'url': url_for('get_repository_detail')},
                    {'name': codename, 'url': url_for('get_codename_detail', codename=codename)},
                    {'name': component, 'url': url_for('get_component_detail', codename=codename, component=component)},
                    {'name': architecture, 'url': url_for('get_architecture_detail', codename=codename, component=component, architecture=architecture)},
                    {'name': package, 'url': request.path},]

    # get any un-referenced versions of our package name
    all_versions = repository.list(codename, package)
    return render_template('api/detail/package.html', package=package, versions=all_versions)

@app.route('/api/<codename>/<component>/<architecture>/<package>/<version>')
@app.route('/api/<codename>/<component>/<architecture>/<package>/<version>/<format>')
def get_package_detail(codename, component, architecture, package, version, format=None):
    g.breadcrumb = [{'name': 'browse', 'url': url_for('get_repository_detail')},
                    {'name': codename, 'url': url_for('get_codename_detail', codename=codename)},
                    {'name': component, 'url': url_for('get_component_detail', codename=codename, component=component)},
                    {'name': architecture, 'url': url_for('get_architecture_detail', codename=codename, component=component, architecture=architecture)},
                    {'name': package, 'url': url_for('get_package_versions', codename=codename, component=component, architecture=architecture, package=package)},
                    {'name': version, 'url': request.path},]

    # get any un-referenced versions of our package name
    all_versions = repository.list(codename, package)

    try:
        reference = cache(settings).read(codename, component, architecture, package, version)
        app.logger.debug('Rendering from cache')
    except:
        # loop through the references until we find a match. Cache it out afterwards
        # so that we don't have to do this again.
        app.logger.debug('Exception caught, loading from repository')
        for ref in repository.dumpreferences():
            if ref['package'] == package and ref['version'] == version:
                ref['deb'] = os.path.join(repository.options.basedir, ref['deb'])

                try:
                    cache(settings).write(codename, component, architecture, package, ref['version'], ref)
                    reference = ref
                except Exception as e:
                    # unable to cache result. reference local variable will not have been set.
                    app.logger.warn(e)

    if 'reference' in locals():
        return render_template('api/detail/version.html', package=package, reference=reference, versions=all_versions)

    return render_template('api/detail/version.html', package=package)

@app.route('/api/<codename>/<component>/<architecture>/<package>/<version>/download')
def download_deb(**kwargs):
    app.logger.debug(kwargs)
    ref = cache(settings).read(kwargs['codename'], kwargs['component'], kwargs['architecture'], kwargs['package'], kwargs['version'])
    return send_file(ref['deb'], as_attachment=True)


