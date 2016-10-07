'''
Created on Aug 30, 2016

@author: Isaac Jessop

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

import sys
import math
from datfile.FileEnd import FileEnd
from datfile.Corrupted import Corrupted
from datfile.Quaternion import Quaternion
from datfile.Util import Util 
from datcom.Payload import Payload
from datcom.Record207 import Record207
from datcom.Record42_12 import Record42_12
from datcom.Record152_0 import Record152_0
from datcom.Record92_3 import Record92_3
from datcom.Record255_1 import Record255_1
from datcom.Record218_241 import Record218_241
from datcom.Record68_17 import Record68_17
from datcom.Record30_18 import Record30_18
from datcom.Record255_2 import Record255_2
from datcom.Record44_52 import Record44_52
from datcom.Record193_43 import Record193_43
from datcom.Record198_13 import Record198_13

class ConvertDat(object):
    '''
    classdocs
    '''
    EXPERIMENTAL = False
    def __init__(self, datFile):
        '''
        Constructor
        '''

        self.version = "2.3.1";
        self._findFile = FileEnd()
        self._datFile = datFile
        self.tickNo = 0L
        self.tickRangeLower = 0L 
        self.tickRangeUpper = sys.maxsize 
        self.sampleRate = float(600.0)
        self.timeOffset = 0L
        self.records = []
        self.rexcordDict = {}
        self.kmlType = -1; ## -1 = none, 0 = groundTrack, 1 = profile 
        self.kmlFile = None 
        self.kmlFileName = ""
        self.homePointElevation = float(0.0) 
        self.csvEventLogOutput = False 
        self.eloPS = None 
        self.cloPS = None 
        self.kmlPS = None 
        self.cvsPS = None 
        self.tloPS = None 
        self.printVersion = None
        self.lastLatRad = float(0.0)
        self.lastLongRad = float(0.0)
        self.lastTickNo = 0L
        self.notFirstLine = False
        
        self.util = Util()

    def analyze(self,printVersion):
        self.printVersion = printVersion
        sampleSize = int(600.0/self.sampleRate)
        try:
            self._datFile.setStartOfRecord(128)
            fileLength = long(self._datFile.getLength())
            # If there is a .csv being produced go ahead and output
            # the first row containing the column headings
            if self.csvPS is not None:
                self.csvPS.write("Tick#,offsetTime") 
                self.printCsvLine(self.csvPS,self.lineType.HEADER)

            lastTickNoPrinted = long (-1 * sampleSize)            

            # Main loop that gets a tick#Group and processes all the records in
            # that group
            while True:
                if self._datFile.getPos() > fileLength - 8 :    
                    raise self._fileEnd

                # Get the next tick#Group
                tG = self._datFile.getTickGroup()
                processedSomePayloads = False
                self.tickNo = tG.tickNo

                if self.tickNo < self.tickRangeUpper:
                    for tgIndex in range(tG.numElements):
                        payloadType = tG.payloadType[tgIndex]
                        payloadStart = long(tG.start[tgIndex])
                        payloadLength = tG.length[tgIndex]
                        subType = tG.subType[tgIndex]

                        for i in range(len(self.records)):
                            # For each record found in this tick#Group is it
                            # something
                            # that we want to process
                            if self.records[i].isType(payloadType, subType):
                                payload = Payload(self._datFile, payloadStart, payloadLength,
                                                  payloadType, subType, self.tickNo);

                                self.records[i].process(payload)
                                processedSomePayloads = True

                    if self.tickRangeLower < self.tickNo:
                        # some payloads in this tick#Group were processed
                        # then output the .csv line
                        if self.csvPS is not None and processedSomePayloads is True \
                            and self.tickNo >= lastTickNoPrinted + sampleSize:

                            self.csvPS.write("%s,%s" %( self.tickNo,self.util.timeString(self.tickNo,self.timeOffset)))
                            self.printCsvLine(self.csvPS, self.lineType.LINE);
                            lastTickNoPrinted = self.tickNo

        except FileEnd:
            pass

        except Corrupted:
            pass

        return self._datFile.getResults()

    class lineType():
        HEADER = 100
        LINE = 200

    def printCsvValue(self, header, value, lineT, valid):
        if lineT == self.lineType.HEADER :
            self.csvPS.write(",%s" % header)

        else: 
            self.csvPS.write(",");

            if valid is True :
                self.csvPS.write("%s" % value)

    def printCsvLine(self, _csv, lineT) :
        if lineT == self.lineType.HEADER :
            self.notFirstLine = False
        # Rec207
        R207 = self.rexcordDict.get('Record207')
        vel = float(math.sqrt(R207.current.velN \
                * R207.current.velN + R207.current.velE \
                * R207.current.velE + R207.current.velD \
                * R207.current.velD))

        velH = float(math.sqrt(R207.current.velN \
                * R207.current.velN + R207.current.velE \
                * R207.current.velE))

        magMod = int(math.sqrt(R207.current.magX \
                * R207.current.magX + R207.current.magY \
                * R207.current.magY + R207.current.magZ \
                * R207.current.magZ))

        error = float(math.sqrt(R207.current.diffX \
                * R207.current.diffX + R207.current.diffY \
                * R207.current.diffY + R207.current.diffZ \
                * R207.current.diffZ))

        accel = float(math.sqrt(R207.current.accelX \
                * R207.current.accelX + R207.current.accelY \
                * R207.current.accelY + R207.current.accelZ \
                * R207.current.accelZ))

        gyro = float(math.sqrt(R207.current.gyroX \
                * R207.current.gyroX + R207.current.gyroY \
                * R207.current.gyroY + R207.current.gyroZ \
                * R207.current.gyroZ))

        q = Quaternion(R207.current.quatX, R207.current.quatY,
                 R207.current.quatZ,R207.current.quatW)

        eulerAngs = q.toEuler()
        pitch = math.degrees(eulerAngs[0])
        roll = math.degrees(eulerAngs[1])
        yaw = math.degrees(eulerAngs[2])
        R42_12 = self.rexcordDict.get('Record42_12')

        self.printCsvValue("flightTime(msec)", R42_12.current.flightTime, lineT, True);

        longitude = math.degrees(R207.current.longRad);
        latitude = math.degrees(R207.current.latRad);
        coordsValid = False

        if longitude != 0.0 and latitude != 0.0 and abs(longitude) > 0.0175 \
                and abs(latitude) > 0.0175:

            coordsValid = True

        self.printCsvValue("Longitude", longitude, lineT, coordsValid)
        self.printCsvValue("Latitude", latitude, lineT, coordsValid)
        self.printCsvValue("numSats", R207.current.numSats, lineT, True)
        R152_0 = self.rexcordDict.get('Record152_0')
        self.printCsvValue("gpsHealth", R152_0.current.gpsHealth, lineT, True);
        self.printCsvValue("gpsAltitude(meters)", R207.current.gpsAlt, lineT, True)
        self.printCsvValue("baroAlt(meters)", R207.current.baroAlt, lineT, True)
        R92_3 = self.rexcordDict.get('Record92_3')
        self.printCsvValue("vpsHeight(M)", R92_3.current.vpsHeight, lineT,(R92_3.current.vpsQuality > 190))
        self.printCsvValue("relativeHeight", R42_12.current.height, lineT, True)
        self.printCsvValue("accelX(M/S2)", R207.current.accelX, lineT, True)
        self.printCsvValue("accelY(M/S2)", R207.current.accelY, lineT, True)
        self.printCsvValue("accelZ(M/S2)", R207.current.accelZ, lineT, True)
        self.printCsvValue("accel(M/S2)", accel, lineT, True)
        self.printCsvValue("gyroX(degrees/s)", R207.current.gyroX, lineT, True)
        self.printCsvValue("gyroY(degrees/s)", R207.current.gyroY, lineT, True)
        self.printCsvValue("gyroZ(degrees/s)", R207.current.gyroZ, lineT, True)
        self.printCsvValue("gyro(degrees/s)", gyro, lineT, True)

        self.printCsvValue("errorX", R207.current.diffX, lineT, True)
        self.printCsvValue("errorY", R207.current.diffY, lineT, True)
        self.printCsvValue("errorZ", R207.current.diffZ, lineT, True)
        self.printCsvValue("error", error, lineT, True)
        self.printCsvValue("magX", R207.current.magX, lineT, True)
        self.printCsvValue("magY", R207.current.magY, lineT, True)
        self.printCsvValue("magZ", R207.current.magZ, lineT, True)
        self.printCsvValue("magMod", magMod, lineT, True)
        self.printCsvValue("velN(M/S)", R207.current.velN, lineT, True)
        self.printCsvValue("velE(M/S)", R207.current.velE, lineT, True)
        self.printCsvValue("velD(M/S)", R207.current.velD, lineT, True)
        self.printCsvValue("vel(M/S)", vel, lineT, True)
        self.printCsvValue("velH(M/S)", velH, lineT, True)
        velGPS = float(0.0)

        if lineT == self.lineType.HEADER :
            self.printCsvValue("velGPS-velH(M/S)", 0.0, lineT, True)

        else:
            if self.notFirstLine is True :
                distance = self.util.distance(R207.current.latRad,
                                         R207.current.longRad, self.lastLatRad, self.lastLongRad)

                velGPS = distance / (float(self.tickNo - self.lastTickNo) / 600.0)

            else:
                velGPS = 0.0;

            self.lastLatRad = R207.current.latRad
            self.lastLongRad = R207.current.longRad
            self.printCsvValue("velGPS-velH(M/S)", velGPS - velH, lineT, True)

        self.printCsvValue("quatW", R207.current.quatW, lineT, True)
        self.printCsvValue("quatX", R207.current.quatX, lineT, True)
        self.printCsvValue("quatY", R207.current.quatY, lineT, True)
        self.printCsvValue("quatZ", R207.current.quatZ, lineT, True)
        self.printCsvValue("Roll", roll, lineT, True)
        self.printCsvValue("Pitch", pitch, lineT, True)
        self.printCsvValue("Yaw", yaw, lineT, True)
        self.printCsvValue("Yaw360", ((yaw + 360.0) % 360.0), lineT, True)
        self.printCsvValue("totalGyroZ", R207.current.totalZGyro, lineT, True)

        if lineT == self.lineType.HEADER :
            self.printCsvValue("magYaw", 0.0, lineT, True)

        else:
            qAcc = Quaternion(0,0,0).fromAngles(eulerAngs[0], eulerAngs[1], 0.0)
            magX = R207.current.magX
            magY = R207.current.magY
            magZ = R207.current.magZ
            x = Quaternion(magX, magY, magZ,0.0)
            magXYPlane = qAcc.times(x).times(qAcc.conjugate())
            X = magXYPlane.getX()
            Y = magXYPlane.getY()
            magYaw = math.degrees(-1 * math.atan2(Y, X))
            self.printCsvValue("magYawX", magYaw, lineT, True)

        R218_241 = self.rexcordDict.get('Record218_241') 
        lbrfDiff = R218_241.current.lBackSpeed - R218_241.current.rFrontSpeed
        rblfDiff = R218_241.current.rBackSpeed - R218_241.current.lFrontSpeed
        thrust1 = math.degrees(math.atan2(lbrfDiff, rblfDiff))
        thrust2 = (thrust1 + 315.0) % 360.0
        thrustTheta = thrust2

        if thrust2 > 180.0 :
            thrustTheta = thrust2 - 360.0

        self.printCsvValue("thrustAngle", thrustTheta, lineT, True)
        R255_1 = self.rexcordDict.get('Record255_1') 
        distanceHP = self.util.distance(R207.current.latRad,
                                    R207.current.longRad, R255_1.current.latitudeHP,
                                    R255_1.current.longitudeHP)

        self.printCsvValue("homePointLongitude",
                R255_1.current.longitudeHPDegrees, lineT,
                (R255_1.current.validHP))

        self.printCsvValue("homePointLatitude",
                R255_1.current.latitudeHPDegrees, lineT,
                (R255_1.current.validHP))

        self.printCsvValue("homePointAltitude", R255_1.current.heightHP, lineT,
                (R255_1.current.validHP))

        self.printCsvValue("geoMagDeclination", R255_1.current.declination,
                lineT, (R255_1.current.validHP))

        self.printCsvValue("geoMagInclination", R255_1.current.inclination,
                lineT, (R255_1.current.validHP))

        self.printCsvValue("distancHP(M)", distanceHP, lineT,
                (R255_1.current.validHP))

        self.printCsvValue("distanceTravelled(M)",
                R207.current.distanceTraveled, lineT, True)

        self.printCsvValue("directionOfTravel", R207.current.bearingDeclined,
                lineT, True)

        self.printCsvValue("directionOfTravelTrue", R207.current.bearingTrue,
                lineT, True)

        self.printCsvValue("IMUTemp(C)", R207.current.imuTemp, lineT, True)
        # Rec42_12
        R42_12.setStateStrings()
        self.printCsvValue("flyCState", R42_12.current.flyc_state, lineT, True)
        self.printCsvValue("flyCState:String", R42_12.current.FLCS, lineT, True)
        self.printCsvValue("nonGPSCause", R42_12.current.nonGPSError, lineT, True)
        self.printCsvValue("nonGPSCause:String", R42_12.current.NGPE, lineT, True)
        self.printCsvValue("DW flyCState", R42_12.current.dwflyState, lineT, True)
        connectedToRC = 0

        if R42_12.current.connectedToRC == 0 :
            connectedToRC = 1

        self.printCsvValue("conectedToRC", connectedToRC, lineT, True)

        if self.EXPERIMENTAL is True:
            self.printCsvValue("X:Roll", R42_12.current.roll, lineT, True)
            self.printCsvValue("X:Pitch", R42_12.current.pitch, lineT, True)
            self.printCsvValue("X:Yaw", R42_12.current.yaw, lineT, True)
            self.printCsvValue("motorStartFailure",
                               "%02X" % R42_12.current.failure, lineT, True);
        # Rec68_17 Battery Stuff
        R68_17 = self.rexcordDict.get('Record68_17') 
        self.printCsvValue("Current", R68_17.current.crrnt, lineT, True)
        self.printCsvValue("Volt1", R68_17.current.volt1, lineT, True)
        self.printCsvValue("Volt2", R68_17.current.volt2, lineT, True)
        self.printCsvValue("Volt3", R68_17.current.volt3, lineT, True)
        self.printCsvValue("Volt4", R68_17.current.volt4, lineT, True)
        self.printCsvValue("Volt5", R68_17.current.volt5, lineT,
                (R255_1.current.inspire1))

        self.printCsvValue("Volt6", R68_17.current.volt6, lineT,
                (R255_1.current.inspire1))

        self.printCsvValue("totalVolts", R68_17.current.totalVolts, lineT, True)
        self.printCsvValue("voltSpread", R68_17.current.voltDiff, lineT, True)
        self.printCsvValue("Watts", R68_17.current.watts, lineT, True)
        self.printCsvValue("batteryTemp(C)", R68_17.current.temp, lineT, True)
        self.printCsvValue("ratedCapacity", R68_17.current.ratedCapacity,
                lineT, True)

        self.printCsvValue("remaingCapacity", R68_17.current.remainingCapacity,
                lineT, True)

        self.printCsvValue("percentageCapacity",
                R68_17.current.relativeCapacity, lineT, True)

        R30_18 = self.rexcordDict.get('Record30_18') 
        self.printCsvValue("usefulTime", R30_18.current.batteryUsefulTime,
                lineT, (R30_18.current.validBUT));

        self.printCsvValue("percentageVolts", R30_18.current.voltagePercent,
                lineT, (R30_18.current.validVP));

        R255_2 = self.rexcordDict.get('Record255_2') 
        self.printCsvValue("batteryCycleCount",
                R255_2.current.batteryCycleCount, lineT, True)

        self.printCsvValue("batteryLifePercentage",
                R255_2.current.batteryPercentage, lineT, True)

        self.printCsvValue("batteryBarCode", R255_1.current.batteryBarCode,
                lineT, True)

        self.printCsvValue("minCurrent", R68_17.current.minCurrent, lineT, True)
        self.printCsvValue("maxCurrent", R68_17.current.maxCurrent, lineT, True)
        self.printCsvValue("avgCurrent", R68_17.current.avgCurrent, lineT, True)
        self.printCsvValue("minVolts", R68_17.current.minVolts, lineT, True)
        self.printCsvValue("maxVolts", R68_17.current.maxVolts, lineT, True)
        self.printCsvValue("avgVolts", R68_17.current.avgVolts, lineT, True)
        self.printCsvValue("minWatts", R68_17.current.minWatts, lineT, True)
        self.printCsvValue("maxWatts", R68_17.current.maxWatts, lineT, True)
        self.printCsvValue("avgWatts", R68_17.current.avgWatts, lineT, True)
        # Rec44_52
        R44_52 = self.rexcordDict.get('Record44_52') 
        self.printCsvValue("Gimbal:roll", math.degrees(R44_52.current.roll),
                lineT, True)

        self.printCsvValue("Gimbal:pitch",
                math.degrees(R44_52.current.pitch), lineT, True)

        self.printCsvValue("Gimbal:yaw", math.degrees(R44_52.current.yaw),
                lineT, True)

        qGimbal = Quaternion( R44_52.current.quatX, R44_52.current.quatY,
                R44_52.current.quatZ,R44_52.current.quatW)

        rpy = qGimbal.toRollPitchYaw()
        self.printCsvValue("Gimbal:Xroll", rpy.getRollDeg(), lineT, True)
        self.printCsvValue("Gimbal:Xpitch", rpy.getPitchDeg(), lineT, True)
        self.printCsvValue("Gimbal:Xyaw", rpy.getYawDeg(), lineT, True)
        self.printCsvValue("MotorCmnd:RFront", R44_52.current.rFront, lineT, True)
        self.printCsvValue("MotorCmnd:LFront", R44_52.current.lFront, lineT, True)
        self.printCsvValue("MotorCmnd:LBack", R44_52.current.lBack, lineT, True)
        self.printCsvValue("MotorCmnd:RBack", R44_52.current.rBack, lineT, True)
        # Rec218_241
        self.printCsvValue("MotorSpeed:RFront", R218_241.current.rFrontSpeed,
                lineT, R255_1.current.standard == False)

        self.printCsvValue("MotorSpeed:LFront", R218_241.current.lFrontSpeed,
                lineT, R255_1.current.standard == False)

        self.printCsvValue("MotorSpeed:LBack", R218_241.current.lBackSpeed,
                lineT, R255_1.current.standard == False)

        self.printCsvValue("MotorSpeed:RBack", R218_241.current.rBackSpeed,
                lineT, R255_1.current.standard == False)

        self.printCsvValue("MotorLoad:RFront", R218_241.current.rFrontLoad,
                lineT, R255_1.current.standard == False)

        self.printCsvValue("MotorLoad:LFront", R218_241.current.lFrontLoad,
                lineT, R255_1.current.standard == False)

        self.printCsvValue("MotorLoad:LBack", R218_241.current.lBackLoad,
                lineT, R255_1.current.standard == False)

        self.printCsvValue("MotorLoad:RBack", R218_241.current.rBackLoad,
                lineT, R255_1.current.standard == False)
        # Rec152_0
        self.printCsvValue("Control:Aileron", R152_0.current.aileron, lineT, True)
        self.printCsvValue("Control:Elevator", R152_0.current.elevator, lineT, True)
        self.printCsvValue("Control:Throttle", R152_0.current.throttle, lineT, True)
        self.printCsvValue("Control:Rudder", R152_0.current.rudder, lineT, True)
        self.printCsvValue("Control:ModeSwitch", R152_0.current.modeSwitch,
                lineT, True)

        if self.EXPERIMENTAL == True:
            self.printCsvValue("ContrlLinkQual", R152_0.current.clq, lineT,
                    (R152_0.current.clqHasValue));

        R193_43 = self.rexcordDict.get('Record193_43') 
        self.printCsvValue(
                "tabletLongitude",
                R193_43.current.longitudeTablet,
                lineT,
                (R193_43.current.valid and R42_12.current.flyc_state == 25));

        self.printCsvValue(
                "tabletLatitude",
                R193_43.current.latitudeTablet,
                lineT,
                (R193_43.current.valid and R42_12.current.flyc_state == 25));
        # Rec92_3
        if self.EXPERIMENTAL == True :
            self.printCsvValue("errorStatus", R92_3.current.errorStatus, lineT, True)

        model = ""

        if R255_1.current.P3 is True:
            model = "P3Adv/Pro"

        elif R255_1.current.inspire1 is True:
            model = "Inspire1"

        elif R255_1.current.standard is True:
            model = "P3Standard"

        self.printCsvValue("A/C model", model, lineT, True)

        if self.csvEventLogOutput :
            noComma = R255_1.text.replace(",", ".")
            self.printCsvValue("eventLog", noComma, lineT, True)
            R255_1.current.text = ""

        if self.printVersion is True:
            self.printCsvValue(self.version, "", lineT, False)

        _csv.write("\n");

        if lineT == self.lineType.LINE :
            self.notFirstLine = True
            self.lastTickNo = self.tickNo

    def setRecords(self,recs): 
        self.records = recs

    def setSampleRate(self, sampleRate):
        self.sampleRate = sampleRate

    def createRecords(self):
        self.records.append(Record207())
        self.records.append(Record42_12(self))
        self.records.append(Record68_17())
        self.records.append(Record44_52())
        self.records.append(Record218_241())
        self.records.append(Record152_0(self))
        self.records.append(Record30_18())
        self.records.append(Record198_13())
        self.records.append(Record193_43())
        self.records.append(Record92_3())
        self.records.append(Record255_1(self))
        self.records.append(Record255_2(self))

        # put all the records in a dictionary with the
        # record name as the key
        for i in range(len(self.records)):
            self.rexcordDict.update({str(type(self.records[i])).split('.')[1]:self.records[i]})
            
