
# coding: utf-8

# In[imports]:

from __future__ import print_function
import os
import gzip
import threading
import sys

# In[constants]:

WKDIR = "H://Downloads//adjustedr2"
#WKDIR = 'C:\\Users\\Admin\\Documents\\MelbDatathon2018'
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
scan_cnt = {
        '1On':0
        ,'1Off':0
        ,'2On':0
        ,'2Off':0
        ,'3On':0
        ,'3Off':0
        ,'OthOn':0
        ,'OthOff':0
        }
scan_headers = 'Mode|BusinessDate|DateTime|CardID|CardType|ParentRoute|VehicleID|RouteID|StopID' + os.linesep

threads = []

# In[file setup]:
# Make the placeholder files
for v in files_out.values():
    with open(os.path.join(WKDIR,v), 'wb') as f_out:
        f_out.write(scan_headers.encode())

# In[file scan def]:
def scan_create(root,f,scan_tp):
    global scan_cnt
    print(f)
    with gzip.open(os.path.join(root,f), 'rb') as f_in:
        for line in f_in.readlines():
            mode = line.decode().split(sep='|')[0]
            if mode in ('1','2','3'):
                mode_tp = mode + scan_tp
            else: # mode not in 1 or 2 or 3
                mode_tp = 'Oth' + scan_tp
            with open(os.path.join(WKDIR,files_out[mode_tp]), 'ab') as f_out:
                f_out.write(line)
            scan_cnt[mode_tp] = scan_cnt[mode_tp] + 1

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
    global scan_cnt # initialise
    for k in scan_cnt.keys():
        scan_cnt[k] = 0

    main() # need this for threading I believe

# In[demo import]:

import pandas as pd
df = pd.read_csv(os.path.join(WKDIR,'On_Train'), sep='|')
