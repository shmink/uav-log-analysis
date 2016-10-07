'''
Created on Sep 3, 2016

@author: Isaac Jessop
/* Record198_13 class

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

#     //length 36
#     // 1 hZ

from datfile.TSAGeoMag import TSAGeoMag
from datcom.Record import Record
import math

class Record198_13(Record):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

        self.current = self
        self.longitudeHP = 0.0 
        self.latitudeHP = 0.0 
        self.valid = False 
        self.devlination = 0.0 
        self.geoMag = TSAGeoMag()
    
        super(Record198_13, self).__init__(_type = 198, _subtype = 13)

    def process(self, _payload) :

        super(Record198_13, self).process(_payload)

        payloadBB = _payload.getBB()
        longRad = payloadBB.getDouble(0)
        latRad = payloadBB.getDouble(8)
        if self.valid is False :
            if longRad < 100.0 and latRad < 100.0 :
                self.valid = True
                longDeg = math.degrees(longRad)
                latDeg = math.degrees(latRad)
                self.declination = self.geoMag.getDeclination(latDeg, longDeg);

        if self.valid is True :
            self.longitudeHP = longRad
            self.latitudeHP = latRad
