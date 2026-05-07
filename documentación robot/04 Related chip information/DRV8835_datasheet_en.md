# DRV8835_datasheet_en

---

DRV8835
www.ti.com.cn

ZHCS380D – MARCH 2012 – REVISED JANUARY 2014

双路低电压 H 桥集成电路 (IC)
查询样片: DRV8835

特性

1

•

2

•
•
•

•
•
•
•

双 H 桥电机驱动器
– 能够驱动两个直流电机或者一个步进电机
– 低金属氧化物半导体场效应晶体管 (MOSFET)
导通电阻：
高侧 + 低侧 (HS + LS) 305mΩ
每个 H 桥 1.5A 的最大驱动电流
两桥并联可实现 3A 的驱动电流
单独的电机和逻辑电源引脚：
– 0V 至 11V 电机运行电源电压范围
– 2V 至 7V 逻辑电源电压范围
独立的逻辑和电机电源引脚
灵活的脉宽调制 (PWM) 或者相位/使能接口
具有 95nA 最大电源电流的低功耗睡眠模式
极小型 2mm x 3mm 晶圆级小外形尺寸无引线
(WSON) 封装

应用范围
•

由电池供电的设备：
– 摄像机
– 数字单镜头反光 (DSLR) 镜头
– 消费类产品
– 玩具
– 机器人技术
– 医疗设备

说明
DRV8835 为摄像机、消费类产品、玩具、和其它低电压或者电池供电的运动控制类应用提供了一个集成的电机驱
动器解决方案。 此器件有两个 H 桥驱动器，并且能够驱动两个直流电机或者一个步进电机，以及其它诸如螺线管
的器件。 每个输出驱动器功能块包括配置为 H 桥的 N 通道功率 MOSFET 以驱动电机绕组。 一个内部电荷泵生成
所需的栅极驱动电压。
DRV8835 的每个 H 桥能够提供高达 1.5A 的输出电流。 它在 0V 至 11V 的电机电源电压范围，以及 2V 至 7V 的
器件电源电压范围内运行。
可选择的相位/使能和 IN/IN 接口与工业标准器件兼容。
内部关断功能支持过流保护、短路保护、欠压锁定以及过温保护。
DRV8835 采用具有 PowerPAD™ 的极小型 12 引脚 WSON 封装（环保型：符合 RoHS 标准且不含 Sb/Br）。
ORDERING INFORMATION (1)
PACKAGE (2)
PowerPAD™ (WSON) - DSS
(1)
(2)

Reel of 3000

ORDERABLE PART
NUMBER

TOP-SIDE
MARKING

DRV8835DSSR

835

For the most current packaging and ordering information, see the Package Option Addendum at the end of this document, or see the TI
web site at www.ti.com.
Package drawings, thermal data, and symbolization are available at www.ti.com/packaging.

1

2

Please be aware that an important notice concerning availability, standard warranty, and use in critical applications of
Texas Instruments semiconductor products and disclaimers thereto appears at the end of this data sheet.
PowerPAD is a trademark of Texas Instruments.

PRODUCTION DATA information is current as of publication date.
Products conform to specifications per the terms of the Texas
Instruments standard warranty. Production processing does not
necessarily include testing of all parameters.

Copyright © 2012–2014, Texas Instruments Incorporated

English Data Sheet: SLVSB18

DRV8835
ZHCS380D – MARCH 2012 – REVISED JANUARY 2014

www.ti.com.cn

DEVICE INFORMATION
Functional Block Diagram
0 to 11V
VM
VM

VM

Drives 2x DC motor
or 1x Stepper
Gate
Drive

Charge
Pump

OCP

AOUT1

2.0 to 7 V

Step
Motor

VCC
DCM

VCC

VM

AOUT2
Gate
Drive

OCP

AIN1/APHASE

AIN2/AENBL
Logic
VM

BIN1/BPHASE
Gate
Drive

BIN2/BENBL

OCP

BOUT1

DCM

MODE
VM

OverTemp

Gate
Drive

OCP

BOUT2

Osc
GND

2

Copyright © 2012–2014, Texas Instruments Incorporated

DRV8835
www.ti.com.cn

ZHCS380D – MARCH 2012 – REVISED JANUARY 2014

Table 1. TERMINAL FUNCTIONS
NAME

PIN

I/O (1)

EXTERNAL COMPONENTS
OR CONNECTIONS

DESCRIPTION

POWER AND GROUND
GND

6

-

Device ground

VM

1

-

Motor supply

Bypass to GND with a 0.1-μF (minimum)
ceramic capacitor.

VCC

12

-

Device supply

Bypass to GND with a 0.1-μF (minimum)
ceramic capacitor.

MODE

11

I

Input mode select

Logic low selects IN/IN mode.
Logic high selects PH/EN mode.
Internal pulldown resistor.

AIN1/APHASE

10

I

Bridge A input 1/PHASE input

IN/IN mode: Logic high sets AOUT1 high.
PH/EN mode: Sets direction of H-bridge A.
Internal pulldown resistor.

AIN2/AENBL

9

I

Bridge A input 2/ENABLE input

IN/IN mode: Logic high sets AOUT2 high.
PH/EN mode: Logic high enables H-bridge A.
Internal pulldown resistor.

BIN1/BPHASE

8

I

Bridge B input 1/PHASE input

IN/IN mode: Logic high sets BOUT1 high.
PH/EN mode: Sets direction of H-bridge B.
Internal pulldown resistor.

BIN2/BENBL

7

I

Bridge B input 2/ENABLE input

IN/IN mode: Logic high sets BOUT2 high.
PH/EN mode: Logic high enables H-bridge B.
Internal pulldown resistor.

AOUT1

2

O

Bridge A output 1

AOUT2

3

O

Bridge A output 2

BOUT1

4

O

Bridge B output 1

BOUT2

5

O

Bridge B output 2

CONTROL

OUTPUT

(1)

Connect to motor winding A
Connect to motor winding B

Directions: I = input, O = output, OZ = tri-state output, OD = open-drain output, IO = input/output
DSS PACKAGE
(TOP VIEW)

VM
AOUT1
AOUT2
BOUT1
BOUT2
GND

Copyright © 2012–2014, Texas Instruments Incorporated

1

12

2

11

3
4

GND
(PPAD )

10
9

5

8

6

7

VCC
MODE
AIN1 / APHASE
AIN2 / AENBL
BIN1 / BPHASE
BIN2 / BENBL

3

DRV8835
ZHCS380D – MARCH 2012 – REVISED JANUARY 2014

www.ti.com.cn

ABSOLUTE MAXIMUM RATINGS (1) (2)
VALUE

UNIT

VM

Power supply voltage range

–0.3 to 12

V

VCC

Power supply voltage range

-0.3 to 7

V

Digital input pin voltage range

–0.5 to VCC + 0.5

V

Peak motor drive output current

Internally limited

A

Continuous motor drive output current per H-bridge (3)

1.5

A

TJ

Operating junction temperature range

–40 to 150

°C

Tstg

Storage temperature range

–60 to 150

°C

(1)
(2)
(3)

Stresses beyond those listed under absolute maximum ratings may cause permanent damage to the device. These are stress ratings
only, and functional operation of the device at these or any other conditions beyond those indicated under recommended operating
conditions is not implied. Exposure to absolute–maximum–rated conditions for extended periods may affect device reliability.
All voltage values are with respect to network ground terminal.
Power dissipation and thermal limits must be observed.

THERMAL INFORMATION
DRV8835
THERMAL METRIC

DSS

UNITS

12 PINS
θJA

Junction-to-ambient thermal resistance (1)

θJCtop

Junction-to-case (top) thermal resistance (2)

58

θJB

Junction-to-board thermal resistance (3)

19.9

ψJT

Junction-to-top characterization parameter (4)

0.9

ψJB

Junction-to-board characterization parameter (5)

20

θJCbot

Junction-to-case (bottom) thermal resistance (6)

6.9

(1)
(2)
(3)
(4)
(5)
(6)

50.4

°C/W

The junction-to-ambient thermal resistance under natural convection is obtained in a simulation on a JEDEC-standard, high-K board, as
specified in JESD51-7, in an environment described in JESD51-2a.
The junction-to-case (top) thermal resistance is obtained by simulating a cold plate test on the package top. No specific JEDECstandard test exists, but a close description can be found in the ANSI SEMI standard G30-88.
The junction-to-board thermal resistance is obtained by simulating in an environment with a ring cold plate fixture to control the PCB
temperature, as described in JESD51-8.
The junction-to-top characterization parameter, ψJT, estimates the junction temperature of a device in a real system and is extracted
from the simulation data for obtaining θJA, using a procedure described in JESD51-2a (sections 6 and 7).
The junction-to-board characterization parameter, ψJB, estimates the junction temperature of a device in a real system and is extracted
from the simulation data for obtaining θJA , using a procedure described in JESD51-2a (sections 6 and 7).
The junction-to-case (bottom) thermal resistance is obtained by simulating a cold plate test on the exposed (power) pad. No specific
JEDEC standard test exists, but a close description can be found in the ANSI SEMI standard G30-88.
Spacer

xxx

RECOMMENDED OPERATING CONDITIONS
TA = 25°C (unless otherwise noted)
MIN

NOM

MAX

UNIT

VCC

Device power supply voltage range

2

7

V

VM

Motor power supply voltage range

0

11

V

IOUT

H-bridge output current (1)

0

1.5

A

fPWM

Externally applied PWM frequency

0

250

kHz

VIN

Logic level input voltage

0

VCC

V

(1)

4

Power dissipation and thermal limits must be observed.

Copyright © 2012–2014, Texas Instruments Incorporated

DRV8835
www.ti.com.cn

ZHCS380D – MARCH 2012 – REVISED JANUARY 2014

ELECTRICAL CHARACTERISTICS
TA = 25°C, VM = 5 V, VCC = 3 V (unless otherwise noted)
PARAMETER

TEST CONDITIONS

MIN

TYP

MAX

UNIT

POWER SUPPLY
IVM

VM operating supply current

IVMQ

VM sleep mode supply current

IVCC

VCC operating supply current

VUVLO

VCC undervoltage lockout
voltage

No PWM, no load

85

200

µA

50 kHz PWM, no load

650

2000

µA

VM = 2 V, VCC = 0 V, all inputs 0 V

5

VM = 5 V, VCC = 0 V, all inputs 0 V

10

95

450

2000

VCC rising

2

VCC falling

1.9

nA
µA
V

LOGIC-LEVEL INPUTS
VIL

Input low voltage

VIH

Input high voltage

IIL

Input low current

VIN = 0

IIH

Input high current

VIN = 3.3 V

RPD

Pulldown resistance

0.3 x VCC

V

5

μA

0.5 x VCC

V

-5

50
100

μA
kΩ

H-BRIDGE FETS

RDS(ON)

IOFF

HS + LS FET on resistance

VCC = 3 V, VM = 3 V, I O = 800 mA,
TJ = 25°C

370

420

VCC = 5 V, VM = 5 V, I O = 800 mA,
TJ = 25°C

305

355

mΩ

Off-state leakage current

±200

nA

PROTECTION CIRCUITS
IOCP

Overcurrent protection trip level

tDEG

Overcurrent deglitch time

1.6
1

3.5

µs

tOCR

Overcurrent protection retry time

1

ms

tDEAD

Output dead time

tTSD

Thermal shutdown temperature

100
Die temperature

Copyright © 2012–2014, Texas Instruments Incorporated

150

160

A

ns
180

°C

5

DRV8835
ZHCS380D – MARCH 2012 – REVISED JANUARY 2014

www.ti.com.cn

TIMING REQUIREMENTS
TA = 25°C, VM = 5 V, VCC = 3 V, RL = 20 Ω
NO.

PARAMETER

CONDITIONS

MIN

MAX

UNIT

1

t1

Delay time, xPHASE high to xOUT1 low

300

ns

2

t2

Delay time, xPHASE high to xOUT2 high

200

ns

3

t3

Delay time, xPHASE low to xOUT1 high

200

ns

4

t4

Delay time, xPHASE low to xOUT2 low

300

ns

5

t5

Delay time, xENBL high to xOUTx high

200

ns

6

t6

Delay time, xENBL high to xOUTx low

300

ns

7

t7

Output enable time

300

ns

8

t8

Output disable time

300

ns

9

t9

Delay time, xINx high to xOUTx high

160

ns

10

t10

Delay time, xINx low to xOUTx low

160

ns

11

tR

Output rise time

30

188

ns

12

tF

Output fall time

30

188

ns

xENBL

IN1

xPHASE

IN2
7

9

8

3

5

OUT1

xOUT1

z

z
10

1

xOUT2

6

5

2

4

6

OUT2

z

z
IN/IN mode

PHASE/ENBL mode

80%

80%

OUTx
20%

20%

11

6

12

Copyright © 2012–2014, Texas Instruments Incorporated

DRV8835
www.ti.com.cn

ZHCS380D – MARCH 2012 – REVISED JANUARY 2014

FUNCTIONAL DESCRIPTION
Bridge Control
Two control modes are available in the DRV8835: IN/IN mode, and PHASE/ENABLE mode. IN/IN mode is
selected if the MODE pin is driven low or left unconnected; PHASE/ENABLE mode is selected if the MODE pin is
driven to logic high. The following tables show the logic for these modes.
Table 2. IN/IN MODE
MODE

xIN1

xIN2

xOUT1

xOUT2

FUNCTION
(DC MOTOR)

0

0

0

Z

Z

Coast

0

0

1

L

H

Reverse

0

1

0

H

L

Forward

0

1

1

L

L

Brake

Table 3. PHASE/ENABLE MODE
MODE

xENABLE

xPHASE

xOUT1

xOUT2

FUNCTION
(DC MOTOR)

1

0

X

L

L

Brake

1

1

1

L

H

Reverse

1

1

0

H

L

Forward

Sleep Mode
If the VCC pin is brought to 0 volts, the DRV8835 will enter a low-power sleep mode. In this state all
unnecessary internal circuitry is powered down. For minimum supply current, all inputs should be low (0 V)
during sleep mode.

Power Supplies and Input Pins
There is a weak pulldown resistor (approximately 100 kΩ) to ground on the input pins.
VCC and VM may be applied and removed in any order. When VCC is removed, the device will enter a low
power state and draw very little current from VM. The input pins should be kept at 0 V during sleep mode to
minimize current draw.
The VM voltage supply does not have any undervoltage lockout protection (UVLO), so as long as VCC > 1.8 V,
the internal device logic will remain active. This means that the VM pin voltage may drop to 0 V, however, the
load may not be sufficiently driven at low VM voltages.

Protection Circuits
The DRV8835 is fully protected against undervoltage, overcurrent and overtemperature events.
Overcurrent Protection (OCP)
An analog current limit circuit on each FET limits the current through the FET by removing the gate drive. If this
analog current limit persists for longer than the OCP time, all FETs in the H-bridge will be disabled. After
approximately 1 ms, the bridge will be re-enabled automatically.
Overcurrent conditions on both high and low side devices; i.e., a short to ground, supply, or across the motor
winding will all result in an overcurrent shutdown.
Thermal Shutdown (TSD)
If the die temperature exceeds safe limits, all FETs in the H-bridge will be disabled . Once the die temperature
has fallen to a safe level operation will automatically resume.

Copyright © 2012–2014, Texas Instruments Incorporated

7

DRV8835
ZHCS380D – MARCH 2012 – REVISED JANUARY 2014

www.ti.com.cn

Undervoltage Lockout (UVLO)
If at any time the voltage on the VCC pins falls below the undervoltage lockout threshold voltage, all circuitry in
the device will be disabled, and internal logic will be reset. Operation will resume when VCC rises above the
UVLO threshold.

8

Copyright © 2012–2014, Texas Instruments Incorporated

DRV8835
www.ti.com.cn

ZHCS380D – MARCH 2012 – REVISED JANUARY 2014

APPLICATIONS INFORMATION
Parallel Mode
The two H-bridges in the DRV8835 can be connected in parallel for double the current of a single H-bridge. The
drawing below shows the connections.

Figure 1. Parallel Mode Connections

Copyright © 2012–2014, Texas Instruments Incorporated

9

DRV8835
ZHCS380D – MARCH 2012 – REVISED JANUARY 2014

www.ti.com.cn

THERMAL INFORMATION
Thermal Protection
The DRV8835 has thermal shutdown (TSD) as described above. If the die temperature exceeds approximately
150°C, the device will be disabled until the temperature drops to a safe level.
Any tendency of the device to enter thermal shutdown is an indication of either excessive power dissipation,
insufficient heatsinking, or too high an ambient temperature.

Power Dissipation
Power dissipation in the DRV8835 is dominated by the power dissipated in the output FET resistance, or
RDS(ON). Average power dissipation when running both H-bridges can be roughly estimated by:
PTOT = 2 x RDS(ON) x (IOUT(RMS))2

(1)

Where PTOT is the total power dissipation, RDS(ON) is the resistance of the HS plus LS FETs, and IOUT(RMS) is the
RMS output current being applied to each winding. IOUT(RMS) is equal to the approximately 0.7x the full-scale
output current setting. The factor of 2 comes from the fact that there are two H-bridges.
The maximum amount of power that can be dissipated in the device is dependent on ambient temperature and
heatsinking.
Note that RDS(ON) increases with temperature, so as the device heats, the power dissipation increases. This must
be taken into consideration when sizing the heatsink.

Heatsinking
The PowerPAD™ package uses an exposed pad to remove heat from the device. For proper operation, this pad
must be thermally connected to copper on the PCB to dissipate heat. On a multi-layer PCB with a ground plane,
this can be accomplished by adding a number of vias to connect the thermal pad to the ground plane. On PCBs
without internal planes, copper area can be added on either side of the PCB to dissipate heat. If the copper area
is on the opposite side of the PCB from the device, thermal vias are used to transfer the heat between top and
bottom layers.
For details about how to design the PCB, refer to TI application report SLMA002, " PowerPAD™ Thermally
Enhanced Package" and TI application brief SLMA004, " PowerPAD™ Made Easy", available at www.ti.com.
In general, the more copper area that can be provided, the more power can be dissipated.

10

Copyright © 2012–2014, Texas Instruments Incorporated

DRV8835
www.ti.com.cn

ZHCS380D – MARCH 2012 – REVISED JANUARY 2014

修订历史记录
Changes from Revision C (September 2013) to Revision D

Page

•

Changed 特性着重号 ............................................................................................................................................................ 1

•

Changed 说明部分中的电机电源电压范围 ............................................................................................................................ 1

•

Changed Motor power supply voltage range in RECOMMENDED OPERATING CONDITIONS ........................................ 4

•

Added tOCR and tDEAD parameters to ELECTRICAL CHARACTERISTICS ........................................................................... 5

•

Added paragraph to Power Supplies and Input Pins section ............................................................................................... 7

Copyright © 2012–2014, Texas Instruments Incorporated

11

PACKAGE OPTION ADDENDUM

www.ti.com

13-Jan-2014

PACKAGING INFORMATION
Orderable Device

Status
(1)

DRV8835DSSR

ACTIVE

Package Type Package Pins Package
Drawing
Qty
WSON

DSS

12

3000

Eco Plan

Lead/Ball Finish

MSL Peak Temp

(2)

(6)

(3)

Green (RoHS
& no Sb/Br)

CU NIPDAU

Level-2-260C-1 YEAR

Op Temp (°C)

Device Marking
(4/5)

-40 to 85

835

(1)

The marketing status values are defined as follows:
ACTIVE: Product device recommended for new designs.
LIFEBUY: TI has announced that the device will be discontinued, and a lifetime-buy period is in effect.
NRND: Not recommended for new designs. Device is in production to support existing customers, but TI does not recommend using this part in a new design.
PREVIEW: Device has been announced but is not in production. Samples may or may not be available.
OBSOLETE: TI has discontinued the production of the device.
(2)

Eco Plan - The planned eco-friendly classification: Pb-Free (RoHS), Pb-Free (RoHS Exempt), or Green (RoHS & no Sb/Br) - please check http://www.ti.com/productcontent for the latest availability
information and additional product content details.
TBD: The Pb-Free/Green conversion plan has not been defined.
Pb-Free (RoHS): TI's terms "Lead-Free" or "Pb-Free" mean semiconductor products that are compatible with the current RoHS requirements for all 6 substances, including the requirement that
lead not exceed 0.1% by weight in homogeneous materials. Where designed to be soldered at high temperatures, TI Pb-Free products are suitable for use in specified lead-free processes.
Pb-Free (RoHS Exempt): This component has a RoHS exemption for either 1) lead-based flip-chip solder bumps used between the die and package, or 2) lead-based die adhesive used between
the die and leadframe. The component is otherwise considered Pb-Free (RoHS compatible) as defined above.
Green (RoHS & no Sb/Br): TI defines "Green" to mean Pb-Free (RoHS compatible), and free of Bromine (Br) and Antimony (Sb) based flame retardants (Br or Sb do not exceed 0.1% by weight
in homogeneous material)
(3)

MSL, Peak Temp. - The Moisture Sensitivity Level rating according to the JEDEC industry standard classifications, and peak solder temperature.

(4)

There may be additional marking, which relates to the logo, the lot trace code information, or the environmental category on the device.

(5)

Multiple Device Markings will be inside parentheses. Only one Device Marking contained in parentheses and separated by a "~" will appear on a device. If a line is indented then it is a continuation
of the previous line and the two combined represent the entire Device Marking for that device.
(6)

Lead/Ball Finish - Orderable Devices may have multiple material finish options. Finish options are separated by a vertical ruled line. Lead/Ball Finish values may wrap to two lines if the finish
value exceeds the maximum column width.
Important Information and Disclaimer:The information provided on this page represents TI's knowledge and belief as of the date that it is provided. TI bases its knowledge and belief on information
provided by third parties, and makes no representation or warranty as to the accuracy of such information. Efforts are underway to better integrate information from third parties. TI has taken and
continues to take reasonable steps to provide representative and accurate information but may not have conducted destructive testing or chemical analysis on incoming materials and chemicals.
TI and TI suppliers consider certain information to be proprietary, and thus CAS numbers and other limited information may not be available for release.
In no event shall TI's liability arising out of such information exceed the total purchase price of the TI part(s) at issue in this document sold by TI to Customer on an annual basis.

Addendum-Page 1

Samples

PACKAGE OPTION ADDENDUM

www.ti.com

13-Jan-2014

Addendum-Page 2

PACKAGE MATERIALS INFORMATION
www.ti.com

2-Jul-2018

TAPE AND REEL INFORMATION

*All dimensions are nominal

Device

DRV8835DSSR

Package Package Pins
Type Drawing

SPQ

WSON

3000

DSS

12

Reel
Reel
A0
Diameter Width (mm)
(mm) W1 (mm)
180.0

8.4

Pack Materials-Page 1

2.25

B0
(mm)

K0
(mm)

P1
(mm)

W
Pin1
(mm) Quadrant

3.25

1.05

4.0

8.0

Q1

PACKAGE MATERIALS INFORMATION
www.ti.com

2-Jul-2018

*All dimensions are nominal

Device

Package Type

Package Drawing

Pins

SPQ

Length (mm)

Width (mm)

Height (mm)

DRV8835DSSR

WSON

DSS

12

3000

210.0

185.0

35.0

Pack Materials-Page 2

PACKAGE OUTLINE

DSS0012A

WSON - 0.8 mm max height
SCALE 5.000

PLASTIC SMALL OUTLINE - NO LEAD

2.1
1.9

B

A

0.35
0.25

PIN 1 INDEX AREA
3.1
2.9
0.3
0.2

DETAIL

OPTIONAL TERMINAL
TYPICAL

C

0.8 MAX

SEATING PLANE
0.08 C
0.9±0.1
4X (0.2)
EXPOSED
THERMAL PAD

7

2X
2.5

10X 0.5

0.05
0.00

(0.7)
6

SEE TERMINAL
DETAIL

(0.2) TYP

13

12

1

PIN 1 ID
(OPTIONAL)

2±0.1

12X

0.35
0.25

12X

0.3
0.2
0.1
0.05

C A
C

B
4222684/A 02/2016

NOTES:
1. All linear dimensions are in millimeters. Any dimensions in parenthesis are for reference only. Dimensioning and tolerancing
per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. The package thermal pad must be soldered to the printed circuit board for thermal and mechanical performance.

www.ti.com

EXAMPLE BOARD LAYOUT

DSS0012A

WSON - 0.8 mm max height
PLASTIC SMALL OUTLINE - NO LEAD

(0.9)

12X (0.5)

12

1
12X (0.25)

13

SYMM

10X (0.5)

(0.75)

(2)

(R0.05) TYP
( 0.2) VIA TYP
NOTE 5

6

7
SYMM
(1.9)

LAND PATTERN EXAMPLE
SCALE:20X

0.07 MIN
ALL AROUND

0.07 MAX
ALL AROUND

SOLDER MASK
OPENING

METAL

METAL UNDER
SOLDER MASK

NON SOLDER MASK
DEFINED
(PREFERRED)

SOLDER MASK
OPENING
SOLDER MASK
DEFINED

SOLDER MASK DETAILS

4222684/A 02/2016

NOTES: (continued)
4. This package is designed to be soldered to a thermal pad on the board. For more information, see Texas Instruments literature
number SLUA271 (www.ti.com/lit/slua271).
5. Vias are optional depending on application, refer to device data sheet. If some or all are implemented, recommended via locations are shown.
It is recommended that vias located under solder paste be filled, plugged or tented.

www.ti.com

EXAMPLE STENCIL DESIGN

DSS0012A

WSON - 0.8 mm max height
PLASTIC SMALL OUTLINE - NO LEAD

SYMM

12X (0.5)
1

12

12X (0.25)

METAL
TYP

10X (0.5)

SYMM

13

(0.9)

(R0.05) TYP

6

7
(0.9)
(1.9)

SOLDER PASTE EXAMPLE

BASED ON 0.125 mm THICK STENCIL
EXPOSED PAD 13:
90% PRINTED SOLDER COVERAGE BY AREA UNDER PACKAGE
SCALE:20X

4222684/A 02/2016

NOTES: (continued)
6. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release. IPC-7525 may have alternate
design recommendations.

www.ti.com

重要声明和免责声明
TI 均以“原样”提供技术性及可靠性数据（包括数据表）、设计资源（包括参考设计）、应用或其他设计建议、网络工具、安全信息和其他资
源，不保证其中不含任何瑕疵，且不做任何明示或暗示的担保，包括但不限于对适销性、适合某特定用途或不侵犯任何第三方知识产权的暗示
担保。
所述资源可供专业开发人员应用TI 产品进行设计使用。您将对以下行为独自承担全部责任：(1) 针对您的应用选择合适的TI 产品；(2) 设计、
验证并测试您的应用；(3) 确保您的应用满足相应标准以及任何其他安全、安保或其他要求。所述资源如有变更，恕不另行通知。TI 对您使用
所述资源的授权仅限于开发资源所涉及TI 产品的相关应用。除此之外不得复制或展示所述资源，也不提供其它TI或任何第三方的知识产权授权
许可。如因使用所述资源而产生任何索赔、赔偿、成本、损失及债务等，TI对此概不负责，并且您须赔偿由此对TI 及其代表造成的损害。
TI 所提供产品均受TI 的销售条款 (http://www.ti.com.cn/zh-cn/legal/termsofsale.html) 以及ti.com.cn上或随附TI产品提供的其他可适用条款的约
束。TI提供所述资源并不扩展或以其他方式更改TI 针对TI 产品所发布的可适用的担保范围或担保免责声明。IMPORTANT NOTICE
邮寄地址：上海市浦东新区世纪大道 1568 号中建大厦 32 楼，邮政编码：200122
Copyright © 2019 德州仪器半导体技术（上海）有限公司


