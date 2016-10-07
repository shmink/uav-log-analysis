'''
Created on Aug 27, 2016

@author: isaac jessop zeek@zeeksgeeks.com
'''

class FileEnd(Exception):
    '''Raise when end of file reached'''
    def __init__(self):

        super(FileEnd, self).__init__("file end reached")

        
if __name__ == '__main__':
        
    try:
        raise FileEnd()
    except FileEnd as e:
        print e
        
