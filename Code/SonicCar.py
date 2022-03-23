import BaseCar as bc

class SonicCar(bc.BaseCar):
# class SonicCar:
    """
    Eine Klasse SonicCar soll die Eigenschaften der Klasse BaseCar
    erben und zusätzlich den Zugriff auf den Ultraschall‑Sensor ermöglichen. Die Fahrdaten
    umfassen die Geschwindigkeit, die Fahrtrichtung, den Lenkwinkel und die Daten des
    Ultraschall‑Sensors. Dazu soll Folgendes entwickelt und getestet werden.
    """
    # def __init__(self, speed: int = 0, direction: int = 0, steering_angle: int = 90):
    #     super().__init__(speed, direction, steering_angle)

    def __init__(self):
        # super().__init__(speed, direction, steering_angle)
        # super().__init__()

        # self._speed = 0
        # self._direction = 0
        # self._steering_angle = 90
        self.fw = bc.bk.Front_Wheels()
        self.bw = bc.bk.Back_Wheels()
        self.us = bc.bk.Ultrasonic()
        self._too_close = 10


    @property
    def too_close(self):
        return self._too_close

    @too_close.setter
    def too_close(self, too_close):
        if too_close <= 0:
            print("Warnwert muss > 0 sein und nicht {}!".format(too_close))
            print("Warnwert wird auf 10 cm gesetzt!")
            self._too_close = 10
        else:
            self._too_close = too_close
    
    
    def obstacle(self, too_close):
        """
        Ermittelt Abstand und unterbricht bei Wert < "too_close"
        """
        while True:
            bc.bk.time.sleep(0.1)
            dist = self.us.distance()
            print(dist, "cm")
            if dist > 0 and dist < too_close:
                print("Achtung!", dist, "cm")
                self.stop()
                break

    
    def Fahrparcours_3(self) -> None:

        self.drive(40, 1, 90)
        self.too_close = -4
        self.obstacle(self.too_close)


def main():
    sc = SonicCar()
    sc.Fahrparcours_3()


if __name__ == '__main__':
    main()
