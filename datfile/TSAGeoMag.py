'''
Created on Sep 3, 2016

@author: Isaac Jessop

comments for java source
# /*                PUBLIC DOMAIN NOTICE
# This program was prepared by Los Alamos National Security, LLC 
# at Los Alamos National Laboratory (LANL) under contract No. 
# DE-AC52-06NA25396 with the U.S. Department of Energy (DOE). 
# All rights in the program are reserved by the DOE and 
# Los Alamos National Security, LLC.  Permission is granted to the 
# public to copy and use this software without charge, 
# provided that this Notice and any statement of authorship are 
# reproduced on all copies.  Neither the U.S. Government nor LANS 
# makes any warranty, express or implied, or assumes any liability 
# or responsibility for the use of this software.
# */
# 
# /*           License Statement from the NOAA
# The WMM source code is in the public domain and not licensed or 
# under copyright. The information and software may be used freely 
# by the public. As required by 17 U.S.C. 403, third parties producing 
# copyrighted works consisting predominantly of the material produced 
# by U.S. government agencies must provide notice with such work(s) 
# identifying the U.S. Government material incorporated and stating 
# that such material is not subject to copyright protection. 
# */
# 
# ////////////////////////////////////////////////////////////////////////////
# //
# //GeoMag.java - originally geomag.c
# //Ported to Java 1.0.2 by Tim Walker    
# //tim.walker@worldnet.att.net
# //tim@acusat.com
# //
# //Updated: 1/28/98
# //
# //Original source geomag.c available at 
# //http://www.ngdc.noaa.gov/seg/potfld/DoDWMM.html
# //
# //NOTE: original comments from the geomag.c source file are in ALL CAPS
# //Tim's added comments for the port to Java are not
# //
# ////////////////////////////////////////////////////////////////////////////
# 
# import java.util.Calendar;
# import java.util.GregorianCalendar;
# 
# /**<p>
#  * 
#  *  Last updated on May 26, 2015</p><p>
#  *  <b>NOTE: </b>Comment out the logger references, and put back in the System.out.println 
#  *     statements if not using log4j in your application. Checks are not made on the method inputs
#  *     to ensure they are within a valid range.</p><p>
#  *     
#  *      Verified by a JUnit test using the test values distributed with the 2015 update.</p><p>
#  *  
#  *      This is a class to generate the magnetic declination,
#  *      magnetic field strength and inclination for any point
#  *      on the earth.  The true bearing = magnetic bearing + declination.
#  *      This class is adapted from an Applet from the NOAA National Data Center
#  *      at <a href ="http://www.ngdc.noaa.gov/seg/segd.shtml"> http://www.ngdc.noaa.gov/seg/segd.shtml.</a>
#  *      None of the calculations
#  *      were changed.  This class requires an input file named WMM.COF, which
#  *      must be in the same directory that the application is run from. <br> 
#  *      <b>NOTE:</b> If the WMM.COF file is missing, the internal fit coefficients
#  *      for 2015 will be used.
#  *
#  *      Using the correct date, the declination is accurate to about 0.5 degrees.</p><p>
#  *
#  *  This is the LANL D-3 version of the GeoMagnetic calculator from
#  *      the NOAA National Data Center at http://www.ngdc.noaa.gov/seg/segd.shtml.</p><p>
#  *      
#  *      Adapted by John St. Ledger, Los Alamos National Laboratory
#  *      June 25, 1999</p><p>
#  *
#  *
#  *      Version 2 Comments:  The world magnetic model is updated every 5 years.
#  *      The data for 2000 uses the same algorithm to calculate the magnetic
#  *      field variables.  The only change is in the spherical harmonic coefficients
#  *      in the input file.  The input file has been renamed to WMM.COF.  Once again,
#  *      the date was fixed.  This time to January 1, 2001.  Also, a deprecated
#  *      constructor for StreamTokenizer was replaced, and the error messages in the catch
#  *      clause were changed.  Methods to get the field strength and inclination
#  *      were added.</p><p>
#  *
#  *      Found out some interesting information about the altitude. The altitude entered 
#  *      for the calculations is the height above the WGS84 spheroid, not height MSL. Using
#  *      MSL height means that the altitude could be in error by as much as 200 meters.
#  *      This should not be significant for our applications.</p>
#  *      
#  *      <p><b>NOTE:</b> This class is not thread safe.</p>
#  *
#  *
#  * @version 3.0 January 19, 2000
#  *      <p>Updated for 2000 data.</p>
#  *
#  * @version 4.0 March 1, 2002
#  *      <p>Changed so that if data file doesn't exist,
#  *      it uses an internal version of the coefficients from
#  *      the 2000 update.</p>
#  *
#  *
#  * @version 5.0 June 1, 2005
#  *      <p>Changed so that if data file doesn't exist,
#  *      it uses an internal version of the coefficients from
#  *      the 2005 update.  Previously, only calculated the declination at sea level
#  *      for one date.  Now can return all of the variables as a function of date and
#  *      altitude.  Original version used float variables.  All changed to type double.
#  *      Does not check if the input date is within the valid block.</p>
#  *
#  * @version 5.1 June 20, 2005
#  *      <p>Fixed a bug discovered by Alvin Liem.  In my zeal to clean up compiler comments
#  *      I deleted some double casts for integers that resulted in an integer division
#  *      being made when double division was needed.</p>
#  *
#  *  @version 5.2  June 1, 2006
#  *  <p>Took out the input error variable, which was no longer being used.
#  *  Now verified with a JUnit test.  Deleted the main() method which printed
#  *  a table of test values.</p>
#  *  
#  *  @version 5.3  January 28, 2009
#  *  <p>Fixed JavaDoc comments, and replaced the StringTokenizer uses with String.split().
#  *  
#  *  @version 5.4 January 5, 2010
#  *  <p>Updated for 2010 data. The new 2010 WMM.COF values are now used. Also, added 
#  *  <a href ="http://logging.apache.org/log4j/1.2/"> log4j</a> support.</p>
#  *  
#  *  @version 5.5 October 10, 2012
#  *  <p>Made minor changes. The default date used when the caller does not input a date is now the epoch + 2.5 years,
#  *     rather than being a fixed value. This means that the default date is automatically updated if a new WMM.COF file
#  *     is used. Also, now have a method to return the date as a decimal year, given the Gregorian Calendar date.</p>
#  *  
#  *  @version 5.6 January 15, 2015
#  *  <p>Updated the internal coefficients to the 2015 values. Passes the new JUnit tests.</p>
#  *     
#  *  @version 5.7 May 26, 2015
#  *  <p>Martin Frassl discovered a major bug in the code. I thought that X was in the East direction. It is not. The X axis
#  *     is in the North direction. This is now fixed so that getNorthIntensity and getEastIntensity return the correct values.
#  *     Thank you Martin!. The X, Y, and Z axes are defined in table 1 of the reference:</p>
#  *     <ul>Reference:
#  *     <li>Chulliat, A., S. Macmillan, P. Alken, C. Beggan, M. Nair, B. Hamilton, A. Woods, V. Ridley, S. Maus and A. Thomson, 
#  *     2015, The US/UK World Magnetic Model for 2015-2020: Technical Report, National Geophysical Data Center, NOAA. 
#  *     doi: 10.7289/V5TB14V7</li></ul>
#  *     
#  *     <ul>References:
#  *
#  *       <li>JOHN M. QUINN, DAVID J. KERRIDGE AND DAVID R. BARRACLOUGH,
#  *            WORLD MAGNETIC CHARTS FOR 1985 - SPHERICAL HARMONIC
#  *            MODELS OF THE GEOMAGNETIC FIELD AND ITS SECULAR
#  *            VARIATION, GEOPHYS. J. R. ASTR. SOC. (1986) 87,
#  *            PP 1143-1157</li>
#  *
#  *       <li>DEFENSE MAPPING AGENCY TECHNICAL REPORT, TR 8350.2:
#  *            DEPARTMENT OF DEFENSE WORLD GEODETIC SYSTEM 1984,
#  *            SEPT. 30 (1987)</li>
#  *
#  *       <li>JOSEPH C. CAIN, ET AL.; A PROPOSED MODEL FOR THE
#  *            INTERNATIONAL GEOMAGNETIC REFERENCE FIELD - 1965,
#  *            J. GEOMAG. AND GEOELECT. VOL. 19, NO. 4, PP 335-355
#  *            (1967) (SEE APPENDIX)</li>
#  *
#  *       <li>ALFRED J. ZMUDA, WORLD MAGNETIC SURVEY 1957-1969,
#  *            INTERNATIONAL ASSOCIATION OF GEOMAGNETISM AND
#  *            AERONOMY (IAGA) BULLETIN #28, PP 186-188 (1971)</li>
#  *
#  *       <li>JOHN M. QUINN, RACHEL J. COLEMAN, MICHAEL R. PECK, AND
#  *            STEPHEN E. LAUBER; THE JOINT US/UK 1990 EPOCH
#  *            WORLD MAGNETIC MODEL, TECHNICAL REPORT NO. 304,
#  *            NAVAL OCEANOGRAPHIC OFFICE (1991)</li>
#  *
#  *       <li>JOHN M. QUINN, RACHEL J. COLEMAN, DONALD L. SHIEL, AND
#  *            JOHN M. NIGRO; THE JOINT US/UK 1995 EPOCH WORLD
#  *            MAGNETIC MODEL, TECHNICAL REPORT NO. 314, NAVAL
#  *            OCEANOGRAPHIC OFFICE (1995)</li></ul>
#  *
#  *
#  *
#  *
#  *     <p>WMM-2000 is a National Imagery and Mapping Agency (NIMA) standard 
#  *     product. It is covered under NIMA Military Specification: 
#  *     MIL-W-89500 (1993).
#  *
#  *     For information on the use and applicability of this product contact</p>
#  *
#  *                     DIRECTOR<br>
#  *                     NATIONAL IMAGERY AND MAPPING AGENCY/HEADQUARTERS<br>
#  *                     ATTN: CODE P33<br>
#  *                     12310 SUNRISE VALLEY DRIVE<br>
#  *                     RESTON, VA 20191-3449<br>
#  *                     (703) 264-3002<br>
#  *
#  *
#  *     <p>The FORTRAN version of GEOMAG PROGRAMMED BY:</p>
#  *
#  *                     JOHN M. QUINN  7/19/90<br>
#  *                     FLEET PRODUCTS DIVISION, CODE N342<br>
#  *                     NAVAL OCEANOGRAPHIC OFFICE (NAVOCEANO)<br>
#  *                     STENNIS SPACE CENTER (SSC), MS 39522-5001<br>
#  *                     USA<br>
#  *                     PHONE:   COM:  (601) 688-5828<br>
#  *                               AV:        485-5828<br>
#  *                              FAX:  (601) 688-5521<br>
#  *
#  *     <p>NOW AT:</p>
#  *
#  *                     GEOMAGNETICS GROUP<br>
#  *                     U. S. GEOLOGICAL SURVEY   MS 966<br>
#  *                     FEDERAL CENTER<br>
#  *                     DENVER, CO   80225-0046<br>
#  *                     USA<br>
#  *                     PHONE:   COM: (303) 273-8475<br>
#  *                              FAX: (303) 273-8600<br>
#  *                     EMAIL:   quinn@ghtmail.cr.usgs.gov<br>
#  */
'''
        
import math

class TSAGeoMag(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        # variables for magnetic calculations 
        # Variables were identified in geomag.for, the FORTRAN
        # version of the geomag calculator.
        # 
        # /** The input string array which contains each line of input for the
        #  *  wmm.cof input file.  Added so that all data was internal, so that 
        #  *  applications do not have to mess with carrying around a data file.
        #  *   In the TSAGeoMag Class, the columns in this file are as follows:
        #  *   n, m,      gnm,      hnm,       dgnm,      dhnm
        #  */
        self.input = [
              "    2015.0            WMM-2015        12/15/2014",
              "  1  0  -29438.5       0.0       10.7        0.0",
              "  1  1   -1501.1    4796.2       17.9      -26.8",
              "  2  0   -2445.3       0.0       -8.6        0.0",
              "  2  1    3012.5   -2845.6       -3.3      -27.1",
              "  2  2    1676.6    -642.0        2.4      -13.3",
              "  3  0    1351.1       0.0        3.1        0.0",
              "  3  1   -2352.3    -115.3       -6.2        8.4",
              "  3  2    1225.6     245.0       -0.4       -0.4",
              "  3  3     581.9    -538.3      -10.4        2.3",
              "  4  0     907.2       0.0       -0.4        0.0",
              "  4  1     813.7     283.4        0.8       -0.6",
              "  4  2     120.3    -188.6       -9.2        5.3",
              "  4  3    -335.0     180.9        4.0        3.0",
              "  4  4      70.3    -329.5       -4.2       -5.3",
              "  5  0    -232.6       0.0       -0.2        0.0",
              "  5  1     360.1      47.4        0.1        0.4",
              "  5  2     192.4     196.9       -1.4        1.6",
              "  5  3    -141.0    -119.4        0.0       -1.1",
              "  5  4    -157.4      16.1        1.3        3.3",
              "  5  5       4.3     100.1        3.8        0.1",
              "  6  0      69.5       0.0       -0.5        0.0",
              "  6  1      67.4     -20.7       -0.2        0.0",
              "  6  2      72.8      33.2       -0.6       -2.2",
              "  6  3    -129.8      58.8        2.4       -0.7",
              "  6  4     -29.0     -66.5       -1.1        0.1",
              "  6  5      13.2       7.3        0.3        1.0",
              "  6  6     -70.9      62.5        1.5        1.3",
              "  7  0      81.6       0.0        0.2        0.0",
              "  7  1     -76.1     -54.1       -0.2        0.7",
              "  7  2      -6.8     -19.4       -0.4        0.5",
              "  7  3      51.9       5.6        1.3       -0.2",
              "  7  4      15.0      24.4        0.2       -0.1",
              "  7  5       9.3       3.3       -0.4       -0.7",
              "  7  6      -2.8     -27.5       -0.9        0.1",
              "  7  7       6.7      -2.3        0.3        0.1",
              "  8  0      24.0       0.0        0.0        0.0",
              "  8  1       8.6      10.2        0.1       -0.3",
              "  8  2     -16.9     -18.1       -0.5        0.3",
              "  8  3      -3.2      13.2        0.5        0.3",
              "  8  4     -20.6     -14.6       -0.2        0.6",
              "  8  5      13.3      16.2        0.4       -0.1",
              "  8  6      11.7       5.7        0.2       -0.2",
              "  8  7     -16.0      -9.1       -0.4        0.3",
              "  8  8      -2.0       2.2        0.3        0.0",
              "  9  0       5.4       0.0        0.0        0.0",
              "  9  1       8.8     -21.6       -0.1       -0.2",
              "  9  2       3.1      10.8       -0.1       -0.1",
              "  9  3      -3.1      11.7        0.4       -0.2",
              "  9  4       0.6      -6.8       -0.5        0.1",
              "  9  5     -13.3      -6.9       -0.2        0.1",
              "  9  6      -0.1       7.8        0.1        0.0",
              "  9  7       8.7       1.0        0.0       -0.2",
              "  9  8      -9.1      -3.9       -0.2        0.4",
              "  9  9     -10.5       8.5       -0.1        0.3",
              " 10  0      -1.9       0.0        0.0        0.0",
              " 10  1      -6.5       3.3        0.0        0.1",
              " 10  2       0.2      -0.3       -0.1       -0.1",
              " 10  3       0.6       4.6        0.3        0.0",
              " 10  4      -0.6       4.4       -0.1        0.0",
              " 10  5       1.7      -7.9       -0.1       -0.2",
              " 10  6      -0.7      -0.6       -0.1        0.1",
              " 10  7       2.1      -4.1        0.0       -0.1",
              " 10  8       2.3      -2.8       -0.2       -0.2",
              " 10  9      -1.8      -1.1       -0.1        0.1",
              " 10 10      -3.6      -8.7       -0.2       -0.1",
              " 11  0       3.1       0.0        0.0        0.0",
              " 11  1      -1.5      -0.1        0.0        0.0",
              " 11  2      -2.3       2.1       -0.1        0.1",
              " 11  3       2.1      -0.7        0.1        0.0",
              " 11  4      -0.9      -1.1        0.0        0.1",
              " 11  5       0.6       0.7        0.0        0.0",
              " 11  6      -0.7      -0.2        0.0        0.0",
              " 11  7       0.2      -2.1        0.0        0.1",
              " 11  8       1.7      -1.5        0.0        0.0",
              " 11  9      -0.2      -2.5        0.0       -0.1",
              " 11 10       0.4      -2.0       -0.1        0.0",
              " 11 11       3.5      -2.3       -0.1       -0.1",
              " 12  0      -2.0       0.0        0.1        0.0",
              " 12  1      -0.3      -1.0        0.0        0.0",
              " 12  2       0.4       0.5        0.0        0.0",
              " 12  3       1.3       1.8        0.1       -0.1",
              " 12  4      -0.9      -2.2       -0.1        0.0",
              " 12  5       0.9       0.3        0.0        0.0",
              " 12  6       0.1       0.7        0.1        0.0",
              " 12  7       0.5      -0.1        0.0        0.0",
              " 12  8      -0.4       0.3        0.0        0.0",
              " 12  9      -0.4       0.2        0.0        0.0",
              " 12 10       0.2      -0.9        0.0        0.0",
              " 12 11      -0.9      -0.2        0.0        0.0",
              " 12 12       0.0       0.7        0.0        0.0",] 
        
        # /**
        #  *  Geodetic altitude in km. An input,
        #  *  but set to zero in this class.  Changed 
        #  *  back to an input in version 5.  If not specified,
        #  *  then is 0.
        #  */
        self.alt = 0.0

        # /**
        #  *  Geodetic latitude in deg.  An input.
        #  */
        self.glat = 0.0

        # /**
        #  *  Geodetic longitude in deg.  An input.
        #  */
        self.glon = 0.0

        # /**
        #  *  Time in decimal years.  An input.
        #  */
        self.time = 0.0

        # /**
        #  *  Geomagnetic declination in deg.
        #  *  East is positive, West is negative.
        #  *  (The negative of variation.)
        #  */
        self.dec = 0.0

        # /**
        #  *  Geomagnetic inclination in deg.
        #  *  Down is positive, up is negative.
        #  */
        self.dip = 0.0

        # /**
        #  *  Geomagnetic total intensity, in nano Teslas.
        #  */
        self.ti = 0.0

        # /**
        #  *  The maximum number of degrees of the spherical harmonic model.
        #  */
        self.maxdeg = 12

        # /**
        #  *  The maximum order of spherical harmonic model.
        #  */
        self.maxord = 0

        # /** Added in version 5.  In earlier versions the date for the calculation was held as a
        #  *  constant.  Now the default date is set to 2.5 years plus the epoch read from the
        #  *  input file.
        #  */
        self.defaultDate = 2018.5
        # /** Added in version 5.  In earlier versions the altitude for the calculation was held as a
        #  *  constant at 0.  In version 5, if no altitude is specified in the calculation, this
        #  *  altitude is used by default.
        #  */
        self.defaultAltitude = 0.0
        # /**
        #  *  The Gauss coefficients of main geomagnetic model (nt).
        #  */
        self.c = [[0.0 * x ] * 13  for x in range(13)]
        # /**
        #  *  The Gauss coefficients of secular geomagnetic model (nt/yr).
        #  */
        self.cd = [[0.0 * x ] * 13  for x in range(13)]
        # /**
        #  *  The time adjusted geomagnetic gauss coefficients (nt).
        #  */
        self.tc = [[0.0 * x ] * 13  for x in range(13)]
        # /**
        #  *  The theta derivative of p(n,m) (unnormalized).
        #  */
        self.dp = [[0.0 * x ] * 13  for x in range(13)]
        # /**
        #  *  The Schmidt normalization factors.
        #  */
        self.snorm = [float(0)] * 169
        # /**
        #  *  The sine of (m*spherical coord. longitude).
        #  */
        self.sp = [float(0)] * 13
        # /**
        #  *  The cosine of (m*spherical coord. longitude).
        #  */
        self.cp = [float(0)] * 13
        self.fn = [float(0)] * 13
        self.fm = [float(0)] * 13
        # /**
        #  *  The associated Legendre polynomials for m=1 (unnormalized).
        #  */
        self.pp = [float(0)] * 13
        self.k = [[0.0 * x ] * 13  for x in range(13)]
        # /**
        #  * The variables otime (old time), oalt (old altitude),
        #  * olat (old latitude), olon (old longitude), are used to
        #  * store the values used from the previous calculation to
        #  * save on calculation time if some inputs don't change.
        #  */
        self.otime = float(0)
        self.oalt = float(0)
        self.olat = float(0)
        self.olon = float(0)
# 
        # /** The date in years, for the start of the valid time of the fit coefficients */
        self.epoch = float(0);
        # /** bx is the north south field intensity
        #  *  by is the east west field intensity
        #  *  bz is the vertical field intensity positive downward
        #  *  bh is the horizontal field intensity
        #  */
        self.bx = float(0)
        self.by = float(0)
        self.bz = float(0)
        self.bh = float(0)
        self.re = float(0)
        self.a2 = float(0)
        self.b2 = float(0)
        self.c2 = float(0)
        self.a4 = float(0)
        self.b4 = float(0)
        self.c4 = float(0)
        
        # even though these only occur in one method, they must be
        # created here, or won't have correct values calculated
        # These values are only recalculated if the altitude changes.
        self.r = float(0)
        self.d = float(0)
        self.ca = float(0)
        self.sa = float(0)
        self.ct = float(0)
        self.st = float(0)

        # /**
        #  *  Instantiates object by calling initModel().
        #  */
        self.initModel()

    # /**
    #  *  Reads data from file and initializes magnetic model.  If
    #  *  the file is not present, or an IO exception occurs, then the internal
    #  *  values valid for 2015 will be used. Note that the last line of the
    #  *  WMM.COF file must be 9999... for this method to read in the input
    #  *  file properly.
    #  */
    def initModel(self):
        self.glat = 0
        self.glon = 0
        self.maxord = self.maxdeg
        self.sp[0] = 0.0;
        self.cp[0] = self.snorm[0] = self.pp[0] = 1.0
        self.dp[0][0] = 0.0
        # /**
        #  *      Semi-major axis of WGS-84 ellipsoid, in km.
        #  */
        a = 6378.137
        # /**
        #  *      Semi-minor axis of WGS-84 ellipsoid, in km.
        #  */
        b = 6356.7523142
        # /**
        #  *      Mean radius of IAU-66 ellipsoid, in km.
        #  */
        self.re = 6371.2
#         re = 6371.2;
        self.a2 = a * a
#         a2 = a * a;
        self.b2 = b * b
#         b2 = b * b;
        self.c2 = self.a2 - self.b2
#         c2 = a2 - b2;
        self.a4 = self.a2 * self.a2
#         a4 = a2 * a2;
        self.b4 = self.b2 * self.b2
#         b4 = b2 * b2;
        self.c4 = self.a4 - self.b4
#         c4 = a4 - b4;
# 
        self.setCoeff()
        # // CONVERT SCHMIDT NORMALIZED GAUSS COEFFICIENTS TO UNNORMALIZED
        self.snorm[0] = 1.0
        for n in range(1,self.maxord + 1):
            self.snorm[n] = self.snorm[n-1] *  float((2 * n - 1)) / float(n)
            j = 2
            m = 0
            D1 = 1
            D2 = (n - m + D1) / D1 

            while D2 > 0:
                self.k[m][n] = float(((n - 1.0) * (n - 1.0)) - (m * m)) / float((2.0 * n - 1) * (2.0 * n - 3.0))

                if m > 0 : 
                    flnmj = ((n - m + 1.0) * j) /  (n + m);
                    self.snorm[n + m * 13] = self.snorm[n + (m - 1) * 13] * math.sqrt(flnmj)
                    j = 1
                    self.c[n][m - 1] = self.snorm[n + m * 13] * self.c[n][m - 1];
                    self.cd[n][m - 1] = self.snorm[n + m * 13] * self.cd[n][m - 1];

                self.c[m][n] = self.snorm[n + m * 13] * self.c[m][n];
                self.cd[m][n] = self.snorm[n + m * 13] * self.cd[m][n];
                m += D1
                D2 -= 1 
            self.fn[n] = (n + 1);
            self.fm[n] = n;
        self.k[1][1] = 0.0;
        self.otime = self.oalt = self.olat = self.olon = -1000.0;

    # /**     <p><b>PURPOSE:</b>  THIS ROUTINE COMPUTES THE DECLINATION (DEC),
    #  *               INCLINATION (DIP), TOTAL INTENSITY (TI) AND
    #  *               GRID VARIATION (GV - POLAR REGIONS ONLY, REFERENCED
    #  *               TO GRID NORTH OF POLAR STEREOGRAPHIC PROJECTION) OF
    #  *               THE EARTH'S MAGNETIC FIELD IN GEODETIC COORDINATES
    #  *               FROM THE COEFFICIENTS OF THE CURRENT OFFICIAL
    #  *               DEPARTMENT OF DEFENSE (DOD) SPHERICAL HARMONIC WORLD
    #  *               MAGNETIC MODEL (WMM-2010).  THE WMM SERIES OF MODELS IS
    #  *               UPDATED EVERY 5 YEARS ON JANUARY 1'ST OF THOSE YEARS
    #  *               WHICH ARE DIVISIBLE BY 5 (I.E. 1980, 1985, 1990 ETC.)
    #  *               BY THE NAVAL OCEANOGRAPHIC OFFICE IN COOPERATION
    #  *               WITH THE BRITISH GEOLOGICAL SURVEY (BGS).  THE MODEL
    #  *               IS BASED ON GEOMAGNETIC SURVEY MEASUREMENTS FROM
    #  *               AIRCRAFT, SATELLITE AND GEOMAGNETIC OBSERVATORIES.</p><p>
    #  *
    #  *
    #  *
    #  *     <b>ACCURACY:</b>  IN OCEAN AREAS AT THE EARTH'S SURFACE OVER THE
    #  *                ENTIRE 5 YEAR LIFE OF A DEGREE AND ORDER 12
    #  *                SPHERICAL HARMONIC MODEL SUCH AS WMM-95, THE ESTIMATED
    #  *                RMS ERRORS FOR THE VARIOUS MAGENTIC COMPONENTS ARE:</p>
    #  *<ul>
    #  *                DEC  -   0.5 Degrees<br>
    #  *                DIP  -   0.5 Degrees<br>
    #  *                TI   - 280.0 nanoTeslas (nT)<br>
    #  *                GV   -   0.5 Degrees<br></ul>
    #  *
    #  *                <p>OTHER MAGNETIC COMPONENTS THAT CAN BE DERIVED FROM
    #  *                THESE FOUR BY SIMPLE TRIGONOMETRIC RELATIONS WILL
    #  *                HAVE THE FOLLOWING APPROXIMATE ERRORS OVER OCEAN AREAS:</p>
    #  *<ul>
    #  *                X    - 140 nT (North)<br>
    #  *                Y    - 140 nT (East)<br>
    #  *                Z    - 200 nT (Vertical)  Positive is down<br>
    #  *                H    - 200 nT (Horizontal)<br></ul>
    #  *
    #  *                <p>OVER LAND THE RMS ERRORS ARE EXPECTED TO BE SOMEWHAT
    #  *                HIGHER, ALTHOUGH THE RMS ERRORS FOR DEC, DIP AND GV
    #  *                ARE STILL ESTIMATED TO BE LESS THAN 0.5 DEGREE, FOR
    #  *                THE ENTIRE 5-YEAR LIFE OF THE MODEL AT THE EARTH's
    #  *                SURFACE.  THE OTHER COMPONENT ERRORS OVER LAND ARE
    #  *                MORE DIFFICULT TO ESTIMATE AND SO ARE NOT GIVEN.</p><p>
    #  *
    #  *                THE ACCURACY AT ANY GIVEN TIME OF ALL FOUR
    #  *                GEOMAGNETIC PARAMETERS DEPENDS ON THE GEOMAGNETIC
    #  *                LATITUDE.  THE ERRORS ARE LEAST AT THE EQUATOR AND
    #  *                GREATEST AT THE MAGNETIC POLES.</p><p>
    #  *
    #  *                IT IS VERY IMPORTANT TO NOTE THAT A DEGREE AND
    #  *                ORDER 12 MODEL, SUCH AS WMM-2010 DESCRIBES ONLY
    #  *                THE LONG WAVELENGTH SPATIAL MAGNETIC FLUCTUATIONS
    #  *                DUE TO EARTH'S CORE.  NOT INCLUDED IN THE WMM SERIES
    #  *                MODELS ARE INTERMEDIATE AND SHORT WAVELENGTH
    #  *                SPATIAL FLUCTUATIONS OF THE GEOMAGNETIC FIELD
    #  *                WHICH ORIGINATE IN THE EARTH'S MANTLE AND CRUST.
    #  *                CONSEQUENTLY, ISOLATED ANGULAR ERRORS AT VARIOUS
    #  *                POSITIONS ON THE SURFACE (PRIMARILY OVER LAND, IN
    #  *                CONTINENTAL MARGINS AND OVER OCEANIC SEAMOUNTS,
    #  *                RIDGES AND TRENCHES) OF SEVERAL DEGREES MAY BE
    #  *                EXPECTED. ALSO NOT INCLUDED IN THE MODEL ARE
    #  *                NONSECULAR TEMPORAL FLUCTUATIONS OF THE GEOMAGNETIC
    #  *                FIELD OF MAGNETOSPHERIC AND IONOSPHERIC ORIGIN.
    #  *                DURING MAGNETIC STORMS, TEMPORAL FLUCTUATIONS CAN
    #  *                CAUSE SUBSTANTIAL DEVIATIONS OF THE GEOMAGNETIC
    #  *                FIELD FROM MODEL VALUES.  IN ARCTIC AND ANTARCTIC
    #  *                REGIONS, AS WELL AS IN EQUATORIAL REGIONS, DEVIATIONS
    #  *                FROM MODEL VALUES ARE BOTH FREQUENT AND PERSISTENT.</p><p>
    #  *
    #  *                IF THE REQUIRED DECLINATION ACCURACY IS MORE
    #  *                STRINGENT THAN THE WMM SERIES OF MODELS PROVIDE, THEN
    #  *                THE USER IS ADVISED TO REQUEST SPECIAL (REGIONAL OR
    #  *                LOCAL) SURVEYS BE PERFORMED AND MODELS PREPARED BY
    #  *                THE USGS, WHICH OPERATES THE US GEOMAGNETIC
    #  *                OBSERVATORIES.  REQUESTS OF THIS NATURE SHOULD
    #  *                BE MADE THROUGH NIMA AT THE ADDRESS ABOVE.</p><p>
    #  *
    #  *
    #  *
    #  *     NOTE:  THIS VERSION OF GEOMAG USES THE WMM-2010 GEOMAGNETIC
    #  *            MODEL REFERENCED TO THE WGS-84 GRAVITY MODEL ELLIPSOID</p>
    #  *
    #  * @param   fLat                    The latitude in decimal degrees.
    #  * @param   fLon                    The longitude in decimal degrees.
    #  * @param   year                    The date as a decimal year.
    #  * @param   altitude                The altitude in kilometers.
    #  */
    def calcGeoMag(self, fLat, fLon, year, altitude): 
        self.glat = fLat;
        self.glon = fLon;
        self.alt = altitude;

        # /**
        #  *      The date in decimal years for calculating the magnetic field components.
        #  */
        self.time = year;

        dt = self.time - self.epoch
        pi = math.pi
        dtr = (pi / 180.0);
        rlon = self.glon * dtr;
        rlat = self.glat * dtr;
        srlon = math.sin(rlon);
        srlat = math.sin(rlat);
        crlon = math.cos(rlon);
        crlat = math.cos(rlat);
        srlat2 = srlat * srlat;
        crlat2 = crlat * crlat;
        self.sp[1] = srlon;
        self.cp[1] = crlon;

        # // CONVERT FROM GEODETIC COORDS. TO SPHERICAL COORDS.
        if self.alt != self.oalt or self.glat != self.olat :
            q = math.sqrt(self.a2 - self.c2 * srlat2);
            q1 = self.alt * q;
            q2 = ((q1 + self.a2) / (q1 + self.b2)) * ((q1 + self.a2) / (q1 + self.b2));
            self.ct = srlat / math.sqrt(q2 * crlat2 + srlat2);
            self.st = math.sqrt(1.0 - (self.ct * self.ct));
            r2 = ((self.alt * self.alt) + 2.0 * q1 + (self.a4 - self.c4 * srlat2) / (q * q));
            self.r = math.sqrt(r2);
            self.d = math.sqrt(self.a2 * crlat2 + self.b2 * srlat2);
            self.ca = (self.alt + self.d) / self.r;
            self.sa = self.c2 * crlat * srlat / (self.r * self.d);

        if self.glon != self.olon :
            for m in range(2,self.maxord + 1):
                self.sp[m] = self.sp[1] * self.cp[m - 1] + self.cp[1] * self.sp[m - 1];
                self.cp[m] = self.cp[1] * self.cp[m - 1] - self.sp[1] * self.sp[m - 1];

        aor = self.re /self.r
        ar = aor * aor
        br = 0
        bt = 0
        bp = 0
        bpp = 0;

        for n in range(1,self.maxord + 1):
            ar = ar * aor
            m = 0 
            D3 = 1
            D4 = (n + m + D3) / float(D3)
            while D4 > 0:
                # //COMPUTE UNNORMALIZED ASSOCIATED LEGENDRE POLYNOMIALS
                # //AND DERIVATIVES VIA RECURSION RELATIONS
                if self.alt != self.oalt or self.glat != self.olat :
                    if n == m :
                        self.snorm[n + m * 13] = self.st * self.snorm[n - 1 + (m - 1) * 13];
                        self.dp[m][n] = self.st * self.dp[m - 1][n - 1] + \
                            self.ct * self.snorm[n - 1 + (m - 1) * 13]

                    if n == 1 and m == 0 :
                        self.snorm[n + m * 13] = self.ct * self.snorm[n - 1 + m * 13];
                        self.dp[m][n] = self.ct * self.dp[m][n - 1] - self.st * self.snorm[n - 1 + m * 13];

                    if n > 1 and n != m :
                        if m > n - 2:
                            self.snorm[n - 2 + m * 13] = 0.0;

                        if m > n - 2:
                            self.dp[m][n - 2] = 0.0;

                        self.snorm[n + m * 13] = self.ct * self.snorm[n - 1 + m * 13]\
                             - self.k[m][n] * self.snorm[n - 2 + m * 13]

                        self.dp[m][n] = self.ct * self.dp[m][n - 1]\
                             - self.st * self.snorm[n - 1 + m * 13]\
                             - self.k[m][n] * self.dp[m][n - 2]

                # //TIME ADJUST THE GAUSS COEFFICIENTS

                if self.time != self.otime :
                    self.tc[m][n] = self.c[m][n] + dt * self.cd[m][n];

                    if m != 0: 
                        self.tc[n][m - 1] = self.c[n][m - 1] + dt * self.cd[n][m - 1];

                # //ACCUMULATE TERMS OF THE SPHERICAL HARMONIC EXPANSIONS
                temp1 = 0.0
                temp2 = 0.0;
                par = ar * self.snorm[n + m * 13];

                if m == 0:
                    temp1 = self.tc[m][n] * self.cp[m];
                    temp2 = self.tc[m][n] * self.sp[m];
                else:
                    temp1 = self.tc[m][n] * self.cp[m] + self.tc[n][m - 1] * self.sp[m];
                    temp2 = self.tc[m][n] * self.sp[m] - self.tc[n][m - 1] * self.cp[m];

                bt = bt - ar * temp1 * self.dp[m][n]
                bp += (self.fm[m] * temp2 * par)
                br += (self.fn[n] * temp1 * par)
                
                # //SPECIAL CASE:  NORTH/SOUTH GEOGRAPHIC POLES
                if self.st == 0.0 and m == 1 :
                    if n == 1:
                        self.pp[n] = self.pp[n - 1];

                    else:
                        self.pp[n] = self.ct * self.pp[n - 1] - self.k[m][n] * self.pp[n - 2];

                    parp = ar * self.pp[n];
                    bpp += (self.fm[m] * temp2 * parp);

                D4 -= 1
                m += D3

        if self.st == 0.0:
            bp = bpp;

        else:
            bp /= self.st

        # //ROTATE MAGNETIC VECTOR COMPONENTS FROM SPHERICAL TO
        # //GEODETIC COORDINATES
        # // bx must be the east-west field component
        # // by must be the north-south field component
        # // bz must be the vertical field component.
        self.bx = -bt * self.ca - br * self.sa;
        self.by = bp;
        self.bz = bt * self.sa - br * self.ca;

        # //COMPUTE DECLINATION (DEC), INCLINATION (DIP) AND
        # //TOTAL INTENSITY (TI)

        self.bh = math.sqrt((self.bx * self.bx) + (self.by * self.by))
        self.ti = math.sqrt((self.bh * self.bh) + (self.bz * self.bz));
        # //      Calculate the declination.
        self.dec = (math.atan2(self.by, self.bx) / dtr);
        self.dip = (math.atan2(self.bz, self.bh) / dtr);
        # //      This is the variation for grid navigation.
        # //      Not used at this time.  See St. Ledger for explanation.
        # //COMPUTE MAGNETIC GRID VARIATION IF THE CURRENT
        # //GEODETIC POSITION IS IN THE ARCTIC OR ANTARCTIC
        # //(I.E. GLAT > +55 DEGREES OR GLAT < -55 DEGREES)
        # // Grid North is referenced to the 0 Meridian of a polar
        # // stereographic projection.
        # 

        self.otime = self.time
        self.oalt = self.alt
        self.olat = self.glat
        self.olon = self.glon

    # /**
    #  *  Returns the declination from the Department of
    #  *  Defense geomagnetic model and data, in degrees.  The
    #  *  magnetic heading + declination = true heading. The date and
    #  *  altitude are the defaults, of half way through the valid 
    #  *  5 year period, and 0 elevation.
    #  *  (True heading + variation = magnetic heading.)
    #  *
    #  * @param   dlat    Latitude in decimal degrees.
    #  * @param   dlong   Longitude in decimal degrees.
    #  * 
    #  * @return  The declination in degrees.
    #  */
    
    def getDeclination(self, dlat, dlong, year = None, altitude = None) :
        if year is None:
            year = self.defaultDate
        if altitude is None:
            altitude = self.defaultAltitude
        self.calcGeoMag(dlat, dlong, year, altitude)
        return self.dec

    # /**
    #  *  Returns the magnetic field intensity from the
    #  *  Department of Defense geomagnetic model and data
    #  *  in nano Tesla. The date and
    #  *  altitude are the defaults, of half way through the valid 
    #  *  5 year period, and 0 elevation.
    #  *
    #  * @param   dlat    Latitude in decimal degrees.
    #  * @param   dlong   Longitude in decimal degrees.
    #  * 
    #  * @return  Magnetic field strength in nano Tesla.
    #  */
    def getIntensity(self, dlat, dlong, year = None, altitude = None):
        if year is None:
            year = self.defaultDate
        if altitude is None:
            altitude = self.defaultAltitude
        self.calcGeoMag(dlat, dlong, year, altitude)
        return self.ti

    # /**
    #  *  Returns the horizontal magnetic field intensity from the
    #  *  Department of Defense geomagnetic model and data
    #  *  in nano Tesla. The date and
    #  *  altitude are the defaults, of half way through the valid 
    #  *  5 year period, and 0 elevation.
    #  *
    #  * @param   dlat    Latitude in decimal degrees.
    #  * @param   dlong   Longitude in decimal degrees.
    #  * 
    #  * @return  The horizontal magnetic field strength in nano Tesla.
    #  */
    def getHorizontalIntensity(self, dlat, dlong, year = None, altitude = None):
        if year is None:
            year = self.defaultDate
        if altitude is None:
            altitude = self.defaultAltitude
        self.calcGeoMag(dlat, dlong, year, altitude)
        return self.bh

    # /**
    #  *  Returns the vertical magnetic field intensity from the
    #  *  Department of Defense geomagnetic model and data
    #  *  in nano Tesla. The date and
    #  *  altitude are the defaults, of half way through the valid 
    #  *  5 year period, and 0 elevation.
    #  *
    #  * @param   dlat    Latitude in decimal degrees.
    #  * @param   dlong   Longitude in decimal degrees.
    #  * 
    #  * @return  The vertical magnetic field strength in nano Tesla.
    #  */
    def getVerticalIntensity(self, dlat, dlong, year = None, altitude = None):
        if year is None:
            year = self.defaultDate
        if altitude is None:
            altitude = self.defaultAltitude
        self.calcGeoMag(dlat, dlong, year, altitude)
        return self.bz


    # /**
    #  *  Returns the northerly magnetic field intensity from the
    #  *  Department of Defense geomagnetic model and data
    #  *  in nano Tesla. The date and
    #  *  altitude are the defaults, of half way through the valid 
    #  *  5 year period, and 0 elevation.
    #  *
    #  * @param   dlat    Latitude in decimal degrees.
    #  * @param   dlong   Longitude in decimal degrees.
    #  * 
    #  * @return  The northerly component of the magnetic field strength in nano Tesla.
    #  */
    def getNorthIntensity(self, dlat, dlong, year = None, altitude = None):
        if year is None:
            year = self.defaultDate
        if altitude is None:
            altitude = self.defaultAltitude
        self.calcGeoMag(dlat, dlong, year, altitude)
        return self.bx

    # /**
    #  *  Returns the easterly magnetic field intensity from the
    #  *  Department of Defense geomagnetic model and data
    #  *  in nano Tesla. The date and
    #  *  altitude are the defaults, of half way through the valid 
    #  *  5 year period, and 0 elevation.
    #  *
    #  * @param   dlat            Latitude in decimal degrees.
    #  * @param   dlong   Longitude in decimal degrees.
    #  * 
    #  * @return  The easterly component of the magnetic field strength in nano Tesla.
    #  */
    def getEastIntensity(self, dlat, dlong, year = None, altitude = None):
        if year is None:
            year = self.defaultDate
        if altitude is None:
            altitude = self.defaultAltitude
        self.calcGeoMag(dlat, dlong, year, altitude)
        return self.by
    # /**
    #  *  Returns the magnetic field dip angle from the
    #  *  Department of Defense geomagnetic model and data,
    #  *  in degrees.  The date and
    #  *  altitude are the defaults, of half way through the valid 
    #  *  5 year period, and 0 elevation.
    #  *
    #  * @param   dlat    Latitude in decimal degrees.
    #  * @param   dlong   Longitude in decimal degrees.
    #  * 
    #  * @return  The magnetic field dip angle, in degrees.
    #  */
    def getDipAngle(self, dlat, dlong, year = None, altitude = None):
        if year is None:
            year = self.defaultDate
        if altitude is None:
            altitude = self.defaultAltitude
        self.calcGeoMag(dlat, dlong, year, altitude)
        return self.dip

    # /** This method sets the input data to the internal fit coefficents.
    #  *  If there is an exception reading the input file WMM.COF, these values 
    #  *  are used.
    #  *
    #  *  NOTE:  This method is not tested by the JUnit test, unless the WMM.COF file
    #  *         is missing.
    #  */
    def setCoeff(self) :
        import re
        self.c[0][0] = 0.0;
        self.cd[0][0] = 0.0;
        self.epoch = float(re.split("[\\s]+", self.input[0].strip())[0])
        self.defaultDate = self.epoch + 2.5

        tokens = []
        # loop to get data from internal values
        for i in range(1,len(self.input)):
            tokens = re.split("[\\s]+", self.input[i].strip())

            n = int(tokens[0])
            m = int(tokens[1])
            gnm = float(tokens[2])
            hnm = float(tokens[3])
            dgnm = float(tokens[4])
            dhnm = float(tokens[5])

            if m <= n :
                self.c[m][n] = gnm
                self.cd[m][n] = dgnm

                if m != 0 :
                    self.c[n][m - 1] = hnm
                    self.cd[n][m - 1] = dhnm

    ## given a datetime.date object return the decimal year
    def decimalYear(self, dateIn) :
        import calendar as cal

        daysInYear = 0;
        if cal.isleap(dateIn.year) :
            daysInYear = 366.0

        else:
            daysInYear = 365.0

        return dateIn.year + (dateIn.timetuple().tm_yday / daysInYear)

