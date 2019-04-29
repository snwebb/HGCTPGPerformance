#! /usr/bin/env bash

# setup Python 2.7 and ROOT 6


source /cvmfs/sft.cern.ch/lcg/contrib/gcc/4.9/x86_64-centos7/setup.sh
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.06.08/x86_64-centos7-gcc49-opt/root/bin/thisroot.sh


export PYPATH=/usr/bin

export PATH=${PYPATH}/root/usr/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=${PYPATH}/root/usr/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export MANPATH=${PYPATH}/root/usr/share/man:${MANPATH}
# For systemtap
export XDG_DATA_DIRS=${PYPATH}/root/usr/share:${XDG_DATA_DIRS:-/usr/local/share:/usr/share}
# For pkg-config
export PKG_CONFIG_PATH=${PYPATH}/root/usr/lib64/pkgconfig${PKG_CONFIG_PATH:+:${PKG_CONFIG_PATH}}




#source /opt/rh/python27/enable

#scl enable python27 bash

#which root
 # unset PYTHONPATH
 # export PYTHONPATH=:/lib
 # unset PYTHONHOME

# Install virtualenvwrapper package if not already installed
if [ ! -f ~/.local/bin/virtualenvwrapper.sh ]; then
  # deleting cached packages to force download
  rm -rf ~/.cache/pip/
  pip install --user -I virtualenvwrapper
fi

# Create virtual env and install dependencies
if [ ! -d ~/.virtualenvs/hgc_tpg/ ]; then
  mkdir -p ~/.virtualenvs/
  export WORKON_HOME=~/.virtualenvs
  export VIRTUALENVWRAPPER_PYTHON=`which python`
  export VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv
  source ~/.local/bin/virtualenvwrapper.sh
  mkvirtualenv hgc_tpg
  # deleting cached packages to force download
  rm -rf ~/.cache/pip/
  pip install -r requirements.txt -I
  pip install -e .
else
  export WORKON_HOME=~/.virtualenvs
  export VIRTUALENVWRAPPER_PYTHON=`which python`
  export VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv
  source ~/.local/bin/virtualenvwrapper.sh
  workon hgc_tpg
  # Check if all the package requirements are satisfied
  available_dep_count=$(pip freeze | grep -f requirements.txt | wc -l)
  needed_dep_count=$(cat requirements.txt | wc -l)
  if [ "$available_dep_count" != "$needed_dep_count" ]; then
    echo "Updating dependencies"
    # deleting cached packages to force download
    rm -rf ~/.cache/pip/
    pip install -r requirements.txt -I
  fi
fi
