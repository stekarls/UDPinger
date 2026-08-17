import socket
import time

SERVER_NAME = "192.168.1.183"
SERVER_PORT = 13000
CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
CLIENT_SOCKET.settimeout(1.0)
NUM_PACKETS = 10

rtt_array = []
packets_sent = 0

for sequence in range(1, NUM_PACKETS + 1):
    packets_sent += 1
    try:
        message = f"Packet {sequence} | timestamp {time.time():.2f}"
        start_time = time.perf_counter()
        CLIENT_SOCKET.sendto(message.encode(), (SERVER_NAME, SERVER_PORT))
        received_message, server_address = CLIENT_SOCKET.recvfrom(1024)
        end_time = time.perf_counter()
        rtt = (end_time - start_time) * 1000
        print(f"Message from {server_address}: {received_message.decode()} |  RTT: {rtt:.3f}ms")
        rtt_array.append(rtt)
    except socket.timeout:
        print(f"Packet {sequence} timed out")
        continue

packets_received = len(rtt_array)


if packets_received > 0:
    min_rtt = min(rtt_array)
    max_rtt = max(rtt_array)
    rtt_sum = 0

    for i in range(packets_received):
        rtt_sum += rtt_array[i]

    avg_rtt = rtt_sum / packets_received

    lost_packets_percentage = (packets_sent - packets_received) / packets_sent * 100
    print("---Statistics---")
    print(f"{packets_sent} packets sent, {packets_received} received, {lost_packets_percentage:.2f}% packet loss")
    print(f"Min RTT: {min_rtt:.3f}ms | Max RTT: {max_rtt:.3f}ms | Avg RTT: {avg_rtt:.3f}ms")


CLIENT_SOCKET.close()


