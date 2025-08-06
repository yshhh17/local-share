import socket
import time

DISCOVERY_PORT = 50001
DISCOVERY_PING = "localshare-discovery-ping"
DISCOVERY_PONG = "localshare-discovery-pong"
BUFFER_SIZE = 1024
TIMEOUT = 3

def start_listening():
    sockt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockt.bind(("0.0.0.0", DISCOVERY_PORT))

    print(f"[DISCOVERY] listening for pings on port {DISCOVERY_PORT}...")

    while True:
        try:
            data, addr = sockt.recvfrom(BUFFER_SIZE)
            message = data.decode().strip()

            if message == DISCOVERY_PING:
                print(f"[DISCOVERY] ping from {addr[0]}")
                sockt.sendto(DISCOVERY_PONG.encode(), addr)

        except Exception as e:
            print(f"[DISCOVERY] Error in listener: {e}")


def send_broadcast():
    discovered_ips = []
    sockt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockt.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sockt.settimeout(TIMEOUT)

    try:
        sockt.sendto(DISCOVERY_PING.encode(), ("<broadcast>", DISCOVERY_PORT))
        print("[DISCOVERY] broadcast sent, waiting for replies...")

        start_time = time.time()

        while True:

            try:
                data, addr = sockt.recvfrom(BUFFER_SIZE)
                if data.decode().strip() == DISCOVERY_PONG:
                    print(f"[DISCOVERY] pong received from address: {addr[0]}")
                    if addr[0] not in discovered_ips:
                        discovered_ips.append(addr[0])

            except socket.timeout:
                print("[DISCOVERY] search finished.")
                break

    except Exception as e:
        print(f"[DISCOVERY] error in broadcast: {e}")
    finally:
        sockt.close()

    return discovered_ips
