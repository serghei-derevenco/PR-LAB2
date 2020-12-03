import transport_protocol as tp
from aes_cipher import get_key, encrypt, decrypt


if __name__ == "__main__":
    proto_handler = tp.socket()
    tp.connect_to(proto_handler, 'localhost', 2020)
    secret_key = get_key()

    resp = tp.recv(proto_handler)
    r = decrypt(resp, secret_key)
    print(r)

    mess_1 = "Yo!"
    tp.send(proto_handler, encrypt(mess_1, secret_key))
    print(mess_1)
    resp_1 = tp.recv(proto_handler)
    r = decrypt(resp, secret_key)
    print(resp_1)

    mess_2 = "I'm fine!"
    tp.send(proto_handler, encrypt(mess_2, secret_key))
    print(mess_2)
    resp_2 = tp.recv(proto_handler)
    r = decrypt(resp_2, secret_key)
    print(r)