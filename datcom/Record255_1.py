'''
Created on Sep 4, 2016

@author: isaac
/* Record255_1 class

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
from datfile.TSAGeoMag import TSAGeoMag
from datfile.Util import Util
import math
import re

class Record255_1(Record):
    '''
    classdocs
    '''
    declination = 0.0
    inspire1 = False

    def __init__(self, ConvertDat):
        '''
        Constructor
        gets passed a instance of ConvertDat
        '''

        self.current = self
        self.longitudeHP = 0.0
        self.latitudeHP = 0.0 
        self.longitudeHPDegrees = 0L 
        self.latitudeHPDegrees =0L 
        self.heightHP = 0.0 
        self.validHP = False 
        self.geoMag = TSAGeoMag() 
        self.inclination = 0.0 
        self.text = "" 
        self.convertDat = ConvertDat
        self.standard = False 
        self.batteryBarCode = "" 
        self.P3 = False 
    
        super(Record255_1, self).__init__(_type = 255, _subtype = 1)
    
    def process(self, _payload):
        super(Record255_1, self).process(_payload)
        tickNo = _payload.getTickNo()
        timeOffset = self.convertDat.timeOffset;
        payloadString = _payload.getString();

        if len(payloadString) > 0 :
            if self.convertDat.csvEventLogOutput and self.convertDat.tickRangeLower <= _payload.getTickNo():
                if len(self.text) > 0 :
                    self.text = "%s|" % self.text

                self.text = "%s%s" % (self.text,payloadString)

            if self.convertDat.eloPS is not None and self.convertDat.tickRangeLower <= _payload.getTickNo():
                self.convertDat.eloPS.write("%s : %s : %s" %(
                                Util.timeString(tickNo, timeOffset), tickNo, payloadString))

            if payloadString.find("Home Point") > -1 :
                latlonPattern = re.compile(".*?(-*\\d+\\.\\d+)\\s+(-*\\d+\\.\\d+)\\s+(-*\\d+\\.\\d+)")
                latlonMatcher = re.match(latlonPattern, payloadString)

                if latlonMatcher is not None:
                    lat = latlonMatcher.groups()[0]
                    lon = latlonMatcher.groups()[1]
                    hei = latlonMatcher.groups()[2]
                    self.longitudeHPDegrees = float(lon)
                    self.latitudeHPDegrees = float(lat)
                    self.declination = self.geoMag.getDeclination(self.latitudeHPDegrees,
                                                                  self.longitudeHPDegrees)
                    Record255_1.declination = self.declination

                    self.inclination = self.geoMag.getDipAngle(self.latitudeHPDegrees,
                                                               self.longitudeHPDegrees)

                    self.heightHP = float(hei)
                    self.longitudeHP = math.radians(self.longitudeHPDegrees)
                    self.latitudeHP = math.radians(self.latitudeHPDegrees);
                    self.validHP = True

            elif payloadString.find("Battery barcode:") > -1 :
                self.batteryBarCode = payloadString[payloadString.find(":")+1:].strip()

            if payloadString.find("Board") > -1 :
                if payloadString.find("wm320v2") > -1 :
                    self.P3 = True

                elif payloadString.find("wm610") > -1 :
                    self.inspire1 = True
                    Record255_1.inspire1 = True

                elif payloadString.find("wm321") > -1 :
                    self.standard = True

                elif payloadString.find("tp1406") > -1 :
                    pass

