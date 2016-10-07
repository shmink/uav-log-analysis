'''
Created on Aug 27, 2016

@author: isaac jessop zeek@zeeksgeeks.com
'''

class FileBeingUsed(Exception):
    '''Raise when data file provided is not a valid data file'''
    def __init__(self,filename):

        # Call the base class constructor with the parameters it needs
        super(FileBeingUsed, self).__init__("File in use")

        # Now for your custom code...
        self.filename = filename
    def getFileName(self):
        return self.filename
        
if __name__ == '__main__':
        
    try:
        raise FileBeingUsed('inusefile.dat')
    except FileBeingUsed as e:
        print e.message
        print e.getFileName()
        
