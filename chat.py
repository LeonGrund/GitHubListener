import sys
import socket
import select
import struct
import time

# ARGUMENTS
host_name = sys.argv[1]
host_ip = sys.argv[2].split(':')[0]  #localhost
host_port = sys.argv[2].split(':')[1]
dest_name = sys.argv[3]
dir_ip = sys.argv[4].split(':')[0]
dir_port = sys.argv[4].split(':')[1]

# CLIENT SOCKET
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_address = (host_ip, int(host_port))
sock.bind(host_address)

# DIRSERVICE INFO
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.connect((dir_ip, int(dir_port)))
#tcp_sock.send(MESSAGE)
#tcp_data = tcp_sock.recv(4096)
#print(tcp_data)


def encode_chat_msg(seqnum, UID, DID, msg, version=150):
    header_buf = bytearray(36)
    UID = UID + ' ' * (16 - len(UID))
    DID = DID + ' ' * (16 - len(DID))
    header_buf = struct.pack('!HH16s16s', version, seqnum, UID.encode('utf-8'), DID.encode('utf-8'))
    header_buf = header_buf + msg.encode('utf-8')
    return header_buf

def decode_chat_msg(msg_buf):
    tuple = struct.unpack('!HH16s16s', msg_buf[:36])
    (version, seqnum, UID, DID) = tuple
    UID = UID.decode('utf-8')
    DID = DID.decode('utf-8')
    msg = msg_buf[36:].decode('utf-8')
    return (seqnum, UID, DID, msg)

def decode_response(msg_buf):
    tuple = struct.unpack('!16s16s', msg_buf[:32])
    (error_code, dest_addr) = tuple
    error_code = error_code.decode('utf-8')
    dest_addr = dest_addr.decode('utf-8')
    return (error_code, dest_addr)

def encode_registration(UID, user_addr, DID):
    header_buf = bytearray(48)
    UID = UID + ' ' * (16 - len(UID))
    user_addr = user_addr + ' ' * (16 - len(user_addr))
    DID = DID + ' ' * (16 - len(DID))
    header_buf = struct.pack('!16s16s16s', UID.encode('utf-8'), user_addr.encode('utf-8'), DID.encode('utf-8'))
    return header_buf

seq_num = 0
try:

    # TCP CONNECTION WITH DIRSERVICE
    dest_address = ()   # init the destination
    while True:
        tcp_sock.send(encode_registration(host_name, sys.argv[2], dest_name))
        tcp_data = tcp_sock.recv(4096)
        tcp_sock.close()

        tcp_response = decode_response(tcp_data)
        error_code = tcp_response[0].split(' ')[0]

        # SUCC CONNECTION
        if(error_code == '400'):
            dest_addr = tcp_response[1].split(' ')[0]
            dest_ip = dest_addr.split(':')[0]
            dest_port = dest_addr.split(':')[1]
            dest_address = (dest_ip, int(dest_port))
            print('\nConnected with %s:' % dest_name)
            break
        # RECONNECT WITH DIRSERVICE
        if(error_code == '600'):
            time.sleep(5)
            tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_sock.connect((dir_ip, int(dir_port)))
            print('Reconnecting with DIRSERVICE')

    # UDP CONNECTION WITH OTHER CLIENT
    while True:
        user_input = None
        rlist, wlist, elist = select.select([sock, sys.stdin], [], [])

        if sys.stdin in rlist:
            # if you do input when the sys.stdin has data available to read from,
            # it will NOT BLOCK
            user_input = raw_input()
            #print('sending "%s"' % user_input)
            #user_input_bytes = user_input.encode('utf-8')
            user_input_bytes = encode_chat_msg(seq_num, host_name, tcp_response[1], user_input)
            sent = sock.sendto(user_input_bytes, dest_address)
            seq_num += 1

        if sock in rlist:
            # data is pending on the socket
            # reading form the socket will NOT block
            data, server = sock.recvfrom(4096)
            #print('encoded received "%s"' % data)
            decode_msg = decode_chat_msg(data)
            #print(decode_msg)
            seq_num = decode_msg[0] + 1
            print('[%d]%s: %s' % (decode_msg[0], decode_msg[1].split(' ')[0], decode_msg[-1]))

finally:
    print('%s OFFLINE\n' % host_name)
    sock.close()