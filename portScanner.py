import socket, random
import sys # Redirect print output to a txt file usage
from scapy.all import *

def scanMe():
        # Ask for (multiple) IP input from user
        IPinputs = input("Please enter IP(s) with a space in between: ")
        targets = IPinputs.split()

        if not targets:        # End program if no IPs were passed
                return
        
        # Ask for port numbers or ranges
        ports = []
        portOption = input("Enter [1] for specific port numbers or [2] for a port range: ")
        if portOption == '1':
                portsInput = input("Please enter ports with a space in between: ")
                ports = portsInput.split()
        elif portOption == '2':
                portsInput = input("Please enter a port range, ex. 0-445: ")
                ports = portsInput.split('-')
                portStart = ports[0]
                cnt = int(portStart)
                end = int(ports[-1])
                for i in range(cnt,end-1,1): #add in the ports in the range given
                        cnt += 1
                        add = str(cnt)
                        ports.insert(-1, add)
                        
        # Ask for TCP or UDP Scanning
        tcpudp = input("Enter [TCP] or [UDP] for port scanning: ")
        
        # Optional requests below
        timeoutVal = input("Please enter a timeout value if you'd like, default is [1]: ")
        save = input("Would you like to save results to a txt file? [y] or [n]: ")

        if(timeoutVal == '') or (int(timeoutVal) < 1):      #check timeout value 
                timeoutVal = 1
                timeoutVal = int(timeoutVal)
        elif type(timeoutVal) == str:
                timeoutVal = int(timeoutVal)
                
        
        for IPs in range(len(targets)):                 # Multiple IP iteration
                if(save.lower()[0] == 'y'):             # Save each IP results to txt file option
                        sys.stdout = open(f'{targets[IPs]}{tcpudp}.txt', 'w')
                        
                print(f"\nScanning ports for {targets[IPs]}...")
                
                for each in range(len(ports)):          # Multiple Port iteration
                        # TCP Port Scanning Below
                        if tcpudp.lower()[0] == 't':
                                t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #TCP socket params
                                t.settimeout(timeoutVal)
                                try:
                                        t.connect((targets[IPs],int(ports[each])))    #TCP socket connection
                                        print(ports[each],"\tTCP Port Open")
                                        t.close()
                                except Exception as e:
                                        t.close()


                        # UDP Port Scanning Below
                        if tcpudp.lower()[0] == 'u':
                                udp = sr1(IP(dst=targets[IPs])/UDP(sport=RandShort(), dport=int(ports[each])), timeout=timeoutVal, verbose=0)
                                if(udp == None):
                                        #try again to make sure because I was getting false positives
                                        retry = sr1(IP(dst=targets[IPs])/UDP(dport=int(ports[each])), timeout=timeoutVal, verbose=0)
                                        if (retry == None):
                                                print(ports[each],"\tUDP Open|Filtered")


                if(save.lower()[0] == 'y'):     # Close file writing
                        sys.stdout.close()
                        
        return


scanMe()