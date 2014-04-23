from time import sleep
from sr import OUTPUT
from log import log, indented

class Sound:
    def __init__(self, robot):
        log(robot, "Initialisig Sound Controller...")
        self.rduino = robot.ruggeduinos[0]
        self.set_pin = self.rduino.digital_write
        self.data = [4,3,2]
        self.read = 5
        self.set_pins()
        
        self.sounds = {
            'STOP': '000',
            'R2D2': '001',
            'Radar': '010',
            'Valkyries': '011',
            'DialUp': '100',
            'Dixie': '101',
            '': '110',
            'Mario': '111'
        }
        
        for pin in self.data:
            self.set_pin(pin, False) #0's all pins at startup
        
        #message pi to start code
        self.set_pin(self.read, True)
        sleep(.05)
        self.set_pin(self.read, False)
        sleep(.05)
    log(robot, "Sound Controller Initialised.")
        
    def set_pins(self):
        for pin in self.data + [self.read]:
            self.rduino.pin_mode(pin, OUTPUT)
        
    def play(self, sound):
        """ Sends command to play sound. """
        sound_data = self.sounds.get(sound)

        if sound_data == None:
            log(robot, "Error Playing Sound '" + sound + "'")
            return

        for bit, pin in enumerate(self.data):
            self.set_pin(pin, int(sound_data[bit]))
    
        self.set_pin(self.read, True)
        if sound_data == "STOP":
            log(robot, "Stopping Playback of sounds")
        else:
            log(robot, 'Now Playing:' + sound + 'with binary code' + sound_data)
            
        sleep(.05) 
        self.set_pin(self.read, False)
        sleep(.05)
        
    def stop(self):
        """ Sends command to stop playing all sounds. """
        self.play('STOP')