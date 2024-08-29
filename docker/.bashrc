# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# Activate the virtual environment
source /opt/venv/bin/activate

# Activate ACI
source /root/commands/defaults.sh
source /root/commands/search.sh
source /root/commands/edit_linting.sh
source /root/commands/env.sh
source /root/commands/_split_strings.sh
