import transport_protocol as tp
from aes_cipher import get_key, encrypt, decrypt, key_generator


if __name__ == "__main__":
    server_handler = tp.server_socket('localhost', 2020)
    key_generator()
    tp.recv(server_handler) # connect
    secret_key = get_key()

    mess_1 = "Hello"
    print(mess_1)
    tp.send(server_handler, encrypt(mess_1, secret_key))
    resp_1 = tp.recv(server_handler)
    r = decrypt(resp_1, secret_key)
    print(r)

    mess_2 = "How are you?"
    print(mess_2)
    tp.send(server_handler, encrypt(mess_2, secret_key))
    resp_2 = tp.recv(server_handler)
    r = decrypt(resp_2, secret_key)

    mess_3 = "Have a nice day!"
    print(mess_3)
    tp.send(server_handler, encrypt(mess_3, secret_key))
