'''
Created on Aug 27, 2016

@author: isaac jessop
datfile class

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

import math
import traceback
from datcom.Payload import Payload
from datfile.FileEnd import FileEnd
from tickGroup import tickGroup
from AnalyzeDatResults import AnalyzeDatResults
from bitstring import Bits
from datfile.NotDatFile import NotDatFile
from datfile.Corrupted import Corrupted
from datfile.ResultCode import ResultCode

class DatFile(object):
    '''
    classdocs
    Class for reading byte data
    '''
 

    def __init__(self, fileName):
        '''
        Constructor
        fileName full path to data file to be read
        '''

        self.headerLength = 10
        self.memory = None
        self.filePos = 0
        self.file = None 
        self.inputStream = None 
        self._channel = None 
        self.fileLength = 0 
        self.buildStr = ""
        self.nextFilPos = 128 
        self.nextTickGroup = 0 
        self._fileEnd = FileEnd()
        self.numCorrupted = 0 
        self.results = None 
        self.startOfRecord = 0 
        self.lowestTickNo = -1L 
        self.highestTickNo = -1L
        self.motorStartTick = 0L
        self.motorStopTick = -1L 
        self.flightStartTick = -1L 
        self.gpsLockTick = -1L 
        self.tickGroups = [tickGroup(),tickGroup()]
        self.tgIndex = 1
        self.lastRecordTickNo = 0L
        self.alternateStructure = False 
        self.datfile(fileName)
        #     protected boolean alternateStructure = false;
    def datfile(self, _file):
        """ _file should be the full path to the data file """
        
        self.tickGroups[0] = tickGroup()
        self.tickGroups[1] = tickGroup()
        self.results = AnalyzeDatResults()
        self.file = open(_file,'rb')
        ## create a bits object with the content of the file
        dataAsBits = Bits(self.file)
        ## 8 bits per byte
        self.fileLength = (dataAsBits.length / 8)
        self.memory = dataAsBits.tobytes()
        try:
            if self.getByte(128) != 0x55:
                self.alternateStructure = True
        except FileEnd:
            self.close()
            raise NotDatFile()
        buildStr = self.getString(16)
        if buildStr.find("BUILD") < 0:
            self.close()
            raise NotDatFile()

    def reset(self):
        self.tickGroups[0].reset()
        self.tickGroups[1].reset()
        self.tgIndex = 1
        self.numCorrupted = 0
        self.results = AnalyzeDatResults()
        self.startOfRecord = 128
        self.setPosition(self.startOfRecord)

    def getTickGroup(self):
        thisTickGroup = None
        nextTickGroup = None
        if self.tgIndex == 1:
            self.tgIndex = 0
            thisTickGroup = self.tickGroups[0]
            nextTickGroup = self.tickGroups[1]
        else:
            self.tgIndex = 1
            thisTickGroup = self.tickGroups[1]
            nextTickGroup = self.tickGroups[0]
    
        thisGroupsTickNo = thisTickGroup.tickNo
        nextTickGroup.numElements = 0
        done = False
        length =0
        nextStartOfRecord = 0L
        while done is False:
            try:
                self.setPosition(self.startOfRecord)
                if self.getByte(self.startOfRecord) != 0X55:
                    raise Corrupted(thisGroupsTickNo, self.startOfRecord)
    
                length = (0xFF & self.getByte(self.startOfRecord + 1))
                # type in python is a reserved work so adding so type = mainType
                mainType = (0xFF & self.getByte(self.startOfRecord + 3))
                subType = (0xFF & self.getByte(self.startOfRecord + 4))
                msg = self.getByte(self.startOfRecord + 5)
                thisRecordTickNo = self.getUnsignedInt(self.startOfRecord + 6)
                if thisRecordTickNo < 0 or (self.alternateStructure is True \
                                            and thisRecordTickNo > 4500000)\
                                            or (self.alternateStructure is False\
                                            and thisRecordTickNo > 1500000):

                    raise Corrupted(self.lastRecordTickNo, self.startOfRecord + 1)
    
                self.lastRecordTickNo = thisRecordTickNo

                if length == 0:
                    raise Corrupted(thisGroupsTickNo, self.startOfRecord + 1)
    
                nextStartOfRecord = self.startOfRecord + length # the next 0x55 , we hope
                
                if nextStartOfRecord > self.fileLength:
                    raise self._fileEnd
    
                if self.getByte(nextStartOfRecord) != 0x55:
                    raise Corrupted(thisGroupsTickNo, nextStartOfRecord)
    
                if (0xff & msg) == 0x80:
                    mainType = 255 
                    subType = 1 

                if (0xff & msg) == 0xFF:
                    mainType = 255 
                    subType = 2 
    
                if thisGroupsTickNo == -1: # thisTickGroup doesn't yet have a tickNo
                    thisGroupsTickNo = thisRecordTickNo
                    thisTickGroup.tickNo = thisRecordTickNo
    
                if thisRecordTickNo > thisTickGroup.tickNo: # start next group 
                    nextTickGroup.reset()
                    nextTickGroup.add(self.startOfRecord + self.headerLength, 
                                      length - self.headerLength, mainType, subType, msg,thisRecordTickNo); 
                    done = True;
                    
                elif thisRecordTickNo == thisTickGroup.tickNo:
                    thisTickGroup.add(self.startOfRecord + self.headerLength, 
                                      length - self.headerLength, mainType, subType, msg)
                else:#tickNo < thisTickGroup.tickNo) in the last group
                    pass
                    ## for now, just ignore
                self.startOfRecord = nextStartOfRecord;

            except Corrupted as c:
                if self.getPos() > self.fileLength - 600: 
                    raise self._fileEnd

                self.numCorrupted += 1
                if self.numCorrupted > 25:
                    self.results.setResultCode(ResultCode.CORRUPTED);
                    raise Corrupted(thisGroupsTickNo, self.startOfRecord)
    
                try:
                    self.setPosition(c.filePos)
                    fiftyfive = self.readByte()
                    while fiftyfive != 0x55:
                        if self.getPos( ) > self.fileLength - 1000 :
                            raise self._fileEnd
    
                        fiftyfive = self.readByte()
    
                except Corrupted:
                    raise Corrupted(thisGroupsTickNo, self.startOfRecord)
    
                ##set position right before the next 0x55
                self.startOfRecord = self.getPos() -1
    
            except FileEnd:
                raise self._fileEnd
            except Corrupted:
                self.results.setResultCode(ResultCode.CORRUPTED)
                raise Corrupted(thisGroupsTickNo, self.startOfRecord)
    
        return thisTickGroup;

    def close(self): 
        self.file.close()
        self.memory = None

    def skipOver(self, num):
        newpos = self.filePos + num
        if newpos > self.fileLength:
            raise IOError
    
        self.filePos = newpos
    
    def toString(self):
        return self.file.name

    def bufferToString(self):
        rtstr = "%s:%0X : %s :Shrt %s :UShrt %s :I %s :UI %s :L %s :F %s :D %s " % (self.filePos, 
                    (0xff & self.getByte()), (0xff & self.getByte()), str(self.getShort()), 
                    str(self.getUnsignedShort()), str(self.getInt()), str(self.getUnsignedInt()),
                    str(self.getLong()), str(self.getFloat()),str(self.getDouble()))
        return rtstr

    def setPosition(self, pos):
        self.filePos = pos

        if self.filePos >= self.fileLength:
            raise FileEnd()

    def getPos(self):
        return self.filePos

    def getLength(self): 
        return self.fileLength

    def getByte(self, pos = None):
        if pos is None:
            pos = self.filePos
            self.filePos += 1
        if pos >= self.fileLength :
                raise FileEnd()
        ## get the string representation of the byte
        ## create a bits object encodes as hex and convert to little endian int    
        #rtv = Bits(hex=self.memory[pos].encode('hex')).intle
        rtv = int("0x%s" % self.memory[pos].encode('hex'),0)
        return rtv

    def getString(self, fp):
        length = 256
        rbytes = ""
        l = 0
        B = 0x00
        for i in range(length):
            try:
                B = self.getByte(fp + i)

            except FileEnd as e:
                print e
                traceback.print_stack()

            if B == 0x00 or B == "\r" or B == "\n":
                l = i
                break

            rbytes += chr(B)

        return rbytes[0:l]

    def readByte(self):
        rv = self.getByte()
        return rv;

    def  getShort(self):
        rtv = int("0x%s" % self.memory[self.filePos:self.filePos +1].encode('hex'),0)
        return rtv

    def getUnsignedShort(self, fp = None):
        if fp is None:
            fp = self.filePos
        
        if fp > self.fileLength - 2:
                raise FileEnd()
        ## get 2 bites create bites object encoded in hex
        ## return as unsigned int little endian
        #return Bits(hex=self.memory[fp:fp + 1].encode('hex')).uintle
        rtv = int("0x%s" % self.memory[fp:fp + 1].encode('hex'),0)
        return rtv

    def getInt(self):
        #return Bits(hex=self.memory[self.filePos:self.filePos +3].encode('hex')).intle
        rtv = int("0x%s" % self.memory[self.filePos:self.filePos +3].encode('hex'),0)
        return rtv

    def getUnsignedInt(self, fp = None):
        if fp is None:
            fp = self.filePos
        
        if fp > self.fileLength - 4:
                raise FileEnd()
        ## get 4 bites create bites object encoded in hex
        ## return as unsigned int little endian
        return Bits(hex=self.memory[fp:fp + 3].encode('hex')).uintle

    def getLong(self): 
        rtv = int("0x%s" % self.memory[self.filePos:self.filePos +7].encode('hex'),0)
        return rtv

    def getFloat(self):
        return float(Bits(hex=self.memory[self.filePos:self.filePos +3].encode('hex')).floatle)

    def getDouble(self):
        return float(Bits(hex=self.memory[self.filePos:self.filePos +7].encode('hex')).floatle)

    def getResults(self): 
        return self.results;

    def getFile(self):
        return self.file;

    def setStartOfRecord(self, sor):
        self.startOfRecord = sor;

    def fileName(self):
        return self.file.name

    def  findMarkers(self):
        self.findMotorStartEnd()
        self.findLowestTickNo()
        length = 0
        done = False
        nextStartOfRecord = 0
        localFilePos = long(self.fileLength - 200000)
        try:
            self.setPosition(localFilePos)
            fiftyfive = self.readByte()
            while fiftyfive != 0x55:
                if self.getPos() > self.fileLength - 1000:
                    raise self._fileEnd

                fiftyfive = self.readByte()

            ## bad form to use the same name for a local var that is already global
            ## change filePos to localFilePos
            localFilePos = self.getPos() -1
            while done is False:
                try:
                    self.setPosition(localFilePos)
                    length = (0xFF & self.getByte(localFilePos + 1));
                    if length == 0: 
                        raise Corrupted()

                    nextStartOfRecord = localFilePos + length
                    if nextStartOfRecord > self.fileLength:
                        raise self._fileEnd

                    if self.getByte(nextStartOfRecord) != 0x55:
                        raise Corrupted()

                    tickNo = long(self.getUnsignedInt(localFilePos + 6))
                    if self.lowestTickNo < 0:
                        self.lowestTickNo = tickNo

                    self.highestTickNo = tickNo
                    localFilePos = nextStartOfRecord

                except Corrupted:
                    self.setPosition(self.getPos() + 1)
                    fiftyfive = self.readByte()

                    while fiftyfive != 0x55:
                        if self.getPos() > self.fileLength - 1000:
                            raise self._fileEnd

                        fiftyfive = self.readByte()

                    localFilePos = self.getPos() - 1

        except Exception :
            pass

    def  findLowestTickNo(self):
        length = 0
        done = False
        nextStartOfRecord = 0
        localFilePos = 128;

        try:
            self.setPosition(localFilePos)
            fiftyfive = self.readByte()

            while fiftyfive != 0x55:
                if self.getPos() > self.fileLength - 1000 :
                    raise self._fileEnd
                fiftyfive = self.readByte()

            localFilePos = self.getFilePos() - 1

            while done is False:
                try:
                    self.setPosition(localFilePos)
                    length = (0xFF & self.getByte(localFilePos + 1))
                    if length == 0:
                        raise Corrupted()

                    nextStartOfRecord = localFilePos + length

                    if nextStartOfRecord > self.fileLength :
                        raise self._fileEnd

                    if self.getByte(nextStartOfRecord) != 0x55:
                        raise Corrupted()

                    tickNo = long(self.getUnsignedInt(localFilePos + 6))
                    self.lowestTickNo = tickNo
                    done = True

                except Corrupted:
                    self.setPosition(self.getPos() + 1)
                    fiftyfive = self.readByte()

                    while fiftyfive != 0x55:
                        if self.getPos() > self.fileLength - 1000 :
                            raise self._fileEnd

                        fiftyfive = self.readByte()

                    localFilePos = self.getPos() - 1

        except Exception:
            pass

    def findMotorStartEnd(self):
        try:
            self.reset()
            tickNo = 0L

            while True:
                if self.getPos() > self.fileLength - 8 :
                    raise self._fileEnd

                tG = self.getTickGroup()
                tickNo = tG.tickNo
                
                for tgIndex in range(tG.numElements):
                    payloadType =  tG.payloadType[tgIndex]
                    payloadStart = tG.start[tgIndex]
                    payloadLength = tG.length[tgIndex]
                    subType = tG.subType[tgIndex]

                    if payloadType == 255 and subType == 1:
                        xorBB =  Payload(self, payloadStart,payloadLength, payloadType, subType, tickNo)
                        payloadString = xorBB.getString()

                        if payloadString.find("M.Start") > 0 and self.motorStartTick == 0:
                            self.motorStartTick = tickNo

                        if payloadString.find("M. Stop") > 0:
                            self.motorStopTick = tickNo

                    elif self.gpsLockTick == -1  and payloadType == 42 and subType == 12:
                        payload = Payload(self, payloadStart,payloadLength, payloadType, subType, tickNo)
                        longitude = math.degrees(payload.getDouble(0))
                        latitude = math.degrees(payload.getDouble(8))

                        if longitude != 0.0 and latitude != 0.0\
                             and math.fabs(longitude) > 0.0175 and math.fabs(latitude) > 0.0175:
                            self.gpsLockTick = tickNo

                    elif self.flightStartTick == -1L and payloadType == 42 and subType == 12:
                        payload = Payload(self, payloadStart,payloadLength, payloadType, subType, tickNo)

                        if payload.getShort(42) > 0:
                            self.flightStartTick = tickNo - long(float(payload.getShort(42) * 100))
                            
        except FileEnd:
            pass

        except Corrupted: 
            pass

        except IOError:
            pass


if __name__ == "__main__":
    """ this code is intended for testing this module"""
    import time
    import cProfile
    st = time.time()
    # number of files from the list to test
    numtotest = 1
    # the list pf expected files
    testfiles = ['FLY000.DAT','FLY002.DAT','FLY013.DAT','FLY016.DAT']
    testfiles = ['FLY013.DAT','FLY016.DAT']
    # the full path to the data file directory
    datafile_dir = "C:/Users/isaac/workspace/DavidKovar/datcompy/src/data/"
    print "------- testing %d files --------" % numtotest
    for fname in testfiles[0:numtotest]:
        myd = DatFile('%s%s' %(datafile_dir,fname))
        print "processing file",myd.fileName()
        print "file length = ", myd.fileLength
        cProfile.run('myd.findMarkers()')
        print "lowest tick mark =", myd.lowestTickNo
        print "motor start tick =",myd.motorStartTick
        print "flight start tick =", myd.flightStartTick
        myd.close()
        print "-------- end file --------"
        
    print " test complete "
    print "runtime = ", time.time() - st