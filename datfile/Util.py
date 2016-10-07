'''
Created on Sep 3, 2016

@author: Isaac Jessop
/* Util class

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

import math

class Util(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass

    def distance(self,lat1,lon1,lat2,lon2):
        R = 6371 ## Radius of earth
        if lat1 == 0.0 or lon1 == 0 or lat2 == 0 or lon2 == 0: 
            return 0.0

        latDistance = lat2 - lat1
        lonDistance = lon2 - lon1
        a = math.sin(latDistance / 2) * math.sin(latDistance / 2)+\
                     + math.cos((lat1)) * math.cos((lat2))\
                     * math.sin(lonDistance / 2) * math.sin(lonDistance / 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));
        distance = R * c * 1000; ## convert to meters
        return distance;

    # // computes true(not magnetic) bearing
    def bearing(self,lat1,lon1,lat2,lon2):
        longDiff = lon2 - lon1
        y = math.sin(longDiff) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1)\
                * math.cos(lat2) * math.cos(longDiff)
        return (math.degrees(math.atan2(y, x)))
 
    def time(self, tickNo, offset):
        return float(tickNo - offset)/ float(600.0)
 
    def timeString(self, tickNo, offset):
        return '%.3f' % (self.time(tickNo, offset))

    def getTickFromTime(self, time,offset):  
        return long(600.00 * long(time)) + offset

