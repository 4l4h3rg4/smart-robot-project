# 01 For Windows Setting up development environment

---

1

Arduino IDE
As an open source software,Arduino IDE, based on ongoing Processing
IDE development is an integrated development environment oﬃcially
launched by Arduino.

By using Arduino IDE, you just write the program code in the IDE and upload
itto the Arduino circuit board. The program will tell the Arduino circuit board
what to do.

So,Where can we download Arduino IDE?

STEP 1:
Go to https://www.arduino.cc/en/Main/Software and you will see the
following page.
The version available at this website is usually the latest version, and the
actual version may be newer than the version in the picture.

STEP 2:
Download the development sofaware that is suited for the operating system
of your computer.
Take Windows as an example here.
If you are MacOS, please open 01 For Mac and Ubuntu Building a Developed
Environment.
You can install it using the EXE installation package or the green package.
The following is the exe implementation of the installation procedures.
Press the option“Windows Installer”.

STEP 3:
Pressthe button“JUST DOWNLOAD”to download the software.

The download ﬁle:

STEP 4：
These are available in the materials we provide, and the versions of our
materials are the latest versions when this course was made.
Choose "I Agree" to see the following interface.
Choose "Next" to see the following interface.
Press "Install" to initiate installation.

Finally,the following interface appears, you should choose Install to
ensure the correct installation.
The installation is required to work with the UNO board. If you don't install
the software, the computer would not be able to talk to the board.

STEP 5：
Next,the following icon appears on the desktop.

Double-click to enter the desired development environment.
① veriﬁcation
② upload

③ new ﬁle
④ open
⑤ save

⑥ serial monitor

⑦ code writing area
⑧ information bar

STEP 6：
Connect development board to the computer.

STEP 7：
Open the Arduino IDE. Select“ Tool ”→“Board ”→“Arduino/Genuino Uno ”.
Select“ Tool ”→“ Port ”→“COM (Arduino/Genuino Uno) ”.

Each Arduino Uno board has a diﬀerent COM number on the same computer
and usually the COM number is associated with a suﬃx
name“(Arduino/Genuino Uno)”in Arduino 1.8.9. You should choose the COM
number that is shown.
if your computer'sOS iswin7, you should download the
usbbridgesetup_ ca_WIN7 on our
website: http://www.elegoo.com/download/
unzipthe zipﬁle,running the installer"USBBridgeSetup_CA

If you see the COM port , your automatic installation is complete and
working, go to Step 9.

Otherwise, you need to install the driverin the following way manually.

The controller board on the robot car does not need to install the driver
software on Windows 10, Linux, and macOS operatingsystems. If you can not
ﬁnd the robot car device on the device manager, please use another USB
cable and connect the robot car to another USB port. Please connect the
robot car to other computers to make sure this is not a computer issue.
STEP 8：
Open Device Manager by right clicking
My Computer⸺Management⸺Device Manager.

Right click unknown device --Update Driver Software.

It shows that the driver has not been installed, and you need to click Browse
my computer for driver software to ﬁnd the drivers. The driver is in the
Arduino folder.Normally you will install the folder

in C:\Program Files (x86)\Arduino.

Arduino install folder.

Selectthe Arduino driverfolder.

Install Arduino USBdevice.

STEP 9：
After the driver is installed,please open the IDE and then click
“ Tools ”→“Board ”→“Arduino/Genuino Uno ”.

And then Select“ Tool ”→“ Select ”→“ Tool ”→“ Port: ”→“COM”.

Each Arduino Uno board has a diﬀerent COM number on the same
computerin Arduino 1.8.9. You should choose the COM number that is shown.
At this time, the Arduino development environment has been successfully
built !

STEP 10：
In this step, I will show you how to upload program to the UNO controller
board.

Open the code ﬁle in the directory "\02 Manual & Main Code & APP\
SmartRobotCarV4.0\SmartRobotCarV4.0.ino" and click“upload”button to
upload the code to the UNO controller board.

Tips: Please toggle the button on the robot car to“Upload”when uploading
the program and toggle to“Cam”when using the app.

The picture below shows that the program is uploaded successfully.

At this time, the Arduino development environment has been successfully
built.

http://www.elegoo.com


