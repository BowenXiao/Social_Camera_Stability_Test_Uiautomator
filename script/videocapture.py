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

class CameraTest(unittest.TestCase):
    def setUp(self):
        super(CameraTest,self).setUp()
        #Delete all image/video files captured before
        AD.cmd('rm','/sdcard/DCIM/*')
        #Refresh media after delete files
        AD.cmd('refresh','/sdcard/DCIM/*')
        #Launch social camera
        self._launchCamera()
        SM.switchcamera('video')

    def tearDown(self):
        super(CameraTest,self).tearDown()
        self._pressBack(4)

    def testRecordVideoWithFlash(self):
        '''
            Summary: Record a video with flash
            Steps  : 
                1.Launch video activity
                2.Check flash state, set to ON/OFF
                3.Touch shutter button to capture 30s video
                4.Exit activity
        '''
        flash = random.choice(FLASH_OPTION)
        SM.setCameraSetting('video','flash',flash) 
        if flash == 'on':
            flash = 'torch' #Option 'on' in xml file is actually 'torch'
        assert bool(AD.cmd('cat',FLASH_STATE).find(flash)+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoWithVideoSize(self):
        '''
            Summary: Capture video with setting size
            Steps  :  
                1.Launch video activity
                2.Check video size ,set its size setting
                3.Touch shutter button to capture 30s video
                4.Exit activity 
        '''
        vsize = random.choice(VSIZE_OPTION) #Random select an option
        SM.setCameraSetting('video',3,VSIZE_OPTION.index(vsize)+1) #Tap on the selected option by its index
        assert bool(AD.cmd('cat',VIDEOSIZE_STATE).find(vsize)+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoWithGeoLocation(self):
        '''
            Summary: Record an video with GeoLocation setting
            Steps  :  
                1.Launch video activity
                2.Check geo-tag ,set to ON/OFF
                3.Touch shutter button to capture 30s video
                4.Exit activity 
        '''
        geo = random.choice(GEO_OPTION)
        SM.setCameraSetting('video',2,GEO_OPTION.index(geo)+1)
        assert bool(AD.cmd('cat',GEO_STATE).find(geo)+1)
        self._takeVideoAndCheckCount()

    def testRearFaceRecordVideoWithGeoLocation(self):
        '''
            Summary: Record an video with rear face camera and set GeoLocation
            Steps  :  
                1.Launch video activity
                2.Set to front face camera
                3.Check geo-tag,set to ON/OFF
                4.Touch shutter button to capture 30s video
                5.Exit activity
        '''
        TB.switchBackOrFrontCamera('front') #Set to front camera
        geo = random.choice(GEO_OPTION)
        SM.setCameraSetting('fvideo',1,GEO_OPTION.index(geo)+1)
        assert bool(AD.cmd('cat',GEO_STATE).find(geo)+1)
        self._takeVideoAndCheckCount()
        TB.switchBackOrFrontCamera('back') #Force set setting to the default

    def testRecordVideoCaptureVideoWithBalance(self):
        '''
            Summary: Capture video with White Balance
            Steps  :  
                1.Launch video activity
                2.Set White Balance
                3.Touch shutter button to capture 30s video
                4.Exit activity
        '''
        wbalance = random.choice(WBALANCE_OPTION)
        SM.setCameraSetting('video',5,WBALANCE_OPTION.index(wbalance)+1)
        assert bool(AD.cmd('cat',WBALANCE_STATE).find(wbalance)+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoCaptureVideoWithExposure(self):
        '''
            Summary: Capture video with Exposure
            Steps  :  
                1.Launch Video activity
                2.Touch Exposure Setting icon, set Exposure settings
                3.Touch shutter button
                4.Touch shutter button to capture picture
                5.Exit activity
        '''
        exposue = random.choice(EXPOSURE_OPTION)
        SM.setCameraSetting('video',4,EXPOSURE_OPTION.index(exposue)+1)
        assert bool(AD.cmd('cat',EXPOSURE_STATE).find(exposue)+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoWithCaptureImage(self):
        '''
            Summary: Capture image when record video
            Steps  :  
                1.Launch video activity
                2.Touch shutter button to capture 30s video
                3.Touch screen to capture a picture during recording video
                4.Exit activity 
        '''
        #No setting to be changed
        self._takeVideoAndCheckCount(capturetimes = 5)

    def _takeVideoAndCheckCount(self,recordtime=30,delaytime=2,capturetimes=0):
        beforeNo = AD.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count before capturing
        TB.takeVideo(recordtime,capturetimes)
        time.sleep(delaytime) #Sleep a few seconds for file saving
        afterNo = AD.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count after taking picture
        if beforeNo != afterNo - capturetimes - 1: #If the count does not raise up after capturing, case failed
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
