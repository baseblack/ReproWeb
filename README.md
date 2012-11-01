# PyReproWeb <small>a _micro_ repository browser</small>

## Features

### Browse

> Do you find yourself wanting to know more about your repository? Perhaps how many packages are in a particular component? or perhaps you don't know the structure of your repository and you want to get to know it more intimately?

For you there is the [browser](/api/repository/) view. This view allows you to descend through a repository,  following each branch and leaf. 

<center>![](./images/image_07.png)</center>

The structure will typicially lead you to a filtered packages view only displaying the packages which match the distribution, component and architecture you have selected.

<center>![](./images/image_08.png)</center>

And don't worry about keeping track of where the package or version you have found is currently residing. The menu at the top of the window will always keep track of your current position for you.

### Search

> Do you have a specific package you are looking for? Do you know it's name or version and don't want to have to go browsing around for it?

If this is you, then select [Search](/api/packages/) in the menu. This will load the package view. Here all of the packages for all of the distributions, components and architectures in the repository are listed. 

<center>![](./images/image_05.png)</center>

The list is pagenated, sortable and searchable. To find the package you are looking for type part of its name into the search box. The package list will be filtered down to only show matching packages.

<center>![](./images/image_06.png)</center>

## Upcoming

### Soon

* JSON response on all endpoints.
* Graceful shutdown

### Later (maybe)

* Repository management.
    * See repoman.sourceforge.net or packages.debian.org for examples of where this can go.

## Requirements

This app was developed on Ubuntu 10.04 and required several python packages which are either not included in the base distribution, or are now out of date.

`3rdParty/python` contains several packages which are neccassary for the app to run.

1. [Flask](http://flask.pocoo.org/docs/) - the web framework used to build the app.
1. [Jinja2](http://jinja.pocoo.org/docs/) - templating framework used to build the 
                                            pages.
1. [wekzeug](http://werkzeug.pocoo.org/) - wsgi utility library used by flask.
1. [OrderedDict](http://docs.python.org/2/library/collections.html#collections.OrderedDict) -
   The ordered dictionary python type taken from python 2.7 .
1. [Reepocheep](http://github.com/andrewbunday/repocheep) - A python module which
   wraps reprepro, dpkg-deb and several other package utilities.

## Setup

### Installation

1.    Download the latest tarball out of github from 
      [here](https://github.com/andrewbunday/reproweb/tarball/master). Extract it into the 
      location you want to run your install from. 
      
      The bundle consists of:
      * reproweb/ - a flask based webapp
      * 3rdParty/ - dependencies required by the webapp (flask/werkzerg/orderddict/jinja2/fawps3)
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

1.    If you choose to use fapws3 and are running on a system which is newer than 

1.    Open up a web browser navigating to the localhost, or whatever server you are using.

       <center>![](./images/image_01.png)</center>

1.    When the app runs for the first time it will try to load its settings from disk. 
      The settings are saved in a json file which holds a serialized version of the 
      default configuration as well as any additional settings we add to the app or 
      which are generated during setup.

      If the app cannot load the settings, because the file doesn't exist it will redirect 
      straight to the settings page __http://localhost:5000/settings__:

      <center>![](./images/image_02.png)</center>

      The input fields marked with stars are required for the app to run. If the settings 
      file is not set you will keep being redirect to the settings page and if the Base 
      directory is not set Reproweb has no way of knowing which repository it should be 
      looking at.

1.    Click on the Save button and if the settings have been stored a green success 
      message will be displayed.

      <center>![](./images/image_03.png)</center>

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

<center>![](./images/image_04.png)</center>


