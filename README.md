# piPod - One Button Audio Player #
##  by itcarsales  ##

This program currently supports the GPIO of the Raspberry Pi B+

It can be modified for all versions by changing the wiring and the 2 I/O lines of code, but future versions will include support and documentation for all pi versions.

![board-thumb.jpg](https://github.com/itcarsales/piPod/blob/master/board-thumb.jpg?raw=true) 

- - - -

### Install ###
This has been tested on most versions of Raspbian, but the 'Lite' versions boot faster and use far fewer resources.  If you are building something to use, I would stick to Jessie Lite.  If you are just building this as a project, almost any version of Raspbian or even Ubuntu will work.

Start from the SSH Terminal of a Fresh Install
Issue the following commands 1 line at a time - copy and paste exactly:

`sudo apt-get install mpd`

`sudo apt-get install mpc`

`sudo apt-get install python-mpd`

`sudo apt-get install python-pyudev`

`sudo mkdir -p /music/usb`

`sudo ln -s /var/lib/mpd /music/mpd`

`sudo ln -s /var/lib/mpd/music /music/mp3`

`nano /home/pi/pipod.py`

Now paste in the code exactly from pipod.py - then press Ctrl + x following the prompts to exit Nano and save.
Now were are going to test it out:

`sudo python /home/pi/pipod.py`

Format USB Stick with name 'MEDIA' and add a few mp3 files
Insert USB stick into the Raspberry Pi
**Some Pi's will reboot upon a usb insertion due to an influx of current.  If this is the case, simply boot the Pi with the USB Drive already inserted.  
Unplug the USB Stick once the LED starts flashing every second.
-Press the button to start or stop playing
-While playing, Hold the button for longer than 2 seconds to skip to the next track
-While playing, Hold the button for longer than 4 seconds to skip to the previous track

Do the following to run at startup:

`sudo crontab -e`
 
(It may ask you to select an Editior, if so - select nano which is option 2)

`@reboot python /home/pi/pipod.py &`

 //press Ctrl + x to exit and save following the prompts

`sudo reboot`

### Install Resources ###

* [Writing Images to SD Card](https://www.raspberrypi.org/documentation/installation/installing-images/windows.md)
* [Rasbian Jessie Lite](https://www.raspberrypi.org/downloads/raspbian/)
* [NOOBS](https://www.raspberrypi.org/downloads/noobs/)

### Support ###

* [Support Board](https://www.reddit.com/r/pipod/)
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)
* [Download Project Zip](https://bitbucket.org/itcarsales/pipod/get/ea68dfa67319.zip)
