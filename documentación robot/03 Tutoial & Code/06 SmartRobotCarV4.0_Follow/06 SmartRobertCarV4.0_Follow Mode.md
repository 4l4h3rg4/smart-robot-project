# 06 SmartRobertCarV4.0_Follow Mode

---

6

Introduction:
In this lesson, we will teach you how to achieve the Follow Mode of the
Smart Robot Car and make it follow the target to move forward.

Preparation:

A Smart Robot Car (with battery)
A USB Wire
The realization of Smart Robot Car’s Follow Mode is also uses the
ultrasonic module, but it is slightly diﬀerent from the usage of
Obstacles-avoidance Mode.

Let’s take a look at the overall framework of the implementation principle
of the Follow Mode using the ultrasonic module and then analyze the
program:
Forward
Speed：100
Have obstacles

According to
the state of
Servo

Right
Speed：100

Forward
Speed：100

Left
Speed：100

Follow Mode

Get ultrasonic data
(within 20cm?)
Servo turn
to 80
No obstacles

Servo status
change

Servo turn
to 20
Servo turn
to 80
Servo turn
to 150

Please open Demo1 in the current folder:
First of all, let’s take a look at the deﬁnition of the relative functions and
variables of the Follow Mode.

// in ApplicationFunctionSet_xxx0.h
#ifndef _ApplicationFunctionSet_xxx0_H_
#deﬁne _ApplicationFunctionSet_xxx0_H_
#include <arduino.h>

class ApplicationFunctionSet
{
public:
void ApplicationFunctionSet_Init(void);
void ApplicationFunctionSet_Follow(void);

private:
volatile uint16_t UltrasoundData_mm;
volatile uint16_t UltrasoundData_cm;
boolean UltrasoundDetectionStatus = false;
public:
boolean Car_LeaveTheGround = true;
const int ObstacleDetection = 20;
};
extern ApplicationFunctionSet Application_FunctionSet;
Then, as for the programming of the Follow Mode, you can list the
situations described in the ﬂowchart when the target is not found and write
them down.
// in ApplicationFunctionSet_xxx0.h
void ApplicationFunctionSet::ApplicationFunctionSet_Follow(void)
{.....}
Upload program. (Please toggle the“Upload-Cam”button to“Upload”
when uploading the program.) After successful upload, please put the Smart
Robot Car on the ground steadily and then turn on the switch. By default,
when the ultrasonic module recognizes that there is a target in front, the
Smart Robert Car will go straight ahead, and when there is no target in
front, it will turn to ﬁnd the target intelligently.
http://www.elegoo.com


