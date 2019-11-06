#!/usr/bin/python

import argparse
import socket
import time
from threading import Thread, Lock
import random

def main_loop(tcp_port):
    """
    Start udp and tcp server threads
    """
    
    
    print "Server start on port ",tcp_port
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', int(tcp_port)))
    sock.setblocking(1)
    sock.settimeout(30)
    sock.listen(0)
    while True:

        #  Clean empty rooms
        try:
            conn, addr = sock.accept()
            print "New user connect from: ",str(addr)
            conn.setblocking(1)
            userhandler = HandleUser(conn,addr)
            userhandler.start()
        except :
            #print "user {0} diconnected".format(addr)
            continue
    
        
    self.stop()

class ChoseTimeOut(Exception):
    pass

class HandleUser(Thread):
    def __init__(self,conn,addr):
        """
        Create a new tcp server
        """
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        #self.msg = '{"success": "%(success)s", "message":"%(message)s"}'

    def run(self):
        level = 10
        curlevel = 1
        maxNum = 256*256
        minNum = 1
        maxTime = 13
        
        self.conn.send("Welcome to lucky number game !!!\n")
        try:
            
            correct = 0
            while (correct < level ):
                random.seed(time.time())
                maxNum = maxNum - random.randint(0,1024) + random.randint(0,1024)
                minNum = random.randint(1,1024)
                correct_number = random.randint(minNum,maxNum)
                maxTime -= 1
                self.conn.send("Level {0} \n".format( correct+1))
                self.conn.send("Enter correct number between {0} and {1} !!\n".format(minNum,maxNum))
                time_reference = time.time()
                while (True):
                    data = self.conn.recv(1024)
                    if (time.time() - time_reference > maxTime):
                        raise ChoseTimeOut
                                                
                    try:
                        gnum = int(data)
                        if (gnum > correct_number):
                            self.conn.send("Too big, again!\n")
                            continue 
                        if (gnum < correct_number):
                            self.conn.send("Too small, again!\n")  
                            continue 
                        if (gnum == correct_number):
                            self.conn.send("level {0} pass!!\n".format(correct+1))
                            correct += 1
                            if (correct == level):
                                self.conn.send("Win!, here is your flag:\n")
                                self.conn.send("MTA{S0ck3t_c0din9_1s_n0t_hard}")
                                self.conn.close()
                                print "user {0} win!".format(str(addr))
                            else:
                                self.conn.send("Another level is comming...\n")
                            
                            break
                    
                    except:
                        try:
                            self.conn.send("Wrong format, you must enter a number!!!")
                        except:
                            continue
                            


        except socket.error as se:
            self.conn.close()
            return
    
        except ChoseTimeOut:
            #print "user {0} failed, reason: {1}".format(str(addr),"time over")
            self.conn.send("Too slow, Game Over!!!")
            self.conn.close()
    
    
    def stop(self):
        """
        Stop tcp data
        """
        self.sock.close()


if __name__ == "__main__":
    """
    Start a game server
    """
    parser = argparse.ArgumentParser(description='Simple game server')
    parser.add_argument('-p',
                        dest='tcp_port',
                        help='Listening tcp port',
                        default="13378")
    
    args = parser.parse_args()
    main_loop(args.tcp_port)
