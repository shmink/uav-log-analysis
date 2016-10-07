'''
Created on Aug 29, 2016

@author: isaac
'''

class Corrupted(Exception):
    '''
    classdocs
    '''


    def __init__(self, _tickNo = None, _filePos = None ):
        '''
        Constructor
        '''
        if _tickNo is None:
            self.tickNo = 0L
        else:
            self.tickNo = _tickNo
    
        if _filePos is None:
            self.filePos = 0L
    
        else:
            self.filePos = _filePos
    
    def toString(self):
        return "Partial or missing record at or near tickNo " + self.tickNo + ", file Position " + self.filePos;
    
    def  getFilePos(self):
        return self.filePos;
    