import socket
import argparse
import sys
import csv
from datetime import datetime
import numpy as np
import cv2
import os

def sendImageClient(frame):

    SERVER_HOSTNAME = socket.gethostname()
    TCP_PORT = 50000

    sock = socket.socket()
    sock.connect((SERVER_HOSTNAME, TCP_PORT))

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = np.array(imgencode)
    stringData = data.tostring()

    sock.send(str(len(stringData)).ljust(16));
    sock.send(stringData);
    sock.close()

def sendImageClientRecon(frame, add):
    BUFF_SIZE = 1024
    SERVER_HOSTNAME = add
    TCP_PORT = 50000

    sock = socket.socket()
    sock.connect((SERVER_HOSTNAME, TCP_PORT))

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = np.array(imgencode)
    stringData = data.tostring()

    sock.send(str(len(stringData)).ljust(16));
    sock.send(stringData);

    recvd_bytes=sock.recv(BUFF_SIZE)
    recvd_str = recvd_bytes.decode('utf-8')
    sock.close()

    return recvd_str

def sendDataSharing(frame, weight, time, category, add):
    BUFF_SIZE = 1024
    SERVER_HOSTNAME = add
    TCP_PORT = 45000

    sock = socket.socket()
    sock.connect((SERVER_HOSTNAME, TCP_PORT))

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = np.array(imgencode);
    stringData = data.tostring();
    time_field_bytes = time.encode('utf-8')
    time_size_field = len(time_field_bytes).to_bytes(1, byteorder='big')
    sock.send(time_size_field);
    sock.send(time_field_bytes);
    weight_field_bytes = weight.encode('utf-8')
    weight_size_field = len(weight_field_bytes).to_bytes(1, byteorder='big')
    sock.send(weight_size_field);
    sock.send(weight_field_bytes);
    category_field_bytes = category.encode('utf-8')
    category_size_field = len(category_field_bytes).to_bytes(1, byteorder='big')
    sock.send(category_size_field);
    sock.send(category_field_bytes);
    sock.send(bytes(str(len(stringData)).ljust(16), 'utf-8'));
    sock.send(stringData);
    sock.close()



def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def receiveImageServer():

    SERVER_HOSTNAME = ""
    TCP_PORT = 50000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SERVER_HOSTNAME, TCP_PORT))
    s.listen(True)
    conn, addr = s.accept()

    length = recvall(conn, 16)
    stringData = recvall(conn, int(length))
    data = np.fromstring(stringData, dtype='uint8')
    s.close()

    dateTimeObj = datetime.now()
    filename = "%d_%d_%d_%d_%d_%d_%d.jpg" % (dateTimeObj.year,dateTimeObj.month,dateTimeObj.day,dateTimeObj.hour,dateTimeObj.minute,dateTimeObj.second,dateTimeObj.microsecond)
    decimg = cv2.imdecode(data, 1)
    cv2.imwrite(filename, decimg)


def receiveImageServerRecon():

    SERVER_HOSTNAME = ""
    TCP_PORT = 50000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SERVER_HOSTNAME, TCP_PORT))
    s.listen(True)
    conn, addr = s.accept()

    length = recvall(conn, 16)
    stringData = recvall(conn, int(length))
    data = np.fromstring(stringData, dtype='uint8')

    #results = classification.classificationCV2()

    dateTimeObj = datetime.now()
    filename = "%d_%d_%d_%d_%d_%d_%d.jpg" % (dateTimeObj.year,dateTimeObj.month,dateTimeObj.day,dateTimeObj.hour,dateTimeObj.minute,dateTimeObj.second,dateTimeObj.microsecond)
    decimg = cv2.imdecode(data, 1)
    cv2.imwrite(filename, decimg)
    results = classification.classificationCV2(decimg)
    print(results)
    conn.sendall(results.encode('utf-8'))
    s.close()

def receiveDataSharing():

    SERVER_HOSTNAME = ""
    TCP_PORT = 45000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SERVER_HOSTNAME, TCP_PORT))
    s.listen(True)
    conn, addr = s.accept()

    time_size_byte = recvall(conn,1)
    time_size = int.from_bytes(time_size_byte, byteorder='big')
    time = recvall(conn,time_size)
    time = time.decode('utf-8')

    weight_size_byte = recvall(conn,1)
    weight_size = int.from_bytes(weight_size_byte, byteorder='big')
    weight = recvall(conn,weight_size)
    weight= weight.decode('utf-8')

    category_size_byte = recvall(conn,1)
    category_size = int.from_bytes(category_size_byte, byteorder='big')
    category = recvall(conn,category_size)
    category = category.decode('utf-8')

    length = recvall(conn, 16)
    stringData = recvall(conn, int(length))
    data = np.fromstring(stringData, dtype='uint8')
    filename = time + '.jpg'
    csv_file = 'Data_record.csv'
    if os.path.isfile(csv_file):
        with open(csv_file, 'a+') as f:
            csv_write = csv.writer(f)
            data_row = [time, weight,category,filename]
            csv_write.writerow(data_row)
    else:
        with open(csv_file, 'w') as f:
            csv_write = csv.writer(f)
            csv_head = [time, weight,category,filename]
            csv_write.writerow(csv_head)


    #results = classification.classificationCV2()
    imagePath = 'Image/'
    decimg = cv2.imdecode(data, 1)
    cv2.imwrite(imagePath + filename, decimg)

    s.close()


if __name__ == '__main__':
    frame = cv2.imread('backGround.jpg')
    sendDataSharing(frame, '250g', '2022_5_1', 'background', '192.168.0.114')