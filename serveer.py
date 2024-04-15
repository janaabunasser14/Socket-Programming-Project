from socket import *
import os
from operator import itemgetter
# server port, socket initialization and type
serverPort = 7788
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
print("The server is ready to receive\n\n")
# start getting requests
while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    ip = addr[0]
    port = addr[1]

    print('IP: ' + str(ip) + ', Port: ' + str(port))
    print(sentence)
    # if the sentence is not empty, the requested file is gotten from request header
    if sentence != '':
        requested_file = sentence.split(' ')[1].replace('/', '')
        print(requested_file)
    else:
        # if the request is empty the connection is closed
        connectionSocket.close()
        continue
    # exception in case the requested file is not found
    try:
        # if the request is index.html/main.html or any other file is found in the project file, if the file
        # is not found then exception is raised
        # if the requested file is main.html or index.html
        if requested_file == '' or requested_file == 'main.html' or requested_file == 'index.html' or requested_file == 'en':
            connectionSocket.send(b"HTTP/1.1 200 OK\r\n")
            connectionSocket.send(b"Content-Type: text/html \r\n")
            connectionSocket.send(b"\r\n")
            mhtml = open('main_en.html', 'rb')
            connectionSocket.send(mhtml.read())
            mhtml.close()
        elif requested_file == 'main_ar.html' or requested_file == 'ar':
            connectionSocket.send(b"HTTP/1.1 200 OK\r\n")
            connectionSocket.send(b"Content-Type: text/html \r\n")
            connectionSocket.send(b"\r\n")
            mhtml = open('main_ar.html', 'rb')
            connectionSocket.send(mhtml.read())
            mhtml.close()
        elif requested_file == 'go':
            connectionSocket.send(f"HTTP/1.1 307 Temporary Redirect\r\n".encode())
            connectionSocket.send(f"Location: https://www.google.com/\r\n".encode())
        elif requested_file == 'so':
            connectionSocket.send(f"HTTP/1.1 307 Temporary Redirect\r\n".encode())
            connectionSocket.send(f"Location: https://stackoverflow.com/\r\n".encode())
        elif requested_file == 'bzu':
            connectionSocket.send(f"HTTP/1.1 307 Temporary Redirect\r\n".encode())
            connectionSocket.send(f"Location: https://www.birzeit.edu/en\r\n".encode())
        # if the client requests any html file
        elif '.html' in requested_file:
            connectionSocket.send(b"HTTP/1.1 200 OK\r\n")
            connectionSocket.send(b"Content-Type: text/html \r\n")
            connectionSocket.send(b"\r\n")
            print('Response status: 200 OK\n\n')
            file = open(str(requested_file), "rb")
            connectionSocket.send(file.read())
            file.close()
        # if the client requests any css file
        elif '.css' in requested_file:
            connectionSocket.send(b"HTTP/1.1 200 OK\r\n")
            connectionSocket.send(b"Content-Type: text/css \r\n")
            connectionSocket.send(b"\r\n")
            print('Response status: 200 OK\n\n')
            file = open(str(requested_file), "rb")
            connectionSocket.send(file.read())
            file.close()
        # if the request contains .png image
        elif '.png' in requested_file:
            connectionSocket.send(b"HTTP/1.1 200 OK\r\n")
            connectionSocket.send(b"Content-Type: image/png \r\n")
            connectionSocket.send(b"\r\n")
            print('Response status: 200 OK\n\n')
            file = open(str(requested_file), "rb")
            connectionSocket.send(file.read())
            file.close()
        # if the request contains .jpg image
        elif '.jpg' in requested_file:
            connectionSocket.send(b"HTTP/1.1 200 OK\r\n")
            connectionSocket.send(b"Content-Type: image/jpeg \r\n")
            connectionSocket.send(b"\r\n")
            print('Response status: 200 OK\n\n')
            file = open(str(requested_file), "rb")
            connectionSocket.send(file.read())
            file.close()
        # this is a handler only in order not to get not found error
        elif 'favicon.icon' == requested_file:
            print()
        else:
            print(requested_file)
            raise Exception('Not found')
    # if the file is not found in the project folder
    except Exception as e:
        connectionSocket.send(b"HTTP/1.1 404 Not Found \r\n")
        connectionSocket.send(b"Content-Type: text/html \r\n")
        connectionSocket.send(b"\r\n")
        print(requested_file )
        print('\b\bResponse status: 404 Not Found')
        file = '<!DOCTYPE html><style>* {text-align: center;font-size: large;font-weight: bold;}h1 {font-size: ' \
               '50px;}#error-message {color: red;}</style><main><header><title>Error</title></header><body><div ' \
               'id="error-message"><h1>The file is not found</h1></div><hr><div><p>Jana Abu Nasser - 1201110</p><p>Raneem' \
               'Daqa - 1202093</p></div><hr><div><p>IP Address: ' + str(ip) + \
               ', Port number: ' + str(port) + '</p></div></body></main></html> '
        connectionSocket.send(file.encode())
    connectionSocket.close()
