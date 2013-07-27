*******
replmon
*******

Replmon is a simple MySQL replication monitor.

-----
Usage
-----

First, configure ``/etc/replmon.ini``:

.. code-block:: ini

    [mysql]
    user =   MySQL Username
    passwd = MySQL Password
    host =   MySQL Host (leave empty for local unix socket)
    port =   MySQL Port (leave empty for default port)


Next, launch replmon:

.. code-block:: bash

    $ replmon


Replmon is meant to integrate with tools such as monit. See ``./examples``.

------
Output
------

Replmon will periodically check your MySQL replication status. Each time a check succeeds, Replmon will ``touch``
the ``/var/replmon.status`` file, so you can monitor changes to this file to know your status.

The check interval is by default 10 seconds.

-------
License
-------

See ``LICENSE``.
