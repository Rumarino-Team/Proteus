#!/usr/bin/env python

#Neccesary imports
import sys
from AbstractMissionNode import AbstractMissionNode


#Name variable is necessary
name = 'Test'


#vision Topic name = VisionOutput



class TestNode(AbstractMissionNode):

	#Copy constructor identically
	def __init__(self, name, argv):
		super(TestNode, self).__init__(name, argv)

	def _runMission(self):
		#HERE GOES MISSION CODE
		#For testing purposes
		print("Running test mission")
		var1 = 100
		var2 = 200
		var3 = 300

		while(True):
			if(self.is_vision_dirty()):
				print("Vision Data- x:" + str(self.get_centroid()))
			else:
				print("Data is clean")
			"""
			key_pressed = raw_input()
			if(key_pressed == 'a'):
				print("Key received, read: " + key_pressed)
				self.pitch_degrees(var1)
				var1 = var1 + 1
			elif(key_pressed == 's'):
				print("Key received, read: " + key_pressed)
				self.go_to_depth(var2)
				var2 = var2 + 1
			elif(key_pressed == 'd'):
				print("Key received, read: " + key_pressed)
				self.forwards(True, var3)
				var3 = var3 + 1
			else:
				print("Incorrect key pressed: " + key_pressed + " does nothing")
			"""




#copy y paste identicamente
if __name__ == '__main__':
        mission = TestNode(name, sys.argv) 
