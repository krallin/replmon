replmon
=======

Replmon is a simple MySQL replication monitor.

Usage
=====

First, configure `/etc/replmon.ini`:

    [mysql]
    user =   MySQL Username
    passwd = MySQL Password
    host =   MySQL Host (leave empty for local unix socket)
    port =   MySQL Port (leave empty for default port)


Next, launch replmon:

    $ replmon


Output
======

`replmon` will periodically check your MySQL replication status. Each time a check succeeds, Replmon will `touch`
the `/var/replmon.status` file, so you can monitor changes to this file to know your status.
