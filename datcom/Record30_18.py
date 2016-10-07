'''
Created on Sep 4, 2016

@author: Isaac Jessop

/* Record30_18 class

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

# package src.DatConRecs;
# 
# public class Record30_18 extends Record {
#     // 1 Hz
#     // length 79

from datcom.Record import Record

class Record30_18(Record):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.current = self
        self.batteryUsefulTime = 0
        self.validBUT = False 
        self.validVP = False 
        self.voltagePercent = 0 

        super(Record30_18, self).__init__( _type = 30, _subtype = 18)

    def process(self,_payload):

        super(Record30_18, self).process(_payload)

        self.batteryUsefulTime = _payload.BB.getShort(0)
        if self.validBUT is False:
            if self.batteryUsefulTime > 0 :
                self.validBUT = True

        self.voltagePercent = _payload.BB.get(72)

        if self.validVP is False:
            if self.voltagePercent > 0 :
                self.validVP = True
    