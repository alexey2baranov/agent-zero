# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# Activate the virtual environment
source /opt/venv/bin/activate

# Activate ACI
# source /root/commands/defaults.sh # replaced by Python ACI
# source /root/commands/edit_linting.sh # replaced by Python ACI
# source /root/commands/env.sh # replaced by Python ACI
source /root/commands/search.sh

# Make Python ACI is available
export PATH="/root/aci:$PATH"
