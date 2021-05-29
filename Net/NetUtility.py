import socket

class NetUtility:
    def connect_to(self, ip, port):
        sk = socket.socket()
        sk.connect((ip, port))
        return sk

    def start_listen(self, ip, port):
        sk = socket.socket()
        sk.bind((ip, port))
        sk.listen()
        return sk

    def receive_data_to_file(self, fileName, fileSize, conn):
        orgSize = fileSize
        with open(fileName, mode='wb') as f:
            while fileSize > 0:
                buffer = conn.recv(1024)
                if not buffer:
                    print(f'can not receive data, fileSize={orgSize}, receiveCnt={orgSize - fileSize}')
                    return

                fileSize -= len(buffer)
                f.write(buffer)

    def send_file(self, filePath, fileSize, conn):
        with open(filePath, mode='rb') as f:
            if fileSize > 0:
                conn.sendall(f.read())