# TB6612FNG

---

TB6612FNG
Toshiba Bi-CD Integrated Circuit

Silicon Monolithic

TB6612FNG
Driver IC for Dual DC motor

TB6612FNG is a driver IC for DC motor with output transistor in
LD MOS structure with low ON-resistor. Two input signals, IN1
and IN2, can choose one of four modes such as CW, CCW, short
brake, and stop mode.

Features
•

Power supply voltage; VM = 15 V(Max)

•

Output current; IOUT=1.2 A(ave) / 3.2 A (peak)

•

Output low ON resistor; 0.5Ω (upper+lower Typ. @VM ≥ 5 V)

•

Standby (Power save) system

•

CW / CCW / short brake / stop function modes

•

Built-in thermal shutdown circuit and low voltage detecting circuit

•

Small faced package(SSOP24: 0.65 mm Lead pitch)

•

Response to Pb free packaging

*

This product has a MOS structure and is sensitive to electrostatic discharge. When handling this product,
ensure that the environment is protected against electrostatic discharge by using an earth strap, a conductive
mat and an ionizer. Ensure also that the ambient temperature and relative humidity are maintained at
reasonable levels.

質量: 0.14 g (標準)

The TB6612FNG is a Pb-free product.
The following conditions apply to solderability:
*Solderability
1. Use of Sn-37Pb solder bath
*solder bath temperature = 230°C
*dipping time = 5 seconds
*number of times = once
*use of R-type flux
2. Use of Sn-3.0Ag-0.5Cu solder bath
*solder bath temperature = 245°C
*dipping time = 5 seconds

1

2008-05-09

TB6612FNG
Block Diagram
VM1

PWMA AIN2 AIN1 Vcc

24

23

22

21

20

STBY GND
19

18

BIN1 BIN2 PWMB
17

16

15

VM3 VM2
14

13

11

12

STB
Control Logic
A

Control Logic
B

UVLO
TSD

H-SW
A

3

H-SW
B

1

2

4

5

AO1

AO1 PGND1 PGND1 AO2

6

7

8

9

AO2

BO2

BO2 PGND2

10

PGND2 BO1

BO1

Pin Functions
No.

Pin Name

1

AO1

2

AO1

3

PGND1

4

PGND1

5

AO2

6

AO2

7

BO2

8

BO2

9

PGND2

10

PGND2

I/O

Function

O

ch A output1

⎯

Power GND 1

O

ch A output2

O

ch B output2

⎯

Power GND 2

O

ch B output1

⎯

Motor supply (2.5 V to 13.5 V)

11

BO1

12

BO1

13

VM2

14

VM3

15

PWMB

I

ch B PWM input / 200 kΩ pull-down at internal

16

BIN2

I

ch B input 2 / 200 kΩ pull-down at internal

17

BIN1

I

ch B input 1 / 200 kΩ pull-down at internal

18

GND

⎯

Small signal GND

19

STBY

I

“L”=standby / 200 kΩ pull-down at internal

20

Vcc

⎯

Small signal supply

21

AIN1

I

ch A input 1 / 200 kΩ pull-down at internal

22

AIN2

I

ch A input 2 / 200 kΩ pull-down at internal

23

PWMA

I

ch A PWM input / 200 kΩ pull-down at internal

24

VM1

⎯

Motor supply (2.5 V~13.5 V)

2

2008-05-09

TB6612FNG
Absolute Maximum Ratings (Ta = 25°C)
Characteristics

Symbol

Rating

Unit

Remarks

VM

15

VCC

6

Input voltage

VIN

-0.2 to 6

V

IN1,IN2,STBY,PWM pins

Output voltage

VOUT

15

V

O1,O2 pins

IOUT

1.2

Supply voltage

Output current

V

Per 1 ch

IOUT (peak)

tw = 20 ms Continuous pulse, Duty ≤ 20%

A

2
3.2

tw = 10 ms Single pulse

0.78

IC only

Power dissipation

PD

0.89

W

Operating temperature

Topr

-20 to 85

℃

Storage temperature

Tstg

-55 to 150

℃

1.36

Operating Range

50 mm × 50 mm

t=1.6 mm Cu ≥ 40% in PCB mounting

76.2 mm × 114.3 mm

t=1.6 mm Cu ≥ 30% in PCB monting

(Ta=-20～85℃)

Characteristics
Supply voltage

Symbol

Min

VCC

2.7

3

5.5

V

VM

2.5

5

13.5

V

⎯

⎯

1.0

Output current (H-SW)

IOUT

Switching frequency

fPWM

Typ.

Max

⎯

⎯

0.4

⎯

⎯

100

Input
入
力 端pin;
子 ; IN1,IN2,PWM,STBY

Unit

Remarks

VM ≥ 4.5 V
4.5 V > VM ≥ 2.5 V

A

Without PWM Operation
kHz

Output
出 力 端pin;
子 O1,O2

Vcc

VM

Input

O1 O2

200kΩ

Internal
circuit

GND

PGND

3

2008-05-09

TB6612FNG
H-SW Control Function
Input

Output

IN1

IN2

PWM

STBY

OUT1

OUT2

Mode

H

H

H/L

H

L

L

Short brake

L

H

H

H

L

H

CCW

L

H

L

L

Short brake

H

L

H

H

H

L

CW

L

H

L

L

Short brake

L

L

H

H

H/L

H/L

H/L

L

OFF

Stop

(High impedance)
OFF

Standby

(High impedance)

H-SW Operating Description
・To prevent penetrating current, dead time t2 and t4 is provided in switching to each mode in the IC.
VM

OUT1

M

VM

OUT1

OUT2

M

OUT2

GND

VM

OUT1

GND

GND

<OFF>
t2

<ON>
t1

<Short brake>
t3

VM

OUT1

OUT2

M

VM

OUT2

M

OUT1

M

GND

OUT2

GND

<OFF>
t4

<ON>
t5
VM
t5

t1
OUT1
Voltage wave

t3
GND
t4

t2

4

2008-05-09

TB6612FNG
Electrical Characteristics (unless otherwise specified, Ta = 25°C, VCC = 3 V, VM = 5 V)
Characteristics

Supply current

Symbol

Test Condition

Min

Typ.

Max

ICC(3V)

STBY = VCC = 3 V, VM = 5 V

⎯

1.1

1.8

ICC(5.5V)

STBY = VCC = 5.5 V, VM = 5 V

⎯
⎯
⎯

1.5

2.2

⎯
⎯
⎯
⎯

1

ICC(STB)
IM(STB)

Control input voltage
Control input current
Standby input voltage
Standby input current
Output saturating voltage

Low voltage detecting
voltage
Recovering voltage

VIH

VCC×0.7

VIL

-0.2

Thermal shutdown circuit
operating temperature
Thermal shutdown
hysteresis

μA

1
VCC+0.2
VCC×0.3

VIN = 3 V

5

15

25

IIL

VIN = 0 V

⎯

⎯
⎯
⎯

1
VCC+0.2

VCC×0.7

VIL(STB)

-0.2
VIN = 3 V

5

15

25

IIL(STB)

VIN = 0 V

⎯

1

Vsat(U+L)1

IO = 1 A, VCC = VM = 5 V

⎯
⎯

Vsat(U+L)2

IO = 0.3 A, VCC = VM = 5 V

IL(U)

VM = VOUT = 15 V

⎯

IL(L)

VM = 15 V, VOUT = 0 V

-1

VF(U)
VF(L)
UVLD

⎯
⎯
⎯

IF = 1A

(Designed value)

UVLC
(Designed value)

tf
Dead

H to L

Penetration protect time

time

L to H

(Designed value)

TSD

0.5

0.7

0.15

0.21

⎯
⎯

1

⎯

1

1.1

1

1.1

1.9

5

V
μA
V

⎯
⎯

⎯
⎯
⎯

41
230

⎯
⎯
⎯

⎯

175

⎯

⎯

20

⎯

(Designed value)
△TSD

μA

V

2.2

50

V

⎯

⎯
⎯

24

V
μA

VCC×0.3

IIH(STB)

tr
Response speed

mA

IIH
VIH(STB)

Output leakage current
Regenerative diode VF

STBY = 0 V

Unit

ns

℃

2008-05-09

TB6612FNG
Target characteristics
PD-- Ta
PD
Ta

(w)

1.50

2.5

①IC①IC単体θj-a=160℃/W
only θj – a = 160℃/W

③

Iout
IOUT-- Duty
Duty

(A)

PCB面積 50×50×1.6mm
Cu箔面積≧40%
③基板実装時
③In boarding
PCB面積 76.2×114.3×1.6mm
PCB area
76.2 mm×114.3 mm×1.6 mm
Cu箔面積≧30%
Cu area ≥ 40%

1.00

②

Cu area ≥ 30%

①
0.50

2.0
1 ch
driving
1ch動作時

1.5

Output current

Power dissipation

PD

PCB area 50 mm×50 mm×1.6 mm

IOUT

②In②基板実装時
boarding

2ch動作時
2 ch driving

1.0

0.5
Ta
= 25℃, IC only
Ta=25℃,IC単体

0.0

0.00
0

50

100

Ta (℃)

0%

150

6

20%

40%

Duty

60%

80%

100%

2008-05-09

TB6612FNG
Typical Application Diagram

+2.7
V
+2.7V
to 5.5
V
～
5.5V

Vcc
C4
0.1uF

+ C3
10uF

STBY

20

UVLO

19

STBY
24

AIN1

21

1
2

AIN2

PWMA

22

Control
Logic
A

H-SW
Driver
A

23

5
6

3

MCU

4

TSD

13

BIN1

17

14
11

BIN2

PWMB

16

Control
Logic
B

H-SW
Driver
B

12
7
8

15
9
10

GND

Note:

VM1
AO1

C2

AO1

0.1uF

AO2

+ C1
10uF

+4.5 V
+4.5V
to 13.5 V
～ 13.5V

M

AO2
PGND1
PGND1
VM2
VM3
BO1
BO1
BO2

M

BO2
PGND2
PGND2

18

Condensers for noise absorption (C1, C2, C3, and C4) should be connected as close as possible to the IC.

7

2008-05-09

TB6612FNG
Package Dimennsions

Weght: 0.14 g (typ)

8

2008-05-09

TB6612FNG
Notes on Contents
1. Block Diagrams

Some of the functional blocks, circuits, or constants in the block diagram may be omitted or simplified
for explanatory purposes.

2. Equivalent Circuits

The equivalent circuit diagrams may be simplified or some parts of them may be omitted for
explanatory purposes.

3. Timing Charts

Timing charts may be simplified for explanatory purposes.

4. Application Circuits

The application circuits shown in this document are provided for reference purposes only. Thorough
evaluation is required, especially at the mass production design stage.
Toshiba does not grant any license to any industrial property rights by providing these examples of
application circuits.

5. Test Circuits

Components in the test circuits are used only to obtain and confirm the device characteristics. These
components and circuits are not guaranteed to prevent malfunction or failure from occurring in the
application equipment.

IC Usage Considerations
Notes on handling of ICs
[1] The absolute maximum ratings of a semiconductor device are a set of ratings that must not be
exceeded, even for a moment. Do not exceed any of these ratings.
Exceeding the rating(s) may cause the device breakdown, damage or deterioration, and may result
injury by explosion or combustion.
[2] Use an appropriate power supply fuse to ensure that a large current does not continuously flow in
case of over current and/or IC failure. The IC will fully break down when used under conditions that
exceed its absolute maximum ratings, when the wiring is routed improperly or when an abnormal
pulse noise occurs from the wiring or load, causing a large current to continuously flow and the
breakdown can lead smoke or ignition. To minimize the effects of the flow of a large current in case
of breakdown, appropriate settings, such as fuse capacity, fusing time and insertion circuit location,
are required.
[3] If your design includes an inductive load such as a motor coil, incorporate a protection circuit into
the design to prevent device malfunction or breakdown caused by the current resulting from the
inrush current at power ON or the negative current resulting from the back electromotive force at
power OFF. IC breakdown may cause injury, smoke or ignition.
Use a stable power supply with ICs with built-in protection functions. If the power supply is
unstable, the protection function may not operate, causing IC breakdown. IC breakdown may cause
injury, smoke or ignition.
[4] Do not insert devices in the wrong orientation or incorrectly.
Make sure that the positive and negative terminals of power supplies are connected properly.
Otherwise, the current or power consumption may exceed the absolute maximum rating, and
exceeding the rating(s) may cause the device breakdown, damage or deterioration, and may result
injury by explosion or combustion.
In addition, do not use any device that is applied the current with inserting in the wrong orientation
or incorrectly even just one time.

9

2008-05-09

TB6612FNG
Points to remember on handling of ICs
(1) Thermal Shutdown Circuit
Thermal shutdown circuits do not necessarily protect ICs under all circumstances. If the thermal
shutdown circuits operate against the over temperature, clear the heat generation status
immediately.
Depending on the method of use and usage conditions, such as exceeding absolute maximum ratings
can cause the thermal shutdown circuit to not operate properly or IC breakdown before operation.
(2) Heat Radiation Design
In using an IC with large current flow such as power amp, regulator or driver, please design the
device so that heat is appropriately radiated, not to exceed the specified junction temperature (TJ)
at any time and condition. These ICs generate heat even during normal use. An inadequate IC heat
radiation design can lead to decrease in IC life, deterioration of IC characteristics or IC breakdown.
In addition, please design the device taking into considerate the effect of IC heat radiation with
peripheral components.
(3) Back-EMF
When a motor rotates in the reverse direction, stops or slows down abruptly, a current flow back to
the motor’s power supply due to the effect of back-EMF. If the current sink capability of the power
supply is small, the device’s motor power supply and output pins might be exposed to conditions
beyond maximum ratings. To avoid this problem, take the effect of back-EMF into consideration in
system design.

10

2008-05-09

TB6612FNG

RESTRICTIONS ON PRODUCT USE

070122EBA_R6

• The information contained herein is subject to change without notice. 021023_D
• TOSHIBA is continually working to improve the quality and reliability of its products. Nevertheless, semiconductor
devices in general can malfunction or fail due to their inherent electrical sensitivity and vulnerability to physical
stress. It is the responsibility of the buyer, when utilizing TOSHIBA products, to comply with the standards of
safety in making a safe design for the entire system, and to avoid situations in which a malfunction or failure of
such TOSHIBA products could cause loss of human life, bodily injury or damage to property.
In developing your designs, please ensure that TOSHIBA products are used within specified operating ranges as
set forth in the most recent TOSHIBA products specifications. Also, please keep in mind the precautions and
conditions set forth in the “Handling Guide for Semiconductor Devices,” or “TOSHIBA Semiconductor Reliability
Handbook” etc. 021023_A
• The TOSHIBA products listed in this document are intended for usage in general electronics applications
(computer, personal equipment, office equipment, measuring equipment, industrial robotics, domestic appliances,
etc.). These TOSHIBA products are neither intended nor warranted for usage in equipment that requires
extraordinarily high quality and/or reliability or a malfunction or failure of which may cause loss of human life or
bodily injury (“Unintended Usage”). Unintended Usage include atomic energy control instruments, airplane or
spaceship instruments, transportation instruments, traffic signal instruments, combustion control instruments,
medical instruments, all types of safety devices, etc. Unintended Usage of TOSHIBA products listed in this
document shall be made at the customer’s own risk. 021023_B
• The products described in this document shall not be used or embedded to any downstream products of which
manufacture, use and/or sale are prohibited under any applicable laws and regulations. 060106_Q
• The information contained herein is presented only as a guide for the applications of our products. No
responsibility is assumed by TOSHIBA for any infringements of patents or other rights of the third parties which
may result from its use. No license is granted by implication or otherwise under any patents or other rights of
TOSHIBA or the third parties. 070122_C
• Please use this product in compliance with all applicable laws and regulations that regulate the inclusion or use of
controlled substances.
Toshiba assumes no liability for damage or losses occurring as a result of noncompliance with applicable laws
and regulations. 060819_AF
• The products described in this document are subject to foreign exchange and foreign trade control laws. 060925_E

11

2008-05-09


