# Tremolometer

## Install (Mac)

### Install compiler
```bash
$ brew tap ArmMbed/homebrew-formula
$ brew install arm-none-eabi-gcc
```

### Pull submodules
```bash
$ git submodule update --init --recursive
```

## Building microcontroller project
```bash
$ mkdir build
$ cd build
$ cmake ..
$ make
```

### Install python packages
```bash
$ pip install -r requirements.txt
```

## Running client
```bash
$ python3 client/client.py
```

## Generate Documentation
To generate the documentation install [Doxygen](https://www.doxygen.nl/download.html#srcbin).

When doxygen is installed run the following command to generate latex and HTML doc:
```bash
$ doxygen -u TremoloConf 
$ doxygen TremoloConf
```

The documentation will be generated in the folder `/doc`