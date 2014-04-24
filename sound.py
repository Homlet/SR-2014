from time import sleep
from sr import OUTPUT
from log import log, indented

class Sound:
    def __init__(self, robot, active):
        log(robot, "Initialisig Sound Controller...")
        self.rduino = robot.ruggeduinos[0]
        self.set_pin = self.rduino.digital_write
        self.data = [4,3,2]
        self.read = 5
        self.set_pins()
        self.robot = robot
        self.enabled = active
        if not self.robot.enabled: # if sound is disabled in constant of robot.py
            log(robot, "Sound Disabled in Constant!")
            return
        
        self.sounds = {
            'STOP': '000',
            'R2D2': '001',
            'Radar': '010',
            'Valkyries': '011',
            'Heart': '100',
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
        log(self.robot, "Sound Controller Initialised.")
        
    def set_pins(self):
        """Initialises the Pins on the ruggeduino for sound output"""
        for pin in self.data + [self.read]:
            self.rduino.pin_mode(pin, OUTPUT)
        
    def play(self, sound):
        """ Sends command to play sound. """
        if not self.enabled: #if sound is disabled.
            log(self.robot, "Sound is Disabled, Ignoring Request.")
            return
        
        sound_data = self.sounds.get(sound)

        if sound_data == None:
            log(self.robot, "Error Playing Sound '" + sound + "'")
            return

        for bit, pin in enumerate(self.data):
            self.set_pin(pin, int(sound_data[bit]))
    
        self.set_pin(self.read, True)
        if sound_data == "STOP":
            log(self.robot, "Stopping Playback of sounds")
        else:
            log(self.robot, 'Now Playing:' + sound + 'with binary code' + sound_data)
            
        sleep(.05) 
        self.set_pin(self.read, False)
        sleep(.05)
        
    def stop(self):
        """ Sends command to stop playing all sounds. """
        self.play('STOP')