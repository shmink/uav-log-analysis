'''
Created on Sep 3, 2016

@author: Isaac Jessop

/* Record193_43 class

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

class Record193_43(Record):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        super(Record193_43, self).__init__(_type = 193, _subtype = 43)

        self.current = self
        self.longRad = 0.0  
        self.latRad = 0.0 
        self.longitudeTablet = 0.0 
        self.latitudeTablet = 0.0 
        self.valid = False 

    def process(self, _payload):
        super(Record193_43, self)._process(_payload)
        self.latRad = self.payloadBB.getDouble(155);
        self.longRad = self.payloadBB.getDouble(163);
        self.longitudeTablet = math.degrees(self.longRad);
        self.latitudeTablet = math.degrees(self.latRad);

        if self.valid is False:
            if self.longitudeTablet != 0.0 and self.latitudeTablet != 0.0:
                self.valid = True
        