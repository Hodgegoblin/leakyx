#!/usr/bin/env python
# Read forensic log, parse out auth strings, decode base64 and then dump to stdio
# 

data = {}
got_one = 0 
with open('/var/log/apache2/forensic.log') as f:

    while True:
        line = f.readline()
        if line:
            #print line,
            arr_spl = line.split('|')
            # if the array length is between 12-13 it probably contains our data 
            for temp in arr_spl:
                # Parse out password from array 4
                if ('Authorization:Basic' in temp): 
                    passwd = temp.split(' ')
                    if (passwd[1]) and ('Authorization:Basic'in passwd[0]): 
                        data[0] = passwd[1].decode('base64')
                        got_one = 1

                if 'Host:' in temp:
                    hostname = temp.split(':')
                    if (hostname[1]) and ('Host' in hostname[0]): 
                        data[1] = hostname[1]
             
                if ('User-Agent' in temp):
                    agent = temp.split(':')
                    if (agent[1]) and ('User-Agent' in agent[0]):
                        data[2] = agent[1]
            # end for loop
            if (len(data) > 0) and (got_one):
                print data

            # clear out the array for the next line
            data.clear()
            got_one = 0
