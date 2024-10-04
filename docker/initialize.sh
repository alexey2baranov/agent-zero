#!/bin/bash

# Copy shell & Python ACI in the root directorys
cp -r /etc/skel/commands /root/commands
cp -r /etc/skel/aci /root/aci

# Ensure .bashrc is in the root directory
cp /etc/skel/.bashrc /root/.bashrc
chmod 444 /root/.bashrc

# Ensure .profile is in the root directory
cp /etc/skel/.bashrc /root/.profile
chmod 444 /root/.profile

# Start SSH service
exec /usr/sbin/sshd -D