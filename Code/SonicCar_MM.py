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

def main():
    sc = SonicCar()
    sc.Fahrparcours_1()


if __name__ == '__main__':
    main()
