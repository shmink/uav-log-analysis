'''
Created on Aug 27, 2016

@author: isaac jessop zeek@zeeksgeeks.com
'''

class NotDatFile(Exception):
    '''Raise when data file provided is not a valid data file'''
    def __init__(self,errors):

        # Call the base class constructor with the parameters it needs
        super(NotDatFile, self).__init__("data file provided is not a valid data file")

        self.errors = errors
        
if __name__ == '__main__':
        
    try:
        raise NotDatFile({'filename':'baddatafile.dat'})
    except NotDatFile as e:
        print e
        print e.errors
        
