import random
import sys
from socket import *

serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('', 13000))

serverSocket.settimeout(1.0)  # check for interrupt

print("Server is now running and ready to accept ping requests on port 12000")
print("Press Ctrl+C to stop the server\n")

try:
    while True:
        try:
            rand = random.randint(0, 10)
            message, address = serverSocket.recvfrom(1024)

            print(f"Received ping from {address}")
            message = message.upper()

            if rand < 4:
                print(f"  -> Packet intentionally dropped (rand={rand})")
                continue

            serverSocket.sendto(message, address)
            print(f"  -> Response sent to {address} (rand={rand})")
            
        except timeout:
            continue
            
except KeyboardInterrupt:
    print("\nServer shutting down...")
    serverSocket.close()
    sys.exit(0)