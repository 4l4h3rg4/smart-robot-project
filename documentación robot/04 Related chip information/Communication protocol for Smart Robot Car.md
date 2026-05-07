# Communication protocol for Smart Robot Car

---

R

Motor
Command
Function
Return

Parameter
Description

Command
Function
Return

Parameter
Description

Command
Function
Return

Parameter
Description

{ "H": ID , "N" :1 , "D1": parameter 1 , "D2": parameter 2 , "D3": parameter 3 }
Select the motor to set the rotation direction and speed.
{ ID_ ok}
Parameter 1 ( select the corresponding motor )
0 : All motors
1 : Left motor
2 : Right motor
Parameter 2 ( the rotation speed value of the selected motor )
The range of speed value: 0~ 255
Parameter 3 ( select the rotation direction of the selected motor)
1 : Clockwise
2 : Counterclockwise

{ "H": ID , "N": 3 , "D1": parameter 1 , "D2" : parameter 2 }
Set the direction and speed of the car.
{ ID_ ok}
Parameter 1 ( the rotation direction of the selected motor )
1 : Turn left
2 : Turn right
3 : Go forward
4 : Back
Parameter 2 ( the rotation speed value of the selected motor )
The range of speed value: 0~ 255

{ "H": ID , "N": 4 , "D1": parameter 1 , "D2" : parameter 2 }
Set the speed of the left and right motors separately.
{ ID_ ok}
Parameter 1 ( the speed of left wheel )
The range of speed value: 0~ 255
Parameter 2 ( the speed of right wheel )
The range of speed value: 0~ 255

Servo motor
Command
Function
Return

Parameter
Description

{ "H": ID , "N": 5 , "D1": parameter 1 , "D2" : parameter 2 }
Select the rotation angle of the servo motor.
{ ID_ ok}
Parameter 1 ( select the servo motor )
1 Servo motor that can turn left and right
2 Servo motor that can turn up and down
Parameter 2 ( the rotation angle of the servo motor: 0-180 )

Joystick clear mode
Command
Function
Return

{ "N":100 }
Clear all functions being executed.
No return

Command for remotely switching the car mode
Command
Function
Return

Parameter
Description

{ "N" : 101 , "D1" : Parameter 1 }
Switch the car mode.
No return
Parameter 1
1 : Tracking mode
2 ：Obstacle-avoidance mode
3 : Follow mode

Joystick movement command
Command

{ "N": 102 , "D1": parameter 1 , "D2": parameter 2 }

Return

No return

Function

Parameter
Description

Make the car move in a certain direction at the default maximum speed.
Parameter 1
1 : Go forward
2 : Back
3 : Turn left
4 : Turn right
5 : Left front
6 : Rear left
7 : Right front
8 : Rear Right

Parameter 2 : Speed value

Remote control - Threshold adjustment
Command

{ "N": 104 , "D1": Parameter 1 }

Return

No return

Function

Parameter
Description

Adjust the tracking sensitivity of the car.

Parameter 1 : 50-1000

Camera rotation
Command
Function
Return

Parameter
Description

{ "N": 106 , "D1": Parameter 1 }
Set the rotation direction of the camera.
No return
Parameter 1
1 : Turn up
2 : Turn down
3 : Turn left
4 : Turn right

Ultrasonic module
Command
Function
Return

Parameter
Description

{ "H": ID , "N": 21, "D1": parameter 1 }
Check whether an obstacle is detected.
{ ID_ false } : No obstacles detected
{ ID_ true } : Obstacles detected
{ Ultrasonic value }

1 : Check whether an obstacle is detected.
2 : Check the value of the ultrasonic sensor.

Infrared module
Command
Function
Return

Parameter
Description

Command
Function
Return

{ "H":ID , "N" : 22,"D1":0 }
Check the value of the infrared sensor.
{ ID_Infrared sensor value }
Parameter D 1
0 : The value of the L infrared sensor
1 : The value of the M infrared sensor
2 : The value of the R infrared sensor

{ "H":ID , "N" : 23 }
Check if the car leaves the ground
{ ID_ false} : the car does not leave the ground
{ ID _ true } : the car leaves the ground

Programming mode clears all states
Command
Function
Return

{ "H":ID , "N":110 }
Clear all the functions being executed, and do not enter the standby mode.
{ID_ok}

http://www.elegoo.com


