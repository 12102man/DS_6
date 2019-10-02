import base64
import math
import os
import socket
import sys
import time



def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    # Print New Line on Complete
    if iteration == total:
        print()

if __name__ == '__main__':

    # Connecting to server
    s = socket.socket()  # Create a socket object
    host = 'the-o.co'
    port = 8801  # Reserve a port for your service.
    s.connect((host, port))

    # Reading filename from arguments
    filename = sys.argv[1]
    f = open(filename, 'rb')

    # Calculating metadata
    total = os.stat(filename).st_size
    sent = 0
    i = 0

    # Printing info
    print('Sending %s. Size: %d bytes, %d chunks' % (filename, total, math.ceil(total/1024)))

    # Sending filename
    s.send((filename+'||').encode().strip())
    time.sleep(0.2)


    # Reading chunk & sending
    l = f.read(1024)
    printProgressBar(0, math.ceil(total / 1024), decimals=round(sent / total), length=100)
    while l:
        s.send(l)
        sent += 1024
        i += 1
        time.sleep(0.2)
        printProgressBar(i, math.ceil(total / 1024), decimals=round(sent / total), length=100)
        l = f.read(1024)
    f.close()


