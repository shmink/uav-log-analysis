'''
Created on Sep 4, 2016

@author: Isaac Jessop

/* Record42_12 class

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

from datcom.Record import Record
import math

class Record42_12(Record):
    '''
    classdocs
    '''


    def __init__(self, convertDat):
        '''
        Constructor
        '''
        self.current = self
        self.longitude = 0.0 
        self.latitude = 0.0 
        self.height = 0.0 # height above HP meters 
        self.flightTime = 0 
        self.roll = 0 
        self.pitch = 0 
        self.yaw = 0 
        self.convertDat = convertDat 
        self.failure = 0x00 
        self.flyc_state = 0x000 
        self.nonGPSError = 0x00 
        self.NGPE = "" 
        self.dwflyState = 0 
        self.FLCS = "" 
        self.connectedToRC = 0x80 
# 
#     // 10 hz
#     // length 52
        super(Record42_12, self).__init__(_type = 42,_subtype = 12)

    def process(self, _payload) :
        super(Record42_12, self).process(_payload)
        payloadBB = _payload.getBB();
        self.longitude = math.degrees(payloadBB.getDouble(0));
        self.latitude = math.degrees(payloadBB.getDouble(8));
        self.height = float(payloadBB.getShort(16)) / 10.0
        self.pitch = float(payloadBB.getShort(24)) / 10.0
        self.roll = float(payloadBB.getShort(26)) / 10.0
        self.yaw = float(payloadBB.getShort(28)) / 10.0
        self.flyc_state = (0x7F & payloadBB.get(30))
        self.connectedToRC  = (0x80 & payloadBB.get(30))
        self.failure = payloadBB.get(38) ## possible linked to MOTOR_START_FAILED_CAUSE in osd.js
        self.nonGPSError = (0x07 & payloadBB.get(39))
        self.flightTime = payloadBB.getShort(42) * 100;

        if self.convertDat.kmlType >= 0 and self.convertDat.tickRangeLower <= _payload.getTickNo(): 
            if self.longitude != 0.0 and self.latitude != 0.0 and self.height != 0.0 :
                alt = self.height
                if self.convertDat.kmlType == 1 :
                    alt += self.convertDat.homePointElevation

                self.convertDat.kmlPS.write("             %s,%s,%s" % (
                                            self.longitude,self.latitude, alt))

    def setStateStrings(self): 

        NGPEStats = {
            1:"FORBIN",
            2:"GPSNUM_NONENOUGH",
            3:"GPS_HDOP_LARGE",
            4:"GPS_POSITION_NON_MATCH",
            5:"SPEED_ERROR_LARGE",
            6:"YAW_ERROR_LARGE",
            7:"COMPASS_ERROR_LARGE"
        }
        self.NPGE = NGPEStats.get(self.nonGPSError)

        FLCSStats = {
                    0:{'st':"MANUAL",'dwflyState': 1},
                    1:{'st':"ATTI",'dwflyState': 2},
                    2:{'st':"ATTI_CL",'dwflyState': 3},
                    3:{'st':"ATTI_HOVER",'dwflyState': 4},
                    4:{'st':"HOVER",'dwflyState': 5},
                    5:{'st':"GSP_BLAKE",'dwflyState': 6},
                    6:{'st':"GPS_ATTI",'dwflyState': 7},
                    7:{'st':"GPS_CL",'dwflyState': 8},
                    8:{'st':"GPS_HOME_LOCK",'dwflyState': 9},
                    9:{'st':"GPS_HOT_POINT",'dwflyState': 20},
                    10:{'st':"ASSISTED_TAKEOFF",'dwflyState': 30},
                    11:{'st':"AUTO_TAKEOFF",'dwflyState': 40},
                    12:{'st':"AUTO_LANDING",'dwflyState': 50},
                    13:{'st':"ATTI_LANDING",'dwflyState': 60},
                    14:{'st':"NAVI_GO",'dwflyState': 70},
                    15:{'st':"GO_HOME",'dwflyState': 80},
                    16:{'st':"CLICK_GO",'dwflyState': 90},
                    17:{'st':"JOYSTICK",'dwflyState': 200},
                    23:{'st':"ATTI_LIMITED",'dwflyState': 300},
                    24:{'st':"GPS_ATTI_LIMITED",'dwflyState': 400},
                    25:{'st':"FOLLOW_ME",'dwflyState': 500},
                    100:{'st':"OTHER",'dwflyState': 600}
                    }

        stat = FLCSStats.get(self.flyc_state)
        self.FLCS = stat.get('st')
        self.dwflyState = stat.get('dwflyState')

        