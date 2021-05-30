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
    
    def recv_ack(self, conn):
        conn.recv(2)
        
    def send_ack(self, conn):
        msg = 'ok'.encode(encoding="utf-8")
        conn.send(msg)

    def receive_file(self, fileName, fileSize, conn):
        if fileSize == 0:
            return
        
        orgSize = fileSize
        with open(fileName, mode='wb') as f:
            while fileSize > 0:
                buffer = conn.recv(1024)
                if not buffer:
                    print(f'can not receive data, fileSize={orgSize}, receiveCnt={orgSize - fileSize}')
                    return

                fileSize -= len(buffer)
                f.write(buffer)
    
    def receive_file_with_ack(self, fileName, fileSize, conn):
        if fileSize == 0:
            return
        self.receive_file(fileName, fileSize, conn)
        self.send_ack(conn)

    def send_file(self, filePath, fileSize, conn):
        if fileSize == 0:
            return
        with open(filePath, mode='rb') as f:
            conn.sendall(f.read())

    def send_file_with_ack(self, filePath, fileSize, conn):
        if fileSize == 0:
            return
        self.send_file(filePath, fileSize, conn)
        self.recv_ack(conn)

        