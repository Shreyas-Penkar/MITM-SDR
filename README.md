# MITM-SDR
An SDR based GNURadio client-side exploit/malware which injects itself between two SDR communications to provide reverse shell to the attacker SDR.

### DESCRIPTION
This exploit/malware infects the GNURadio python files to change the UDP ports of Source and Sinks and also changes the Center Frequency of Osmocom, LimeSDR and USRP Sinks allowing the attacker SDR to inject between the two SDR communicating devices and provide a reverse shell to the attacker.
It also consists of a Linux based Rootkit to hide the malicious process and the rootkit itself, providing stealth to the attacker.

### ASSUMPTIONS
* Victim SDRs and the attacker SDR must all be full duplex.
* The victim SDR communication uses GNURadio and the python file generated from grc running on a Linux system.
* The exploit/malware has sudo access to the victim Linux system.
* The GNURadio program used for victim communication is OFDM message transfer having strictly one UDP Source and UDP Sink to pipe the text message to the terminal.

### EXPLANATION

### DIRECTORY STRUCTURE
```
  "attacker" folder consists of the python scripts which the attacker system has to run in order to operate the reverse shell obtained.
  |
  |__ trx_ofdm.py -> The attacker SDR GNURadio OFDM text transfer script to operate the reverse shell and to forward the text recieved from victim to     |                  second victim to allow MITM between two devices.
  |
  |__ reverse_shell.py -> The script to operate the reverse shell program along with trx_ofdm.py
  |
  |__ udp_sink.py -> The script to diffrentiate between the messages sent by the victim as reverse shell output or messages intended for second victim.
                     The script uses the "%@#" notation to filter the messages and react accordingly.


  "victim" folder consists of the python scripts which the victim systems has to run to communicate with other victim systems.
  |
  |__ trx_ofdm.py -> A SDR GNURadio text message transfer program which uses OFDM and UDP Source/Sinks for full duplex text transfer between devices.
  |
  |__ udp_source.py -> Python script to communicate text to UDP Source in trx_ofdm.py program.
  |
  |__ udp_sink.py -> Python script to communicate text to UDP Sink in trx_ofdm.py program.


  "exploit" folder consists of the python scripts which the attacker will send the victim systems to be run so that the victim systems get infected and   provide reverse shell.
  |
  |__ exploit.py -> The main exploit program which will infect the target's machine and provide reverse shell (explained in detail below)
  |
  |__ attacker_udp_sink.py -> A malicious udp_sink injector which injects between the UDP Sink connection to filter the messages and run the comands     |                           sent by the attacker system and return an output back to attacker SDR.
  
```
