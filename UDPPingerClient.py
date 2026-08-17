import socket
import time

serverName = "192.168.1.183"
serverPort = 13000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.settimeout(1.0)

rttArray = []
packetsSent = 0

for sequence in range(1, 11):
    packetsSent += 1
    try:
        message = f"Packet {sequence} | timestamp {time.time():.2f}"
        startTime = time.perf_counter()
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        receivedMessage, serverAddress = clientSocket.recvfrom(1024)
        endTime = time.perf_counter()
        rtt = (endTime - startTime) * 1000
        print(f"Message from {serverAddress}: {receivedMessage.decode()} |  RTT: {rtt:.3f}ms")
        rttArray.append(rtt)
    except socket.timeout:
        print(f"Packet {sequence} timed out")
        continue

packetsReceived = len(rttArray)


if packetsReceived > 0:
    minRtt = min(rttArray)
    maxRtt = max(rttArray)
    rttSum = 0

    for i in range(packetsReceived):
        rttSum += rttArray[i]

    avgRtt = rttSum / packetsReceived

    lostPacketsPercentage = (packetsSent - packetsReceived) / packetsSent* 100
    print("---Statistics---")
    print(f"{packetsSent} packets sent, {packetsReceived} received, {lostPacketsPercentage:.2f}% packet loss")
    print(f"Min RTT: {minRtt:.3f}ms | Max RTT: {maxRtt:.3f}ms | Avg RTT: {avgRtt:.3f}ms")


clientSocket.close()


