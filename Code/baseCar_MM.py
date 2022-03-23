import basisklassen as bk

class BaseCar:
    """
    Entwicklung und Testen einer Klasse BaseCar mittels der Basisklassen
    mit vorgegebenen Anforderungen. Die Klasse soll folgende Attribute (mit entsprechen‑
    den Gettern und Settern) und Methoden haben:
    - steering_angle: Zugriff auf den Lenkwinkel
    - drive(int, int): Fahren mit übergebener Geschwindigkeit und Fahrrichtung
    - stop(): Anhalten des Autos
    - speed: Zugriff auf die Geschwindigkeit
    - direction: Zugriff auf die Fahrrichtung (1: vorwärts, 0: Stillstand, ‑1 Rückwärts)
    Die Klasse BaseCar soll mittels folgenden Aufgaben getestet werden.
    """


    def __init__(self, steering_angle: int = 0, speed: int = 0, direction: int = 0):

        self._steering_angle = steering_angle
        self._speed = speed
        self._direction = direction

        self.bw = bk.Back_Wheels()


    def Fahrparcours_1(self):
        bw = bk.Back_Wheels()
        bw.speed = 43
        bw.forward()
        bk.time.sleep(3)
        bw.stop()
        print("Fahrparcours1 gefahren")


def main():
    bc = BaseCar()
    bc.Fahrparcours_1()


main()
