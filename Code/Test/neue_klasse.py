import basisklassen as bk

class BaseCar(object):

    """Klasse - BaseCar: Entwicklung und Testen einer Klasse BaseCar mittels der Basisklassen
        mit vorgegebenen Anforderungen. Die Klasse soll folgende Attribute (mit entsprechenden
        Gettern und Settern) und Methoden haben:
        • steering_angle: Zugriff auf den Lenkwinkel
        • drive(int, int): Fahren mit übergebener Geschwindigkeit und Fahrrichtung
        • stop(): Anhalten des Autos
        • speed: Zugriff auf die Geschwindigkeit
        • direction: Zugriff auf die Fahrrichtung (1: vorwärts, 0: Stillstand, -1 Rückwärts)
        Die Klasse BaseCar soll mittels folgenden Aufgaben getestet werden.
        • Fahrparcours 1 - Vorwärts und Rückwärts: Das Auto fährt mit langsamer Geschwindigkeit
        3 Sekunden geradeaus, stoppt für 1 Sekunde und fährt 3 Sekunden rückwärts.
        • Fahrparcours 2 - Kreisfahrt mit maximalem Lenkwinkel: Das Auto fährt 1 Sekunde
        geradeaus, dann für 8 Sekunden mit maximalen Lenkwinkel im Uhrzeigersinn und stoppt.
        Dann soll das Auto diesen Fahrplan in umgekehrter Weise abfahren und an den Ausgangspunkt
        zurückkehren. Die Vorgehensweise soll für eine Fahrt im entgegengesetzten
        Uhrzeigersinn wiederholt werden.
        """
        
    def __init__(self, steering_angle: int = 0, direction: int = 0, drivingTime: int = 0):

        self._steering_angle = steering_angle
       # self._speed = bk.Back_Wheels.speed()
        self._direction = direction
        self._drivingTime = drivingTime
    
    def Fahrparcours_1(self) -> None:
        """
        Fahrparcours 1 - Vorwärts und Rückwärts: Das Auto fährt mit langsamer Geschwindigkeit
        3 Sekunden geradeaus, stoppt für 1 Sekunde und fährt 3 Sekunden rückwärts.
        """
        t = 1
        bk.Back_Wheels.speed = 10
        bk.Back_Wheels.forward()
        print('forward speed : {}'.format(bk.Back_Wheels.speed))

        bk.time.sleep(t*3)
        bk.Back_Wheels.stop()
        bk.time.sleep(t*1)

        bk.Back_Wheels.backward()
        bk.time.sleep(t*3)

        bk.Back_Wheels.speed = 0
        print('stop speed : {}'.format(bk.Back_Wheels.speed))



def main():
    bw = BaseCar()
    bw.Fahrparcours_1()

main