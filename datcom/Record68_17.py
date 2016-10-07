'''
Created on Sep 5, 2016

@author: Isaac Jessop

/* Record68_17 class

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

import sys
from datcom.Record import Record
from datcom.Record255_1 import Record255_1


class Record68_17(Record):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
# // 50 HZ
# //length 47

        super(Record68_17, self).__init__( _type = 68, _subtype = 17)

        self.current = self

        self.crrnt = 0.0 
        self.volt1 = 0.0 
        self.volt2 = 0.0 
        self.volt3 = 0.0 
        self.volt4 = 0.0 
        self.volt5 = 0.0 
        self.volt6 = 0.0 
        self.temp = 0.0
        self.remainingCapacity = 0.0 
        self.ratedCapacity = 0.0
        self.totalVolts = 0.0
        self.maxVolts = 0.0 
        self.minVolts = 0.0 
        self.sumOfVolts = 0.0 
        self.avgVolts = 0.0 
        self.sumOfCurrents = 0L 
        self.numSamples = 0L
        self.voltDiff = 0.0 
        self.maxCurrent = 0.0 
        self.minCurrent = 0.0 
        self.avgCurrent = 0.0 
        self.watts = 0.0 
        self.maxWatts = 0.0  
        self.minWatts = 0.0 
        self.sumOfWatts = 0.0 
        self.avgWatts = 0.0 
        self.relativeCapacity = 0 

    def init(self) :

        self.maxVolts = -1.0;
        self.minVolts = sys.float_info.max
        self.minCurrent = sys.float_info.max
        self.avgCurrent = 0.0
        self.maxWatts = -1.0
        self.minWatts = sys.float_info.max

    def process(self, _payload) :

        super(Record68_17, self).process(_payload)

        if self.numSamples == 0 : #// first time
            self.init()

        self.numSamples += 1
        self.ratedCapacity = float(_payload.BB.getShort(2))
        self.remainingCapacity = float(_payload.BB.getShort(4))
        self.totalVolts = float(_payload.BB.getShort(6)) / 1000.0
        self.crrnt = -1 * float(_payload.getUnsignedShort(8) - 65536) / 1000.0
        self.relativeCapacity = _payload.BB.get(11);
        self.temp = float(_payload.BB.get(12))
        self.volt1 = float(_payload.BB.getShort(18)) / 1000.0
        self.volt2 = float(_payload.BB.getShort(20)) / 1000.0
        self.volt3 = float(_payload.BB.getShort(22)) / 1000.0
        self.volt4 = float(_payload.BB.getShort(24)) / 1000.0
        self.volt5 = float(_payload.BB.getShort(26)) / 1000.0
        self.volt6 = float(_payload.BB.getShort(28)) / 1000.0

        if Record255_1.inspire1 is True :
            voltMax = float(max( self.volt1, 
                            max( self.volt2, 
                                max(self.volt3, 
                                        max(self.volt4, 
                                                max(self.volt5, self.volt6))))))

            voltMin = float(min( self.volt1,
                            min(self.volt2,
                                min(self.volt3,
                                    min(self.volt4, 
                                        min(self.volt5, self.volt6))))))

            self.voltDiff = voltMax - voltMin

        else:
            voltMax = float(max(self.volt1,
                    max(self.volt2, max(self.volt3, self.volt4))))

            voltMin = float(min(self.volt1,
                    min(self.volt2, min(self.volt3, self.volt4))))

            self.voltDiff = voltMax - voltMin

        if self.totalVolts > self.maxVolts :
            self.maxVolts = self.totalVolts

        if self.totalVolts < self.minVolts :
            self.minVolts = self.totalVolts

        self.sumOfVolts += self.totalVolts
        self.avgVolts = self.sumOfVolts / float(self.numSamples)

        if self.crrnt > self.maxCurrent :
            self.maxCurrent = self.crrnt

        if self.crrnt < self.minCurrent :
            self.minCurrent = self.crrnt

        self.sumOfCurrents += self.crrnt
        self.avgCurrent = self.sumOfCurrents / float(self.numSamples)
        self.watts = self.totalVolts * self.crrnt

        if self.watts > self.maxWatts :
            self.maxWatts = self.watts

        if self.watts < self.minWatts :
            self.minWatts = self.watts

        self.sumOfWatts += self.watts
        self.avgWatts = self.sumOfWatts / float(self.numSamples)
