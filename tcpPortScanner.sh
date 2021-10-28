#! /bin/bash
echo "Enter IP to scan:"
read IP                             #read in user input
echo "Scanning ports for $IP..."

for port in {1..1023};                          #loop ports 1-1023
    do
        2>/dev/null echo >/dev/tcp/$IP/$port    #Redirect port scan errors and scan for tcp/user IP/port#
        if [[ $? == 0 ]];                       #The exit status of the prev command 0=succ and 1=fail
        then
            echo "$port TCP Port Open"          #Output open tcp port
        fi
    done
