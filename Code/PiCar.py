import BaseCar as bc
import SonicCar as sc
import SensorCar as rc

class PiCar(object):
    def __init__(self): # ist notwendig?
        pass

    def menu(self):
        """Function for selecting the Fahrparcours methoden

        Args:
            Fahrparcours (int): The Fahrparcours that can be choosen by the user
        """
        print('-- FAHRPARCOURSES--------------------')

        fahrparcour = None

        fp1_text = 'Fahrparcours 1 - Vorwärts und Rückwärts fahren'
        fp2_text = 'Fahrparcours 2 - Kreisfahrt mit maximalem Lenkwinkel Vorwärts und Rückwärts fahren'
        fp3_text = 'Fahrparcours 3 - Vorwärtsfahren bis zum Hindernis und stoppen'
        fp4_text = 'Fahrparcours 4 - FP3 + Hindernis umfahren'
        fp5_text = 'Fahrparcours 5 - Linie verfolgen + Hinderniserkennung aktiv'
        fp6_text = 'Fahrparcours 6 - Linie verfolgen + Hinderniserkennung aktiv + Rückwärtsfahren bei engen Kurven'

        Fahrparcour = {
            1: fp1_text,
            2: fp2_text,
            3: fp3_text,
            4: fp4_text,
            5: fp5_text,
            6: fp6_text
        }

        if fahrparcour == None:
            print('--' * 20)
            print('Auswahl:')
            for m in Fahrparcour.keys():
                print('{i} - {name}'.format(i=m, name=Fahrparcour[m]))
            print('--' * 20)

        while fahrparcour == None:
            fahrparcour = input('Fahrparcours auswählen[1..6] ')
            
            if fahrparcour in ['1', '2', '3', '4', '5', '6']:
                break
            # elif fahrparcour == "i":
            #     print('Fahrparcours 1 - Vorwärts und Rückwärts fahren')
            #     print('Fahrparcours 2 - Kreisfahrt mit maximalem Lenkwinkel Vorwärts und Rückwärts fahren')
            #     print('Fahrparcours 3 - Vorwärtsfahren bis zum Hinderniss und stoppen')
            #     print('Fahrparcours 4 - FP3 + Hinderniss umfahren')
            #     print('Fahrparcours 5 - Linie verfolgen + Hindernisserkennung aktiv')
            #     print('Fahrparcours 6 - Linie verfolgen + Hindernisserkennung aktiv + Rückwärtsfahren bei engen Kurven')
            else:
                fahrparcour = None
                print('Getroffene Auswahl nicht möglich.')           
            
        
        fahrparcour = int(fahrparcour)

        if fahrparcour == 1:
            print(fp1_text)
            fp1 = bc.BaseCar()
            fp1.Fahrparcours_1()

        if fahrparcour == 2:
            print(fp2_text)
            fp2 = bc.BaseCar()
            fp2.Fahrparcours_2()

        if fahrparcour == 3:
            print(fp3_text)
            fp3 = sc.SonicCar()
            fp3.Fahrparcours_3()

        if fahrparcour  == 4:
            print(fp4_text)
            fp4 = sc.SonicCar()
            fp4.Fahrparcours_4()

        if fahrparcour == 5:
            print(fp5_text)
            fp5 = rc.SensorCar()
            fp5.Fahrparcours_5()
        
        if fahrparcour == 6:
            print(fp6_text)
            fp6 = rc.SensorCar()
            fp6.Fahrparcours_6()

def main():
    pc = PiCar()
    pc.menu()
if __name__ == '__main__':
    main()

