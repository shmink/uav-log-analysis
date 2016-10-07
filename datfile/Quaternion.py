'''
Created on Sep 5, 2016

@author: Isaac Jessop

/* Quaternion class

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
#  this comment pulled from the original java code
# /******************************************************************************
#  * Compilation: javac Quaternion.java Execution: java Quaternion
#  * 
#  * Data type for quaternions.
#  * 
#  * http://mathworld.wolfram.com/Quaternion.html
#  * 
#  * The data type is "immutable" so once you create and initialize a Quaternion,
#  * you cannot change it.
#  * 
#  * % java Quaternion
#  * 
#  ******************************************************************************/
# 

import math
import decimal
from datfile.RollPitchYaw import RollPitchYaw

class Quaternion(object):
    '''
    classdocs
    '''


    def __init__(self, x1, x2,  x3 ,scalar = None):
        '''
        Constructor
        '''

        if scalar is not None:
            self.SCALAR = scalar
            self.X = x1
            self.Y = x2
            self.Z = x3

        else:
            x = x1 * decimal.Decimal(0.5)
            y = x2 * decimal.Decimal(0.5)
            z = x3 * decimal.Decimal(0.5)
 
            c1 = math.cos(z)
            c2 = math.cos(y)
            c3 = math.cos(x)

            s1 = math.sin(z)
            s2 = math.sin(y)
            s3 = math.sin(x)
     
            self.SCALAR = c1 * c2 * c3 - s1 * s2 * s3
            self.X = c1 * s2 * c3 - s1 * c2 * s3
            self.Y = s1 * s2 * c3 + c1 * c2 * s3
            self.Z = s1 * c2 * c3 + c1 * s2 * s3
 
    def fromAngles(self, pitch, roll, yaw):
        pitch = decimal.Decimal(pitch) * decimal.Decimal(0.5)
        roll = decimal.Decimal(roll) * decimal.Decimal(0.5)
        yaw = decimal.Decimal(yaw) * decimal.Decimal(0.5)

        c1 = math.cos(yaw)
        c2 = math.cos(roll)
        c3 = math.cos(pitch);
        s1 = math.sin(yaw)
        s2 = math.sin(roll)
        s3 = math.sin(pitch)
        
        return Quaternion( c1 * s2 * c3 - s1 * c2 * s3, s1 * s2 * c3 + c1 * c2 * s3,
                 s1 * c2 * c3 + c1 * s2 * s3,c1 * c2 * c3 - s1 * s2 * s3)

    def fromVector(self, x, y, z) :
        xy = math.atan2(y, x)
        xz = math.atan2(z, x)
        yz = math.atan2(y, z)
        retv =  Quaternion(yz, xz, xy)

        return retv

    def fromXYVector(self, x, y) :
        xy = math.atan2(y, x);
        retv = Quaternion(0.0, 0.0, xy)
        return retv

    def fromZYVector(self, z, y) :
        zy = math.atan2(z, y);
        retv = Quaternion(0.0, zy, 0.0)
        return retv

    def fromZXVector(self, z, x) :
        zx = math.atan2(z, x)
        retv = Quaternion(zx, 0.0, 0.0)
        return retv

    # return a string representation of the invoking object
    def toString(self) :
        return "%5f + %5fi + %5fj + %5fk" % (self.SCALAR, self.X, self.Y, self.Z)

    # return the quaternion norm
    def norm(self) :
        return math.sqrt(self.SCALAR * self.SCALAR + self.X * self.X + self.Y * self.Y + self.Z * self.Z)

    # return the quaternion conjugate
    def conjugate(self) :
        return  Quaternion( -1 * self.X, -1 * self.Y, -1 * self.Z,self.SCALAR)

    # return a new Quaternion whose value is (this + b)
    def plus(self, b) :
        a = self
        return Quaternion( a.X + b.X, a.Y + b.Y, a.Z + b.Z,a.SCALAR + b.SCALAR)

    # return a new Quaternion whose value is (this * b)
    def times(self, b) :
        a = self
        y0 = a.SCALAR * b.SCALAR - a.X * b.X - a.Y * b.Y - a.Z * b.Z
        y1 = a.SCALAR * b.X + a.X * b.SCALAR + a.Y * b.Z - a.Z * b.Y
        y2 = a.SCALAR * b.Y - a.X * b.Z + a.Y * b.SCALAR + a.Z * b.X
        y3 = a.SCALAR * b.Z + a.X * b.Y - a.Y * b.X + a.Z * b.SCALAR
        return Quaternion(y1, y2, y3,y0)

    # return a new Quaternion whose value is the inverse of this
    def inverse(self):
        d = self.SCALAR * self.SCALAR + self.X * self.X + self.Y * self.Y + self.Z * self.Z
        return Quaternion( -1 * self.X / d, -1 * self.Y / d, -1 * self.Z / d,self.SCALAR / d)

    # return a / b
    # we use the definition a * b^-1 (as opposed to b^-1 a)
    def  divides(self, b) :
        a = self
        return a.times(b.inverse())

    def toRollPitchYaw(self) :
        sqW = self.SCALAR * self.SCALAR
        sqX = self.X * self.X
        sqY = self.Y * self.Y
        sqZ = self.Z * self.Z
        yaw = 0.0
        pitch = 0.0
        roll = 0.0
        unit = sqX + sqY + sqZ + sqW; ## if normalised is one, otherwise  is correction factor 
        test = self.SCALAR * self.X + self.Y * self.Z

        if test > 0.499 * unit : ## singularity at north pole
            yaw = 2 * math.atan2(self.Y, self.SCALAR);
            pitch = math.pi / 2;
            roll = 0

        elif test < -0.499 * unit : ## // singularity at south pole
            yaw = -2 * math.atan2(self.Y, self.SCALAR);
            pitch = -1 * math.pi / 2;
            roll = 0
        else :
            yaw = math.atan2(2.0 * (self.SCALAR * self.Z - self.X * self.Y), 1.0 - 2.0 * (sqZ + sqX));
            try:
                roll = math.asin(2.0 * test / unit);

            except ZeroDivisionError:
                roll = 0.0

            pitch = math.atan2(2.0 * (self.SCALAR * self.Y - self.X * self.Z), 1.0 - 2.0 * (sqY + sqX));

        return RollPitchYaw(roll, pitch, yaw)

    def toEuler(self) :
        sqW = self.SCALAR * self.SCALAR
        sqX = self.X * self.X
        sqY = self.Y * self.Y
        sqZ = self.Z * self.Z
        yaw = 0.0
        roll = 0.0
        pitch = 0.0
        retv = [0.0] * 3
        unit = sqX + sqY + sqZ + sqW #// if normalised is one, otherwise is correction factor
        test = self.SCALAR * self.X + self.Y * self.Z

        if test > 0.499 * unit : #// singularity at north pole
            yaw = 2 * math.atan2(self.Y, self.SCALAR)
            pitch = math.pi / 2;
            roll = 0

        elif test < -0.499 * unit : #// singularity at south pole
            yaw = -2 * math.atan2(self.Y, self.SCALAR)
            pitch = -1 * math.pi / 2
            roll = 0

        else :
            yaw = math.atan2(2.0 * (self.SCALAR * self.Z - self.X * self.Y), 1.0 - 2.0 * (sqZ + sqX))
            try:
                roll = math.asin(2.0 * test / unit)

            except ZeroDivisionError:
                roll = 0.0

            pitch = math.atan2(2.0 * (self.SCALAR * self.Y - self.X * self.Z), 1.0 - 2.0 * (sqY + sqX))

        retv[0] = pitch
        retv[1] = roll
        retv[2] = yaw;
        return retv

    def getScalar(self) :
        return self.SCALAR

    def getX(self) :
        return self.X

    def getY(self) :
        return self.Y

        