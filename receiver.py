import os
import socket
from pathlib import Path
from threading import Thread

clients = []


# Thread to listen one particular client
class ClientListener(Thread):
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name

    # clean up
    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')

    def run(self):
        filename = ''
        file_content = b''
        while True:
            # try to read 1024 bytes from user
            # this is blocking call, thread will be paused here
            data = self.sock.recv(1024)
            if data:

                # If we haven't found filename:
                if len(filename) == 0:
                    cleared = data.decode()

                    # Name is sent as filename.bla||
                    # We detect filename by ||
                    if '||' in cleared:

                        # Clearing filename
                        filename = cleared.replace('||', '')
                        print('Receiving %s' % filename)
                        my_file = Path(filename)
                        dot_index = filename.index('.')
                        copy_of_file = 1

                        # Checking if file exists
                        if my_file.is_file():

                            # If exists - define a new name with filename_copy%number%.bla
                            # and find non-existing copy
                            filename = filename[:dot_index] + '_copy%s' + filename[dot_index:]
                            while Path(filename % str(copy_of_file)).is_file():
                                copy_of_file += 1

                            # Saving unique filename
                            filename = filename % str(copy_of_file)
                            print('Duplicate exists, saving as %s' % filename)
                else:
                    # Saving received data to buffer
                    file_content += data
            else:
                # Transmission is ended, save file with content from file_content
                self._close()
                file = open(filename, "wb")
                file.write(file_content)
                file.close()
                return


def main():
    next_name = 1
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 8801))
    sock.listen()
    while True:
        con, addr = sock.accept()
        clients.append(con)

        name = 'u' + str(next_name)
        next_name += 1
        print(str(addr) + ' connected')
        ClientListener(name, con).start()


if __name__ == "__main__":
    main()
