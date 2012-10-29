from . import app
from flask import render_template, url_for, redirect, request, json
import flask

import os

# Application setup/configuration etc.
from backend import repository, save_settings, PackageCache


@app.route('/')
def index():
    """Displays a welcome splash screen and triggers creation/setup on first run."""

    if not os.path.exists(app.config['REPO_SETTINGS_FILE']):
        return redirect(url_for('get_settings'))

    return render_template('index.html')



@app.route('/settings', methods=['GET', 'POST'])
def get_settings():
    if request.method == 'POST':
        try:
            result = save_settings(request.form)
            return json.dumps(result)
        except Exception as e:
            app.logger.debug(e)
            app.logger.warn('unable to save settings file')
            return json.dumps({})
    else:
        flask.g.breadcrumb = [ {'name': 'settings', 'url': url_for('get_settings')}, ]

        try:
            settings = json.load(open(app.config['REPO_SETTINGS_FILE'], 'r'))
            return render_template('settings.html', settings=settings)
        except Exception as e:
            app.logger.debug(e)
            return render_template('settings.html', settings={})

@app.route('/about')
def get_about():
    flask.g.breadcrumb = [ {'name': 'about', 'url': url_for('get_about')}, ]
    return render_template('about.html')


@app.route('/help')
def get_help():
    flask.g.breadcrumb = [ {'name': 'help', 'url': url_for('get_help')}, ]
    return render_template('help.html')

@app.route('/api/packages/')
def get_packages():
    flask.g.breadcrumb = [ {'name': 'search', 'url': flask.request.path}, ]

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

    return render_template('api/packages.html', packages=sorted(package_list))

@app.route('/api/distributions/')
def get_codenames():
    codenames = repository.list_dists()
    flask.g.repository = repository

    for codename in codenames:
        if codename:
            url = url_for('get_codename_detail', codename=codename.get('Codename','#'))
            codename['url'] = url
            #app.logger.debug(url)

    flask.g.breadcrumb = [ {'name': 'browse', 'url': url_for('get_codenames')}, ]
    return render_template('api/distributions.html', codenames=codenames)

@app.route('/api/<codename>/')
def get_codename_detail(codename):
    flask.g.breadcrumb = [ {'name': 'browse', 'url': url_for('get_codenames')},
                           {'name': codename, 'url': flask.request.path}, ]

    components = repository.list_components(codename)
    if components:
        print components
        for c in components:
            url = url_for('get_component_detail', codename=codename, component=c['component'])
            c['url'] = url
            app.logger.debug(url)

        return render_template('api/detail/codename.html', codename=codename, components=components)

    return render_template('api/detail/codename.html', codename=codename)

@app.route('/api/<codename>/<component>/')
def get_component_detail(codename, component):
    flask.g.breadcrumb = [ {'name': 'browse', 'url': url_for('get_codenames')},
                           {'name': codename, 'url': url_for('get_codename_detail', codename=codename)},
                           {'name': component, 'url': flask.request.path}, ]

    archs = repository.list_architectures(codename)
    if archs:
        for a in archs:
            url = url_for('get_architecture_detail', codename=codename, component=component, architecture=a['architecture'])
            a['url'] = url
            app.logger.debug(url)

        return render_template('api/detail/component.html', codename=codename, component=component, archs=archs)

    return render_template('api/detail/component.html', codename=codename, component=component)

@app.route('/api/<codename>/<component>/<architecture>/')
def get_architecture_detail(codename, component, architecture):
    flask.g.breadcrumb = [ {'name': 'browse', 'url': url_for('get_codenames')},
                           {'name': codename, 'url': url_for('get_codename_detail', codename=codename)},
                           {'name': component, 'url': url_for('get_component_detail', codename=codename, component=component)},
                           {'name': architecture, 'url': flask.request.path}, ]

    repository.options.components = [str(component)]
    repository.options.architectures = [str(architecture)]
    package_list = repository.list('auto-lucid')
    repository.options.components = []
    repository.options.architectures = []

    for package in package_list:
        if package:
            version_url = url_for('get_package_detail', codename = package.get('codename'),
                                                component = package.get('component'),
                                                architecture = package.get('architecture'),
                                                package = package.get('package'),
                                                version = package.get('version') )

            package_url = url_for('get_package_versions', codename = package.get('codename'),
                                                component = package.get('component'),
                                                architecture = package.get('architecture'),
                                                package = package.get('package') )

            package['package_url'] = package_url
            package['version_url'] = version_url

    return render_template('api/packages.html', packages=sorted(package_list), codename=codename, component=component, architecture=architecture)

@app.route('/api/<codename>/<component>/<architecture>/<package>/')
def get_package_versions(codename, component, architecture, package):
    flask.g.breadcrumb = [ {'name': 'browse', 'url': url_for('get_codenames')},
                           {'name': codename, 'url': url_for('get_codename_detail', codename=codename)},
                           {'name': component, 'url': url_for('get_component_detail', codename=codename, component=component)},
                           {'name': architecture, 'url': url_for('get_architecture_detail', codename=codename, component=component, architecture=architecture)},
                           {'name': package, 'url': flask.request.path}, ]

    try:
        ref = PackageCache().read(codename, component, architecture, package)
        all_versions = repository.list(codename, package)
        app.logger.debug('rendering from cache')
        return render_template('api/detail/package.html', package=package, reference=ref, versions=all_versions)
    except:
        app.logger.debug('gathering package info')
        references = repository.dumpreferences()
        all_versions = repository.list(codename, package)
        for ref in references:
            try:
                if ref['package'] == package:  # only 1 version of a package will be the current reference
                    ref['deb'] = os.path.join(repository.options.basedir, ref['deb'])
                    PackageCache().write(codename, component, architecture, package, ref['version'], ref)
                    return render_template('api/detail/package.html', package=package, reference=ref, versions=all_versions)
            except:
                print ref

    return render_template('api/package_versions.html', package=package)

@app.route('/api/<codename>/<component>/<architecture>/<package>/<version>')
@app.route('/api/<codename>/<component>/<architecture>/<package>/<version>/<format>')
def get_package_detail(codename, component, architecture, package, version, format=None):
    flask.g.breadcrumb = [ {'name': 'browse', 'url': url_for('get_codenames')},
                           {'name': codename, 'url': url_for('get_codename_detail', codename=codename)},
                           {'name': component, 'url': url_for('get_component_detail', codename=codename, component=component)},
                           {'name': architecture, 'url': url_for('get_architecture_detail', codename=codename, component=component, architecture=architecture)},
                           {'name': package, 'url': url_for('get_package_versions', codename=codename, component=component, architecture=architecture, package=package)},
                           {'name': version, 'url': flask.request.path}, ]

    try:
        app.logger.debug('attmpting to read from cache')
        ref = PackageCache().read(codename, component, architecture, package, version)
        all_versions = repository.list(codename, package)
        if format=='json':
            return json.dumps(ref)
        return render_template('api/detail/package.html', package=package, reference=ref, versions=all_versions)
    except Exception as e:
        app.logger.debug(e)
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
                    return render_template('api/detail/package.html', package=package, reference=ref, versions=all_versions)
            except:
                print ref

    return render_template('api/detail/package.html', package=package)

@app.route('/api/<codename>/<component>/<architecture>/<package>/<version>/download')
def download_deb(**kwargs):
    app.logger.debug(kwargs)
    ref = PackageCache().read(kwargs['codename'], kwargs['component'], kwargs['architecture'], kwargs['package'], kwargs['version'])
    deb_filepath = ref['deb']
    return flask.send_file(ref['deb'], as_attachment=True)


