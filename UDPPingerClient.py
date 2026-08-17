import socket
import time

SERVER_NAME = "192.168.1.183"
SERVER_PORT = 13000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)
NUM_PACKETS = 10

rtt_array = []
try:
    for sequence in range(1, NUM_PACKETS + 1):
        message = f"Packet {sequence} | timestamp {time.time():.2f}"
        try:
            start_time = time.perf_counter()
            client_socket.sendto(message.encode(), (SERVER_NAME, SERVER_PORT))
            received_message, server_address = client_socket.recvfrom(1024)
            end_time = time.perf_counter()
            rtt = (end_time - start_time) * 1000
            print(f"Message from {server_address}: {received_message.decode()} |  RTT: {rtt:.3f}ms")
            rtt_array.append(rtt)
        except socket.timeout:
            print(f"Packet {sequence} timed out")
        except OSError as e:
            print(f"Packet {sequence} failed: {e}")
finally:
    client_socket.close()

packets_received = len(rtt_array)
if packets_received > 0:
    avg_rtt = sum(rtt_array) / packets_received
    lost_packets_percentage = (NUM_PACKETS - packets_received) / NUM_PACKETS * 100
    print("---Statistics---")
    print(f"{NUM_PACKETS} packets sent, {packets_received} received, {lost_packets_percentage:.2f}% packet loss")
    print(f"Min RTT: {min(rtt_array):.3f}ms | Max RTT: {max(rtt_array):.3f}ms | Avg RTT: {avg_rtt:.3f}ms")




