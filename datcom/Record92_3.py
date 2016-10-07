'''
Created on Sep 5, 2016

@author: Isaac Jessop

/* Record92_3 class

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


# // offset 28 float height vps in meters  <=================
# // offset 32 Short validity of height 0 not valid, 190 and over valid
# // 34   40 non-GPS 36 compass error


from datcom.Record import Record

class Record92_3(Record):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

#     // 200 Hz
#     // width 44
        self.vpsHeight = 0.0 
        self.vpsQuality = 0.0 
        self.errorStatus = 0x0 

        super(Record92_3, self).__init__( _type = 92, _subtype = 3)

        self.current = self 

    def process(self, _payload) :

        super(Record92_3, self).process(_payload)

        payloadBB = _payload.getBB();
        self.vpsHeight = payloadBB.getFloat(28)
        self.vpsQuality = payloadBB.getShort(32)
        self.errorStatus = payloadBB.get(34)
