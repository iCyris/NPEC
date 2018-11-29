# coding = utf-8

from scapy.all import *
import matplotlib.pyplot as plt 

path = "Exp2pcap.pcapng"

pcapfile = rdpcap(path)

p1 = False
p2 = False
p3 = False

t_dst = ['218.75.123.181', '218.75.123.182']

for i in range(0,len(pcapfile)):
    if (str(pcapfile[i][IP].dst) == t_dst[1] and str(pcapfile[i][TCP].flags) == 'S'):
        print("good")
        p1 = pcapfile[i]
        break

for i in range(0,len(pcapfile)):
    if (p1 == False):
        print("No p1")
        break
    if (str(pcapfile[i][IP].src) == t_dst[1] and str(pcapfile[i][TCP].flags) == "SA"\
        and (int(pcapfile[i][TCP].ack) == int(p1[TCP].seq) + 1)):
        p2 = pcapfile[i]
        break

for i in range(0,len(pcapfile)):
    if (p2 == False):
        print("No p2")
        break
    if (str(pcapfile[i][IP].dst)==t_dst[1] and str(pcapfile[i][TCP].flags) == 'A'\
        and (int(pcapfile[i][TCP].ack) == int(p2[TCP].seq) + 1)):
        p3 = pcapfile[i]
        break
        
if (p3 == False):
    print("No p3")

print(int(p1[TCP].seq))
print(str(p2[TCP].flags))
print(str(p3[TCP].flags))

p1_src = str(p1[IP].src)
p1_dst = str(p1[IP].dst)
p1_ack = str(p1.ack)
p1_seq = str(p1.seq)

p2_src = str(p2[IP].src)
p2_dst = str(p2[IP].dst)
p2_ack = str(p2.ack)
p2_seq = str(p2.seq)

p3_src = str(p3[IP].src)
p3_dst = str(p3[IP].dst)
p3_ack = str(p3.ack)
p3_seq = str(p3.seq)

pd_1 = [p1_src, p1_dst, p1_ack, p1_seq]
pd_2 = [p2_src, p2_dst, p2_ack, p2_seq]
pd_3 = [p3_src, p3_dst, p3_ack, p3_seq]

print(p1.show())
print(p2.show())
print(p3.show())

plt.title('TCP imitate')
plt.plot([0, 0],[0, 9], 'black')
plt.plot([8, 8],[0, 9], 'black')
plt.plot([1, 7],[9, 6], 'b')
plt.plot([1, 7],[3, 6], 'r')
plt.plot([1, 7],[3, 0], 'b')
plt.text(1, 7, r'$src:\ $' + pd_1[0] + '\n' + r'$dst:\ $' + pd_1[1] + '\n' + r'$ack:\ $' + pd_1[2] + '\n' + r'$seq:\ $' + pd_1[3],
         fontdict={'size': 10, 'color': 'black'})
plt.text(3, 4, r'$src:\ $' + pd_2[0] + '\n' + r'$dst:\ $' + pd_2[1] + '\n' + r'$ack:\ $' + pd_2[2] + '\n' + r'$seq:\ $' + pd_2[3],
         fontdict={'size': 10, 'color': 'black'})
plt.text(4, 1, r'$src:\ $' + pd_3[0] + '\n' + r'$dst:\ $' + pd_3[1] + '\n' + r'$ack:\ $' + pd_3[2] + '\n' + r'$seq:\ $' + pd_3[3],
         fontdict={'size': 10, 'color': 'black'})
plt.text(0, 5, r'$LOCAL$',
         fontdict={'size': 8, 'color': 'black'})
plt.text(8, 5, r'$REMOTE$',
         fontdict={'size': 8, 'color': 'black'})
plt.axis('off')
plt.show()