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
        
    def __init__(self):
    
        self._speed = 0
        self._direction = 0
        self._steering_angle = 90
        self.bw = bk.Back_Wheels()
        self.fw = bk.Front_Wheels()

    @property    
    def speed(self):
        """Gets the speed. 0-100. 0 is stop. 100 is max speed.

        Use as getter: Int=BW.speed 

        Returns:
            int: speed of the motors.
        """
        return self._speed

    @speed.setter
    def speed(self, speed):
        """Sets the speed. 0-100. 0 is stop. 100 is max speed. It also sets the speed of the left and right back wheels.

        Use as setter: Bs.speed=Int

        Args:
            speed (int): speed of the motors.
        """
        self._speed = speed     
    
    @property
    def steering_angle(self):
        """Gets the steering angle. 45-135. 90 is straight.

        Use as getter: Int=BC.steering_angle 

        Returns:
            int: steering angle.
        """
        return self._steering_angle

    @steering_angle.setter
    def steering_angle(self, steering_angle):
        """Sets the steering angle. 45-135. 90 is straight.

        Use as setter: BC.steering_angle=Int

        Args:
            steering_angle (int): steering angle of the front wheels.
        """
        self._steering_angle = steering_angle
    
    @property    
    def direction(self):
        """1: forwards, 0: stop, -1: backwards.

        Use as getter: Int=BC.direction

        Returns:
            int: direction (1: forwards, 0: stop, -1: backwards).
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        """Sets the direction. 1: forwards, 0: stop, -1: backwards.

        Use as setter: BC.direction=Int

        Args:
            direction (int): direction. 1: forwards, 0: stop, -1: backwards.
        """
        self._direction = direction   
    
    def drive(self, speed: int = 0, direction: int = 0, steering_angle: int = 90) -> None:
        
        self.fw.turn(steering_angle)
        self.bw.speed = speed
        self.speed = speed
        self.direction = direction
        self.steering_angle = steering_angle
        if direction == 1:
            self.bw.forward()
        elif direction == -1:
            self.bw.backward()          

 
    def stop(self) -> None:
        """Sets the speed to 0.
        """
        self.speed = 0
        self.bw.speed = self.speed

    def Fahrparcours_1(self) -> None:
        """
        Fahrparcours 1 - Vorwärts und Rückwärts: Das Auto fährt mit langsamer Geschwindigkeit
        3 Sekunden geradeaus, stoppt für 1 Sekunde und fährt 3 Sekunden rückwärts.
        """
        t = 1
        self.speed = 40
        self.direction = 1
        self.drive(self.speed, self.direction)
        print('forward speed : {}'.format(self.speed))

        bk.time.sleep(t*3)
        self.stop()
        bk.time.sleep(t*1)

        self.speed = 40
        self.direction = -1
        self.drive(self.speed, self.direction)
        bk.time.sleep(t*3)

        self.stop()
        print('stop speed : {}'.format(self.speed))

    def Fahrparcours_2(self) -> None:
        """
        Fahrparcours 2 - Kreisfahrt mit maximalem Lenkwinkel: Das Auto fährt 1 Sekunde
        geradeaus, dann für 8 Sekunden mit maximalen Lenkwinkel im Uhrzeigersinn und stoppt.
        Dann soll das Auto diesen Fahrplan in umgekehrter Weise abfahren und an den Ausgangspunkt
        zurückkehren. Die Vorgehensweise soll für eine Fahrt im entgegengesetzten
        Uhrzeigersinn wiederholt werden.
        """
        t = 1
        
        # 1 Sek geradeaus vorwärts
        
        self.drive(40, 1, 90)
        print('{} speed : {}, steering angle : {}'.format("forward" if self.direction == 1 else "backward", self.speed, self.steering_angle))
        bk.time.sleep(t*1)
        
       # 8 Sek. vorwärts mit max Lenkwinkel im Uhrzeigersinn 
           
        self.drive(40, 1, 135)
        print('{} speed : {}, steering angle : {}'.format("forward" if self.direction == 1 else "backward", self.speed, self.steering_angle))
        bk.time.sleep(t*8)
        
       # Stop 
               
        self.stop()
        print('stop speed : {}'.format(self.speed))
        bk.time.sleep(t*1)

       # 8 Sek. rückwärts mit max Lenkwinkel im Uhrzeigersinn 
    
        self.drive(40, -1, 135)
        print('{} speed : {}, steering angle : {}'.format("forward" if self.direction == 1 else "backward", self.speed, self.steering_angle))
        bk.time.sleep(t*8)

        # 1 Sek geradeaus rückwärts
        
        self.speed = 40
        self.direction = -1
        self.steering_angle = 90
        self.drive(40, -1, 90)
        print('{} speed : {}, steering angle : {}'.format("forward" if self.direction == 1 else "backward", self.speed, self.steering_angle))
        bk.time.sleep(t*1)

       # Stop 
               
        self.stop()
        print('stop speed : {}'.format(self.speed))
        bk.time.sleep(t*1)

def main():
    bc = BaseCar()
    bc.Fahrparcours_1()
   # bc.Fahrparcours_2()
    

if __name__ == '__main__':
    main()
    
