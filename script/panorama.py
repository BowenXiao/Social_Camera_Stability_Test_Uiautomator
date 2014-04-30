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
        sm.switchcamera('panorama')

    def tearDown(self):
        super(CameraTest,self).tearDown()
        #4.Exit  activity
        self._pressBack(4)
        a.cmd('pm','com.intel.camera22')

### Panorama capture 12 ###
# Test case 1
    def testPanoramaCaptureWithExposureAuto(self):
    	'''
        Summary:testCapturepictureWithGeoLocationOn: capture Panorama picture in geolocation on mode
        Steps: 
    	1.Launch Panorama activity
        2.Touch Exposure Setting icon, set Exposure auto
        3.Touch shutter button
        4.Touch shutter button to capture picture
        '''
        # step 2
        sm.setCameraSetting('panorama',2,3)
        # step 4~5
        assert bool(a.cmd('cat',PATH + EXPOSURE_KEY).find('0')+1)
        self._PanoramaCapturePic()

# Test case 2
    def testPanoramaCaptureWithExposurePlusOne(self):   
        '''
        Summary:testCaptureWithExposurePlusOne:capture Panorama picture with Exposure +1
        Steps  :
        1.Launch Panorama activity
        2.Touch Exposure Setting icon, set Exposure 1
        3.Touch shutter button 
        4.Touch shutter button to capture picture
        '''

        # step 2
        sm.setCameraSetting('panorama',2,4)
        assert bool((a.cmd('cat',PATH + EXPOSURE_KEY).find('3')+1)
        # step 4~5
        self._PanoramaCapturePic()

# Test case 3
    def testPanoramaCaptureWithExposurePlusTwo(self):
        '''
        Summary:testCapturePictureWithExposurePlusOne: capture Panorama picture with Exposure +2
        Steps: 
        1.Launch Panorama activity
        2.Touch Exposure Setting icon, set Exposure 2
        3.Touch shutter button 
        4.Touch shutter button to capture picture
        '''

        # step 2
        sm.setCameraSetting('panorama',2,5)
        assert bool(a.cmd('cat',PATH + EXPOSURE_KEY).find('6')+1)
        # step 4~5
        self._PanoramaCapturePic()

# Test case 4
    def testPanoramaCaptureWithExposureRedOne(self):
        '''
        Summary:testCaptureWithExposureRedOne: capture Panorama picture with Exposure -1
        Steps:
        1.Launch Panorama activity
        2.Touch Exposure Setting icon, set Exposure -1
        3.Touch shutter button 
        4.Touch shutter button to capture picture
        '''   

        # step 2
        sm.setCameraSetting('panorama',2,2)
        assert bool(a.cmd('cat',PATH + EXPOSURE_KEY).find('-3')+1)
        # step 4~5
        self._PanoramaCapturePic() 

# Test case 5    
    def testPanoramaCaptureWithExposureRedTwo(self):
        '''
        Summary:testCaptureWithExposureRedTwo: capture Panorama picture with Exposure -2
        Steps:
        1.Launch Panorama activity
        2.Touch Exposure Setting icon, set Exposure -1
        3.Touch shutter button 
        4.Touch shutter button to capture picture
        '''   

        # step 2
        sm.setCameraSetting('panorama',2,1)
        assert bool(a.cmd('cat',PATH + EXPOSURE_KEY).find('-6')+1)
        # step 4~5
        self._PanoramaCapturePic() 

# Test case 6
    def testPanoramaCapturepictureWithGeoLocationOn(self):
        """
        Summary:testCapturepictureWithGeoLocationOn: capture Panorama picture in geolocation on mode
        Steps:  1.Launch Panorama activity
                2.Check geo-tag ,set to ON
                3.Touch shutter button to capture picture
        """ 
        # step 1

        # step 2
        sm.setCameraSetting('panorama',1,2)
        assert bool(a.cmd('cat',PATH1 + LOCATION_KEY).find('on')+1)
        # step 3
        self._PanoramaCapturePic() 

# Test case 7
    def testPanoramaCapturepictureWithGeoLocationOff(self):
        """
        Summary:testCapturepictureWithGeoLocationOff: capture Panorama picture in geolocation off mode
        Steps:  1.Launch Panorama activity
                2.Check geo-tag ,set to Off
                3.Touch shutter button to capture picture
                4.Exit activity
        """ 


        # step 2
        sm.setCameraSetting('panorama',1,1)
        assert bool(a.cmd('cat',PATH1 + LOCATION_KEY).find('off')+1)
        # step 3
        self._PanoramaCapturePic() 

# Test case 8
    def testPanoramaCapturepictureWithISOSettingAuto(self):
        """
        Summary:testCapturepictureWithISOSettingAuto: Capture image with ISO Setting Auto
        Steps:  1.Launch Panorama activity
                2.Touch Geo-tag setting  icon,Set Geo-tag OFF
                3.Touch shutter button
                4.Touch shutter button to capture picture
                5.Exit  activity 
        """

        # step 2
        sm.setCameraSetting('panorama',3,5)
        assert bool(a.cmd('cat',PATH + IOS_KEY).find('iso-auto')+1)
        # step 3~4
        self._PanoramaCapturePic() 

# Test case 9    
    def testPanoramaCapturepictureWithISOSetting100(self):
        """
        Summary:testCapturepictureWithISOSetting100: Capture image with ISO Setting 100
        Steps:  1.Launch Panorama activity
        2.Set ISO Setting 100
        3.Touch shutter button
        4.Touch shutter button to capture picture
        """

        # step 2
        sm.setCameraSetting('panorama',3,4)
        assert bool(a.cmd('cat',PATH + IOS_KEY).find('iso-100')+1)
        # step 3~4
        self._PanoramaCapturePic() 

# Test case 10
    def testPanoramaCapturepictureWithISOSetting200(self):
        """
        Summary:testCapturepictureWithISOSetting200: Capture image with ISO Setting 200
        Steps:  1.Launch Panorama activity
        2.Set ISO Setting 200
        3.Touch shutter button
        4.Touch shutter button to capture picture  
        """

        # step 2
        sm.setCameraSetting('panorama',3,3)
        assert bool(a.cmd('cat',PATH + IOS_KEY).find('iso-200')+1)
        # step 3~4
        self._PanoramaCapturePic() 

# Test case 11
    def testPanoramaCapturepictureWithISOSetting400(self):
        """
        Summary:testCapturepictureWithISOSetting400: Capture image with ISO Setting 400
        Steps:  1.Launch Panorama activity
        2.Set ISO Setting 400
        3.Touch shutter button
        4.Touch shutter button to capture picture
        5.Exit  activity 
        """

        # step 2
        sm.setCameraSetting('panorama',3,2)
        assert bool(a.cmd('cat',PATH + IOS_KEY).find('iso-400')+1)
        # step 3~4
        self._PanoramaCapturePic() 

# Test case 12
    def testPanoramaCapturepictureWithISOSetting800(self):
        """
        Summary:testCapturepictureWithISOSetting800: Capture image with ISO Setting 800
        Steps:  1.Launch Panorama activity
        2.Set ISO Setting 800
        3.Touch shutter button
        4.Touch shutter button to capture picture
        """

        # step 2
        sm.setCameraSetting('panorama',3,1)
        assert bool(a.cmd('cat',PATH + IOS_KEY).find('iso-800')+1)
        # step 3~4
        self._PanoramaCapturePic()     





#######################################
    def _PanoramaCapturePic(self):
        beforeNo = a.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count before capturing
        tb.takePicture('smile')
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
