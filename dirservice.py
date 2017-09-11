import socket
import struct

dir_ip = '127.0.0.1'
dir_port = 4111

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((dir_ip, dir_port))
s.listen(2)
print('DIRSERVICE IP:Port - %s:%d' % (dir_ip, dir_port))

# THE HASH TABLE OF UIDs/IP:PORT
directory = {}

def encode_response(error_code, dest_addr):
    header_buf = bytearray(32)
    error_code = error_code + ' ' * (16 - len(error_code))
    dest_addr = dest_addr + ' ' * (16 - len(dest_addr))
    header_buf = struct.pack('!16s16s', error_code.encode('utf-8'), dest_addr.encode('utf-8'))
    return header_buf

def decode_registration(msg_buf):
    #tuple = struct.unpack('!400s400s', msg_buf[:800])
    #(head, payload) = tuple
    #head = head.decode('utf-8')
    #payload = payload.decode('utf-8')
    #return (head, payload)
    payload = msg_buf.decode('utf-8')
    return payload

while True:

    conn, addr = s.accept()
    data = conn.recv(16384)
    print(data)
    payload = decode_registration(data)
    #print(payload)
    print('\n\n\n')

    errorNum = 201
    errorType = 'OK'
    #header = 'HTTP/1.1 %d %s \r\nContent-Type: text/html\n' % (errorNum, errorType)
    header = "Status: 200 OK\r\nLink: <https://api.github.com/resource?page=2>; rel='next',<https://api.github.com/resource?page=5>; rel='last'"
    body = "{'status_code':200,'msg':'OK','details':{'allowed':'GET','method':'POST'}}"
    conn.send((header + body + '\r\n\r\n').encode())
    conn.close()
