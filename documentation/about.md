## Background

At Baseblack we manage how we install and update the software and tools on our workstations, rendernodes and servers (physical+virtual) using a combination of [Apt](http://wiki.debian.org/Apt) _(which handles software installation, versioning and file collisions)_ and [Puppet](http://puppetlabs.com) _(which handles configuration and selection of packages for apt to install)_.

Our primary apt repository now has around 450 packages origanized into a number of distributions, components and architectures. And as with any repository that number is ever increasing.

As we add more distributions into the primary repository, merge repositories together and start auto-generating packages off of code commits, that number begins to become frighteningly large.

We needed to find something to help us view/manage our repository.

### Alternatives

In the interests of due diligence we looked at the currently available solutions for handling apt repositories.

1.  [packages.debian.org](http://packages.debian.org)
    
    After checking out the source for the pretty fantastic offical debian repository 
    browser site we decided against using it.

    This came down to a few factors. The primary one is that it's written in bash/perl 
    neither of which we were too keen on having to edit to add any additional features 
    we might want in the future.

    Secondary is the static generation of the site. We wanted to have real-time access 
    into the repository, without the need for cronjobs and offline processing.

1.  [RepoDepo](http://sourceforge.net/projects/repodepo/)

    This is a webapp which makes it fairly easy to ingest from one repository into another.
    Using a waterfall method you can use it to move packages from testing -> production
    through a series of stages. 

    Again we chose not to persue it, primarily due to the general pain levels involved in
    anything PHP related.

1.  [Repoman](https://github.com/synack/repoman) 

    Repoman provides a RESTful client/server interface for managing Debian repositories and 
    building packages. Which is great, but still fairly limited in scope, and didn't provide
    us with a gui. 

    Since this was something which we would need to write ourselves, we chose not to go with
    repoman.

## Enter Lukas

Using our background research and our production requirements we decided to try and build a web
app ourselves. We gave ourselves 7 days and Lukas is the product.

**_Lukas is a pet name used for the project and does not reflect any real persona._**