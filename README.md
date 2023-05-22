# self2023_iot
SELF 2023, IOT, MQTT, Raspberry PI, ESP32

## Raspberry PI Machine

- Hardware
    - Raspberry PI-4B 8GB
    - SanDisk Extreme Pro microSDHC UHS-I Card, 32 GB

- Operating System
    - Raspbian GNU/Linux 11 (bullseye) 32-bit Edition

- Software
    - MS Visual Studio Code
        - Installs using Recommended Software ![](./images/Screenshot-from%202023-05-22-11-48-34.png)
    - gnome-screenshot
        - sudo apt install gnome-screenshot
    - git was preinstalled on Raspberry PI OS Rasbian 11

## Git Setup

- [Add SSH Key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

- git config --global user.email "you@example.com"
- git config --global user.name "Your Name"


## Repo

- I have created a Github repo for this talk.
    - [Self 2023 IoT](https://github.com/datajango/self2023_iot)

- Add SSH keys for git

- git clone git@github.com:datajango/self2023_iot.git

## Mosquitto Setup

1. Update your package list: First, it's always a good idea to update your package list before installing any new software. This ensures that you'll get the latest available version. You can update your package list with the following command:

```
sudo apt update
```

1. Install Mosquitto: You can install the Mosquitto broker with the following command:
```
sudo apt install -y mosquitto mosquitto-clients
```

1. Start and enable Mosquitto service: You'll want to configure Mosquitto to start on boot. You can do this with the following commands:

```
sudo systemctl enable mosquitto.service
sudo systemctl start mosquitto.service
```

1. Test the broker: To test if your broker is working, you can subscribe to a topic in one terminal window, and then publish to that topic in another terminal window. Here are the commands you can use to do that:

In one terminal window, enter:
```
mosquitto_sub -h localhost -t "test/topic"
```
And in another terminal window, enter:
```
mosquitto_pub -h localhost -t "test/topic" -m "Hello, World!"
```
You should see Hello, World! printed in the first terminal window. This means that the broker is successfully relaying messages between the publisher and subscriber.

## Setup Python

1. Create the virtual environment. You do this with the python3 -m venv command, followed by the name of the virtual environment. 
```bash
python3 -m venv .venv
```
1. Activate the virtual environment. 
```bash
source .venv/bin/activate
```
1. You can use the pip install -r command to install all the packages listed in the requirements file. For example:
```bash
pip install -r requirements.txt
```
