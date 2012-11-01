# ReproWeb <small>a _micro_ repository browser</small>

## Getting Started

Reproweb is designed to provide insight into your self hosted apt repository. It is built on top of the standard debian dpkg toolchain and the repository builder/mirroror [reprepro](http://mirrorer.alioth.debian.org/).

If any packages are taking a long time to load go the __COG__ icon and select the __'Reload Cache'__ menu option.


### Browse

> Do you find yourself wanting to know more about your repository? Perhaps how many packages are in a particular component? or perhaps you don't know the structure of your repository and you want to get to know it more intimately?

For you there is the [browser](/api/repository/) view. This view allows you to descend through a repository,  following each branch and leaf.

<center>![](https://raw.github.com/baseblack/ReproWeb/master/documentation/images/image_07.png)</center>

The structure will typicially lead you to a filtered packages view only displaying the packages which match the distribution, component and architecture you have selected.

<center>![](https://raw.github.com/baseblack/ReproWeb/master/documentation/images/image_08.png)</center>

And don't worry about keeping track of where the package or version you have found is currently residing. The menu at the top of the window will always keep track of your current position for you.

### Search

> Do you have a specific package you are looking for? Do you know it's name or version and don't want to have to go browsing around for it?

If this is you, then select [Search](/api/packages/) in the menu. This will load the package view. Here all of the packages for all of the distributions, components and architectures in the repository are listed.

<center>![](https://raw.github.com/baseblack/ReproWeb/master/documentation/images/image_05.png)</center>

The list is pagenated, sortable and searchable. To find the package you are looking for type part of its name into the search box. The package list will be filtered down to only show matching packages.

<center>![](https://raw.github.com/baseblack/ReproWeb/master/documentation/images/image_06.png)</center>



