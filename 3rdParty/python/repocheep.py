################################################################################
#
#
#
#
################################################################################

import os
import re
import logging
import inspect
import subprocess
from ordereddict import OrderedDict
from debian_bundle import debfile

class RepositoryException(Exception):
    pass

class ConfigurationException(Exception):
    pass

def config_reader(file_path):

    def parse(file_path):
        settings = OrderedDict()
        for i, line in enumerate(open(file_path)):
            tokens = [ x.strip() for x in line.split(":")]
            if len(tokens) == 2:
                try:
                    k,v = tokens
                    settings[k] = v
                except Exception as e:
                    raise ConfigurationException(e)
            else:
                yield settings
                settings = OrderedDict()

    return [ x for x in parse(file_path) ]

config_reader("/mnt/tech/repositories/apt/auto-lucid/conf/distributions")

class reprepro(object):

    def __init__(self, settings):
        self.configuration = settings
        self.listformat = '${$identifier} ${package} ${version}\n'

    def action(self, action, *params):
        cmd = ['reprepro']
        if self.configuration.verbose:
            cmd.append('-V')
        if self.configuration.components:
            cmd.append('-C')
            cmd.extend(self.configuration.components)
        if self.configuration.architectures:
            cmd.append('-A')
            cmd.extend(self.configuration.architectures)
        cmd.extend(['-b', self.configuration.settings['basedir']])
        cmd.append(action)
        cmd.extend(params)
        #... build up cmd
        return self._exec(cmd)

    def _exec(self, cmd):

        print " ".join(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        p.wait()
        out, err = p.communicate()

        if p.returncode:
            raise RepositoryException('not a reprepro repository')
        return out.strip().split('\n')

class dpkg_deb(object):

    def __init__(self):
        object.__init__(self)

    def action(self, action, *args, **params):
        cmd = ['dpkg-deb']
        cmd.extend(['--showformat', '${Package}\t${Version}\t"${Description}",\t${Replaces},\t${Maintainer}'])
        cmd.append(action)
        for item in params.items():
            cmd.extend(item)
        cmd.extend(args)
        return self._exec(cmd)

    def _exec(self, cmd):

        #print " ".join(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        p.wait()
        out, err = p.communicate()

        if p.returncode:
            raise RepositoryException('dpkg-deb fail')

        return out.strip().split(';')

def deb_listchanges(path):

    deb = debfile.DebFile(path)
    chg = deb.changelog()

    # handle if not changelog has been provided
    try:
        entries = chg._blocks
    except:
        entries = []

    return [str(entry) for entry in entries]

class DefaultSetup(object):
    """
    Configuration class. Provides options and settings used by reprepro cli.
    """
    verbose = True
    settings = {}

    def __init__(self, **kwargs):
        object.__init__(self)
        self.set_path(**kwargs)
        self.set_filters(**kwargs)

    def set_path(self, **paths):
        """
        Set/Update all paths for the repository. If only basedir is given all other
        paths will be set relative to this path.
        """
        # Set first, since the others depend on it.
        self.settings['basedir']   = paths.get('basedir', '.')

        # And then all the rest.
        self.settings['dbdir']     = paths.get('dbdir', '%s/db' % self.settings['basedir'])
        self.settings['outdir']    = paths.get('outdir', self.settings['basedir'])
        self.settings['logdir']    = paths.get('logdir', '%s/logs' % self.settings['basedir'])
        self.settings['confdir']   = paths.get('confdir', '%s/conf' % self.settings['basedir'])
        self.settings['distdir']   = paths.get('distdir', '%s/dists' % self.settings['basedir'])
        self.settings['listdir']   = paths.get('listdir', '%s/lists' % self.settings['basedir'])
        self.settings['morgedir']  = paths.get('morgedir', '')
        self.settings['methoddir'] = paths.get('methoddir', '')

    def set_filters(self, **filters):
        """
        Set global filter options.
        """
        self.settings['components']   = filters.get('components', [])
        self.settings['architectures']   = filters.get('architectures', [])

    def __getattr__(self, attr):
        try:
            return self.settings[attr]
        except:
            raise AttributeError("%s has no attribute '%s'" % (self, attr))

    def __repr__(self):
        return str(self.settings)


class Repository(object):
    """
    Top level class. Used for grabbing a repository instance and handling it
    gracefully.
    """
    def __init__(self, basedir):
        object.__init__(self)

        self.name = os.path.basename(basedir)
        self.options = DefaultSetup(basedir=basedir)

    def dist(self, codename):
        d = Dist(codename)
        d.options = self.options  # inherit our current settings.
        return d

    def list_dists(self):
        """
        Multi parse of conf/distributions. 1st parse detects the number of
        Codenames declared in the file. 2nd parse returns Dist() objects for
        each codename.

        Returns - A list of dictionaries which contain the configuration for the
                  dists.
        """
        return config_reader("%s/distributions" % self.options.confdir)

    def list_components(self, codename):
        for dist in self.list_dists():
            if dist['Codename'] == codename:
                components = []
                for component in dist['Components'].split():
                    components.append( {'component': component} )

                return components

    def list_architectures(self, codename):
        for dist in self.list_dists():
            if dist['Codename'] == codename:
                architectures = []
                for arch in dist['Architectures'].split():
                    architectures.append( {'architecture': arch} )

                return architectures

    def list_changes(self, debfile):
        return deb_listchanges(debfile)

    ### reprepro actions

    def check(self):
        return reprepro(self.options).action('check')

    def dumpreferences(self):
        """Print out which files are marked to be needed by whom."""
        # print inspect.stack()[0][3]  # <-- could use to to generate annonymouse calls.

        def parse_raw_package_data(raw):

            try:
                codename, component, arch, deb = re.split('\|+| ', raw)
                fields = OrderedDict({'codename': codename, 'component': component, 'arch': arch, 'deb': deb})
            except Exception as e:
                logging.warn(e)
                logging.warn('unparseable result 1=> %s' % raw)
                fields = None

            try:
                package_info = dpkg_deb().action('--show', os.path.join(self.options.basedir,deb))[0]
                #print package_info
                package, version, description, replaces, maintainer = package_info.split('\t')
                fields['package'] = package
                fields['version'] = version
                fields['description'] = description
                fields['replaces'] = replaces
                fields['maintainer'] = maintainer
            except RepositoryException as e:
                logging.warn(e)
                logging.warn('dpkg fail')
                fields = None

            except Exception as e:
                logging.warn(e)
                logging.warn(package_info)
                logging.warn('unparseable result 2=> %s' % raw)
                fields = None

            return fields

        #format ='{"codename":"${$codename}", "component":"${$component}", "arch":"${$architecture}", "package":"${package}", "version":"${version}"}\t'

        return [ parse_raw_package_data(p) for p in reprepro(self.options).action('dumpreferences') if parse_raw_package_data(p) ]

    def ls(self, package_name):
        """List the versions of the the specified package in all distributions."""

        return reprepro(self.options).action('ls', package_name)

    def list(self, codename, package_name=''):

        def parse_raw_package_data(raw):
            try:
                var = re.split( '\|+|\:', raw )
                fields = OrderedDict({'codename': var[0], 'component': var[1], 'architecture': var[2]})
                fields['package'], fields['version'] = var[3].split()
            except Exception as e:
                logging.warn(e)
                logging.warn('unscriptable package => %s' % raw)
                fields = {}

            return fields

        if package_name:
            package_strings = reprepro(self.options).action('list', codename, package_name)
        else:
            package_strings = reprepro(self.options).action('list', codename)

        packages = [ parse_raw_package_data(p) for p in package_strings]
        return packages

    def listmatched(self, codename, glob):
        return reprepro(self.options).action('listmatched', codename, glob)

class Dist(Repository):
    """
    Distribution level class, performs actions on a specific distro within a
    repo.
    """
    def __init__(self, codename, basedir='.'):
        self.codename = codename
        Repository.__init__(self, basedir)

    def listmatched(self, glob):
        return reprepro(self.options).action('listmatched', self.codename, glob)

class Package(object):
    def __init__(self, **kwargs):
        if 'deb' in kwargs:
            self.info_from_deb(kwargs['deb'])




