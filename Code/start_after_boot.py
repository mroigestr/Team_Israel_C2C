#coding=utf-8
#!/usr/bin/env python

import os
"""
Dieses Programm starte ein Kommando mittels des Standard-Modul 'os'.
Der String command enthält ein Kommando in der Form, welches auch direkt im Terminal einzugeben ist.
"""

print('-- START AFTER BOOT --')
#Beispielhaft wird in den folgendne 3 Zeilen das Programm 'greet.py' gestartet
command = 'python3 greet.py' 
print('start_after_boot.py startet: {x}'.format(x=command))
os.system(command)

"""
#Beispielhaft wird in den folgenden 3 Zeilen das Programm 'greet_and_select.py' gestartet
command = 'python3 demo_projektphase1.py --modus 1'
print('start_after_boot.py startet: {x}'.format(x=command))
os.system(command)
"""
