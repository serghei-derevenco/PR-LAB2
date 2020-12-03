import json
import hashlib
import socket as skt

BUFF_SIZE = 1024

def get_checksum(val):
    return hashlib.md5(val.encode("utf-8")).hexdigest()

def make_packet(payload):
    return json.dumps({"checksum": get_checksum(payload), "data": payload}).encode("utf-8")

def is_valid(packet):
    return packet["checksum"] == get_checksum(packet["data"])

class Socket:
    def __init__(self, sock):
        self.sock = sock
        self.to_addr = None

def socket():
    return Socket(skt.socket(skt.AF_INET, skt.SOCK_DGRAM))

def server_socket(host, port):
    sock = socket()
    sock.sock.setsockopt(skt.SOL_SOCKET, skt.SO_REUSEADDR, 1)
    sock.sock.bind((host, port))
    return sock

def connect_to(sock, host, port):
    sock.to_addr = (host, port)
    print("Connecting...")
    send(sock, 'connect')
    return sock

def send(sock, val):
    sock.sock.sendto(make_packet(val), sock.to_addr)
    data, addr = sock.sock.recvfrom(BUFF_SIZE)
    packet = json.loads(data.decode("utf-8"))
    while packet["data"] == "nok":
        sock.sock.sendto(make_packet(val), sock.to_addr)
        data, addr = sock.sock.recvfrom(BUFF_SIZE)

def recv(sock):
    while True:
        data, addr = sock.sock.recvfrom(BUFF_SIZE)
        packet = json.loads(data.decode("utf-8"))
        print()

        if is_valid(packet):
            sock.sock.sendto(make_packet('ok'), addr)
            if packet['data'] == b'connect':
                sock.to_address = addr
                print('Connected!')
                return
            else:
                return packet['data']
        else:
            sock.sock.sendto(make_packet('nok'), addr)
    return packet['data']