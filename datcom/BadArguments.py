'''
Created on Aug 27, 2016

@author: isaac jessop zeek@zeeksgeeks.com
'''

class BadArguments(Exception):
    '''Raise when Bad Arguments are supplied'''
    def __init__(self,error):

        super(BadArguments, self).__init__("Bad Arguments")
        self.error = error
    def getMsg(self):
        return "Bad Arguments " + self.error;
        
if __name__ == '__main__':
        
    try:
        raise BadArguments('need 2 args')
    except BadArguments as e:
        print e
        print e.error
        print e.getMsg()
        
