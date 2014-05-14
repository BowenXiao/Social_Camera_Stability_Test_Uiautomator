#!/usr/bin/env python
from devicewrapper.android import device as d
import time
import unittest
import commands
import util
import string
import random

A  = util.Adb()
SM = util.SetMode()
TB = util.TouchButton()

FLASH_MODE      = ['off','on','auto']
EXPOSURE_MODE   = ['-6','-3','0','3','6']
SCENE_MODE      = ['barcode','night-portrait','portrait','landscape','night','sports','auto']
FDFR_MODE       = ['on','off']
PICTURESIZE_MODE= ['WideScreen','StandardScreen']
HINTS_MODE      = ['off','on']
LOCATION_MODE   = ['off','on']
TIMER_MODE      = ['0','3','5','10']
ISO_MODE        = ['iso-800','iso-400','iso-200','iso-100','iso-auto']
WB_MODE         = ['cloudy','fluorescent','daylight','incandescent','auto']
##########################################################################################
class CameraTest(unittest.TestCase):

    def setUp(self):
        super(CameraTest,self).setUp()
        # rm DCIM folder and refresh from adb shell
        A.cmd('rm','/sdcard/DCIM/100ANDRO')
        A.cmd('refresh','/sdcard/DCIM/100ANDRO')
        #Because default camera after launching is single mode, so we set this step in setUp().
        #Step 1. Launch single capture activity
        A.cmd('launch','com.intel.camera22/.Camera')
        time.sleep(2)
        if  d(text = 'OK').wait.exists(timeout = 3000):
            d(text = 'OK').click.wait()
        else:
            assert d(resourceId = 'com.intel.camera22:id/shutter_button'),'Launch camera failed!!'

    def tearDown(self):
        super(CameraTest,self).tearDown()
        #4.Exit  activity
        TB.switchBackOrFrontCamera('back')
        self._pressBack(4)

    # Testcase 1
    def testCaptureSingleImageWithFlash(self):
        """
        Summary:Capture image with Flash.
        Step:
        1.Launch single capture activity
        2.Set flash mode
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        flash_mode = random.choice(FLASH_MODE)
        # Step 2
        SM.setCameraSetting('single','flash',flash_mode)
        self._confirmSettingMode('flash',flash_mode)
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 2
    def testCaptureSingleImageWithExposure(self):
        """
        Summary:Capture image with Exposure mode.
        Step:
        1.Launch single capture activity
        2.Set exposure mode
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        exposure_mode = random.choice(EXPOSURE_MODE)
        # Step 2
        SM.setCameraSetting('single',6,EXPOSURE_MODE.index(exposure_mode)+1)
        self._confirmSettingMode('exposure',exposure_mode)
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 3
    def testCaptureSingleImageWithScene(self):
        """
        Summary:Capture image with Scene mode.
        Step:
        1.Launch single capture activity
        2.Set scene mode
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        scene_mode = random.choice(SCENE_MODE)
        # Step 2 
        SM.setCameraSetting('single',5,SCENE_MODE.index(scene_mode)+1)
        self._confirmSettingMode('scenemode',scene_mode)
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)
        SM.setCameraSetting('single',5,7)

    # Testcase 4
    def testCaptureSingleImageWithFDFR(self):
        """
        Summary:Capture image with FD/FR.
        Step:
        1.Launch single capture activity
        2.Set FD/FR ON
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        fdfr_mode = random.choice(FDFR_MODE)
        # Step 2  Set FD/FR mode, confirm fdfr mode method is achieved in SM.setCameraSetting().
        SM.setCameraSetting('single','fdfr',fdfr_mode)
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 5
    def testCaptureSingleImageWithPictureSize(self):
        """
        Summary:Capture image with Photo size.
        Step:
        1.Launch single capture activity
        2.Set photo size
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        size_mode = random.choice(PICTURESIZE_MODE)
        # Step 2 
        SM.setCameraSetting('single',4,PICTURESIZE_MODE.index(size_mode)+1)
        self._confirmSettingMode('picture_size',size_mode)
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)
        SM.setCameraSetting('single',4,1)

    # Testcase 6
    def testCaptureSingleImageWithHits(self):
        """
        Summary:Capture image with Hints.
        Step:
        1.Launch single capture activity
        2.Set Hints
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        hints_mode = random.choice(HINTS_MODE)
        # Step 2 
        SM.setCameraSetting('single',2,HINTS_MODE.index(hints_mode)+1)
        self._confirmSettingMode('hints',hints_mode)
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 7
    def testCaptureSingleImageWithSelfTimer(self):
        """
        Summary:Capture image with Self-timer.
        Step:
        1.Launch single capture activity
        2.Set Self-timer
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        timer_mode = random.choice(TIMER_MODE)
        # Step 2
        SM.setCameraSetting('single',9,TIMER_MODE.index(timer_mode)+1)
        self._confirmSettingMode('delay',timer_mode)
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)
        SM.setCameraSetting('single',9,1)

    # Testcase 8
    def testCaptureSingleImageWithISO(self):
        """
        Summary:Capture image with ISO Setting.
        Step:
        1.Launch single capture activity
        2.Set ISO Setting
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        iso_mode = random.choice(ISO_MODE)
        # Step 2
        SM.setCameraSetting('single',8,ISO_MODE.index(iso_mode)+1)
        self._confirmSettingMode('iso',iso_mode)
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 9
    def testCaptureSingleImageWithWB(self):
        """
        Summary:Capture image with White Balance.
        Step:
        1.Launch single capture activity
        2.Set White Balance
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        wb_mode = random.choice(WB_MODE)
        # Step 2
        SM.setCameraSetting('single',7,WB_MODE.index(wb_mode)+1)
        self._confirmSettingMode('whitebalance',wb_mode)
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    def testCapturepictureWithLocation(self):
        """
        Summary:Capture image with Location.
        Step:
        1.Launch single capture activity
        2.Set Geo location
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        location_mode = random.choice(LOCATION_MODE)
        # Step 2
        SM.setCameraSetting('single',7,LOCATION_MODE.index(location_mode)+1)
        self._confirmSettingMode('location',location_mode)
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    def testFrontFaceCapturePictureWithFD(self):
        """
        Summary:Capture image with FD/FR on front camera.
        Step:
        1.Launch single capture activity
        2.Switch to front camera
        3.Set FD/FR
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        fdfr_mode = random.choice(FDFR_MODE)
        TB.switchBackOrFrontCamera('front')
        SM.setCameraSetting('single','fdfr',fdfr_mode)
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    def testFrontFaceCapturepictureWithLocation(self):
        """
        Summary:Capture image with location front camera.
        Step:
        1.Launch single capture activity
        2.Switch to front camera
        3.Set Geo location
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        location_mode = random.choice(LOCATION_MODE)
        TB.switchBackOrFrontCamera('front')
        # Step 2
        SM.setCameraSetting('single',7,LOCATION_MODE.index(location_mode)+1)
        self._confirmSettingMode('whitebalance',wb_mode)
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()        

    def _pressBack(self,touchtimes):
        for i in range(1,touchtimes+1):
            d.press('back')

    def _confirmSettingMode(self,sub_mode,option):
        if sub_mode == 'location':
            result = A.cmd('cat','/data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep '+ sub_mode)
            if result.find(option) == -1:
                self.fail('set camera setting ' + sub_mode + ' to ' + option + ' failed')
        else:
            result = A.cmd('cat','/data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep ' + sub_mode)
            if result.find(option) == -1:
                self.fail('set camera setting ' + sub_mode + ' to ' + option + ' failed')

    def _capturePictureAndConfirm(self,timer=0):
        beforeC = A.cmd('ls','/sdcard/DCIM/100ANDRO')
        TB.takePicture('single')
        time.sleep(timer)
        afterC  = A.cmd('ls','/sdcard/DCIM/100ANDRO')
        if afterC == beforeC:
            self.fail('take picture failed !!')