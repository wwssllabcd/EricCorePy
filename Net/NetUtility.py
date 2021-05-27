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
        with open(fileName, mode='wb') as f:
            while fileSize > 0:
                content = conn.recv(1024)
                fileSize -= len(content)
                f.write(content)
    def send_file(self, filePath, fileSize, conn):
        with open(filePath, mode='rb') as f:
            while fileSize > 0:
                content = f.read(1024)
                fileSize -= len(content)
                conn.send(content)