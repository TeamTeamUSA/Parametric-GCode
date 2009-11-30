#Parametric GCode Example 3: Build a wobbly cylinder
#
#Here we'll introduce rotation.  We'll include a function in
# the G1Code class called "Rotate" that rotates the XY
# coordinates by some number of radians.
#To make the effects of this visible, we'll change from a
# circular cross section to an elliptical one.

#Import the math library
import math


#Rounding function
# Input: num=int, float, or string; r=int  
# Output: string  
def myRound(num, r=0):  
	if type(num) is str:  
		num = float(num)  
	num += 0.5/(10**r)  
	if r == 0:  
		return str(int(num))  
	else:
		num = str(num)  
		return num[:num.find('.')+r+1]


#G1 Code Object
class G1Code:
	def __init__(self, X=0, Y=0, Z=0, F=0):
		self.X =X
		self.Y =Y
		self.Z = Z
		self.F = F

	def __str__(self):
		#Added rounding
		string = "G1 X" + myRound(self.X,2) + " Y" + myRound(self.Y,2) + " Z" + myRound(self.Z,2) + " F" + str(self.F)
		return string

	#Rotate the XY point of the GCode
	def rotate(self, Theta):
		OldX = self.X
		OldY = self.Y
		self.X = OldX * math.cos(Theta) - OldY * math.sin(Theta)
		self.Y = OldX * math.sin(Theta) + OldY * math.cos(Theta)



filename = "test.gcode"
ThisGCode = G1Code(X=0, Y=0, Z=0, F=1000)
Zsteps = 0
Tsteps = 0

#Cylinder parameters
MajorAxis = 10
MinorAxis = 7


#Open the output file and paste on the "headers"
FILE = open(filename,"w")
FILE.writelines("G21\n")
FILE.writelines("G90\n")
FILE.writelines("M103\n")
FILE.writelines("M105\n")
FILE.writelines("M104 S220.0\n")
FILE.writelines("M101\n")

#Step through the Z range of the object.
for Zsteps in range(30):
	#Hop up to the next level, staying put
	ThisGCode.Z = 0.4 * Zsteps
	FILE.writelines(str(ThisGCode)+ "\n")
	
	#The Tsteps define the parametric equation for a circle:
	# X = R cos (T), Y = R sin (T)
	# The range of T should be 0 to 2pi
	for Tsteps in range(62):
		ThisGCode.X = MajorAxis * math.cos(Tsteps / 10.0)
		ThisGCode.Y = MinorAxis * math.sin(Tsteps / 10.0)

		#Rotation as a function of the height in Z
		ThisGCode.rotate(Zsteps/15.0)
		FILE.writelines(str(ThisGCode)+"\n")


ThisGCode.Z = ThisGCode.Z + 10
FILE.writelines(str(ThisGCode)+ "\n")
FILE.writelines("M104 S0\n")

FILE.close