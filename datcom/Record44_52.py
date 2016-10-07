'''
Created on Sep 5, 2016

@author: Isaac Jessop
/* Record44_52 class

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

# // 50 HZ
# // length 237

from datcom.Record import Record

class Record44_52(Record):
    '''
    classdocs
    '''


    def __init__(self ):
        '''
        Constructor
        '''
        
        self.quatW = 0.0 
        self.quatX = 0.0  
        self.quatY = 0.0  
        self.quatZ = 0.0  
        self.yaw = 0.0  
        self.roll = 0.0  
        self.pitch = 0.0  
        self.rFront = 0  
        self.lFront = 0  
        self.lBack = 0  
        self.rBack = 0  

        super(Record44_52, self).__init__( _type = 44, _subtype = 52)

        self.current = self

    def process(self, _payload):

        super(Record44_52, self).process(_payload)

        self.quatW = _payload.BB.getFloat(78)
        self.quatX = _payload.BB.getFloat(82)
        self.quatY = _payload.BB.getFloat(86)
        self.quatZ = _payload.BB.getFloat(90)
        self.yaw = _payload.BB.getFloat(94)
        self.roll = _payload.BB.getFloat(98)
        self.pitch = _payload.BB.getFloat(102)
        self.rFront = _payload.BB.getShort(219)
        self.lFront = _payload.BB.getShort(221)
        self.lBack = _payload.BB.getShort(223)
        self.rBack = _payload.BB.getShort(225)

