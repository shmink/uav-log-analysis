'''
Created on Sep 8, 2016

@author: Isaac Jessop

/* RollPitchYaw class

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that redistribution of source code include
the following disclaimer in the documentation and/or other materials provided
with the distribution.

THIS SOFTWARE IS PROVIDED BY ITS CREATOR "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE CREATOR OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
'''


import math
class RollPitchYaw(object):
    '''
    classdocs
    '''

    def __init__(self, roll, pitch, yaw):
        '''
        Constructor
        '''

        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def toString(self):
        return "Roll: %4f Pitch: %4f Yaw: %4f" %(self.roll, self.pitch, self.yaw)

    def toDegString(self):
        return "Roll: %4f Degs Pitch: %4f Degs Yaw: %4f Degs" %(
                 math.degrees(self.roll), math.degrees(self.pitch), math.degrees(self.yaw))

    def getRollDeg(self):
        return math.degrees(self.roll) 

    def getPitchDeg(self):
        return math.degrees(self.pitch) 

    def getYawDeg(self):
        return math.degrees(self.yaw) 

