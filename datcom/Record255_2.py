'''
Created on Sep 4, 2016

@author: Isaac Jessop

/* Record255_2 class

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
import re


class Record255_2(Record):
    '''
    classdocs
    '''


    def __init__(self, convertDat):
        '''
        Constructor
        '''

        self.current = self
        self.payload = None
        self.convertDat = convertDat 
        self.batteryCycleCount = 0 
        self.batteryPercentage =0 
        self.numberPattern = re.compile("\\[\\s*(\\d+)\\s*\\]")

        super(Record255_2, self).__init__( _type = 255, _subtype = 2)
    
    def process(self, _payload):

        super(Record255_2, self).process(_payload)
        self.payload = _payload.getBB()
        payloadString = _payload.getString()

        if len(payloadString) > 0 :
            if self.convertDat.cloPS is not None :
                self.convertDat.cloPS.write("%s : %s") % (_payload.getTickNo(), payloadString)

            if payloadString.find("battery_info.life_percentage_0") > -1 :
                numberMatcher = re.match(self.numberPattern, payloadString)
                if numberMatcher is not None:
                    number = numberMatcher.groups()[0]
                    self.batteryPercentage = int(number)

            if payloadString.find("battery_info.cycle_count_0") > -1 :
                numberMatcher = re.match(self.numberPattern, payloadString)
                if numberMatcher is not None:
                    number = numberMatcher.groups()[0]
                    self.batteryCycleCount = int(number)
        