# KL9005s
python script to read/write and list available commands

You find this reader when searching for uhf rfid reader on chinese warehouse sites.
Characteristic: 2 sample cards,  ISO18000-6B, ISO18000-6C (EPC C1G2) protokoll tag; 902-928 MHz zocorfid
With ~ 45€ it is the cheapest one you can usualy get.
It comes with windows only software, commands hidden in dll, which does not help on linux.
But since it communicates via USB seriel adapter, there is not much magic that can hide.

Shows up as
 CP2102 USB to UART Bridge Controller:
   Product ID:	0xea60
   Vendor ID:	0x10c4  (Silicon Laboratories, Inc.)
  
![Software](https://github.com/bosb/KL9005s/blob/master/images/software.jpg?raw=true "Software")

## Innards

![back_antenna.jpg](https://github.com/bosb/KL9005s/blob/master/images/back_antenna.jpg?raw=true "back_antenna.jpg")
![nxp_lpc2132fb064_csi_1s4acat1025w1](https://github.com/bosb/KL9005s/blob/master/images/nxp_lpc2132fb064_csi_1s4acat1025w1.jpg?raw=true "nxp_lpc2132fb064_csi_1s4acat1025w1")
![max942esa+735](https://github.com/bosb/KL9005s/blob/master/images/max942esa+735.jpg?raw=true "max942esa+735")
![adf7020bcpz_silabs_cp210dclqhx1745+](https://github.com/bosb/KL9005s/blob/master/images/adf7020bcpz_silabs_cp210dclqhx1745+.jpg?raw=true "adf7020bcpz_silabs_cp210dclqhx1745+")

