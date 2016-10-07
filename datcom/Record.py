'''
Created on Sep 3, 2016

@author: Isaac Jessop
/* RecordType class

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
class Record(object):
    '''
    classdocs
    '''



    def __init__(self, _type = -1 ,_subtype = -1):
        '''
        Constructor
        '''
        self.payloadBB = None
        self._type = _type
        self._subType = _subtype

    class cvsTermType(object):
        FLOAT4 = 100
        DOUBLE = 200
        BYTE = 300
        SHORT = 400
        
        def __init__(self):
            pass

    def  process(self, _record):
        self.payloadBB = _record.getBB()

    def isType(self, _Type,  _subType):
        return self._type == _Type and self._subType == _subType
