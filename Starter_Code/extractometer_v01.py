
# coding: utf-8

# In[27]:

from __future__ import print_function
import os
import gzip
import threading
import sys


# In[29]:

WKDIR = 'C:\\Users\\Admin\\Documents\\MelbDatathon2018'
os.chdir(WKDIR)

fo_s0on = 'samp0_on'
fo_s0off = 'samp0_off'

fo_s1on = 'samp1_on'
fo_s1off = 'samp1_off'

scan_cnt = {'samp0_on':0, 'samp0_off':0, 'samp1_on':0, 'samp1_off':0}
scan_headers = 'Mode|BusinessDate|DateTime|CardID|CardType|ParentRoute|VehicleID|RouteID|StopID\r\n'

threads = []


# In[40]:

def scan_create(root,f,f_scan):
    global scan_cnt
    print(f)
    if not scan_cnt[f_scan]: # create file on first of type
        with gzip.open(os.path.join(root,f), 'rb') as f_in, open(os.path.join(WKDIR,f_scan), 'wb') as f_out:
            f_out.write(scan_headers)
            f_out.write(f_in.read())
    else: # else append to file on subsequent of type
        with gzip.open(os.path.join(root,f), 'rb') as f_in, open(os.path.join(WKDIR,f_scan), 'ab') as f_out:
            f_out.write(f_in.read())
    scan_cnt[f_scan] = scan_cnt[f_scan] + 1


# In[ ]:

def main():
    counter = 0
    for root,dirs,files in os.walk(WKDIR):
        for f in files:
            if f.endswith('.gz'):
                if 'Samp_0' in root and  'On' in root:
                    threads.append(threading.Thread(target=scan_create, args=(root,f,fo_s0on)))
                    threads[-1].start()
                elif 'Samp_0' in root and  'Off' in root:
                    threads.append(threading.Thread(target=scan_create, args=(root,f,fo_s0off)))
                    threads[-1].start()
                elif 'Samp_1' in root and  'On' in root:
                    threads.append(threading.Thread(target=scan_create, args=(root,f,fo_s1on)))
                    threads[-1].start()
                elif 'Samp_1' in root and  'Off' in root:
                    threads.append(threading.Thread(target=scan_create, args=(root,f,fo_s1off)))
                    threads[-1].start()
        for thr in threads:
            thr.join()
    
if __name__ == "__main__":
    global scan_cnt # initialise
    scan_cnt['samp0_on']  = 0   
    scan_cnt['samp0_off'] = 0
    scan_cnt['samp1_on']  = 0
    scan_cnt['samp1_off'] = 0

    main() # need this for threading I believe


# ### NOTE:
# #### The below import command may be exceedingly slow as loading all into memory
# 

# In[ ]:

import pandas as pd
df = pd.read_csv(os.path.join(WKDIR,fo_s0off), sep='|')

