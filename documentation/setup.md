## Getting started

This document demonstrates the installation, setup and usage of the app.

### Requirements

1.  A debian/ubuntu based system which has the following packages installed:
    * __reprepro__ - Debian package repository producer
    * __python-debian__ - Python modules to work with Debian-related data formats
    * __libevX__ - high-performance event loop library modelled after libevent. You'll
      need the appropriate version for you distribution.
    * __fapws3__ - Fast Asyncronous Python Web Server, there is a version bundled in the 3rdParty
     folder which is known to work on ubuntu 10.04. For newer installations you may need to
     rebuild this library. I suggest using [fpm](https://github.com/jordansissel/fpm/wiki/ConvertingPython).

1.   Sudo or _(ick root access)_ if you choose to write the cache files to their preconfigured
     path in /var/cache.


### Installation

1.    Download the latest tarball out of github from
      [here](https://github.com/andrewbunday/reproweb/tarball/master). Extract it into the
      location you want to run your install from.

      The bundle consists of:
      * reproweb/ - a flask based webapp
      * 3rdParty/ - dependencies required by the webapp (flask/werkzerg/orderddict/jinja2)
      * Scripts to launch and run the webserver - `debug-run.py` and `fapws3-run.py`

1.    Next, download the most up to date version of
      [reprocheep](http://github.com/andrewbunday/repocheep).
      Reepocheep is the module which provides an interface to reprepro and dpkg which the
      webapp uses. Drop the reprocheep file into the 3rdParty/python folder, or add it
      somewhere on your PYTHONPATH.

1.    Decide on your configuration file. The file `reproweb/default_settings.py` contains
      the default settings which the app will try to use when it starts up.

      You can either choose to:
      * Edit this file directly
      * Create a new file and inform the webapp to use it by setting the environment variable -

            REPROWEB_SETTINGS=/path/to/my/settings_file

1.    Settings which you can change the defaults of are:

        DEBUG = False

        # Application Settings
        APP_NAME =  'ReproWeb'
        APP_SETTINGSFILE = '/var/tmp/reproweb/settings.json'
        APP_CACHEPATH = '/var/cache/reproweb'
        APP_BASEDIR = '/mnt/tech/repositories/apt/auto-lucid'

        # WSGI Settings
        SERVER_PORT = 5000

1.    __IMPORTANT__ - If you choose to leave the cache setting at the default location of
      `/var/cache/reproweb` then you must make the directory before going any further.

      /var/cache is a restricted directory and will require you to create the the reproweb
      subfolder with sudo access. Once the directory has been created, change the
      permissions on it to allow the user who the web app will run as to write to the
      reproweb directory.

### Running the App

1.    Included with the app are two run scripts.
      * `debug-run.py` will use Flask's native WSGI server to
      serve requests. It's handy to use this when you need to debug something since it
      will provide lots of console output and an interactive error page if a view fails.
      * `fapws3-run.py` uses the Fast Asynchorous Python Web Server to handle requests on
      behalf of Flask. Its generally more stable than flask's server and can handle far
      more concurrent interactions.

1.    Choose one of the run scripts and start it up from the commandline.

        $ python debug-run.py
           * Running on http://0.0.0.0:5000/
           * Restarting with reloader

1.    Open up a web browser navigating to the localhost, or whatever server you are using.

       <center>![](https://raw.github.com/baseblack/ReproWeb/master/documentation/images/image_01.png)</center>

1.    When the app runs for the first time it will try to load its settings from disk.
      The settings are saved in a json file which holds a serialized version of the
      default configuration as well as any additional settings we add to the app or
      which are generated during setup.

      If the app cannot load the settings, because the file doesn't exist it will redirect
      straight to the settings page __http://localhost:5000/settings__:

      <center>![](https://raw.github.com/baseblack/ReproWeb/master/documentation/images/image_02.png)</center>

      The input fields marked with stars are required for the app to run. If the settings
      file is not set you will keep being redirect to the settings page and if the Base
      directory is not set Reproweb has no way of knowing which repository it should be
      looking at.

1.    Click on the Save button and if the settings have been stored a green success
      message will be displayed.

      <center>![](https://raw.github.com/baseblack/ReproWeb/master/documentation/images/image_03.png)</center>

1.    Now you can navigate to any of the other pages in the app. I suggest heading to the
      front page where a welcome message and a few useful links are listed out for you.

### Final Things

When a package version is loaded the app will first try to find it in its local cache. If
it cannot find a cache file it is forced to traul through the repository to locate the
package and read out its data.

This can cause the pages to run slowly and cause fairly heavy disk IO. If this is a problem
you can trigger the app to try and cache all of its apps in one go.

Either make a request to the url: `http://localhost:5000/api/packages/preload` or click on
the menu option 'Reload Cache' under the cog item in the menu.

<center>![](https://raw.github.com/baseblack/ReproWeb/master/documentation/images/image_04.png)</center>

