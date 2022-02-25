# Tremolometer

## Install (Mac)

### Install compiler
```bash
brew tap ArmMbed/homebrew-formula
brew install arm-none-eabi-gcc
```

### Pull submodules
```bash
git submodule update --init --recursive
```

## Building microcontroller project
```
mkdir build
cd build
cmake ..
make
```

### Install python packages
```bash
pip install matplotlib
pip install pandas
pip install pyserial
```

## Running client
```bash
python3 client/client.py
```