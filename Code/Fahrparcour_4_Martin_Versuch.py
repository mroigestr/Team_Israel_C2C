"""
Fahrparcours 4 ‑ Erkundungstour: Das Auto soll geradeaus fahren und im Falle eines
Hindernisses die Fahrrichtung ändern und die Fahrt fortsetzen. Zur Änderung der
Fahrrichtung soll ein maximaler Lenkwinkel eingeschlagen und rückwärts gefahren
werden. Optional können sowohl die Geschwindigkeit als auch die Fahrtrichtung bei
freier Fahrt variiert werden. Zusätzlich sollen die Fahrdaten aufgezeichent werden

"""




from time import time
from tracemalloc import stop
import SonicCar as sc
import Basecar as bc

class Fahrparcours_4(self) -> None:

    def __init__(self) -> None:
        super().__init__()
        self.fw = bc.bk.Front_Wheels()
        self.bw = bc.bk.Back_Wheels()
        self.us = bc.bk.Ultrasonic()
        self._too_close = 10


    #Ausrichten der Vorderräder
    print('Ausrichtung der Vorderräder')
        fw = Front_Wheels()
        fw.turn(45)
        time.sleep(.5)
        fw.turn(135)
        time.sleep(.5)
        print('Servo der Lenkung auf 90 Grad/geradeaus ausgerichtet! (CRTL-C zum beenden)')
        while True:
            fw.turn(90)
            stop



#Ausweichen Rückwärtsfahren + Rechts fahren
    
    
    def evade(self, evade):
        while too_close = True:
        self.drive(40, 2, 180)
        self.too_close = -4
        self.obstacle(self.too_close)


# Wieder gerade ausfahren

    def reset:
    
        if evade == 0:
            self.stop()
            self.drive(40, 1, 90)
            bw.time(10)
        
        else:
            self.fw
            fw.time.sleep(t*3)



def main():

sc = Soniccar()
sc.Fahrparcours_4()



if __name__ == '__main__'
main()


                

      