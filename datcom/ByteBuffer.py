'''
Created on Aug 28, 2016

@author: Isaac Jessop
requires bitstring  -- to install
open a command prompt navigate to /UourPythonInstalldir/Scripts
and run pip install bitstring

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
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
'''
from bitstring import BitArray

class ByteBuffer(object):
    '''
    classdocs
    '''


    def __init__(self, arrIn = None):
        '''
        Constructor
        '''
        if arrIn is None:
            self.dataList = []
        else:
            self.dataList = arrIn
        self.currentPos = 0
        self.mba = BitArray() 
        
    def add(self,byteIn):
        self.dataList.append(byteIn)
        
    def getbitArray(self,start, count):
        self.mba.clear()
        for index in range(start,start + count):
            db = self.dataList[index]
            if db < 0:
                ashex =  format(db & (2**8-1),'#04x')
                self.mba.append(ashex) 
            else:
                self.mba.append(format(db ,'#04x')) 
        return self.mba

    def get(self, index = None):
        if index is None:
            index = self.currentPos
            self.currentPos += 1
        return self.getbitArray(index,1).intle
        
    def  getShort(self, index = None):
        if index is None:
            index = self.currentPos
            self.currentPos += 2
        mba = self.getbitArray(index,2)
        return mba.intle

    def getUnsignedShort(self, index = None):
        if index is None:
            index = self.currentPos
            self.currentPos += 2
        
        mba = self.getbitArray(index,2)
        rtv = mba.uintle
        return rtv

    def getInt(self,index = None):
        if index is None:
            index = self.currentPos
            self.currentPos += 4
        mba = self.getbitArray(index,4)
        return mba.intle

    def getUnsignedInt(self, index = None):
        if index is None:
            index = self.currentPos
            self.currentPos += 4
        mba = self.getbitArray(index,4)
        return mba.uintle

    def getLong(self, index = None): 
        if index is None:
            index = self.currentPos
            self.currentPos += 8
        mba = self.getbitArray(index,8)
        return mba.intle

    def getFloat(self, index = None):
        if index is None:
            index = self.currentPos
            self.currentPos += 4
        mba = self.getbitArray(index,4)
        return mba.floatle

    def getDouble(self, index = None):
        if index is None:
            index = self.currentPos
            self.currentPos += 8
        mba = self.getbitArray(index,8)
        return mba.floatle