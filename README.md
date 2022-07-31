# Torsional Pendulum (*Pohl's Wheel*)
A GUI front-end for undergraduate physics student at the [TU Berlin](https://www.tu.berlin) doing the torsional pendulum (*Pohl's Wheel*) experiment, written in Python using `DearPyGui` and asynchronous threading.

![GUI](/docs/screenshot-gui.png)

This is a reimplementation of the proprietary LabVIEW front-end, the source code of which has been lost.

## Installation
Install all required packages with pip using:
```
pip3 install -r requirements.txt
```

## Usage
This project is currently **work in progress**, as different functions — such as reading/writing from/to the Arduino — are not/partially implemented.

If you want to test the program anyway, simply run [main.py](/main.py) by calling:
```
python3 main.py
```

## License
Copyright © 2022 [Hüseyin Çelik](https://www.github.com/hueseyincelik).

This project is licensed under [AGPL v3](/LICENSE).
