'''
Created on Aug 28, 2016

@author: isaac jessop
'''

class tickGroup(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.numElements = 0
        self.start = [0L] * 30
        self.subType = [0] * 30
        self.msgs = [0] * 30
        self.length = [0] * 30 
        self.payloadType = [0] * 30  
        self.tickNo = -1 

    def reset(self):
        self.numElements = 0
        self.tickNo = -1
        
    ## in the original java add was overloaded one version had _ticNo as the first
    ## parameter the other omitted it i have combined them here moving _tickNo to
    ## the end and defaulting it to none. No changes need to be made for any calls
    ## omitting _tickNo but the order of tickNo to call with tickNo will need to be changed
    ## I searched the existing code and found no uses of the DatFile.add() function
    def add(self, _start, _length, _ptType,  _subType,  _msgs,  _tickNo = None):
        if _tickNo is not None:
            self.tickNo = _tickNo
        self.start[self.numElements] = _start;
        self.length[self.numElements] = _length;
        self.payloadType[self.numElements] = _ptType;
        self.subType[self.numElements] = _subType;
        self.msgs[self.numElements] = _msgs;
        self.numElements += 1
        