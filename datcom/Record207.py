'''
Created on Sep 3, 2016

@author: Isaac Jessop
/* Record207 class

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

#     // 200 hZ
#     // length 122
import math
from datcom.Record import Record
from datcom.Record255_1 import Record255_1
from datfile.Util import Util

class Record207(Record):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

        self.longRad = 0.0
        self.latRad = 0.0;
        self.numSats = 0
        self.quatW = 0.0 
        self.quatX = 0.0 
        self.quatY = 0.0
        self.quatZ = 0.0
        self.gpsAlt = 0.0
        self.accelX = 0.0
        self.accelY = 0.0
        self.accelZ = 0.0
        self.gyroX = 0.0
        self.gyroY = 0.0
        self.gyroZ = 0.0
        self.baroAlt = 0.0
        self.velN = 0.0
        self.velE = 0.0
        self.velD = 0.0
        self.magX = 0.0
        self.magY = 0
        self.magZ = 0
        self.valid = False
        self.diffX = 0.0
        self.diffY = 0.0
        self.diffZ = 0.0
        self.x4 = 0.0
        self.x5 = 0.0
        self.x6 = 0.0
        self.imuTemp = 0
        self.i2 = 0
        self.i3 = 0
        self.i4 = 0
        self.i5 = 0
        self.totalZGyro = 0.0
        self.lastTickNo = 0
        self.dtLastTickNo = 0
        self.distanceTraveled = 0.0
        self.dtLastLat = 0.0
        self.dtLastLong = 0.0
        self.bearingDeclined = 0.0
        self.bearingTrue = 0.0

        super(Record207, self).__init__(_type = 207,_subtype = 1) 

        self.current = self
        self.util = Util()
# 
    def process(self, _payload) :

        super(Record207, self).process(_payload)
        self.longRad = self.payloadBB.getDouble(0)
        self.latRad = self.payloadBB.getDouble(8)
        self.gpsAlt = self.payloadBB.getFloat(16)
        self.accelX = self.payloadBB.getFloat(20)
        self.accelY = self.payloadBB.getFloat(24)
        self.accelZ = self.payloadBB.getFloat(28)
        self.gyroX = float(math.degrees(self.payloadBB.getFloat(32)))
        self.gyroY = float(math.degrees(self.payloadBB.getFloat(36)))
        self.gyroZ = float(math.degrees(self.payloadBB.getFloat(40)))
        self.baroAlt = self.payloadBB.getFloat(44)
        self.quatW = self.payloadBB.getFloat(48)
        self.quatX = self.payloadBB.getFloat(52)
        self.quatY = self.payloadBB.getFloat(56);
        self.quatZ = self.payloadBB.getFloat(60);
        self.diffX = self.payloadBB.getFloat(64);
        self.diffY = self.payloadBB.getFloat(68);
        self.diffZ = self.payloadBB.getFloat(72);
        self.velN = self.payloadBB.getFloat(76);
        self.velE = self.payloadBB.getFloat(80);
        self.velD = self.payloadBB.getFloat(84);
        self.x4 = self.payloadBB.getFloat(88);
        self.x5 = self.payloadBB.getFloat(92);
        self.x6 = self.payloadBB.getFloat(96);
        self.magX = self.payloadBB.getShort(100);
        self.magY = self.payloadBB.getShort(102);
        self.magZ = self.payloadBB.getShort(104);
        self.imuTemp = self.payloadBB.getShort(106);
        self.i2 = self.payloadBB.getShort(108);
        self.i3 = self.payloadBB.getShort(110);
        self.i4 = self.payloadBB.getShort(112);
        self.i5 = self.payloadBB.getShort(114);
        self.numSats = self.payloadBB.get(116);

        if _payload.tickNo > _payload.datFile.flightStartTick :
            if _payload.tickNo > self.dtLastTickNo + 60 :
                if self.dtLastLat == 0.0 and self.dtLastLong == 0.0 :
                    self.dtLastLat = self.latRad;
                    self.dtLastLong = self.longRad;

                dist = self.util.distance(self.latRad, self.longRad, self.dtLastLat, self.dtLastLong)
                self.bearingTrue = self.util.bearing(self.dtLastLat, self.dtLastLong,\
                                                 self.latRad, self.longRad)
                x = self.bearingTrue - Record255_1.declination
                if x < -180.0:
                    self.bearingDeclined = 360.0 + x
                elif x > 180.0:
                    self.bearingDeclined = x - 360.0
                else:
                    self.bearingDeclined = x
                self.distanceTraveled += dist
                self.dtLastLat = self.latRad
                self.dtLastLong = self.longRad
                self.dtLastTickNo = _payload.tickNo

        if self.lastTickNo != 0 :
            self.totalZGyro += self.gyroZ * float(_payload.tickNo - self.lastTickNo) / 600.0

        self.lastTickNo = _payload.tickNo
        