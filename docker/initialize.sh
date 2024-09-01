#!/bin/bash

# Ensure .bashrc is in the root directory
if [ ! -f /root/.bashrc ]; then
    cp /etc/skel/.bashrc /root/.bashrc
    chmod 444 /root/.bashrc
fi

# Ensure .profile is in the root directory
if [ ! -f /root/.profile ]; then
    cp /etc/skel/.bashrc /root/.profile
    chmod 444 /root/.profile
fi

# Ensure ACI is in the root directorys
cp -r /etc/skel/commands /root/commands

# Enshure ACI _split_string.py is available
if [ ! -f /usr/local/bin/_split_string ]; then
    mkdir -p /usr/local/bin
    ln -s /root/commands/_split_string.py /usr/local/bin/_split_string
    chmod +x /usr/local/bin/_split_string
fi

apt-get update

# Start SSH service
exec /usr/sbin/sshd -D
