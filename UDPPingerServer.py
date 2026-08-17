# UDPPingerServer.py

# We will need the following module to generate randomized lost packets
import random
import sys
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind(('', 13000))

# Set a timeout so recvfrom doesn't block forever
# This allows the program to periodically check for Ctrl+C
serverSocket.settimeout(1.0)  # check for interrupt

print("Server is now running and ready to accept ping requests on port 12000")
print("Press Ctrl+C to stop the server\n")

try:
    while True:
        try:
            # Generate random number in the range of 0 to 10
            rand = random.randint(0, 10)

            # Receive the client packet along with the address it is coming from
            # This will now timeout after 1 second if no data received
            message, address = serverSocket.recvfrom(1024)
            
            # Print received ping for debugging/visibility
            print(f"Received ping from {address}")

            # Capitalize the message from the client
            message = message.upper()

            # If rand is less than 4, we consider the packet lost and do not respond
            if rand < 4:
                print(f"  -> Packet intentionally dropped (rand={rand})")
                continue

            # Otherwise, the server responds
            serverSocket.sendto(message, address)
            print(f"  -> Response sent to {address} (rand={rand})")
            
        except timeout:
           # This exception occurs when NO packet has arrived within the timeout period
            continue
            
except KeyboardInterrupt:
    print("\nServer shutting down...")
    serverSocket.close()
    sys.exit(0)