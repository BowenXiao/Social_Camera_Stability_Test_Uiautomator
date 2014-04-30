#!/usr/bin/python
# coding:utf-8

from devicewrapper.android import device as d
import commands
import re
import subprocess
import os
import string
import time
import sys
import util 
import unittest
import random

a  = util.Adb()
sm = util.SetMode()
tb = util.TouchButton()
#Written by Piao chengguo

# PATH
PATH ='/data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml '
PATH1='cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml '
# key
EXPOSURE_KEY ='| grep pref_camera_exposure_key'
IOS_KEY='| grep pref_camera_iso_key'
LOCATION_KEY ='| grep pref_camera_geo_location_key'
SCENE_KEY ='| grep pref_camera_scenemode_key'
FDFR_KEY ='| grep pref_fdfr_key'
PICTURE_SIZE_KEY ='| grep pref_camera_picture_size_key'
HINTS_KEY ='| grep pref_camera_hints_key'
TIMER_KEY ='| grep pref_camera_delay_shooting_key'
WHITEBALANCE_KEY ='| grep pref_camera_whitebalance_key'
FLASH_STATE='| grep pref_camera_flashmode_key'
#################################
FLASH_OPTION=['auto', 'off', 'on']
EXPOSURE_OPTION=['-6','-3','0','3','6']
LOCATION_OPTION=['off','on']
IOS_OPTION=['iso-800', 'iso-400','iso-200','iso-100','iso-auto']
PICTURESIZE_OPTION = ['WideScreen','StandardScreen']
HINTS_OPTION=['off', 'on']
SELFTIMER_OPTION=['0','3','5','10']
WHITEBALANCE_OPTION=['cloudy-daylight', 'fluorescent','daylight','incandescent','auto']
SCENCE_OPTION=['barcode', 'night-portrait', 'portrait','landscape','night','sports','auto']
FDFR_OPTION=['off', 'on']
#################################

PACKAGE_NAME = 'com.intel.camera22'
ACTIVITY_NAME = PACKAGE_NAME + '/.Camera'

class CameraTest(unittest.TestCase):
    
    def setUp(self):
        super(CameraTest,self).setUp()
        # rm DCIM folder and refresh from adb shell
        a.cmd('rm','/sdcard/DCIM/100ANDRO')
        a.cmd('refresh','/sdcard/DCIM/100ANDRO')
        #Because default camera after launching is single mode, so we set this step in setUp().
        #Step 1. Launch single capture activity
        a.cmd('launch','com.intel.camera22/.Camera')
        time.sleep(2)
        if  d(text = 'OK').wait.exists(timeout = 3000):
            d(text = 'OK').click.wait()
        else:
            assert d(resourceId = 'com.intel.camera22:id/shutter_button'),'Launch camera failed!!'


    def tearDown(self):
        super(CameraTest,self).tearDown()
        #4.Exit  activity
        self._pressBack(4)
        a.cmd('pm','com.intel.camera22')

    # Test case 1
    def testCapturePictureWithFlash(self):
        """
        Summary:testCapturePictureWithFlashOn: Take a picture with flash on
        Steps:  1.Launch single capture activity
                2.Set flash ON
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        flash = random.choice(FLASH_OPTION)
        sm.setCameraSetting('single','flash',flash)
        assert bool(a.cmd('cat',PATH + FLASH_STATE).find(flash)+1)
        # Step 3
        self._continuouCapturePic()


    # Test case 2
    def testCaptureWithExposure(self):
        """
        Summary:testCaptureWithExposurePlusOne: Take a picture with Exposure +1
        Steps: 1.Launch single capture activity
               2.Set exposure +1
               3.Touch shutter button to capture picture
               4.Exit  activity
        """       
        # Step 2
        exposure = random.choice( EXPOSURE_OPTION)
        sm.setCameraSetting('single',6,EXPOSURE_OPTION.index(exposure)+1)
        assert bool(a.cmd('cat',PATH + EXPOSURE_KEY).find(exposure)+1)
        # Step 3
        self._continuouCapturePic()


    # Test case 3
    def testCapturePictureWithScenes(self):
        """
        Summary:testCapturePictureWithScenesSport: Take a picture with set scenes to Sports
        Steps:  1.Launch single capture activity
                2.Set scene mode Sports
                3.Touch shutter button to capture picture
                4.Exit  activity
        """

        scence = random.choice(SCENCE_OPTION)
        sm.setCameraSetting('single',5,SCENCE_OPTION.index(scence)+1)
        assert bool(a.cmd('cat',PATH + SCENE_KEY).find(scence)+1)
        #Step 3
        self._continuouCapturePic()
   


    # Test case 4
    def testCapturePictureWithFD(self):
        """
        Summary:testCapturePictureWithFDON: Take a picture with set FD/FR on
        Steps:  1.Launch single capture activity
                2.Set FD/FR ON
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        fdfr =random.choice(FDFR_OPTION)
        sm.setCameraSetting('single','fdfr',fdfr)
        self._continuouCapturePic()


    # Test case 5
    def testCapturePictureWithPictureSize(self):
        """
        Summary:testCapturePictureWithPictureSizeStandard: Take a picture with picture size is standard
        Steps:  1.Launch single capture activity
                2.Set picture size is standard
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        picturesize = random.choice(PICTURESIZE_OPTION)
        sm.setCameraSetting('single',4,PICTURESIZE_OPTION.index(picturesize)+1)
        assert bool(a.cmd('cat',PATH + PICTURE_SIZE_KEY).find(picturesize)+1)
        self._continuouCapturePic()



    # Test case 6
    def testCapturepictureWithGeoLocation(self):
        """
        Summary:testCapturepictureWithGeoLocationOn:Take a picture with  geolocation is on
        Steps:  1.Launch camera app
                2.Set geo location on 
                3.Touch shutter button to capture picture
                4.Exit  activity
        """ 
        #Step 2
        location = random.choice(LOCATION_OPTION)
        sm.setCameraSetting('single',3,LOCATION_OPTION.index(location)+1)
        assert bool(a.cmd('cat',PATH1 + LOCATION_KEY).find(location)+1)
        #Step 3
        self._continuouCapturePic()




    # Test case 7
    def testCapturepictureWithHints(self):
        """
        Summary:testCapturepictureWithHintsOn: Take a picture with  hints is on
        Steps:  1.Launch camera app
                2.Set hints on
                3.Touch shutter button to capture picture
                4.Exit  activity
        """ 
        #Step 2
        hints = random.choice(HINTS_OPTION)
        sm.setCameraSetting('single',2,HINTS_OPTION.index(hints)+1)
        assert bool(a.cmd('cat',PATH + HINTS_KEY).find(hints)+1)
        #Step 3
        self._continuouCapturePic()



    # Test case 8
    def testRearFaceCapturePictureWithFD(self):
        """
        Summary:testRearFaceCapturePictureWithFDON: Take a picture using fear face camera and set FD/FR on
        Steps:  1.Launch single capture activity
                2.Set FD/FR ON
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        tb.switchBackOrFrontCamera('front')
        fdfr =random.choice(FDFR_OPTION)
        sm.setCameraSetting('single','fdfr',fdfr)
        self._continuouCapturePic()



    # Test case 9
    def testRearFaceCapturepictureWithGeoLocation(self):
        """
        Summary:testRearFaceCapturepictureWithGeoLocationOn: Take a picture using fear face camera and set geolocation on 
        Steps:  1.Launch camera app
                2.Set geolocation on 
                3.Touch shutter button to capture picture
                4.Exit  activity
        """ 
        tb.switchBackOrFrontCamera('front')
        location = random.choice(LOCATION_OPTION)
        print location
        print LOCATION_OPTION.index(location)+1
        sm.setCameraSetting('fsingle',1,LOCATION_OPTION.index(location)+1)
        assert bool(a.cmd('cat',PATH1 + LOCATION_KEY).find(location)+1)
        #Step 3
        #Step 3
        self._continuouCapturePic()

    # Test case 10
    #def testCapturepictureWithSelfTimer(self):
        """
        Summary:testCapturepictureWithSelfTimerOff: Capture image with Self-timer off
        Steps:  1.Launch single capture activity
                2.Set Self-timer off
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        # Step 2
     #   selftimer = random.choice(SELFTIMER_OPTION)
      #  sm.setCameraSetting('single',9,SELFTIMER_OPTION.index(selftimer)+1)
       # assert bool(a.cmd('cat',PATH + TIMER_KEY).find(selftimer)+1)
        #self._continuouCapturePic()





    # Test case 11
    def testCapturepictureWithISO(self):
        """
        Summary:testCapturepictureWithISOAuto: Capture image with ISO Setting Auto
        Steps:  1.Launch single capture activity
                2.Set ISO Setting Auto
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        iso = random.choice(IOS_OPTION)
        sm.setCameraSetting('single',8,IOS_OPTION.index(iso)+1)
        assert bool(a.cmd('cat',PATH + IOS_KEY).find(iso)+1)
        #Step 3
        self._continuouCapturePic()



    # Test case 12
    def testCapturepictureWithWhiteBalance(self):
        """
        Summary:testCapturepictureWithWhiteBalanceAuto: Capture image with White Balance Auto
        Steps:  1.Launch single capture activity
                2.Set White Balance Auto
                3.Touch shutter button to capture picture
                4.Exit  activity
        """
        # Step 2
        WhiteBalance = random.choice(WHITEBALANCE_OPTION)
        sm.setCameraSetting('single',7,WHITEBALANCE_OPTION.index(WhiteBalance)+1)
        assert bool(a.cmd('cat',PATH + WHITEBALANCE_KEY).find(WhiteBalance)+1)
        #Step 3
        self._continuouCapturePic()

#######################################################3
    def _continuouCapturePic(self):
        beforeNo = a.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count before capturing
        tb.takePicture('longclick')
        afterNo = a.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count after taking picture
        if beforeNo == afterNo: #If the count does not raise up after capturing, case failed
            self.fail('Taking picture failed!')
    
    def _pressBack(self,touchtimes):
        for i in range(1,touchtimes+1):
            d.press('back')


if __name__ =='__main__':  
    unittest.main() 
