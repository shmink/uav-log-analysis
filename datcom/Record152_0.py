'''
Created on Sep 3, 2016

@author: Isaac Jessop
/* Record152_0 class

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

class Record152_0(Record):
    '''
    classdocs
    '''


    def __init__(self,_convertDat):
        '''
        Constructor
        '''
        super(Record152_0, self).__init__(_type = 152, _subtype = 0)

        self.ConvertDat = _convertDat
        self.current = self 
        self.aileron = 0 
        self.elevator = 0
        self.throttle = 0
        self.rudder = 0;
        self.modeSwitch = 0 
        self.gpsHealth = 0 
        self.hits = []
        self.numHits = 0 
        self.clq  = float(0.0)
        self.clqHasValue = False 

    def process(self, _payload):

        super(Record152_0, self).process(_payload)
        self.aileron = self.payloadBB.getShort(4)
        self.elevator = self.payloadBB.getShort(6);
        self.throttle = self.payloadBB.getShort(8);
        self.rudder = self.payloadBB.getShort(10);
        self.modeSwitch = self.payloadBB.get(31);
        self.gpsHealth = self.payloadBB.get(41);

        if self.ConvertDat.EXPERIMENTAL is True:
            self.hits.append(long(_payload.tickNo))
            if self.numHits == 500:
                self.hits.remove(self.hits[499])
                count = 0
                for hit in self.hits:
                    ti = long(hit)
                    if ti < _payload.tickNo - 6000:
                        break;
                    count += 1

                self.clq = float( count / self.numHits)
                self.clqHasValue = True;
        else:
                self.numHits += 1

