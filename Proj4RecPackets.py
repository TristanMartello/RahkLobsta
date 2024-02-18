import socket
import keyboard

# UDP_IP = "10.245.158.11"    # pi's address on Tufts Wireless JCC
# UDP_IP = "10.245.145.164"     # pi's address on Tufts Wireless Nolop
UDP_IP = "10.0.0.239"  # pi's address on Old Men 2
# UDP_IP = "10.245.157.202"

UDP_PORT = 5005          # Pi's port?
message = "yeeee haw"

#selfIp = "10.245.151.150"
selfIp = "10.0.0.145"    # Home IP address
# selfIp = "10.245.39.73"  # Nolop Tufts_Secure
# selfIp = "10.245.154.176"  # Nolop Tufts_Wireless


keyList = ["up", "left", "right", "down", "h", "z", "q"]
actionList = ["backward", "left", "right", "forward", "headlights", "hazards", "quit"]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", UDP_PORT))
# sock.bind((UDP_IP, UDP_PORT))

status = "halt"

while True:
    data, addr = sock.recvfrom(1024)
    data = str(data)[2:-1]

    if data == "request":
        sock.sendto(bytes(status, "utf-8"), (UDP_IP, UDP_PORT))

    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:
        if event.name in keyList:
            status = actionList[keyList.index(event.name)]
        else:
            print("unknown key press")

    if event.event_type == keyboard.KEY_UP:
        if event.name == "up" or event.name == "down" or event.name == "left" or event.name == "right":
            status = "halt"
