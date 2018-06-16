#Contacts NTP server for time

import zmq, ntplib, time, datetime, string

context = zmq.Context()

print("Establishing server...")
socket = context.socket(zmq.PUB)
#NTP node's 
socket.bind("tcp://localhost:5555")

call = ntplib.NTPClient()
ntp_pool = ["0.us.pool.ntp.org", "1.us.pool.ntp.org", 
				"2.us.pool.ntp.org", "3.us.pool.ntp.org"]

while True:
	print("Checking time")
	for pool in ntp_pool:
		try:
			response = call.request(pool, version=3)
			break
		except:
			print(pool, "did not respond")
	t = str(response.dest_time)
	t = t[:-3]
	while len(t) <= 14:
		t += "0"
	t += "000"
	mes_type = "message"
	socket.send_string("%s %s" % (mes_type, t))
	print("Message published:", t)

	time.sleep(4)