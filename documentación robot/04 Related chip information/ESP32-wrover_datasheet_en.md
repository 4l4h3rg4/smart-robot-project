# ESP32-wrover_datasheet_en

---

ESP32-WROVER
Datasheet

Version 2.2
Espressif Systems
Copyright © 2019

www.espressif.com

About This Document
This document provides the specifications for the ESP32-WROVER modules with a PCB antenna or an IPEX
antenna.

Revision History
For revision history of this document, please refer to the last page.

Documentation Change Notification
Espressif provides email notifications to keep customers updated on changes to technical documentation. Please
subscribe at www.espressif.com/en/subscribe.

Certification
Download certificates for Espressif products from www.espressif.com/en/certificates.

Disclaimer and Copyright Notice
Information in this document, including URL references, is subject to change without notice. THIS DOCUMENT IS
PROVIDED AS IS WITH NO WARRANTIES WHATSOEVER, INCLUDING ANY WARRANTY OF MERCHANTABILITY, NON-INFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY WARRANTY OTHERWISE
ARISING OUT OF ANY PROPOSAL, SPECIFICATION OR SAMPLE.
All liability, including liability for infringement of any proprietary rights, relating to use of information in this document is disclaimed. No licenses express or implied, by estoppel or otherwise, to any intellectual property rights
are granted herein. The Wi-Fi Alliance Member logo is a trademark of the Wi-Fi Alliance. The Bluetooth logo is a
registered trademark of Bluetooth SIG.
All trade names, trademarks and registered trademarks mentioned in this document are property of their respective
owners, and are hereby acknowledged.
Copyright © 2019 Espressif Inc. All rights reserved.

Contents
1 Overview

1

2 Pin Definitions

3

2.1

Pin Layout

3

2.2

Pin Description

4

2.3

Strapping Pins

5

3 Functional Description

7

3.1

CPU and Internal Memory

7

3.2

External Flash and SRAM

7

3.3

Crystal Oscillators

7

3.4

RTC and Low-Power Management

8

4 Peripherals and Sensors

9

5 Electrical Characteristics

10

5.1

Absolute Maximum Ratings

10

5.2

Recommended Operating Conditions

10

5.3

DC Characteristics (3.3 V, 25 °C)

10

5.4

Wi-Fi Radio

11

5.5

BLE Radio

12

5.5.1 Receiver

12

5.5.2 Transmitter

12

Reflow Profile

13

6 Schematics

14

7 Peripheral Schematics

15

8 Physical Dimensions

17

9 Recommended PCB Land Pattern

18

10U.FL Connector Dimensions

19

11Learning Resources

20

11.1 Must-Read Documents

20

11.2 Must-Have Resources

20

Revision History

21

5.6

List of Tables
1

ESP32-WROVER Ordering Information

1

2

ESP32-WROVER Specifications

1

3

Pin Definitions

4

4

Strapping Pins

5

5

Absolute Maximum Ratings

10

6

Recommended Operating Conditions

10

7

DC Characteristics (3.3 V, 25 °C)

10

8

Wi-Fi Radio Characteristics

11

9

Receiver Characteristics – BLE

12

10

Transmitter Characteristics – BLE

12

List of Figures
1

Pin Layout of ESP32-WROVER (Top View)

3

2

Reflow Profile

13

3

Schematics of ESP32-WROVER

14

4

Peripheral Schematics of ESP32-WROVER

15

5

Discharge Circuit for VDD33 Rail

16

6

Reset Circuit

16

7

Physical Dimensions of ESP32-WROVER

17

8

Recommended PCB Land Pattern of ESP32-WROVER

18

9

U.FL Connector Dimensions

19

1. Overview

1. Overview
ESP32-WROVER is a powerful, generic WiFi-BT-BLE MCU module that targets a wide variety of applications,
ranging from low-power sensor networks to the most demanding tasks, such as voice encoding, music streaming
and MP3 decoding.
This module is provided in two versions: one with a PCB antenna, the other with an IPEX antenna. ESP32WROVER features a 4 MB external SPI flash and an additional 8 MB SPI Pseudo static RAM (PSRAM).
The ordering information on the two variants of ESP32-WROVER is listed as follows:
Table 1: ESP32-WROVER Ordering Information
Module
ESP32-WROVER (PCB)
ESP32-WROVER (IPEX)

Chip embedded

Flash

PSRAM

Dimensions (mm)

ESP32-D0WDQ6

4 MB

8 MB

(18.00±0.10)×(31.40±0.10)×(3.30±0.10)

For detailed ordering information, please see Espressif Product Ordering Information. For dimensions of the IPEX
connector, please see Chapter 10. The information in this datasheet is applicable to both modules.
At the core of this module is the ESP32-D0WDQ6 chip*. The chip embedded is designed to be scalable and
adaptive. There are two CPU cores that can be individually controlled, and the CPU clock frequency is adjustable
from 80 MHz to 240 MHz. The user may also power off the CPU and make use of the low-power co-processor to
constantly monitor the peripherals for changes or crossing of thresholds. ESP32 integrates a rich set of peripherals,
ranging from capacitive touch sensors, Hall sensors, SD card interface, Ethernet, high-speed SPI, UART, I²S and
I²C.
Note:
* For details on the part numbers of the ESP32 family of chips, please refer to the document ESP32 Datasheet.

The integration of Bluetooth, Bluetooth LE and Wi-Fi ensures that a wide range of applications can be targeted,
and that the module is all-around: using Wi-Fi allows a large physical range and direct connection to the Internet
through a Wi-Fi router, while using Bluetooth allows the user to conveniently connect to the phone or broadcast
low energy beacons for its detection. The sleep current of the ESP32 chip is less than 5 µA, making it suitable
for battery powered and wearable electronics applications. The module supports a data rate of up to 150 Mbps,
and 20 dBm output power at the antenna to ensure the widest physical range. As such the module does offer
industry-leading specifications and the best performance for electronic integration, range, power consumption,
and connectivity.
The operating system chosen for ESP32 is freeRTOS with LwIP; TLS 1.2 with hardware acceleration is built in as
well. Secure (encrypted) over the air (OTA) upgrade is also supported, so that users can upgrade their products
even after their release, at minimum cost and effort.
Table 2 provides the specifications of ESP32-WROVER.
Table 2: ESP32-WROVER Specifications
Categories

Items

Specifications

Certification

RF certification

FCC/CE-RED/SRRC/TELEC

Wi-Fi certification

Wi-Fi Alliance

Espressif Systems

1

ESP32-WROVER Datasheet V2.2

1. Overview

Categories

Test

Items

Specifications

Bluetooth certification

BQB

Green certification

RoHS/REACH

Reliablity

HTOL/HTSL/uHAST/TCT/ESD
802.11 b/g/n (802.11n up to 150 Mbps)

Wi-Fi

Protocols

A-MPDU and A-MSDU aggregation and 0.4 µs guard interval support

Frequency range

2.4 GHz ~ 2.5 GHz

Protocols

Bluetooth v4.2 BR/EDR and BLE specification
NZIF receiver with –97 dBm sensitivity

Bluetooth

Radio

Class-1, class-2 and class-3 transmitter
AFH

Audio

CVSD and SBC
SD card, UART, SPI, SDIO, I2 C, LED PWM, Motor PWM,

Module interfaces

I2 S, IR, pulse counter, GPIO, capacitive touch sensor,
ADC, DAC

Hardware

On-chip sensor

Hall sensor

Integrated crystal

40 MHz crystal

Integrated SPI flash

4 MB

Integrated PSRAM

8 MB

Operating voltage/Power supply

2.3 V ~ 3.6 V

Operating current

Average: 80 mA

Minimum current delivered by
power supply
Recommended operating temperature range

Espressif Systems

500 mA
–40 °C ~ 85 °C

Package size

(18.00±0.10) mm × (31.40±0.10) mm × (3.30±0.10) mm

Moisture sensitivity level (MSL)

Level 3

2

ESP32-WROVER Datasheet V2.2

2. Pin Deﬁnitions

2. Pin Definitions
2.1 Pin Layout

Keepout Zone

1

GND

GND

38

2

VDD33

IO23

37

3

EN

IO22

36

4

SENSOR_VP

TXD0

35

5

SENSOR_VN

RXD0

34

6

IO34

IO21

33

7

IO35

NC

32

IO19

31

39 GND

8

IO32

9

IO33

IO18

30

10

IO25

IO5

29

11

IO26

NC

28

12

IO27

NC

27

13

IO14

IO4

26

14

IO12

IO0

25

15

GND

IO2

24

16

IO13

IO15

23

17

SD2

SD1

22

18

SD3

SD0

21

19

CMD

CLK

20

Figure 1: Pin Layout of ESP32-WROVER (Top View)

Espressif Systems

3

ESP32-WROVER Datasheet V2.2

2. Pin Deﬁnitions

2.2 Pin Description
ESP32-WROVER has 38 pins. See pin definitions in Table 3.
Table 3: Pin Definitions
Name

No.

Type

Function

GND

1

P

Ground

3V3

2

P

Power supply

EN

3

I

Module-enable signal. Active high.

SENSOR_VP

4

I

GPIO36, ADC1_CH0, RTC_GPIO0

SENSOR_VN

5

I

GPIO39, ADC1_CH3, RTC_GPIO3

IO34

6

I

GPIO34, ADC1_CH6, RTC_GPIO4

IO35

7

I

GPIO35, ADC1_CH7, RTC_GPIO5

IO32

8

I/O

IO33

9

I/O

IO25

10

I/O

GPIO25, DAC_1, ADC2_CH8, RTC_GPIO6, EMAC_RXD0

IO26

11

I/O

GPIO26, DAC_2, ADC2_CH9, RTC_GPIO7, EMAC_RXD1

IO27

12

I/O

GPIO27, ADC2_CH7, TOUCH7, RTC_GPIO17, EMAC_RX_DV

IO14

13

I/O

IO12 1

14

I/O

GND

15

P

IO13

16

I/O

SHD/SD2

2

17

I/O

GPIO9, SD_DATA2, SPIHD, HS1_DATA2, U1RXD

SWP/SD3

2

18

I/O

GPIO10, SD_DATA3, SPIWP, HS1_DATA3, U1TXD

SCS/CMD

2

19

I/O

GPIO11, SD_CMD, SPICS0, HS1_CMD, U1RTS

SCK/CLK

2

20

I/O

GPIO6, SD_CLK, SPICLK, HS1_CLK, U1CTS

SDO/SD0

2

21

I/O

GPIO7, SD_DATA0, SPIQ, HS1_DATA0, U2RTS

22

I/O

GPIO8, SD_DATA1, SPID, HS1_DATA1, U2CTS

IO15

23

I/O

IO2

24

I/O

IO0

25

I/O

IO4

26

I/O

NC1

27

-

-

NC2

28

-

-

IO5

29

I/O

GPIO5, VSPICS0, HS1_DATA6, EMAC_RX_CLK

IO18

30

I/O

GPIO18, VSPICLK, HS1_DATA7

SDI/SD1

2

Espressif Systems

GPIO32, XTAL_32K_P (32.768 kHz crystal oscillator input), ADC1_CH4,
TOUCH9, RTC_GPIO9
GPIO33, XTAL_32K_N (32.768 kHz crystal oscillator output),
ADC1_CH5, TOUCH8, RTC_GPIO8

GPIO14, ADC2_CH6, TOUCH6, RTC_GPIO16, MTMS, HSPICLK,
HS2_CLK, SD_CLK, EMAC_TXD2
GPIO12, ADC2_CH5, TOUCH5, RTC_GPIO15, MTDI, HSPIQ,
HS2_DATA2, SD_DATA2, EMAC_TXD3
Ground
GPIO13, ADC2_CH4, TOUCH4, RTC_GPIO14, MTCK, HSPID,
HS2_DATA3, SD_DATA3, EMAC_RX_ER

GPIO15, ADC2_CH3, TOUCH3, MTDO, HSPICS0, RTC_GPIO13,
HS2_CMD, SD_CMD, EMAC_RXD3
GPIO2, ADC2_CH2, TOUCH2, RTC_GPIO12, HSPIWP, HS2_DATA0,
SD_DATA0
GPIO0, ADC2_CH1, TOUCH1, RTC_GPIO11, CLK_OUT1,
EMAC_TX_CLK
GPIO4, ADC2_CH0, TOUCH0, RTC_GPIO10, HSPIHD, HS2_DATA1,
SD_DATA1, EMAC_TX_ER

4

ESP32-WROVER Datasheet V2.2

2. Pin Deﬁnitions

Name

No.

Type

Function

IO19

31

I/O

GPIO19, VSPIQ, U0CTS, EMAC_TXD0

NC

32

-

-

IO21

33

I/O

GPIO21, VSPIHD, EMAC_TX_EN

RXD0

34

I/O

GPIO3, U0RXD, CLK_OUT2

TXD0

35

I/O

GPIO1, U0TXD, CLK_OUT3, EMAC_RXD2

IO22

36

I/O

GPIO22, VSPIWP, U0RTS, EMAC_TXD1

IO23

37

I/O

GPIO23, VSPID, HS1_STROBE

GND

38

P

Ground

Notice:
1. GPIO12 is internally pulled high in the module and is not recommended for use as a touch pin.
2. Pins SCK/CLK, SDO/SD0, SDI/SD1, SHD/SD2, SWP/SD3 and SCS/CMD, namely, GPIO6 to GPIO11 are connected to the SPI flash integrated on the module and are not recommended for other uses.

2.3 Strapping Pins
ESP32 has five strapping pins, which can be seen in Chapter 6 Schematics:
• MTDI
• GPIO0
• GPIO2
• MTDO
• GPIO5
Software can read the values of these five bits from register ”GPIO_STRAPPING”.
During the chip’s system reset release (power-on-reset, RTC watchdog reset and brownout reset), the latches
of the strapping pins sample the voltage level as strapping bits of ”0” or ”1”, and hold these bits until the chip
is powered down or shut down. The strapping bits configure the device’s boot mode, the operating voltage of
VDD_SDIO and other initial system settings.
Each strapping pin is connected to its internal pull-up/pull-down during the chip reset. Consequently, if a strapping
pin is unconnected or the connected external circuit is high-impedance, the internal weak pull-up/pull-down will
determine the default input level of the strapping pins.
To change the strapping bit values, users can apply the external pull-down/pull-up resistances, or use the host
MCU’s GPIOs to control the voltage level of these pins when powering on ESP32.
After reset release, the strapping pins work as normal-function pins.
Refer to Table 4 for a detailed boot-mode configuration by strapping pins.
Table 4: Strapping Pins
Voltage of Internal LDO (VDD_SDIO)
Pin

Default

Espressif Systems

3.3 V

1.8 V

5

ESP32-WROVER Datasheet V2.2

2. Pin Deﬁnitions

MTDI

Pull-down

0

1
Booting Mode

Pin

Default

SPI Boot

Download Boot

GPIO0

Pull-up

1

0

GPIO2

Pull-down

Don’t-care

0

Enabling/Disabling Debugging Log Print over U0TXD During Booting
Pin

Default

U0TXD Active

U0TXD Silent

MTDO

Pull-up

1

0
Timing of SDIO Slave

Falling-edge Sampling

Falling-edge Sampling

Rising-edge Sampling

Rising-edge Sampling

Falling-edge Output

Rising-edge Output

Falling-edge Output

Rising-edge Output

Pull-up

0

0

1

1

Pull-up

0

1

0

1

Pin

Default

MTDO
GPIO5

Note:
• Firmware can configure register bits to change the settings of ”Voltage of Internal LDO (VDD_SDIO)” and ”Timing
of SDIO Slave” after booting.
• The MTDI is internally pulled high in the module, as the flash and SRAM in ESP32-WROVER only support a power
voltage of 1.8 V (output by VDD_SDIO).

Espressif Systems

6

ESP32-WROVER Datasheet V2.2

3. Functional Description

3. Functional Description
This chapter describes the modules and functions integrated in ESP32-WROVER.

3.1 CPU and Internal Memory
ESP32-D0WDQ6 contains two low-power Xtensa® 32-bit LX6 microprocessors. The internal memory includes:
• 448 KB of ROM for booting and core functions.
• 520 KB of on-chip SRAM for data and instructions.
• 8 KB of SRAM in RTC, which is called RTC FAST Memory and can be used for data storage; it is accessed
by the main CPU during RTC Boot from the Deep-sleep mode.
• 8 KB of SRAM in RTC, which is called RTC SLOW Memory and can be accessed by the co-processor during
the Deep-sleep mode.
• 1 Kbit of eFuse: 256 bits are used for the system (MAC address and chip configuration) and the remaining
768 bits are reserved for customer applications, including flash-encryption and chip-ID.

3.2 External Flash and SRAM
ESP32 supports multiple external QSPI flash and SRAM chips. More details can be found in Chapter SPI in the
ESP32 Technical Reference Manual. ESP32 also supports hardware encryption/decryption based on AES to protect developers’ programs and data in flash.
ESP32 can access the external QSPI flash and SRAM through high-speed caches.
• The external flash can be mapped into CPU instruction memory space and read-only memory space simultaneously.
– When external flash is mapped into CPU instruction memory space, up to 11 MB + 248 KB can be
mapped at a time. Note that if more than 3 MB + 248 KB are mapped, cache performance will be
reduced due to speculative reads by the CPU.
– When external flash is mapped into read-only data memory space, up to 4 MB can be mapped at a
time. 8-bit, 16-bit and 32-bit reads are supported.
• External SRAM can be mapped into CPU data memory space. Up to 4 MB can be mapped at a time. 8-bit,
16-bit and 32-bit reads and writes are supported.
ESP32-WROVER integrates a 4 MB of external SPI flash and an 8 MB PSRAM for more memory space.

3.3 Crystal Oscillators
The module uses a 40-MHz crystal oscillator.

Espressif Systems

7

ESP32-WROVER Datasheet V2.2

3. Functional Description

3.4 RTC and Low-Power Management
With the use of advanced power-management technologies, ESP32 can switch between different power modes.
For details on ESP32’s power consumption in different power modes, please refer to section ”RTC and Low-Power
Management” in ESP32 Datasheet.

Espressif Systems

8

ESP32-WROVER Datasheet V2.2

4. Peripherals and Sensors

4. Peripherals and Sensors
Please refer to Section Peripherals and Sensors in ESP32 Datasheet.
Note:
1. GPIO12 is internally pulled high in the module and is not recommended for use as a touch pin.
2. External connections can be made to any GPIO except for GPIOs in the range 6-11, 16, or 17. GPIOs 6-11 are
connected to the module’s integrated SPI flash and PSRAM. GPIOs 16 and 17 are connected to the module’s
integrated PSRAM. For details, please see Chapter 6 Schematics.

Espressif Systems

9

ESP32-WROVER Datasheet V2.2

5. Electrical Characteristics

5. Electrical Characteristics
5.1 Absolute Maximum Ratings
Stresses beyond the absolute maximum ratings listed in the table below may cause permanent damage to the
device. These are stress ratings only, and do not refer to the functional operation of the device that should follow
the recommended operating conditions.
Table 5: Absolute Maximum Ratings
Symbol

Parameter

Min

Max

Unit

VDD33

Power supply voltage

–0.3

3.6

V

Cumulative IO output current

-

1,100

mA

Storage temperature

–40

150

°C

Ioutput

1

Tstore

1. The module worked properly after a 24-hour test in ambient temperature at 25 °C, and the IOs in three domains
(VDD3P3_RTC, VDD3P3_CPU, VDD_SDIO) output high logic level to ground. Please note that pins occupied by flash
and/or PSRAM in the VDD_SDIO power domain were excluded from the test.
2. Please see Appendix IO_MUX of ESP32 Datasheet for IO’s power domain.

5.2 Recommended Operating Conditions
Table 6: Recommended Operating Conditions
Symbol

Parameter

Min

Typical

Max

Unit

VDD33

-

2.3

3.3

3.6

V

IV DD

Current delivered by external power supply

0.5

-

-

A

T

Operating temperature

–40

-

85

°C

5.3 DC Characteristics (3.3 V, 25 °C)
Table 7: DC Characteristics (3.3 V, 25 °C)
Symbol
CIN
VIH

Parameter

Min

Pin capacitance

-

High-level input voltage

0.75×VDD

1

Typ

Max

2

-

-

Unit
pF
1

VDD +0.3

V
1

VIL

Low-level input voltage

–0.3

-

0.25×VDD

IIH

High-level input current

-

-

50

nA

IIL

Low-level input current

-

-

50

nA

-

-

VOH
VOL

High-level output voltage

0.8×VDD

Low-level output voltage
High-level source current
1

IOH

1

(VDD = 3.3 V, VOH >= 2.64 V,
output drive strength set to the
maximum)

Espressif Systems

V

V
1

-

-

0.1×VDD

V

VDD3P3_CPU power domain

1, 2

-

40

-

mA

VDD3P3_RTC power domain

1, 2

-

40

-

mA

-

20

-

mA

VDD_SDIO power domain 1, 3

10

ESP32-WROVER Datasheet V2.2

5. Electrical Characteristics

Symbol

Parameter

Min

Typ

Max

Unit

-

28

-

mA

Low-level sink current
(VDD1 = 3.3 V, VOL = 0.495 V,

IOL

output drive strength set to the maximum)
RP U

Resistance of internal pull-up resistor

-

45

-

kΩ

RP D

Resistance of internal pull-down resistor

-

45

-

kΩ

VIL_nRST

Low-level input voltage of CHIP_PU to power off the chip

-

-

0.6

V

Notes:
1. Please see Appendix IO_MUX of ESP32 Datasheet for IO’s power domain. VDD is the I/O voltage for a particular power
domain of pins.
2. For VDD3P3_CPU and VDD3P3_RTC power domain, per-pin current sourced in the same domain is gradually reduced
from around 40 mA to around 29 mA, VOH >=2.64 V, as the number of current-source pins increases.
3. Pins occupied by flash and/or PSRAM in the VDD_SDIO power domain were excluded from the test.

5.4 Wi-Fi Radio
Table 8: Wi-Fi Radio Characteristics
Parameter
Operating frequency range
Output impedance
TX power

note2

note3

Sensitivity

Adjacent channel rejection

note1

Condition

Min

Typical

Max

Unit

-

2412

-

2484

MHz

-

-

See note 2

-

Ω

11n, MCS7

12

13

14

dBm

11b mode

17.5

18.5

20

dBm

11b, 1 Mbps

-

–98

-

dBm

11b, 11 Mbps

-

–89

-

dBm

11g, 6 Mbps

-

–92

-

dBm

11g, 54 Mbps

-

–74

-

dBm

11n, HT20, MCS0

-

–91

-

dBm

11n, HT20, MCS7

-

–71

-

dBm

11n, HT40, MCS0

-

–89

-

dBm

11n, HT40, MCS7

-

–69

-

dBm

11g, 6 Mbps

-

31

-

dB

11g, 54 Mbps

-

14

-

dB

11n, HT20, MCS0

-

31

-

dB

11n, HT20, MCS7

-

13

-

dB

1. Device should operate in the frequency range allocated by regional regulatory authorities. Target operating frequency
range is configurable by software.
2. For the modules that use IPEX antennas, the output impedance is 50 Ω. For other modules without IPEX antennas,
users do not need to concern about the output impedance.
3. Target TX power is configurable based on device or certification requirements.

Espressif Systems

11

ESP32-WROVER Datasheet V2.2

5. Electrical Characteristics

5.5 BLE Radio
5.5.1 Receiver
Table 9: Receiver Characteristics – BLE
Parameter

Conditions

Min

Typ

Max

Unit

Sensitivity @30.8% PER

-

-

–97

-

dBm

Maximum received signal @30.8% PER

-

0

-

-

dBm

Co-channel C/I

-

-

+10

-

dB

F = F0 + 1 MHz

-

–5

-

dB

F = F0 – 1 MHz

-

–5

-

dB

F = F0 + 2 MHz

-

–25

-

dB

F = F0 – 2 MHz

-

–35

-

dB

F = F0 + 3 MHz

-

–25

-

dB

F = F0 – 3 MHz

-

–45

-

dB

30 MHz ~ 2000 MHz

–10

-

-

dBm

2000 MHz ~ 2400 MHz

–27

-

-

dBm

2500 MHz ~ 3000 MHz

–27

-

-

dBm

3000 MHz ~ 12.5 GHz

–10

-

-

dBm

-

–36

-

-

dBm

Adjacent channel selectivity C/I

Out-of-band blocking performance

Intermodulation

5.5.2 Transmitter
Table 10: Transmitter Characteristics – BLE
Parameter

Conditions

Min

Typ

Max

Unit

RF transmit power

-

-

0

-

dBm

Gain control step

-

-

3

-

dBm

RF power control range

-

–12

-

+9

dBm

F = F0 ± 2 MHz

-

–52

-

dBm

F = F0 ± 3 MHz

-

–58

-

dBm

F = F0 ± > 3 MHz

-

–60

-

dBm

∆ f 1avg

-

-

-

265

kHz

∆ f 2max

-

247

-

-

kHz

∆ f 2avg /∆ f 1avg

-

-

–0.92

-

-

ICFT

-

-

–10

-

kHz

Drift rate

-

-

0.7

-

kHz/50 µs

Drift

-

-

2

-

kHz

Adjacent channel transmit power

Espressif Systems

12

ESP32-WROVER Datasheet V2.2

5. Electrical Characteristics

Temperature (℃)

5.6 Reflow Profile

Peak Temp.
235 ~ 250℃

250
Preheating zone
150 ~ 200℃
60 ~ 120s

217
200

Reflow zone
!217℃ 60 ~ 90s

Cooling zone
-1 ~ -5℃/s

Soldering time
> 30s
Ramp-up zone
1 ~ 3℃/s
100

50
25

Time (sec.)

0
0

50

100

150

200

250

Ramp-up zone — Temp.: <150℃ Time: 60 ~ 90s Ramp-up rate: 1 ~ 3℃/s
Preheating zone — Temp.: 150 ~ 200℃ Time: 60 ~ 120s Ramp-up rate: 0.3 ~ 0.8℃/s
Reflow zone — Temp.: >217℃ 7LPH60 ~ 90s; Peak Temp.: 235 ~ 250℃ (<245℃ recommended) Time: 30 ~ 70s
Cooling zone — Peak Temp. ~ 180℃ Ramp-down rate: -1 ~ -5℃/s
Solder — Sn&Ag&Cu Lead-free solder (SAC305)

Figure 2: Reflow Profile

Espressif Systems

13

ESP32-WROVER Datasheet V2.2

5

4

3

2

1

6. Schematics

D

D

ESP32 Module:
with 1.8V Flash & SRAM

Pin.1
GND

Pin.15
GND

Pin.38
GND

GND

The BLUE netname means 1.8V.

GND

GND XOUT
2

GND
XIN

U1

3

4

GND

GND

1

Espressif Systems

6. Schematics

C1
22pF/6.3V(10%)

The values of C1 and C2 vary with
the selection of a crystal.

D1
ESD3.3V88D-LCDN

Pin.2
VDD33

Pin.16
IO13

VDD33

GND

Pin.37
IO23

GPIO13

GND

GPIO23

C2
22pF/6.3V(10%)

Pin.3
CHIP_PU/EN

VDD33

Pin.17
SD2

CHIP_PU

Pin.36
IO22
SHD/SD2

GPIO22

C3
GND

100pF/6.3V(10%)

R1

VDD33
GND

C6

C9

10nF/6.3V(10%)

GND
40MHz+/-10ppm

20K(5%)

GPIO21
U0TXD
U0RXD
GPIO22
GPIO19

C5
3.3nF/6.3V(10%)

0.1uF/6.3V(10%)
GND

J39

GND

GND
ANT1
1
2

C11

C10

R15

GND

0R(5%)

GND
C14

PCB ANT

GND

TBD

C15

L4

C16

TBD

TBD

270pF/6.3V(10%)
C17

GND

GND

GND

270pF/6.3V(10%)

14

1
2
3
4
SENSOR_VP 5
6
7
SENSOR_VN8
CHIP_PU
9
10
GPIO34
11
GPIO35
12
GPIO32

VDD33

VDDA
LNA_IN
VDD3P3
VDD3P3
SENSOR_VP
SENSOR_CAPP
SENSOR_CAPN
SENSOR_VN
CHIP_PU
VDET_1
VDET_2
32K_XP

U2
R12

0R(5%)

Pin.35
TXD0
SWP/SD3

Pin.5
SENSOR_VN

U0TXD

Pin.19
CMD

SENSOR_VN

Pin.34
RXD0
SCS/CMD

U0RXD

C

GND

GPIO23
GPIO18
GPIO5
SD_DATA_1
SD_DATA_0
SD_CLK
SD_CMD
SD_DATA_3
SD_DATA_2
GPIO17
VDD_SDIO
GPIO16

36
35
34
33
32
31
30
29
28
27
26
25

GPIO23
GPIO18
GPIO5
SDI/SD1
SDO/SD0
SCK/CLK
SCS/CMD
SWP/SD3
SHD/SD2
GPIO17
GPIO16
VDD_SDIO

C18

Pin.6
IO34

Pin.20
CLK
FLASH_CLK

GPIO34

Pin.7
IO35

GPIO21

Pin.21
SD0
GPIO35

Pin.32
NC
SDO/SD0

Pin.8
IO32

Pin.22
SD1
GPIO32

C24

Pin.33
IO21

Pin.31
IO19
SDI/SD1

GPIO19

4.7uF/16V(10%) 2K(5%)

ESP32-D0WDQ6
GND

SCK/CLK

Pin.18
SD3

SENSOR_VP

0.1uF/6.3V(10%)

32K_XN
GPIO25
GPIO26
GPIO27
MTMS
MTDI
VDD3P3_RTC
MTCK
MTDO
GPIO2
GPIO0
GPIO4

The values of C14, L4 and C15 vary with
the actual selection of a PCB board.

C4

48
47
46
45
44
43
42
41
40
39
38
37

GND

C12

10uF/6.3V(10%) 10uF/6.3V(10%) 1uF/10V(20%) 0.1uF/6.3V(10%)

13
14
15
16
17
18
19
20
21
22
23
24

3

2

C13

R14 0R(5%)/NC

1

49

GND
IPEX

C

CAP1
CAP2
VDDA
XTAL_P
XTAL_N
VDDA
GPIO21
U0TXD
U0RXD
GPIO22
GPIO19
VDD3P3_CPU

VDD33

Pin.4
SENSOR_VP

GND

VDD33

Pin.9
IO33

FLASH_CLK

Pin.23
IO15
GPIO33

Pin.30
IO18
GPIO15

GPIO18

0R(5%)(NC)
GPIO17

R13

0R(5%)

GPIO13
GPIO15
GPIO2
GPIO0
GPIO4

GPIO33
GPIO25
GPIO26
GPIO27
GPIO14
GPIO12

C19
R11

0.1uF/6.3V(10%)

Pin.10
IO25

GND

SRAM_CLK

Pin.24
IO2
GPIO25

B

Pin.29
IO5
GPIO2

GPIO5

Pin.11
IO26

B

Pin.28
NC
GPIO26

VDD_SDIO

VDD_SDIO

Pin.12
IO27

SHD/SD2

7

U3

8

1

FLASH_CLK 6

/CS
CLK
/HOLD
FLASH

GND

SCS/CMD

VCC

R10

Pin.27
NC
GPIO27

10K(5%)
DI
DO
/WP

5

SDI/SD1

2

SDO/SD0

3

SWP/SD3

U4
1
2
3
4

GPIO16
SDO/SD0
SWP/SD3

CS#
VDD
SO/SIO1 SIO3
SIO2
SCLK
VSS
SI/SIO0

8
7
6
5

SHD/SD2
SRAM_CLK
SDI/SD1

Pin.13
IO14

Pin.26
IO4

VDD33
GPIO14

GPIO4

PSRAM

4

ESP32-WROVER Datasheet V2.2

VDD_SDIO

R9
GND

Pin.14
IO12

GND

10K(5%)
GPIO12

Pin.39
GND

Pin.25
IO0
GND

GPIO0

Figure 3: Schematics of ESP32-WROVER

A

A

Title

ESP32-WROVER-V4
Size

C
Date:

5

4

3

2

Document Number

Rev

<Doc>
Wednesday, November 14, 2018

Sheet

1

of

1

1
Espressif

Systems

7. Peripheral Schematics

7. Peripheral Schematics

U1

R1
C1

C2

TBD

0.1uF/50V(10%)

22uF/25V(10%)

GND

C3
TBD

GND

EN
GPI36 SENSOR_VP
GPI39 SENSOR_VN
GPI34
GPI35
GPIO32
GPIO33
GPIO25
GPIO26
GPIO27
GPIO14
GPIO12
GND
GPIO13
SD2
SD3
CMD

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19

GND1
3V3
EN
SENSOR_VP
SENSOR_VN
IO34
IO35
IO32
IO33
IO25
IO26
IO27
IO14
IO12
GND2
IO13
SD2
SD3
CMD

P_GND
GND3
IO23
IO22
TXD0
RXD0
IO21
NC
IO19
IO18
IO5
NC2
NC1
IO4
IO0
IO2
IO15
SD1
SD0
CLK

VDD33

39
38
37
36
35
34
33
32
31
30
29
28
27
26
25
24
23
22
21
20

GND
GPIO23
GPIO22
TXD0
RXD0
GPIO21

JP1

1
2
3
4

GPIO19
GPIO18
GPIO5

1
2
3
4
UART

GND

GPIO4
GPIO0
GPIO2
GPIO15
SDI
SDO
SCK

1
2

GND

GND

1
2

VDD33

JP2
Boot Option

SW1
R2

C4

0R(5%)

JP3

EN

1
2
3
4

0.1uF/50V(10%)

1
2
3
4

GPIO14
GPIO12
GPIO13
GPIO15

MTMS
MTDI
MTCK
MTDO

JTAG
GND

Figure 4: Peripheral Schematics of ESP32-WROVER

Note:
• Soldering Pad 39 to the Ground of the base board is not necessary for a satisfactory thermal performance. If users
do want to solder it, they need to ensure that the correct quantity of soldering paste is applied.
• To ensure the power supply to the ESP32 chip during power-up, it is advised to add an RC delay circuit at the
EN pin. The recommended setting for the RC delay circuit is usually R = 10 kΩ and C = 0.1 µF. However, specific
parameters should be adjusted based on the power-up timing of the module and the power-up and reset sequence
timing of the chip. For ESP32’s power-up and reset sequence timing diagram, please refer to Section Power Scheme
in ESP32 Datasheet.

Espressif Systems

15

ESP32-WROVER Datasheet V2.2

7. Peripheral Schematics

Discharge Circuit

VCC

1

2

SW1

CAP Added By User

D1

VDD33
Q1

5

+ C1

Bulk CAP

4

ESP
Module
3

R2

R1
100K

1K

GND

GND

GND

GND

Figure 5: Discharge Circuit for VDD33 Rail

Note:
The discharge circuit can be applied in scenarios where ESP32 is powered on and off repeatedly by switching the
power rails, and there is a large capacitor on the VDD33 rail. For details, please refer to Section Power Scheme in
ESP32 Datasheet.

U1
GND
VBAT

R1

0R

3

1

GND

2

CHIP_PU

VCC
RESET#

Power Supply Supervisor

R2
100K

GND

Figure 6: Reset Circuit
Note:
When battery is used as the power supply for ESP32 series of chips and modules, a supply voltage supervisor is recommended to avoid boot failure due to low voltage. Users are recommended to pull CHIP_PU low if the power supply for
ESP32 is below 2.3 V.

Espressif Systems

16

ESP32-WROVER Datasheet V2.2

8. Physical Dimensions

Espressif Systems

8. Physical Dimensions

ESP32-WROVER PCB/IPEX DIMENSIONS

3.30±0.10

Unit: mm

Module Thickness

Module Width
18.00±0.10

6.00±0.10

18.00±0.10

0.90±0.10

PCB Thickness

Antenna Area

0.45±0.10

2.15±0.10
10.45±0.10

22.86±0.10

23.05±0.10

4.00±0.10
5.60±0.10
14.15±0.10

24.10±0.10

20.35±0.10

4.00±0.10

31.40±0.10

17

Module Length

0.80±0.10

1.27±0.10

0.9±0.10

15.85±0.10
1.27±0.10

1.10±0.10

ESP32-WROVER Datasheet V2.2

0.85±0.10

Top View

Side View

Figure 7: Physical Dimensions of ESP32-WROVER

Bottom View

9. Recommended PCB Land Pattern

9. Recommended PCB Land Pattern

Unit: mm
Via for thermal pad
Copper

6.30

18.00

1

38

31.40

5.00

0.90

5.00

1.33

Antenna Area

2.00

1.27

16.46

1.33

8.00
20

19

1.10

0.50

Figure 8: Recommended PCB Land Pattern of ESP32-WROVER

Espressif Systems

18

ESP32-WROVER Datasheet V2.2

10. U.FL Connector Dimensions

10.

U.FL Connector Dimensions
Unit: mm

Figure 9: U.FL Connector Dimensions

Espressif Systems

19

ESP32-WROVER Datasheet V2.2

11. Learning Resources

11.

Learning Resources

11.1

Must-Read Documents

The following link provides documents related to ESP32.
• ESP32 Datasheet
This document provides an introduction to the specifications of the ESP32 hardware, including overview, pin
definitions, functional description, peripheral interface, electrical characteristics, etc.
• ESP-IDF Programming Guide
It hosts extensive documentation for ESP-IDF ranging from hardware guides to API reference.
• ESP32 Technical Reference Manual
The manual provides detailed information on how to use the ESP32 memory and peripherals.
• ESP32 Hardware Resources
The zip files include the schematics, PCB layout, Gerber and BOM list of ESP32 modules and development
boards.
• ESP32 Hardware Design Guidelines
The guidelines outline recommended design practices when developing standalone or add-on systems
based on the ESP32 series of products, including the ESP32 chip, the ESP32 modules and development
boards.
• ESP32 AT Instruction Set and Examples
This document introduces the ESP32 AT commands, explains how to use them, and provides examples of
several common AT commands.
• Espressif Products Ordering Information

11.2

Must-Have Resources

Here are the ESP32-related must-have resources.
• ESP32 BBS
This is an Engineer-to-Engineer (E2E) Community for ESP32 where you can post questions, share knowledge,
explore ideas, and help solve problems with fellow engineers.
• ESP32 GitHub
ESP32 development projects are freely distributed under Espressif’s MIT license on GitHub. It is established
to help developers get started with ESP32 and foster innovation and the growth of general knowledge about
the hardware and software surrounding ESP32 devices.
• ESP32 Tools
This is a webpage where users can download ESP32 Flash Download Tools and the zip file ”ESP32 Certification and Test”.
• ESP-IDF
This webpage links users to the official IoT development framework for ESP32.
• ESP32 Resources
This webpage provides the links to all available ESP32 documents, SDK and tools. �����������

Espressif Systems

20

ESP32-WROVER Datasheet V2.2

Revision History

Revision History
Date

Version

Release notes
• Added Moisture sensitivity level (MSL) 3 in Table 2 ESP32-WROVER Speciﬁcations;
• Added notes about ”Operating frequency range” and ”TX power” under Table

2019.09

V2.2

8 Wi-Fi Radio Characteristics;
• Updated Section 7 Peripheral Schematics and added a note about RC delay
circuit under it;
• Updated Figure 9 Recommended PCB Land Pattern.

2019.01

V2.1

Added a note on the use of GPIO12 under Table 3, as well as in Section 4;
Changed the RF power control range in Table 10 from –12 ~ +12 to –12 ~ +9 dBm.
Updated the recommended operating temperature from –40 °C ~ 65 °C to –40 °C

2018.11

V2.0

~ 85 °C.

Updated Chapter 6: Schematics, where C18 is changed from a 1 µF capacitor to a
4.7 µF capacitor.

2018.10

V1.9

Added ”Cumulative IO output current” entry to Table 5: Absolute Maximum Ratings;
Added more parameters to Table 7: DC Characteristics.
• Added certifications and reliability test items the module has passed in Table 2:
ESP32-WROVER Specifications, and removed software-specific information;
• Updated Section 3.4: RTC and Low-Power Management;
• Changed the module’s dimensions from (18±0.15) mm x (31.4 ±0.2) mm x
(3.5±0.15) mm to (18.00±0.10) mm x (31.40±0.10) mm x (3.30±0.10) mm;

2018.08

V1.8

• Updated Figure 8: Physical Dimensions;
• Updated Chapter 6: Schematics;
• Changed the recommended operating temperature from –40°C ~ 85°C to –
40°C ~ 65°C and added a note to custom order of ESP32-WROVER with high
temperature range;
• Corrected a typo in Electrical Characteristics section;
• Updated Table 8: Wi-Fi Radio.
• Updated the capacity of PSRAM from 32 Mbit to 64 Mbit;
• Deleted Temperature Sensor in Table 2: ESP32-WROVER Specifications;
• Updated Chapter 3: Functional Description;
• Updated Chapter 6: Schematics;
• Added Chapter 9: Recommended PCB Land Pattern;

2018.06

V1.7

Changes to electrical characteristics:
• Updated Table 5: Absolute Maximum Ratings;
• Added Table 6: Recommended Operating Conditions;
• Added Table 7: DC Characteristics;
• Updated the values of ”Gain control step”, ”Adjacent channel transmit power”
in Table 10: Transmitter Characteristics - BLE.

2018.03

V1.6

Corrected typos in Table 3 Pin Definitions.

2018.03

V1.5

Updated Table 2 in Chapter 1.

2018.03

V1.4

Espressif Systems

Updated Chapter 6 Schematics;
Updated Chapter 8 Dimensions.

21

ESP32-WROVER Datasheet V2.2

Revision History

Date

Version

Release notes
Updated section 3.4 RTC and Low-Power Management;

2018.01

V1.3

Deleted information on LNA pre-amplifier;
Updated section 3.4 RTC and Low-Power Management;
Updated the ESP32-WROVER schematics in Chapter 6;
Added a note in Chapter 7;
Added the U.FL dimensions (Figure 10).
Updated the description of the chip’s system reset in Section 2.3 Strapping Pins;
Deleted ”Association sleep pattern” in Table ”Power Consumption by Power Modes”

2017.10

V1.2

and added notes to Active-sleep and Modem-sleep;
Added a note to Output Impedance in Table 8;
Updated the notes to Figure 4 Peripheral Schematics.
Updated Section 2.1 Pin Layout;

2017.09

V1.1

Updated the ESP32-WROVER Schematics and dded a note in Chapter 7;
Added Chapter 8 Dimensions.

2017.08

V1.0

Espressif Systems

First release.

22

ESP32-WROVER Datasheet V2.2


