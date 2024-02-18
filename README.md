# RahkLobsta
Code for both the computer transmitter and Raspberry Pi receiver for the Electronics and Controls final project. The challenge was to create a robot that could drive around remotely on both flat and inclined surfaces.

Proj4RecPackets.py is the main file for the computer. It constantly monitors which keys are being pressed and updates the status variable accordingly. Whenever it receives a "request" packet from the Pi, it sends back the current status.

PiCodeUpgraded.py is the main file for the Raspberry Pi. It requests status data from the computer, and manipulates the motors based on which instruction is received.
