#Worker node

import zmq, threading, random, time, queue
import logging

con = threading.Condition()
flag = False
t = 0000000000.0000
c = 0
max_c = 0

class Sender(threading.Thread):
	def __init__(self, sock):
		threading.Thread.__init__(self)
		self.socket = sock

	def run(self):
		global t
		global c
		global flag
		time.sleep(10)
		while True:
			con.acquire()
			if flag == False:
				print("sender acquiring flag")
				flag = True
				c += 1
				mt = str(t)
				mc = str(c)
				if len(mc) < 3:
					mc = mc.zfill(3)
				while len(mt) <= 14:
					mt += "0"
				message = str(mt) + str(mc)
				print("Sending:", message)
				mes_type = "message"
				self.socket.send_string("%s %s" % (mes_type, message))
				print("Message published:", message)
				flag = False
				con.notify_all()
				print("sender releasing flag")
				con.release()
				x = random.uniform(.01, 1.0)
				time.sleep(x)
			else:
				con.wait()
				con.release()
			# x = random.uniform(.01, 2.0)
			# time.sleep(x)
			# con.release()

class Receiver(threading.Thread):
	def __init__(self, sub_sock):
		threading.Thread.__init__(self)
		self.sub_socket = sub_sock

	def run(self):
		global t
		global c
		global max_c
		global flag
		while True:
			if flag == False:
				message = self.sub_socket.recv_string()
				print("receiver acquiring flag")
				flag = True
				junk, message = message.split()
				print(message)
				con.acquire()
				mc = int(message[-3:])
				mt = float(message[:-3])
				if mt > t:
					t = mt
					c = mc
				elif mc > c:
					c = mc
					logging.info("Seen value: %d", mc)
					if mc > max_c:
						max_c = mc
						logging.info("Max c value: %d", max_c)
				flag = False
				con.notify_all()
				print("receiver releasing flag")
			else:
				con.wait()
			con.release()

context = zmq.Context()

q = queue.Queue()
f = open("socket_list.txt", "r")
for line in f:
	q.put(line.strip('\n'))

print("Establishing server...")
socket = context.socket(zmq.PUB)
#grabs first address in socket_list.txt as the node's own address
socket.bind(q.get())

print("Subscribing to servers...")
sub_socket = context.socket(zmq.SUB)
while not q.empty():
	#adds all other addresses in socket_list to subscribe to
	connection = q.get()
	print(connection)
	sub_socket.connect(connection)
mes_type = "message"
sub_socket.setsockopt_string(zmq.SUBSCRIBE, "message")

logging.basicConfig(filename='stats.log',level=logging.DEBUG)

sen = Sender(socket)
rec = Receiver(sub_socket)

sen.start()
rec.start()

sen.join()
rec.join()
