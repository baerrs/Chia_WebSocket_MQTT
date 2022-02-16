#!/bin/bash
set -e
UBUNTU=false
DEBIAN=false
if [ "$(uname)" = "Linux" ]; then
	#LINUX=1
	if type apt-get; then
		OS_ID=$(lsb_release -is)
		if [ "$OS_ID" = "Debian" ]; then
			DEBIAN=true
		else
			UBUNTU=true
		fi
	fi
fi

# Get submodules
# git submodule update --init mozilla-ca

find_python() {
	set +e
	unset BEST_VERSION
	for V in 39 3.9 38 3.8 37 3.7 3; do
		if which python$V >/dev/null; then
			if [ "$BEST_VERSION" = "" ]; then
				BEST_VERSION=$V
			fi
		fi
	done
	echo $BEST_VERSION
	set -e
}

if [ "$INSTALL_PYTHON_VERSION" = "" ]; then
	INSTALL_PYTHON_VERSION=$(find_python)
fi

# This fancy syntax sets INSTALL_PYTHON_PATH to "python3.7", unless
# INSTALL_PYTHON_VERSION is defined.
# If INSTALL_PYTHON_VERSION equals 3.8, then INSTALL_PYTHON_PATH becomes python3.8

INSTALL_PYTHON_PATH=python${INSTALL_PYTHON_VERSION:-3.7}

echo "Python version is $INSTALL_PYTHON_VERSION"
$INSTALL_PYTHON_PATH -m venv venv
if [ ! -f "activate" ]; then
	ln -s venv/bin/activate .
fi

. ./activate

python -m pip install --upgrade pip
python -m pip install wheel
#if [ "$INSTALL_PYTHON_VERSION" = "3.8" ]; then
# This remains in case there is a diversion of binary wheels

pip install -r requirements.txt

deactivate
cp -r ~/.chia/mainnet/config/ssl/ ssl

echo ""
echo "Chia API-WebSocket -> MQTT install.sh complete."
echo ""
echo "Type '. ./activate' and then 'python main.py' to begin."

