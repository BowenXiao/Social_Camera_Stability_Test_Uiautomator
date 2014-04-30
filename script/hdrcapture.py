#!/usr/bin/python
# coding:utf-8

from devicewrapper.android import device as d
import unittest
import commands
import re
import subprocess
import os
import string
import time
import sys
import util 
import string

AD = util.Adb()
TB = util.TouchButton()
SM = util.SetMode() 

#Written by XuGuanjun

PACKAGE_NAME  = 'com.intel.camera22'
ACTIVITY_NAME = PACKAGE_NAME + '/.Camera'

#All setting info of camera could be cat in the folder
PATH_XML       = '/data/data/com.intel.camera22/shared_prefs/'

#FDFR / GEO / BACK&FROUNT xml file in com.intelcamera22_preferences_0.xml
PATH_0XML      = PATH_XML + 'com.intel.camera22_preferences_0.xml'

#PICSIZE / EXPROSURE / TIMER / WHITEBALANCE / ISO / HITS / VIDEOSIZE in com.intel.camera22_preferences_0_0.xml
PATH_0_0XML    = PATH_XML + 'com.intel.camera22_preferences_0_0.xml'

#####                                    #####
#### Below is the specific settings' info ####
###                                        ###
##                                          ##
#                                            #

#FD/FR states check point
FDFR_STATE      = PATH_0XML   + ' | grep pref_fdfr_key'

#Geo state check point
GEO_STATE       = PATH_0XML   + ' | grep pref_camera_geo_location_key'

#Pic size state check point
PICSIZE_STATE   = PATH_0_0XML + ' | grep pref_camera_picture_size_key'

#Exposure state check point 
EXPOSURE_STATE  = PATH_0_0XML + ' | grep pref_camera_exposure_key'

#Timer state check point
TIMER_STATE     = PATH_0_0XML + ' | grep pref_camera_delay_shooting_key'

#Video Size state check point
VIDEOSIZE_STATE = PATH_0_0XML + ' | grep pref_video_quality_key'

#White balance state check point
WBALANCE_STATE  = PATH_0_0XML + ' | grep pref_camera_whitebalance_key'

#SCENE state check point
SCENE_STATE     = PATH_0_0XML + ' | grep pref_camera_scenemode_key'

class CameraTest(unittest.TestCase):
    def setUp(self):
        super(CameraTest,self).setUp()
        #Delete all image/video files captured before
        AD.cmd('rm','/sdcard/DCIM/*')
        #Refresh media after delete files
        AD.cmd('refresh','/sdcard/DCIM/*')
        #Launch social camera
        self._launchCamera()
        SM.switchcamera('hdr')

    def tearDown(self):
    	AD.cmd('pm','com.intel.camera22') #Force reset the camera settings to default
        super(CameraTest,self).tearDown()
        self._pressBack(4)

    def testCapturePictureWithFDOn(self):
        '''
            Summary: Capture image with FD/FR ON
            Steps  : 
                1.Launch HDR capture activity
                2.Set FD/FR ON
                3.Touch shutter button to capture picture
                4.Exit activity
        '''
        SM.setCameraSetting('hdr','fdfr','on')
        self._captureAndCheckPicCount('single',2)

    def testCapturePictureWithFDOff(self):
        '''
            Summary: Capture image with FD/FR OFF
            Steps  : 
                1.Launch HDR capture activity
                2.Set FD/FR OFF
                3.Touch shutter button to capture picture
                4.Exit  activity
        '''
        SM.setCameraSetting('hdr','fdfr','off')
        self._captureAndCheckPicCount('single',2)

    def testCapturePictureWithPictureSizeStandard(self):
        '''
            Summary: Capture image with Photo size 13MP
            Steps  : 
                1.Launch HDR capture activity
                2.Set photo size 13MP
                3.Touch shutter button to capture picture
                4.Exit  activity
        '''
        SM.setCameraSetting('hdr',2,2)
        assert bool(AD.cmd('cat',PICSIZE_STATE).find('StandardScreen')+1)
        self._captureAndCheckPicCount('single',2)

    def testCaptureWithPictureSizeWidesreen(self):
        '''
            Summary: Capture image with Photo size 6MP
            Steps  : 
                1.Launch HDR capture activity
                2.Set photo size 6MP
                3.Touch shutter button to capture picture
                4.Exit  activity
        '''
        SM.setCameraSetting('hdr',2,1)
        assert bool(AD.cmd('cat',PICSIZE_STATE).find('WideScreen')+1)
        self._captureAndCheckPicCount('single',2)

    def testCapturepictureWithGeoLocationOn(self):
        '''
            Summary: Capture image with Geo-tag ON
            Steps  : 
                1.Launch HDR capture activity
                2.Set photo Geo-tag ON
                3.Touch shutter button to capture picture
                4.Exit  activity
        '''
        SM.setCameraSetting('hdr',1,2)
        assert bool(AD.cmd('cat',GEO_STATE).find('on')+1)
        self._captureAndCheckPicCount('single',2)

    def testCapturepictureWithGeoLocationOff(self):
        """
        Summary: Capture image with Geo-tag OFF
        Steps  :  1.Launch HDR capture activity
                2.Set photo Geo-tag OFF
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        SM.setCameraSetting('hdr',1,1)
        assert bool(AD.cmd('cat',GEO_STATE).find('off')+1)
        self._captureAndCheckPicCount('single',2)

    def testCapturePictureWithSelfTimerOff(self):
        """
        Summary: Capture image with Self-timer off
        Steps  :  1.Launch HDR capture activity
                2.Set Self-timer off
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        SM.setCameraSetting('hdr',3,1)
        assert bool(AD.cmd('cat',TIMER_STATE).find('0')+1)
        self._captureAndCheckPicCount('single',2)

    def testCapturePictureWithThreeSec(self):
        """
        Summary: Capture image with Self-timer 3s
        Steps  :  1.Launch HDR capture activity
                2.Set Self-timer 3s
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        SM.setCameraSetting('hdr',3,2)
        assert bool(AD.cmd('cat',TIMER_STATE).find('3')+1)
        self._captureAndCheckPicCount('single',5)

    def testCapturePictureWithFiveSec(self):
        """
        Summary: Capture image with Self-timer 5s
        Steps  :  1.Launch HDR capture activity
                2.Set Self-timer 5s
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        SM.setCameraSetting('hdr',3,3)
        assert bool(AD.cmd('cat',TIMER_STATE).find('5')+1)
        self._captureAndCheckPicCount('single',7)

    def testCapturePictureWithTenSec(self):
        """
        Summary: Capture image with Self-timer 10s
        Steps  :  1.Launch HDR capture activity
                2.Set Self-timer 10s
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        SM.setCameraSetting('hdr',3,4)
        assert bool(AD.cmd('cat',TIMER_STATE).find('10')+1)
        self._captureAndCheckPicCount('single',12)

    def _captureAndCheckPicCount(self,capturemode,delaytime):
        beforeNo = AD.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count before capturing
        TB.takePicture(capturemode)
        time.sleep(delaytime) #Sleep a few seconds for file saving
        afterNo = AD.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count after taking picture
        if beforeNo != afterNo - 1: #If the count does not raise up after capturing, case failed
            self.fail('Taking picture failed!')

    def _launchCamera(self):
        d.start_activity(component = ACTIVITY_NAME)
        #When it is the first time to launch camera there will be a dialog to ask user 'remember location', so need to check
        try:
            assert d(text = 'OK').wait.exists(timeout = 2000)
            d(text = 'OK').click.wait()
        except:
            pass
        assert d(resourceId = 'com.intel.camera22:id/mode_button').wait.exists(timeout = 3000), 'Launch camera failed in 3s'

    def _pressBack(self,touchtimes):
        for i in range(0,touchtimes):
            d.press('back')
