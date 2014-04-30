#!/usr/bin/python
# coding:utf-8

from devicewrapper.android import device as d
import unittest
import commands
import os
import string
import time
import sys
import util 
import string
import random

AD = util.Adb()
TB = util.TouchButton()
SM = util.SetMode()

#Written by XuGuanjun

PACKAGE_NAME  = 'com.intel.camera22'
ACTIVITY_NAME = PACKAGE_NAME + '/.Camera'

#All setting info of camera could be cat in the folder
PATH_PREF_XML  = '/data/data/com.intel.camera22/shared_prefs/'

#FDFR / GEO / BACK&FROUNT xml file in com.intelcamera22_preferences_0.xml
PATH_0XML      = PATH_PREF_XML + 'com.intel.camera22_preferences_0.xml'

#PICSIZE / EXPROSURE / TIMER / WHITEBALANCE / ISO / HITS / VIDEOSIZE in com.intel.camera22_preferences_0_0.xml
PATH_0_0XML    = PATH_PREF_XML + 'com.intel.camera22_preferences_0_0.xml'

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

#Flash state check point
FLASH_STATE     = PATH_0_0XML + ' | grep pref_camera_video_flashmode_key'

#SCENE state check point
SCENE_STATE     = PATH_0_0XML + ' | grep pref_camera_scenemode_key'

#Exposure options
EXPOSURE_OPTION = ['-6','-3','0','3','6']

#Scene options
SCENE_OPTION    = ['barcode','night-portrait','portrait','landscape','night','sports','auto']

#Picture size options
PICSIZE_OPTION  = ['WideScreen','StandardScreen']

#Geo options
GEO_OPTION      = ['off','on']

#Flash options
FLASH_OPTION    = ['off','on']

#Video size options
VSIZE_OPTION    = ['4','5','5','6','6']

#White balance options
WBALANCE_OPTION = ['cloudy','fluorescent','daylight','incandescent','auto']

#FD/FR options
FDFR_OPTION     = ['on','off']

#Self timer options
TIMER_OPTION    = ['0','3','5','10']

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
        super(CameraTest,self).tearDown()
        self._pressBack(4)

    def testCapturePictureWithFD(self):
        '''
            Summary: Capture image with FD/FR
            Steps  : 
                1.Launch HDR capture activity
                2.Set FD/FR ON/OFF
                3.Touch shutter button to capture picture
                4.Exit activity
        '''
        fdfr = random.choice(FDFR_OPTION)
        SM.setCameraSetting('hdr','fdfr',fdfr)
        self._captureAndCheckPicCount('single')

    def testCapturepictureWithGeoLocation(self):
        '''
            Summary: Capture image with Geo-tag
            Steps  : 
                1.Launch HDR capture activity
                2.Set photo Geo-tag ON/OFF
                3.Touch shutter button to capture picture
                4.Exit  activity
        '''
        geo = random.choice(GEO_OPTION)
        SM.setCameraSetting('hdr',1,GEO_OPTION.index(geo)+1)
        assert bool(AD.cmd('cat',GEO_STATE).find(geo)+1)
        self._captureAndCheckPicCount('single')

    def testCapturePictureWithPictureSize(self):
        '''
            Summary: Capture image with Photo size
            Steps  : 
                1.Launch HDR capture activity
                2.Set photo size 6MP/13MP
                3.Touch shutter button to capture picture
                4.Exit  activity
        '''
        size = random.choice(PICSIZE_OPTION)
        SM.setCameraSetting('hdr',2,PICSIZE_OPTION.index(size)+1)
        assert bool(AD.cmd('cat',PICSIZE_STATE).find(size)+1)
        self._captureAndCheckPicCount('single')
        SM.setCameraSetting('hdr',2,1) #Force set to the default setting

    def testCapturePictureWithSelfTimer(self):
        '''
        Summary: Capture image with Self-timer
        Steps  :  1.Launch HDR capture activity
                2.Set Self-timer setting
                3.Touch shutter button to capture picture
                4.Exit  activity
        '''
        timer = random.choice(TIMER_OPTION)
        SM.setCameraSetting('hdr',3,TIMER_OPTION.index(timer)+1)
        assert bool(AD.cmd('cat',TIMER_STATE).find(timer)+1)
        self._captureAndCheckPicCount('single',string.atoi(timer)+2)
        SM.setCameraSetting('hdr',3,1) #Force set timer to off

    def _captureAndCheckPicCount(self,capturemode,delaytime=2):
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