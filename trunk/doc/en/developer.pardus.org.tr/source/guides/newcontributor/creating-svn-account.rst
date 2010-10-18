.. _creating-svn-account:

Creating SVN Crypt Password
===========================

To create an SVN password you should specify a user name. This user name must not include abusive or any malicious words. The username should not be offensive, discriminatory, or derogatory.

Creating a password with "htpasswd"
-----------------------------------
You can create your password and username by using htpasswd and you can attach the output file to your e-mail. To do this, you can use the command below:

::

    $ htpasswd -c password_file user_name
    New password:
    Re-type new password:
    Adding password for user user_name 

As a result an output file (password_file) will be created and you can attach it to your e-mail.

Creating A Password With Perl
-----------------------------

To do this the, you can use the command below:
::

  perl -e "print crypt('yourpassword','xy'),\"\n\";"2 

This command will create just your password. In your e-mail you should mention the username you want to use.

Creating A Password With Python
-------------------------------

You can do the same with python by using the command below:
::

  python -c "import crypt; print crypt.crypt('password', 'xy')" 

In this case as well, just the shadowed form of your password will be given as output. In your e-mail you should mention the username you want to use. 


**Last Modified Date:** |today|

:Author: Semen Cirit
