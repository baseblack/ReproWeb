## Glossary

To help Paul keep ontop of all this new found _jargon_ here is a simple terms of reference.

### A 

*   #### Architecture

    Specifies the hardware architecture which the software package is capable of
    running on. Examples of this are `amd64`, `i386` and `all`.

### B

*   #### Basedir

    Base directory of the managed repository. The default settings for a reprepro/apt
    repository expect all other directories to be found relative to this path.

    >For example; the /pool directory is expected to be located at $basedir/pool.

### C

*   #### Codename

    A repository can contain any number of distributions. For example `lucid`, 
    `precise`, `quantal`. Each of these distributions is identifed by their _Codename_.

*   #### Component

    Packages are grouped within a distribtion/codename into Components. Under the 
    offical ubuntu repositories there are 4. 

    >**Main** - Officially supported software.

    >**Restricted** - Supported software that is not available under a completely free
                      license.

    >**Universe** - Community maintained software, i.e. not officially supported
                    software.

    >**Multiverse** - Software that is not free. 

*   #### Confdir
   
    Directory which houses the configuration files for the managed repository. 
    Files found in this directory include `options`, and `distributions`. 

    See the reprepro [documentation](http://mirrorer.alioth.debian.org/) for details.

### D

*   #### Deb File

    Debian software package file. The software is stored within the package alongside 
    control and pre/post installation/removal scripts.

    The debs may be downloaded and locally installed using `dpkg -i $debfile`.

*   #### Distdir

    Directory which houses the Releases files for distributions contained in the 
    repository. These directories/files are managed by reprepro.

    See the reprepro [documentation](http://mirrorer.alioth.debian.org/) for details.    

*   #### Distribution

    A repository can contain any number of distributions. For example `lucid`, 
    `precise`, `quantal`. Each of these distributions is identifed by their _Codename_.

*   #### Dump References

    A [reprepro](http://mirrorer.alioth.debian.org/) action. Causes reprepro to dump a 
    list of each of the currently referenced packages within the repository.

    If the Codename/Component for a package has been deleted then the package will no 
    longer be referenced and so will not be listed. Old versions of a package (assuming 
    these are not being deleted will also not be listed.

### E
### F
### G
### H
### I
### J
### K
### L
### M

*   #### Maintainer

    Each package deb when it is added to the repository should have specifed who the 
    package author/maintainer is. This person/team is responsible for updates and code
    fixes required to the software contained in the package.

### N
### O

*   #### Outdir

    Sets  the base-dir of the repository to manage, i.e. where the pool/ subdirectory 
    resides. And in which the dists/ directory is placed by default.  If

### P

*   #### Package

    Stored file, with manually injected or downloaded from another repository into the 
    pool/ hierarchy. 

### Q
### R

*   #### Repository

    A repository is an organised software archive. Each repository may be organized 
    into a number of discreet distributions. These are refered to by their Codenames.
    
    Each distribution is futher organised into separate areas which contain software
    of different types/roles. For example, supported and unsupported software.

    A reprepro managed repository is a disk based file hierarchy which uses a berkley 
    db to track its state. 

*   #### Reprepro

    Reprepro (formerly having the working title mirrorer) is a tool to handle local 
    repositories of debian packages.

    * local addition of files or automatically getting them from some remote repository
    * files are stored in a pool/-hirachy
    * Uses Berkeley libdb, so no database-server is need, but information is stored in    
      local files

### S
### T
### U
### V

*   #### Version

    Each package may only have 1 version of itself stored within a distribtion at a 
    time. When a package file is injected into the repository it's version is checked  
    against the currently referenced version. If they are the same the new file is 
    rejected. If the new file's version is greater than the existing version then the
    old package file is unreferenced and the new one added to the pool/.

### W
### X
### Y
### Z





