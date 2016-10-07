'''
Created on Sep 5, 2016

@author: Isaac Jessop

/* Record218_241 class

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

class Record218_241(Record):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

        self.valid = False
        self.rFrontLoad = 0 
        self.lFrontLoad = 0 
        self.lBackLoad = 0
        self.rBackLoad = 0
        self.rFrontSpeed = 0
        self.lFrontSpeed = 0
        self.lBackSpeed = 0 
        self.rBackSpeed = 0 

        super(Record218_241, self).__init__(_type = 218, _subtype = 241)

        self.current = self

    def process(self, _payload) :

        super(Record218_241, self).process(_payload)

        self.rFrontLoad = _payload.BB.getShort(1)
        self.rFrontSpeed = _payload.BB.getShort(3)
        self.lFrontLoad = _payload.BB.getShort(20)
        self.lFrontSpeed = _payload.BB.getShort(22);
        self.lBackLoad = _payload.BB.getShort(39);
        self.lBackSpeed = _payload.BB.getShort(41);
        self.rBackLoad = _payload.BB.getShort(58);
        self.rBackSpeed = _payload.BB.getShort(60);

