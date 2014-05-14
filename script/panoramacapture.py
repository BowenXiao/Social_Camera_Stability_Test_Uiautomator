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
#################################################
EXPOSURE_OPTION=['-6','-3','0','3','6']
LOCATION_OPTION =['off','on']
IOS_OPTION = ['iso-800', 'iso-400','iso-200','iso-100','iso-auto']

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
        assert d(resourceId = 'com.intel.camera22:id/shutter_button'),'Launch camera failed!!'
        sm.switchcamera('panorama')
        time.sleep(1)

    def tearDown(self):
        super(CameraTest,self).tearDown()
        #4.Exit  activity
        self._pressBack(4)
        a.cmd('pm','com.intel.camera22')

# Test case 1
    def testCaptureWithExposure(self):
        """
        Summary:testCaptureWithExposurePlusOne:capture Panorama picture with Exposure +1
        Steps  : 1.Launch Panorama activity
                 2.Touch Exposure Setting icon, set Exposure +1
                 3.Touch shutter button to capture picture
                 4.Exit  activity 
        """
        #step 2
        #exposure = random.choice( ['3', '6', '0','-3','-6'] )
        exposure = random.choice( EXPOSURE_OPTION)
        sm.setCameraSetting('panorama',2,EXPOSURE_OPTION.index(exposure)+1)
        assert bool(a.cmd('cat',PATH + EXPOSURE_KEY).find(exposure)+1)
        #Step 3
        self._panoramaCapturePic()
# Test case 2
    def testCapturepictureWithGeoLocation(self):
        """
        Summary:testCapturepictureWithGeoLocationOff: capture Panorama picture in geolocation off mode
        Steps:  1.Launch Panorama activity
                2.Check geo-tag ,set to Off
                3.Touch shutter button to capture picture
                4.Exit activity
        """   
        #Step 2
        location = random.choice(LOCATION_OPTION)
        sm.setCameraSetting('panorama',1,LOCATION_OPTION.index(location)+1)
        assert bool(a.cmd('cat',PATH1+ LOCATION_KEY).find(location)+1)
        #Step 3
        self._panoramaCapturePic()

# Test case 3
    def testCapturepictureWithISOSetting(self):
        """
        Summary:testCapturepictureWithISOSettingAuto: Capture image with ISO Setting Auto
        Steps:  1.Launch Panorama activity
                2.Touch Geo-tag setting  icon,Set Geo-tag OFF
                3.Touch shutter button
                4.Touch shutter button to capture picture
        5.Exit  activity 
        """

        #Step 2
        iso = random.choice(IOS_OPTION)
        sm.setCameraSetting('panorama',3,IOS_OPTION.index(iso)+1)
        assert bool(a.cmd('cat',PATH + IOS_KEY).find(iso)+1)
        #Step 3
        self._panoramaCapturePic()

        


######################################33

    
    def _panoramaCapturePic(self):
        beforeNo = a.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count before capturing
        tb.takePicture('smile')
        afterNo = a.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count after taking picture
        if beforeNo == afterNo: #If the count does not raise up after capturing, case failed
            self.fail('Taking picture failed!')
    
    def _pressBack(self,touchtimes):
        for i in range(1,touchtimes+1):
            d.press('back')


if __name__ =='__main__':  
    unittest.main() 
