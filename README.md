# MITM-SDR
An SDR based GNURadio client-side exploit/malware which injects itself between two SDR communications to provide reverse shell to the attacker SDR.

### DESCRIPTION
This exploit/malware infects the GNURadio python files to change the UDP ports of Source and Sinks and also changes the Center Frequency of Osmocom, LimeSDR and USRP Sinks allowing the attacker SDR to inject between the two SDR communicating devices and provide a reverse shell to the attacker.

### ASSUMPTIONS
* Victim SDRs and the attacker SDR must all be full duplex.
* The victim SDR communication uses GNURadio and the python file generated from grc running on a Linux system.
* The exploit/malware has sudo access to the victim Linux system.
* The GNURadio program used for victim communication is OFDM message transfer having strictly one UDP Source and UDP Sink to pipe the text message to the terminal.

### SCHEMATICS
![MITM SDR SCHEMATICS IMAGE (CLICK TO VIEW)](https://github.com/Shreyas-Penkar/MITM-SDR/blob/main/mitm_sdr.png?raw=true)

### DIRECTORY STRUCTURE

  * **attacker** folder consists of the python scripts which the attacker system has to run in order to operate the reverse shell obtained.
```  
  attacker
  |
  |__ trx_ofdm.py -> The attacker SDR GNURadio OFDM text transfer script to operate the reverse shell and to forward the text recieved from victim to second victim to allow MITM between two devices.
  |
  |__ reverse_shell.py -> The script to operate the reverse shell program along with trx_ofdm.py
  |
  |__ udp_sink.py -> The script to diffrentiate between the messages sent by the victim as reverse shell output or messages intended for second victim.
                     The script uses the "%@#" notation to filter the messages and react accordingly.
```

  * **victim** folder consists of the python scripts which the victim systems has to run to communicate with other victim systems.
```
  victim
  |
  |__ trx_ofdm.py -> A SDR GNURadio text message transfer program which uses OFDM and UDP Source/Sinks for full duplex text transfer between devices.
  |
  |__ udp_source.py -> Python script to communicate text to UDP Source in trx_ofdm.py program.
  |
  |__ udp_sink.py -> Python script to communicate text to UDP Sink in trx_ofdm.py program.
```

  * **exploit** folder consists of the python scripts which the attacker will send the victim systems to be run so that the victim systems get infected and provide reverse shell.
```
  exploit
  |
  |__ exploit.py -> The main exploit program which will infect the target's machine and provide reverse shell (explained in detail below)
  |
  |__ attacker_udp_sink.py -> A malicious udp_sink injector which injects between the UDP Sink connection to filter the messages and run the commands   sent by the attacker system and return an output back to attacker SDR.
  
```

### EXPLANATION
* The environment starts with two Linux machines, each with an connected full duplex SDR, running the **trx_ofdm.py** script for OFDM text communication with each other. Suppose Victim 1 transmits at 1GHz and receives at 2 GHz and Victim - 2 transmits at 2GHz and receives at 1 GHz. **udp_source.py** and **udp_sink.py** are used to send and receive text messages respectively.

* The attacker environment begins with runnning **trx_ofdm.py** script for OFDM text communication, running **reverse_shell.py** to operate the reverse shell and **udp_sink.py** to recieve the text from trx_ofdm.py.The attacker SDR transmits at 1GHz and receives at 1.5 GHz.

* So basically before exploit
```
Victim-1 : T:1Ghz R:2Ghz
Victim-2 : T:2Ghz R:1Ghz
Attacker : T:1Ghz (while retransmission) / 2Ghz (for reverse shell) R:1.5GHz  
```
* Then the exploit file (**exploit.py**) is obfuscated into a useful application and is sent to Victim - 1 who runs the files with sudo privileges.
* The exploit.py file runs and installs **attacker_udp_sink.py** onto the system.

* The exploit infects the GNURadio python library files, and changes the udp sink ports, osmocom, limeSDR and USRP sink center frequencies in such a way that the Victim - 1 transmit frequency is changed from 1Ghz to 1.5 Ghz which means that all data is now routed to attacker SDR instead of Victim - 2 causing a Man in the Middle condition (see figure).

* Now if Victim - 1 sends a text for transmission, it will be recieved by attacker SDR which will check whether the text is a message or a reverse shell output. The string "%@#" is added at the start of every reverse shell command or reverse shell output. If the recieved text is a message, then it is retransmitted to Victim - 2 as it is a message sent by Victim - 1. If the text is a reverse shell output, **the udp_sink.py** sends it to **reverse_shell.py** for viewing.
* If Victim - 2 sends a message to Victim - 1 it is directly transmitted to Victim - 1 without any breaks.
* This makes the communication continous as we are only intercepting Victim - 1 messages and retransmitting them.

* So basically after exploit (Victim -1 transmission frequency is changed by exploit)
```
Victim-1 : T:**1.5Ghz** R:2Ghz
Victim-2 : T:2Ghz R:1Ghz
Attacker : T:1Ghz (while retransmission) / 2Ghz (for reverse shell) R:1.5GHz 
```
* Now when reverse shell is to be used, the transmission frequency is changed to 2Ghz and the command is sent to Victim-1. Due to the exploit, the **attacker_udp_sink.py** intercepts the **trx_ofdm.py** and **udp_sink.py** communication. **attacker_udp_sink.py** checks whether the text is a message or a reverse shell command. If the recieved text is a message, then it is sent to udp_sink for viewing as it is a message sent by Victim - 2. If the text is a reverse shell output, **attacker_udp_sink.py** executes the shell command and sends the output for transmission to Attacker SDR.

* In this way, the Victim-Victim communicaion is preserved with stealth, and reverse shell is also obtained since we intercept all messages from Victim-1 and MITM with reverse shell is established.

### exploit.py Details
* The exploit starts with checking sudo privileges if granted.
* Then it runs ```netstat -nvlop | grep udp``` to find all the udp bind ports on the system. One of those bind ports has to be the UDP source bind port used by **trx_ofdm.py** which is useful to us. The exploit grabs the PID of that process and locates the python file using ```ps -ef -q <PID>``` and ```pwdx <PID>```
* Once the python file is located, the exploit opens the file and checks if udp_source, udp_port, any one of these -(Osmocom sink,LimeSDR sink,or USRP sink) is present or not. If yes, then this is the file we were looking for, and the exploit breaks out of the for loop intended to repeat the above process for all PIDs obtained after running ```netstat -nvlop | grep udp``` (since, there could be multiple programs on the system using udp communication, so we need to find which PId corresponds to **trx_ofdm.py**)
* The exploit does not edit trx_ofdm.py since it would br very suspicious if the source code is changed, instead we will infect the library files of GNURadio so that we can achieve MITM without alerting the victim.
* The GNURadio library files are located in ```/usr/lib/python3/dist-packages/gnuradio```.
* Inside this directory the udp sink ports were changed in the file ```blocks/blocks_swig6.py``` and usrp center frequency was changed in the file ```uhd/uhd_swig.py```
* LimeSDR center frequency was changed in ```/usr/lib/python3/dist-packages/limesdr/limesdr_swig.py```
* Osmocom center frequency was changed in ```/usr/lib/python3/dist-packages/osmosdr/osmosdr_swig.py```
* After infecting the above library files, the exploit kills the trx_ofdm.py process using its PID by ```kill -9 <PID>```
* Then the exploit launches the **attacker_udp_sink.py** under the name ```tmp/config-err-P5f3YDS``` and launches it. This file is responsible for the interception of udp communication between **trx_ofdm.py** and **udp_sink.py** enabling us to run reverse shell.
* Then the exploit relaunches the target process trx_ofdm.py using its path. Now the library files are infected, so the program will have changed its udp ports and SDR transmission frequency allowing MITM and reverse shell.

### How to Run
* Obtain 3 full duplex SDRs (LimeSDR, USRP, BladeRF) and connect them to 3 Linux machines (1 each).
* On two of the machines run ```sudo apt-get install gnuradio``` and also install drivers for that SDR device.
* clone the repository on all machines by running ```git clone https://github.com/Shreyas-Penkar/MITM-SDR```
* For the two victim devices open ```gnuradio-companion``` and select your SDR device as the Source and Sink. (3 options have been provided in the **trx_ofdm.grc** flowgraph)
* Make sure you have set the SDR Source and Sink Frequencies correctly for the two Machines.
* Run the flowgraph and run ```python3 udp_sink.py``` and ```python3 udp_source.py``` in two terminals.
* Now you have 2 SDR connected machines communicating to each other.
* On third machine run the trx_ofdm.grc flowgrapgh after select your SDR device as the Source and Sink. Also run ```python3 udp_sink.py``` and ```python3 reverse_shell.py``` in two terminals. Now the attacker has been set up.
* Now on one of the victim machines, run ```pytohn3 exploit.py``` file or ```./exploit``` or the obfuscated file.
* Now you should receive a working reverse shell on **reverse_shell.py**.
