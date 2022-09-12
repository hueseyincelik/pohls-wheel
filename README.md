# Torsional Pendulum (*Pohl's Wheel*)
A GUI front-end for undergraduate physics student at the [TU Berlin](https://www.tu.berlin) doing the torsional pendulum (*Pohl's Wheel*) experiment, written in Python using `DearPyGui` and asynchronous threading.

![GUI](/docs/screenshot-gui.png)

This is a reimplementation of the proprietary [LabVIEW front-end](/docs/labview-gui.png), the source code of which has been lost.

## Installation
Install all required packages with pip using:
```
pip3 install -r requirements.txt
```
The current experimental setups require the source files to be in the home directory, which can be achieved by running the following commands in the terminal:
```bash
git clone https://www.github.com/hueseyincelik/pohls-wheel.git
mv pohls-wheel/src/ pohls-wheel/fonts/ pohls-wheel/main.py $HOME/
rm -rf pohls-wheel/ # optional deletion of leftover files
```

## Usage
The program can be started by simply running [main.py](/main.py):
```
python3 main.py
```

## License
Copyright © 2022 [Hüseyin Çelik](https://www.github.com/hueseyincelik).

This project is licensed under [AGPL v3](/LICENSE).