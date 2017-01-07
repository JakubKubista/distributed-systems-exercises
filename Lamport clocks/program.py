import sys
import threading
import socket
import random
import time

CLOCK = 0
DEBUG = False
RUN = True  # global variable to exit carefully


# server thread.
class ServerThread(threading.Thread):
    def __init__(self, tid, port):
        threading.Thread.__init__(self)
        self.tid = tid
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        global CLOCK, RUN
        try:
            self.sock.bind(('localhost', self.port))
        except socket.error:
            print("must leave. port already in use")
            RUN = False
            sys.exit()

        if DEBUG:
            print("server started")

        while RUN:
            d = self.sock.recvfrom(1024)
            data = d[0]

            if not data:
                continue

            # data messages between the hosts are seperated with a ;
            d = data.decode('utf-8').split(';')
            self.sync(int(d[1]))
            print('r ' + d[0] + ' ' + d[1] + ' ' + str(CLOCK))

    # Lamport algorithm
    def sync(self, recv):
        global CLOCK
        if recv > CLOCK:
            CLOCK = recv
            CLOCK += 1


# writers
class WritingThread(threading.Thread):
    def __init__(self, id, others, others_id):
        threading.Thread.__init__(self)
        self.id = id
        self.others = others
        self.others_id = others_id

    def run(self):
        global CLOCK, RUN
        if DEBUG:
            print("local writing thread started")

        i = 0
        while RUN and i < 100:
            time.sleep(random.randint(1, 1))
            increase = random.randint(1, 9)
            i += 1

            # 50:50 chance to write local or send it
            if random.randint(0, 9) > 5:
                CLOCK += increase
                print("l " + str(increase))
            else:
                randi = random.randint(0, len(self.others) - 1)
                port = self.others[randi]
                addr = ("localhost", port)
                ud = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                data = str(self.id) + ";" + str(CLOCK)
                ud.sendto(data.encode('utf-8'), addr)

                # original solution
                # print("s " + str(port) + " " + str(CLOCK))
                print("s " + str(self.others_id[randi]) + " " + str(CLOCK))
                ud.close()
        RUN = False


# read the data from the config file
def get_data():
    other_ports = []
    other_ids = []  # added it very late
    data = []
    with open(sys.argv[1]) as fp:
        for i, line in enumerate(fp):
            if i == int(sys.argv[2]):
                data = line.split()
                data[0] = int(data[0])
                data[1] = int(data[1])
            else:
                other_ports.append(int(line.split()[1]))
                other_ids.append(int(line.split()[0]))
    data.append(other_ports)
    data.append(other_ids)
    return data


def main():
    data = get_data()

    s = ServerThread(data[0], data[1])
    w = WritingThread(data[0], data[2], data[3])
    w.start()
    s.start()
    exit()


if __name__ == "__main__":
    main()
