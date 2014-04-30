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

class CameraTest(unittest.TestCase):
    def setUp(self):
        super(CameraTest,self).setUp()
        #Delete all image/video files captured before
        AD.cmd('rm','/sdcard/DCIM/*')
        #Refresh media after delete files
        AD.cmd('refresh','/sdcard/DCIM/*')
        #Launch social camera
        self._launchCamera()
        SM.switchcamera('burstfast')

    def tearDown(self):
    	AD.cmd('pm','com.intel.camera22') #Force reset the camera settings to default
        super(CameraTest,self).tearDown()
        self._pressBack(4)

    def testCaptureWithExposureAuto(self):
        '''
            Summary: Capture image with Exposure auto
            Steps  :  
                1.Launch burst activity and select Fast burst mode
                2.Check exposure setting icon ,set to auto
                3.Touch shutter button to capture burst picture
                4.Exit  activity
        '''
        SM.setCameraSetting('burst',4,3)
        assert bool(AD.cmd('cat',EXPOSURE_STATE).find('0')+1)
        self._captureAndCheckPicCount('single',5)

    def testCaptureWithExposurePlugOne(self):
        '''
            Summary: Capture image with Exposure plug one
            Steps  :  
                1.Launch burst activity and select Fast burst mode
                2.Check exposure setting icon ,set to plug one
                3.Touch shutter button to capture burst picture
                4.Exit  activity
        '''
        SM.setCameraSetting('burst',4,4)
        assert bool(AD.cmd('cat',EXPOSURE_STATE).find('3')+1)
        self._captureAndCheckPicCount('single',5)

    def testCaptureWithExposurePlugTwo(self):
        '''
            Summary: Capture image with Exposure plug two
            Steps  :  
                1.Launch burst activity and select Fast burst mode
                2.Check exposure setting icon ,set to plug two
                3.Touch shutter button to capture burst picture
                4.Exit  activity
        '''
        SM.setCameraSetting('burst',4,5)
        assert bool(AD.cmd('cat',EXPOSURE_STATE).find('6')+1)
        self._captureAndCheckPicCount('single',5)

    def testCaptureWithExposureRedOne(self):
        '''
            Summary: Capture image with Exposure red one
            Steps  :  
                1.Launch burst activity and select Fast burst mode
                2.Check exposure setting icon ,set to red one
                3.Touch shutter button to capture burst picture
                4.Exit  activity
        '''
        SM.setCameraSetting('burst',4,2)
        assert bool(AD.cmd('cat',EXPOSURE_STATE).find('-3')+1)
        self._captureAndCheckPicCount('single',5)

    def testCaptureWithExposureRedTwo(self):
        '''
            Summary: Capture image with Exposure red two
            Steps  :  
                1.Launch burst activity and select Fast burst mode
                2.Check exposure setting icon ,set to red two
                3.Touch shutter button to capture burst picture
                4.Exit  activity
        '''
        SM.setCameraSetting('burst',4,1)
        assert bool(AD.cmd('cat',EXPOSURE_STATE).find('-6')+1)
        self._captureAndCheckPicCount('single',5)

    def testCapturePictureWithScenesAuto(self):
        '''
            Summary: Capture image with Scene mode AUTO
            Steps  :  
                1.Launch burst activity and select Fast burst mode
                2.Check scence mode ,set mode to AUTO
                3.Touch shutter button to capture burst picture
                4.Exit  activity
        '''
        SM.setCameraSetting('burst',3,7)
        assert bool(AD.cmd('cat',SCENE_STATE).find('auto')+1)
        self._captureAndCheckPicCount('single',5)

    def testCapturePictureWithScenesSports(self):
        '''
            Summary: Capture image with Scene mode Sports
            Steps  :  
                1.Launch burst activity and select Fast burst mode
                2.Check scence mode ,set mode to Sports
                3.Touch shutter button to capture burst picture
                4.Exit  activity
        '''
        SM.setCameraSetting('burst',3,6)
        assert bool(AD.cmd('cat',SCENE_STATE).find('sports')+1)
        self._captureAndCheckPicCount('single',5)

    def testCapturePictureWithScenesNight(self):
        '''
            Summary: Capture image with Scene mode Night
            Steps  :  
                1.Launch burst activity and select Fast burst mode
                2.Check scence mode ,set mode to Night
                3.Touch shutter button to capture burst picture
                4.Exit  activity
        '''
        SM.setCameraSetting('burst',3,5)
        assert bool(AD.cmd('cat',SCENE_STATE).find('night')+1)
        self._captureAndCheckPicCount('single',5)

    def testCapturePictureWithScenesLandscape(self):
        '''
            Summary: Capture image with Scene mode Landscape
            Steps  :  
                1.Launch burst activity and select Fast burst mode
                2.Check scence mode ,set mode to Landscape
                3.Touch shutter button to capture burst picture
                4.Exit  activity
        '''
        SM.setCameraSetting('burst',3,4)
        assert bool(AD.cmd('cat',SCENE_STATE).find('landscape')+1)
        self._captureAndCheckPicCount('single',5)

    def testCapturePictureWithScenesPortrait(self):
        '''
            Summary: Capture image with Scene mode Portrait
            Steps  :  
                1.Launch burst activity and select Fast burst mode
                2.Check scence mode ,set mode to Portrait
                3.Touch shutter button to capture burst picture
                4.Exit  activity
        '''
        SM.setCameraSetting('burst',3,3)
        assert bool(AD.cmd('cat',SCENE_STATE).find('portrait')+1)
        self._captureAndCheckPicCount('single',5)

    def testCapturePictureWithScenesNightPortrait(self):
        '''
            Summary: Capture image with Scene mode Night-portrait
            Steps  :  
                1.Launch burst activity and select Fast burst mode
                2.Check scence mode ,set mode to Night-portrait
                3.Touch shutter button to capture burst picture
                4.Exit  activity
        '''
        SM.setCameraSetting('burst',3,2)
        assert bool(AD.cmd('cat',SCENE_STATE).find('night-portrait')+1)
        self._captureAndCheckPicCount('single',5)

    def testCapturePictureWithScenesBarcode(self):
        '''
            Summary: Capture image with Scene mode Barcode
            Steps  :  
                1.Launch burst activity and select Fast burst mode
                2.Check scence mode ,set mode to Barcode
                3.Touch shutter button to capture burst picture
                4.Exit  activity
        '''
        SM.setCameraSetting('burst',3,1)
        assert bool(AD.cmd('cat',SCENE_STATE).find('barcode')+1)
        self._captureAndCheckPicCount('single',5)

    def testCapturePictureWithSizeWidescreen(self):
        '''
            Summary: Capture image with Photo size 6MP
            Steps  :  
                1.Launch burst activity and select Fast burst mode
                2.Check photo size ,set to 6MP
                3.Touch shutter button to capture burst picture
                4.Exit  activity
        '''
        SM.setCameraSetting('burst',2,1)
        assert bool(AD.cmd('cat',SCENE_STATE).find('WideScreen')+1)
        self._captureAndCheckPicCount('single',5)

    def testCapturePictureWithSizeStandard(self):
        '''
            Summary: Capture image with Photo size 13MP
            Steps  : 
                1.Launch burst activity and select Fast burst mode
                2.Check photo size ,set to 13MP
                3.Touch shutter button to capture burst picture
                4.Exit  activity
        '''
        SM.setCameraSetting('burst',2,2)
        assert bool(AD.cmd('cat',SCENE_STATE).find('StandardScreen')+1)
        self._captureAndCheckPicCount('single',5)
    
    def testCapturepictureWithGeoLocationOn(self):
        '''
            Summary: Capture image with Geo-tag ON
            Steps  : 
                1.Launch burst activity and select Fast burst mode
                2.Check geo-tag ,set to ON
                3.Touch shutter button to capture burst picture
                4.Exit  activity
        '''
        SM.setCameraSetting('burst',1,2)
        assert bool(AD.cmd('cat',SCENE_STATE).find('on')+1)
        self._captureAndCheckPicCount('single',5)

    def testCapturepictureWithGeoLocationOff(self):
        '''
            Summary: Capture image with Geo-tag Off
            Steps  : 
                1.Launch burst activity and select Fast burst mode
                2.Check geo-tag ,set to Off
                3.Touch shutter button to capture burst picture
                4.Exit  activity
        '''
        SM.setCameraSetting('burst',1,1)
        assert bool(AD.cmd('cat',SCENE_STATE).find('off')+1)
        self._captureAndCheckPicCount('single',5)

    def _captureAndCheckPicCount(self,capturemode,delaytime):
        beforeNo = AD.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count before capturing
        TB.takePicture(capturemode)
        time.sleep(delaytime) #Sleep a few seconds for file saving
        afterNo = AD.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count after taking picture
        if beforeNo != afterNo - 10: #If the count does not raise up after capturing, case failed
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
