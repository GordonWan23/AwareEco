import socket
import argparse
import sys
import csv
from datetime import datetime
import numpy as np
import cv2

def sendImageClient(frame):

    SERVER_HOSTNAME = socket.gethostname()
    TCP_PORT = 50000

    sock = socket.socket()
    sock.connect((SERVER_HOSTNAME, TCP_PORT))

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = np.array(imgencode)
    stringData = data.tostring()

    sock.send(bytes(str(len(stringData)).ljust(16),'utf-8'));
    sock.send(stringData);
    sock.close()


def sendImageClientRecon(frame,add):
    BUFF_SIZE=1024
    SERVER_HOSTNAME = add
    TCP_PORT = 50000

    sock = socket.socket()
    sock.connect((SERVER_HOSTNAME, TCP_PORT))

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = np.array(imgencode)
    stringData = data.tostring()

    sock.send(bytes(str(len(stringData)).ljust(16), 'utf-8'));
    sock.send(stringData);

    recvd_bytes=sock.recv(BUFF_SIZE)
    recvd_str = recvd_bytes.decode('utf-8')
    sock.close()
    return recvd_str

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def receiveImageServer():

    SERVER_HOSTNAME = socket.gethostname()
    TCP_PORT = 50000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SERVER_HOSTNAME, TCP_PORT))
    s.listen(True)
    conn, addr = s.accept()

    length = recvall(conn, 16)
    stringData = recvall(conn, length)
    data = np.fromstring(stringData, dtype='uint8')
    s.close()

    dateTimeObj = datetime.now()
    filename = "%d_%d_%d_%d:%d:%d_%d.jpg" % (dateTimeObj.year,dateTimeObj.month,dateTimeObj.day,dateTimeObj.hour,dateTimeObj.minute,dateTimeObj.second,dateTimeObj.microsecond)
    decimg = cv2.imdecode(data, 1)
    cv2.imwrite(filename, decimg)
