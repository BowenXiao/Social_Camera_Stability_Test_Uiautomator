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
        sm.switchcamera('perfectshot')

    def tearDown(self):
        super(CameraTest,self).tearDown()
        #4.Exit  activity
        self._pressBack(4)
        a.cmd('pm','com.intel.camera22')



# PerfectShot capture 14
# Test case 1
    def testPerfectShotCaptureWithExposureAuto(self):
        """
        Summary:testCaptureWithExposureZero: Take burst piture with exposure 0
        Steps:  1.Launch perfect shot activity
                2.Check exposure setting icon ,set to 0
                3.Touch shutter button to capture picture
        """
        

        # step 2
        sm.setCameraSetting('perfectshot',3,3)
        assert bool(a.cmd('cat',PATH + EXPOSURE_KEY).find('0')+1)
        # step 3
        self._checkCapturedPic()    
# Test case 2        
    def testPerfectShotCaptureWithExposurePlusOne(self):
        """
        Summary:testCaptureWithExposurePlusOne: Take burst piture with exposure +1
        Steps:  1.Launch perfect shot activity
                2.Check exposure setting icon ,set to +1
                3.Touch shutter button to capture picture
        """
        

        # step 2
        sm.setCameraSetting('perfectshot',3,4)
        assert bool(a.cmd('cat',PATH + EXPOSURE_KEY).find('3')+1)
        # step 3
        self._checkCapturedPic() 

# Test case 3    
    def testPerfectShotCaptureWithExposurePlusTwo(self):
        """
        Summary:testCapturePictureWithExposurePlusOne: Take burst piture with exposure +2
        Steps:  1.Launch perfect shot activity
                2.Check exposure setting icon ,set to +2
                3.Touch shutter button to capture picture
        """
        

        # step 2
        sm.setCameraSetting('perfectshot',3,5)
        assert bool(a.cmd('cat',PATH + EXPOSURE_KEY).find('6')+1)
        # step 3
        self._checkCapturedPic() 
# Test case 4
    def testPerfectShotCaptureWithExposureRedOne(self):
        """
        Summary:testCaptureWithExposureRedOne: Take burst piture with exposure -1
        Steps:  1.Launch perfect shot activity
                2.Check exposure setting icon ,set to -1
                3.Touch shutter button to capture picture
        """  
        

        # step 2
        sm.setCameraSetting('perfectshot',3,2)
        assert bool(a.cmd('cat',PATH + EXPOSURE_KEY).find('-3')+1)
        # step 3
        self._checkCapturedPic()

# Test case 5
    def testPerfectShotCaptureWithExposureRedTwo(self):
        """
        Summary:testCaptureWithExposureRedTwo: Take burst piture with exposure -2
        Steps:  1.Launch perfect shot activity
                2.Check exposure setting icon ,set to -2
                3.Touch shutter button to capture picture
        """
        

        # step 2
        sm.setCameraSetting('perfectshot',3,1)
        assert bool(a.cmd('cat',PATH + EXPOSURE_KEY).find('-6')+1)
        # step 3
        self._checkCapturedPic()

# Test case 6
    def testPerfectShotCapturePictureWithScenesAuto(self):
        """
        Summary:testCapturePictureWithScenesAuto: Take picture with set scenes to auto
        Steps:  1.Launch perfect shot activity
                2.Check scence mode ,set mode to auto
                3.Touch shutter button to capture picture
        """
        

        # step 2
        sm.setCameraSetting('perfectshot',2,7)
        assert bool(a.cmd('cat',PATH + SCENE_KEY).find('auto')+1)
        # step 3~4
        self._checkCapturedPic()

# Test case 7
    def testPerfectShotCapturePictureWithScenesSport(self):
        """
        Summary:testCapturePictureWithScenesSport: Take picture with set scenes to Sports
        Steps:  1Launch perfect shot activity
                2.Check scence mode ,set mode to Sports
                3.Touch shutter button to capture picture
        """
        

        # step 2
        sm.setCameraSetting('perfectshot',2,6)
        assert bool(a.cmd('cat',PATH + SCENE_KEY).find('sports')+1)
        # step 3
        self._checkCapturedPic() 

# Test case 8
    def testPerfectShotCapturePictureWithScenesNightPortrait(self):
        """
        Summary:testCapturePictureWithScenes NightPortrait: Capture image with Scene modeNightPortrait
        Steps:  1.Launch perfect shot activity
                2.Set Scene mode Night-portrait
                3.Touch shutter button to capture picture
        """
        

        # step 2
        sm.setCameraSetting('perfectshot',2,2)
        assert bool(a.cmd('cat',PATH + SCENE_KEY).find('night-portrait')+1)
        # step 3
        self._checkCapturedPic()         

# Test case 9
    def testPerfectShotCapturePictureWithScenesLandscape(self):
        """
        Summary:testCapturePictureWithScenesLandscape: Take picture with set scenes to landscape
        Steps:  1.Launch perfect shot activity
                2.Check scence mode ,set mode to landscape
                3.Touch shutter button to capture picture
        """
        

        # step 2
        sm.setCameraSetting('perfectshot',2,4)
        assert bool(a.cmd('cat',PATH + SCENE_KEY).find('landscape')+1)
        # step 3
        self._checkCapturedPic() 

# Test case 10
    def testPerfectShotCapturePictureWithScenesPortrait(self):
        """
        Summary:testCapturePictureWithScenesSport: Take picture with set scenes to portrait
        Steps:  1.Launch perfect shot activity
                2.Check scence mode ,set mode to portrait
                3.Touch shutter button to capture picture
        """
        

        # step 2
        sm.setCameraSetting('perfectshot',2,3)
        assert bool(a.cmd('cat',PATH + SCENE_KEY).find('portrait')+1)
        # step 3
        self._checkCapturedPic()        

# Test case 11
    def testPerfectShotCapturePictureWithScenesNight(self):
        """
        Summary:testCapturePictureWithScenesNight: Take picture with set scenes to night
        Steps:  1.Launch perfect shot activity
                2.Check scence mode ,set mode to night
                3.Touch shutter button to capture picture
        """
        

        # step 2
        sm.setCameraSetting('perfectshot',2,5)
        assert bool(a.cmd('cat',PATH + SCENE_KEY).find('night')+1)
        # step 3
        self._checkCapturedPic()

# Test case 12
    def testPerfectShotCapturePictureWithScenesBarcode(self):
        """
        Summary:testCapturePictureWithScenesBarcode: Capture image with Scene mode Barcode
        Steps:  1.Launch perfect shot activity
        2.Set Scene mode Barcode
        3.Touch shutter button to capture picture
        """
        

        # step 2
        sm.setCameraSetting('perfectshot',2,1)
        assert bool(a.cmd('cat',PATH + SCENE_KEY).find('barcode')+1)
        # step 3
        self._checkCapturedPic()

# Test case 13
    def testPerfectShotCapturepictureWithGeoLocationOn(self):
        """
        Summary:testCapturepictureWithGeoLocationOn: capture PerfectShot picture in geolocation on mode
        Steps:  1.Launch perfect shot activity
                2.Check geo-tag ,set to ON
                3.Touch shutter button to capture picture
        """ 
        

        # step 2
        sm.setCameraSetting('perfectshot',1,2)
        assert bool(a.cmd('cat',PATH1 + LOCATION_KEY).find('on')+1)
        # step 3
        self._checkCapturedPic()

# Test case 14
    def testPerfectShotCapturepictureWithGeoLocationOff(self):
        """
        Summary:testCapturepictureWithGeoLocationOff: capture PerfectShot picture in geolocation off mode
        Steps:  1.Launch perfect shot activity
                2.Check geo-tag ,set to Off
                3.Touch shutter button to capture  picture
        """ 
        

        # step 2
        sm.setCameraSetting('perfectshot',1,1)
        assert bool(a.cmd('cat',PATH1 + LOCATION_KEY).find('off')+1)
        # step 3
        self._checkCapturedPic()



    def _checkCapturedPic(self):
        beforeNo = a.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count before capturing
        tb.takePicture('single')
        afterNo = a.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count after taking picture
        if beforeNo == afterNo: #If the count does not raise up after capturing, case failed
            self.fail('Taking picture failed!')



    def _launchCamera(self):
        d.start_activity(component = ACTIVITY_NAME)
        time.sleep(1)
        assert d(resourceId = 'com.intel.camera22:id/mode_button').wait.exists(timeout = 3000), 'Launch camera failed in 3s'

    def _pressBack(self,touchtimes):
        for i in range(1,touchtimes+1):
            d.press('back')