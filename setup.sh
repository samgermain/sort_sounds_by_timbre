function check_installed_pip() {
   python3 -m pip > /dev/null
   if [ $? -ne 0 ]; then
        echo_block "Installing Pip"
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
        rm get-pip.py
   fi
}

if [ -n "${VIRTUAL_ENV}" ]; then
    echo "Please deactivate your virtual environment before running setup.sh."
    echo "You can do this by running 'deactivate'."
    exit 2
fi

if [ -d ".env" ]; then
    echo "- Deleting your previous virtual env"
    rm -rf .env
fi

echo

python3 -m venv .env
if [ $? -ne 0 ]; then
    echo "Could not create virtual environment. Leaving now"
    exit 1
fi

source .env/bin/activate

check_installed_pip
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade -r requirements.txt

echo "Installation complete. Run 'source .env/bin/activate; python3 ./src/main.py' to use"