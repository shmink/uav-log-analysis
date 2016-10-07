'''
Created on Aug 27, 2016

@author: Isaac Jessop

Payload class

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
'''
from datfile.FileEnd import FileEnd
from datcom.ByteBuffer import ByteBuffer
from bitstring import Bits
from bitstring import BitArray
class Payload(object):
    '''
    classdocs
    '''

    def __init__(self, df, _start, _length, _segtype, _subType, _tickNo):
        '''
        Constructor
        '''
        self.datFile = df
        self.start = _start
        self.length = _length
        self.tickNo = _tickNo
        self.recType = _segtype
        self.subType = _subType
        
        self.BB = ByteBuffer()
        
        bmod = self.tickNo % 256
        bs = bytes(bytearray([bmod]))
        xorKey =  Bits(bytes=bs).intle
        for i in range(0,self.length):
            if self.start + i >= self.datFile.getLength():
                raise FileEnd()
            self.datFile.setPosition(self.start + i);
            mb = self.datFile.getByte()
            self.BB.add(mb ^ xorKey)
            
            
    def getStart(self):
        return self.start
      
    def getBB(self):
        return self.BB
      
    def subtype(self):
        return self.subType

    
    def printBB(self,printStream = None):
        pass  
        outString = "Rec%s_%s FilePos = %s" % (self.recType, self.subType, self.start)
        if self.tickNo >= 0:
            outString =  "%s TickNo = %s" % (outString, self.tickNo)
        if isinstance(printStream, file):
            printStream.write(" ")
            printStream.write(outString)
        else:
            print " "
            print outString
        
        for i in range(0,self.length):
            outString = "%d:%02X:%C:%s" % (i,0xff & self.BB.get(i), 0xff & self.BB.get(i), 
                                           0xff & self.BB.get(i))
            if i < self.length - 1:
                outString = "%s:Shrt %s :UShrt %s" % (outString,self.BB.getShort(i),self.getUnsignedShort(i))           

            if i < self.length -3:
                outString = "%s :I %s :UI %s :F %s" %(outString, self.BB.getInt(i), self.getUnsignedInt(i), 
                                                       self.BB.getFloat(i) )

            if i < self.length - 7 :
                outString = "%s :L  %s :D %s" % (outString, self.BB.getLong(i), self.BB.getDouble(i))

            if isinstance(printStream, file):
                printStream.write(outString)
            else:
                print outString

    def getByte(self, index):
        return self.BB.get(index)

    def getUnsignedByte(self, index):
        return 0xff & self.BB.get(index)

    def getUnsignedInt(self, index):
        return self.BB.getUnsignedInt(index)

    def getUnsignedShort(self,index):
        return self.BB.getUnsignedShort(index)

    def getFloat(self, index):
        return self.BB.getFloat(index)

    def  getShort(self, index):
        return self.BB.getShort(index)

    def  getDouble(self, index):
        return self.BB.getDouble(index) 

    def  getTickNo(self):
        return self.tickNo  

    def getString(self):
        myBytes = [0x00] * self.length  
        l = 0
        B = 0x00
        for i in range(0,self.length):
            B = self.BB.get(i)
            if B == 0x00 or B == '\r' or B == '\n':
                l = i
                break

            myBytes[i] = B

        rtv = ''.join(chr(c) for c in myBytes[0:l])
        return rtv

    