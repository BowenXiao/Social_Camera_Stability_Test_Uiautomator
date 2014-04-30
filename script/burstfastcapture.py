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
        super(CameraTest,self).tearDown()
        self._pressBack(4)

    def testCaptureWithExposure(self):
        '''
            Summary: Capture image with Exposure
            Steps  :  
                1.Launch burst activity and select fast burst mode
                2.Check exposure setting icon, random set a value
                3.Touch shutter button to capture burst picture
                4.Exit activity
        '''
        exposure = random.choice(EXPOSURE_OPTION) #Random select an option
        SM.setCameraSetting('burst',4,EXPOSURE_OPTION.index(exposure)+1) #Tap on the selected option by its index
        assert bool(AD.cmd('cat',EXPOSURE_STATE).find(exposure)+1)
        self._captureAndCheckPicCount('single',5)

    def testCapturePictureWithScenes(self):
        '''
            Summary: Capture image with Scene
            Steps  :  
                1.Launch burst activity and select fast burst mode
                2.Check scence mode ,set mode
                3.Touch shutter button to capture burst picture
                4.Exit activity
        '''
        scene = random.choice(SCENE_OPTION) #Random select an option
        SM.setCameraSetting('burst',3,SCENE_OPTION.index(scene)+1) #Tap on the selected option by its index
        assert bool(AD.cmd('cat',SCENE_STATE).find(scene)+1)
        self._captureAndCheckPicCount('single',5)

    def testCaptureWithPictureSize(self):
        '''
            Summary: Capture image with Photo size
            Steps  :  
                1.Launch burst activity and select fast burst mode
                2.Check photo size ,set its size
                3.Touch shutter button to capture burst picture
                4.Exit activity
        '''
        size = random.choice(PICSIZE_OPTION) #Random select an option
        SM.setCameraSetting('burst',2,PICSIZE_OPTION.index(size)+1) #Tap on the selected option by its index
        assert bool(AD.cmd('cat',PICSIZE_STATE).find(size)+1)
        self._captureAndCheckPicCount('single',5)
        SM.setCameraSetting('burst',2,1) #Force set to the default setting

    def testCapturepictureWithGeoLocation(self):
        '''
            Summary: Capture image with Geo-tag
            Steps  : 
                1.Launch burst activity and select fast burst mode
                2.Check geo-tag ,set Geo on/off
                3.Touch shutter button to capture burst picture
                4.Exit activity
        '''
        geo = random.choice(GEO_OPTION) #Random select an option
        SM.setCameraSetting('burst',1,GEO_OPTION.index(geo)+1) #Tap on the selected option by its index
        assert bool(AD.cmd('cat',GEO_STATE).find(geo)+1)
        self._captureAndCheckPicCount('single',5)

    def _captureAndCheckPicCount(self,capturemode,delaytime=2):
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
