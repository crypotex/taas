Raspberry pi guidelines
=======================

Setup before booting
--------------------

- Download Raspbian Jessie and unzip it:

.. code-block:: bash

    https://www.raspberrypi.org/downloads/raspbian/

- Format your SD card, you can use SD Formatter 4.0

.. code-block:: bash

    https://www.sdcard.org/downloads/formatter_4/

- Copy .iso file to SD card, you can use Win32DiskImager

.. code-block:: bash

    http://sourceforge.net/projects/win32diskimager/

- Insert SD card into Raspberry Pi and boot it


Changing Raspberry Pi configuration
-----------------------------------

- Open the terminal and type in command

.. code-block:: bash

    sudo raspi-config

- Expand the filesystem by choosing "Expand Filesystem". After it has finished changing the partitions, choose "Okay".

* Change user password by choosing "Change User Password". It asks the user to enter new password twice. After entering them, the user's password should now be changed.

- Change the locale by choosing "Internationalisation Options". Then choose "Change Locale". A list of available locales is displayed and you can now choose desired locales. After you have finished choosing, hit "Enter".

.. code-block:: bash

    en_GB.UTF-8 UTF-8
    et_EE.UTF-8 UTF-8

* Change the timezone by choosing "Internationalisation Options". Then choose "Change Timezone". Choose "Europe" and then choose "Helsinki".

- Change the keyboard language by choosing "Internationalisation Options". Then choose "Change Keyboard Layout". A list of models of the keyboard are displayed and choose "Generic 105-key (Intl) PC". Then choose "Estonian" and hit "Enter". After that choose "Default" and then "No multi_key". Then choose "Yes" on the "Control"+Alt+Backspace to kill a server".

* Change the hostname of Raspberry Pi by choosing "Advanced Options" and on the next list choose "Hostname". Hit "Okay" and enter you desired hostname.

- Enable SSH server by choosing "Advanced Options". Then choose "SSH" and hit "Enable".

* Then reboot your Raspberry Pi by choosing "Finish" and then choose "Yes" when asked for reboot.

- After your Raspberry Pi has rebooted, run the following command to update

.. code-block:: bash

    sudo apt-get update


Generating SSH keys
-------------------

* To generate SSH keys, type in the command

.. code-block:: bash

    ssh-keygen -t rsa -b 2048

- When the terminal asks where the save the file for the key, hit "Enter".

*  Then enter your password twice.

- To add your public key to authorized keys, run the following command

.. code-block:: bash

    cat /home/pi/.ssh/id_rsa.pub >> /home/pi/.ssh/authorized_keys

Replication MySQL - Raspberry Pi
--------------------------------

* Follow the `DigitalOcean <https://www.digitalocean.com/community/tutorials/how-to-set-up-master-slave-replication-in-mysql>`_ guide on how to setup MySQL replication. You can find ip-addresses with command "ifconfig". Also don't forget to open port 3306 on main server. 

Python gate controller
----------------------

* Link for files
