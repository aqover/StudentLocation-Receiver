import math

fd = open("data.txt", "r")
signal_strnght_1_meter = 0
out = 0
n = 0
data = []
for line in fd:
	rssi = int(line.strip())
	out = out + rssi
	data.append([rssi, 1.1])
	n = n + 1
fd.close()
signal_strnght_1_meter = out/n
out = 0

for x in data:	
	l = ((x[0] - signal_strnght_1_meter)/ (10 * math.log10(x[1])))
	print (x[0], l)
	out = out + l

print (signal_strnght_1_meter)
print (out, n, out/n)