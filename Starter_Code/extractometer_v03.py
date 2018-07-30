
# coding: utf-8

# In[imports]:

from __future__ import print_function
import os
import gzip
import threading
import sys

# In[constants]:

WKDIR = 'C:\\Users\\Admin\\Documents\\MelbDatathon2018'
os.chdir(WKDIR)

files_out = {
        '1On':'On_Bus'
        ,'1Off':'Off_Bus'
        ,'2On':'On_Train'
        ,'2Off':'Off_Train'
        ,'3On':'On_Tram'
        ,'3Off':'Off_Tram'
        ,'OthOn':'On_Other'
        ,'OthOff':'Off_Other'
        }
scan_cache = {
        '1On':[]
        ,'1Off':[]
        ,'2On':[]
        ,'2Off':[]
        ,'3On':[]
        ,'3Off':[]
        ,'OthOn':[]
        ,'OthOff':[]
        }
scan_headers = 'Mode|BusinessDate|DateTime|CardID|CardType|ParentRoute|VehicleID|RouteID|StopID' + os.linesep

threads = []
temp_cnt = 0

# In[file scan def]:
def scan_create(root,f,scan_tp):
    global temp_cnt
    print(f)
    with gzip.open(os.path.join(root,f), 'rb') as f_in:
        for line in f_in.readlines():
            mode = line.decode().split('|')[0]
            if mode in ('1','2','3'):
                mode_tp = mode + scan_tp
            else: # mode not in 1 or 2 or 3
                mode_tp = 'Oth' + scan_tp
            scan_cache[mode_tp].append(line)
    temp_cnt += 1
    if temp_cnt == 5:
        for k in files_out.keys():
            with open(os.path.join(WKDIR,files_out[mode_tp]), 'ab') as f_out:
                f_out.write(''.join(scan_cache[mode_tp]))
                scan_cache[mode_tp] = []
        temp_cnt = 0

# In[main]:
def main():
    for root,dirs,files in os.walk(WKDIR):
        for f in files:
            if f.endswith('.gz'):
                if 'On' in root:
                    threads.append(threading.Thread(target=scan_create, args=(root,f,'On')))
                    threads[-1].start()
                elif 'Off' in root:
                    threads.append(threading.Thread(target=scan_create, args=(root,f,'Off')))
                    threads[-1].start()
        for thr in threads:
            thr.join()

if __name__ == "__main__":
    global scan_cache # initialise
    for k in scan_cache.keys():
        scan_cache[k] = []
    # Make the placeholder files
    for v in files_out.values():
        with open(os.path.join(WKDIR,v), 'wb') as f_out:
            f_out.write(scan_headers.encode())

    main() # need this for threading I believe

# In[demo import]:

import pandas as pd
df = pd.read_csv(os.path.join(WKDIR,'On_Train'), sep='|')
