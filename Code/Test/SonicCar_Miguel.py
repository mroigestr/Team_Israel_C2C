import BaseCar_new_220323 as bc

class SonicCar(object):
    
    """Klasse - SonicCar: Eine Klasse SonicCar soll die Eigenschaften der Klasse BaseCar
    erben und zusätzlich den Zugriff auf den Ultraschall-Sensor ermöglichen. Die Fahrdaten
    umfassen die Geschwindigkeit, die Fahrtrichtung, den Lenkwinkel und die Daten des
    Ultraschall-sensors. Dazu soll Folgendes entwickelt und getestet werden.
    • Fahrparcours 3 - Vorwärtsfahrt bis Hindernis: Fahren bis ein Hindernis im Weg ist und
    dann stoppen. Während dieser Fahrt sollen die Fahrdaten (Geschwindigkeit, Lenkwinkel,
    Fahrrichtung, Sensordaten) aufgezeichnet werden.
    • Fahrparcours 4 - Erkundungstour: Das Auto soll geradeaus fahren und im Falle eines
    Hindernisses die Fahrrichtung ändern und die Fahrt fortsetzen. Zur Änderung der
    Fahrrichtung soll ein maximaler Lenkwinkel eingeschlagen und rückwärts gefahren
    werden. Optional können sowohl die Geschwindigkeit als auch die Fahrtrichtung bei
    freier Fahrt variiert werden. Zusätzlich sollen die Fahrdaten aufgezeichent werden."""

    def __init__(self):
        
        self._speed = 0
        self._direction = 0
        self._steering_angle = 90
        self.bc1 = bc.BaseCar()
        self.us = bc.bk.Ultrasonic()

    
    def drive_till_obstacle(self, speed: int = 0, direction: int = 0, steering_angle: int = 90) -> None:
        
        self.bc1.drive(speed, direction, steering_angle)
        
        while True:
            print(self.us.distance())
            if self.us.distance() > 0 and self.us.distance() < 5 :
                self.bc1.stop()
                break
            bc.bk.time.sleep(0.1)
        
        print("ende")
                
                
    def Fahrparcours_3(self) -> None:
        
        self.drive_till_obstacle(40, 1, 90)
        
def main():
    sc = SonicCar()
    sc.Fahrparcours_3()


if __name__ == '__main__':
    main()
    



