## Run

Copy and edit `config.py.dist`: `cp config.py.dist config.py`

Then launch the app with `sudo python3 main.py &`

## Installation

Get an rasbian image from [here](https://www.raspberrypi.org/downloads/raspbian/).

Connect to the pi then `sudo apt-get update && sudo apt-get upgrade && sudo reboot`.

Enlarge partition, set up time zone and enable the camera with `sudo raspi-config`.

To be continued.

To start the alarm at boot edit the DIR variable in `scripts/alarm.sh` then:

```
sudo su -
ln -s /path/to/scripts/alarm.sh /etc/init.d/alarm
chmod +rx /etc/init.d/alarm
echo "sudo service alarm start" >> /etc/rc.local
```

## Documentation

#### 06/09/15

* https://www.raspberrypi.org/documentation/usage/gpio/
* http://www.element14.com/community/docs/DOC-73950/l/raspberry-pi-2-model-b-gpio-40-pin-block-pinout
* https://www.jameco.com/Jameco/workshop/circuitnotes/raspberry_pi_circuit_note.html
* https://www.google.fr/imgres?imgurl=http%3A%2F%2Fraspi.tv%2Fwp-content%2Fuploads%2F2013%2F03%2FRasPi.TV-interrupt3_bb.jpg&imgrefurl=http%3A%2F%2Fraspi.tv%2F2013%2Fhow-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3&h=1047&w=1266&tbnid=_PkyDC_QtPJU1M%3A&docid=rCBqrqjXg7Hs6M&ei=MUDpVefcGoOAaYTfqZgF&tbm=isch&client=ubuntu&iact=rc&uact=3&dur=663&page=1&start=0&ndsp=47&ved=0CHoQrQMwHGoVChMIp7mJ_uXcxwIVA0AaCh2EbwpT
* https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md
* https://www.raspberrypi.org/documentation/usage/camera/python/README.md
* https://picamera.readthedocs.org/en/release-1.10/recipes1.html#capturing-timelapse-sequences
* https://learn.adafruit.com/adafruits-raspberry-pi-lesson-12-sensing-movement/configure-and-test
* https://learn.adafruit.com/pir-passive-infrared-proximity-motion-sensor/
* https://learn.adafruit.com/adafruits-raspberry-pi-lesson-12-sensing-movement/hardware
* https://pip.pypa.io/en/latest/installing.html

#### 07/09/15

* https://www.google.fr/search?q=python+send+sms&oq=python+send+sms&aqs=chrome..69i57.4279j0j7&client=ubuntu&sourceid=chrome&es_sm=93&ie=UTF-8
* https://www.twilio.com/docs/quickstart/python/sms/sending-via-rest
* https://www.twilio.com/user/account/voice-sms-mms
* http://the-raspberry.com/connaitre-la-temperature-de-son-raspberry-pi

#### 08/09/15

* http://www.raspberrypi-spy.co.uk/2013/07/running-a-python-script-at-boot-using-cron/*
* https://www.raspberrypi.org/documentation/linux/usage/rc-local.md
* https://docs.python.org/2/library/logging.html#logging.Logger.debug
* https://docs.python.org/3.2/howto/logging.html
* http://www.webupd8.org/2014/09/gdrive-simple-google-drive-cli-client.html
* https://docs.python.org/3.2/library/subprocess.html

#### 09/09/15

* https://docs.python.org/3.2/library/threading.html#thread-objects

#### 12/09/15

* http://docs.python-requests.org/en/latest/user/quickstart/#more-complicated-post-requests
* http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/

#### 24/09/15

* https://stackoverflow.com/questions/20478516/how-to-detect-when-networking-initialized-in-etc-init-d-script*

#### 28/09/15

* http://www.instructables.com/id/Raspberry-Pi-Bluetooth-InOut-Board-or-Whos-Hom/?ALLSTEPS
* https://github.com/karulis/pybluez
* https://stackoverflow.com/questions/21597536/pybluez-installation-in-linux

#### 29/09/15

* https://stackoverflow.com/questions/12229580/python-importing-a-sub-package-or-sub-module
* https://docs.python.org/3.2/reference/datamodel.html

#### 03/10/15

* https://www.pi-supply.com/bright-pi-v1-0-assembly-instructions/

#### 04/10/15

* https://www.pi-supply.com/bright-pi-v1-0-code-examples/
* http://www.raspberry-projects.com/pi/pi-operating-systems/raspbian/io-pins-raspbian/i2c-pins
* https://brightpi.codeplex.com/SourceControl/latest#test1.py

#### 05/10/15

* https://raspberrypi.stackexchange.com/questions/27073/firmware-3-18-x-breaks-i%C2%B2c-spi-audio-lirc-1-wire-e-g-dev-i2c-1-no-such-f
* http://pi.gadgetoid.com/pinout

#### Next Step

* https://learn.adafruit.com/shake-up-a-gift-box/circuit-diagram
* https://learn.adafruit.com/introducing-trinket
* https://learn.adafruit.com/trinket-bluetooth-alarm-system/overview

#### 22/03/16

* https://docs.python.org/3.2/library/logging.handlers.html
* https://docs.python.org/3.2/howto/logging.html

#### 31/03/16

* http://bohdan-danishevsky.blogspot.fr/2015/10/building-python-35-on-raspberry-pi-2.html
* https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=99980#p696458
