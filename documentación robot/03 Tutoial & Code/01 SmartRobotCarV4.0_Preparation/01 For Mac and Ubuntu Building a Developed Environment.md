# 01 For Mac and Ubuntu Building a Developed Environment

---

1

Arduino IDE
As an open source software, Arduino IDE, based on going Processing IDE
development is an integrated development environment oﬃcially launched
by Arduino.

By using arduino IDE, you just write the program code in the IDE and upload
it to the Arduino circuit board. The program will tell the Arduino circuit board
what to do.

So, Where can we download Arduino IDE?

Uplaod program for MacOS

STEP 1:
Download the Arduino Software (IDE) Open the
URL:https://www.arduino.cc/en/Main/Software with browser.
Click“Mac OSX 10.8 Lion or newer”.
The version available at this website is usually the latest version, and the
actual version may be newer than the version in the picture.

STEP 2:
Click“JUST DOWNLOAD”.

STEP 3:
Open Finder.

STEP 4:
After the download is complete, an installation package will appear in the
download directory.

At this time, the Arduino development environment has been successfully
built!

Uplaod program for Ubuntu
STEP 1：
Go to https://www.arduino.cc/en/Main/Software and you will see the
below page.

The version available at this website is usually the latest version, and the
actual version maybe newer than the version in the picture.

STEP 2：
Click“JUST DOWNLOAD”.

STEP 3：
Check that the download was successful.

STEP 4：
Press“CTRL + ALT + T”at the same time to open the command.

STEP 5：
Enter“cd Downloads/”.

STEP 6：
Enter“tar xvjf arduino-1.8.12-linux64.tar.xz”to unzip the ﬁles.

STEP 7：
Enter“sudo mv arduini-1.8.12 /opt”to move the unzipped ﬁles to the
“opt”folder.

STEP 8：
Enter“cd /opt/arduino-1.8.12/”to go to the arduino folder.

STEP 9：
Enter“sudo chmod +x install.sh”and“sudo chmod +x install.sh”to complete
the installation.

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


