#!/usr/bin/env python
#from uiautomatorplug.android import device as d
from devicewrapper.android import device as d
import time
import unittest
import commands
import util
import string

A  = util.Adb()
SM = util.SetMode()
TB = util.TouchButton()

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
        assert d(resourceId = 'com.intel.camera22:id/shutter_button'),'Launch camera failed!!'


    def tearDown(self):
        super(CameraTest,self).tearDown()
        #4.Exit  activity
        self._pressBack(4)
        A.cmd('pm','com.intel.camera22')


    # Testcase 1
    def testCaptureSingleImageWithFlashOn(self):
        """
        Summary:Capture image with Flash ON.
        Step:
        1.Launch single capture activity
        2.Set flash ON
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set flash ON
        SM.setCameraSetting('single','flash','on')
        self._confirmSettingMode('flash','on')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 2
    def testCaptureSingleImageWithFlashOff(self):
        """
        Summary:Capture image with Flash OFF.
        Step:
        1.Launch single capture activity
        2.Set flash OFF
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set flash OFF
        SM.setCameraSetting('single','flash','off')
        self._confirmSettingMode('flash','off')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 3
    def testCaptureSingleImageWithFlashAuto(self):
        """
        Summary:Capture image with Flash AUTO.
        Step:
        1.Launch single capture activity
        2.Set flash to AUTO mode
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set flash AUTO
        SM.setCameraSetting('single','flash','auto')
        self._confirmSettingMode('flash','auto')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 4
    def testCaptureSingleImageWithExposureAuto(self):
        """
        Summary:Capture image with Exposure auto.
        Step:
        1.Launch single capture activity
        2.Set exposure auto
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set exposure auto
        SM.setCameraSetting('single',6,3)
        self._confirmSettingMode('exposure','0')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 5
    def testCaptureSingleImageWithExposurePlusOne(self):
        """
        Summary:Capture image with Exposure 1.
        Step:
        1.Launch single capture activity
        2.Set exposure 1
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set exposure 1
        SM.setCameraSetting('single',6,4)
        self._confirmSettingMode('exposure','3')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 6
    def testCaptureSingleImageWithExposurePlusTwo(self):
        """
        Summary:Capture image with Exposure 2.
        Step:
        1.Launch single capture activity
        2.Set exposure 2
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set exposure 2
        SM.setCameraSetting('single',6,5)
        self._confirmSettingMode('exposure','6')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 7
    def testCaptureSingleImageWithExposureRedOne(self):
        """
        Summary:Capture image with Exposure -1.
        Step:
        1.Launch single capture activity
        2.Set exposure -1
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set exposure -1
        SM.setCameraSetting('single',6,2)
        self._confirmSettingMode('exposure','-3')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 8
    def testCaptureSingleImageWithExposureRedTwo(self):
        """
        Summary:Capture image with Exposure -2.
        Step:
        1.Launch single capture activity
        2.Set exposure -2
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set exposure -2
        SM.setCameraSetting('single',6,1)
        self._confirmSettingMode('exposure','-6')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 9
    def testCaptureSingleImageWithSceneAuto(self):
        """
        Summary:Capture image with Scene mode AUTO.
        Step:
        1.Launch single capture activity
        2.Set scene mode AUTO
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set scene mode AUTO
        SM.setCameraSetting('single',5,7)
        self._confirmSettingMode('scenemode','auto')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 10
    def testCaptureSingleImageWithSceneSports(self):
        """
        Summary:Capture image with Scene mode Sports.
        Step:
        1.Launch single capture activity
        2.Set scene mode Sports
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set scene mode Sports
        SM.setCameraSetting('single',5,6)
        self._confirmSettingMode('scenemode','sports')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 11
    def testCaptureSingleImageWithSceneNight(self):
        """
        Summary:Capture image with Scene mode Night.
        Step:
        1.Launch single capture activity
        2.Set scene mode Night
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set scene mode Night
        SM.setCameraSetting('single',5,5)
        self._confirmSettingMode('scenemode','night')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 12
    def testCaptureSingleImageWithSceneLandscape(self):
        """
        Summary:Capture image with Scene mode Landscape.
        Step:
        1.Launch single capture activity
        2.Set scene mode Landscape
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set scene mode Landscape
        SM.setCameraSetting('single',5,4)
        self._confirmSettingMode('scenemode','landscape')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 13
    def testCaptureSingleImageWithScenePortrait(self):
        """
        Summary:Capture image with Scene mode Portrait.
        Step:
        1.Launch single capture activity
        2.Set scene mode Portrait
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set scene mode Portrait
        SM.setCameraSetting('single',5,3)
        self._confirmSettingMode('scenemode','portrait')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 14
    def testCaptureSingleImageWithSceneNightPortrait(self):
        """
        Summary:Capture image with Scene mode NightPortrait.
        Step:
        1.Launch single capture activity
        2.Set scene mode NightPortrait
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set scene mode NightPortrait
        SM.setCameraSetting('single',5,2)
        self._confirmSettingMode('scenemode','night-portrait')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 15
    def testCaptureSingleImageWithSceneBarcode(self):
        """
        Summary:Capture image with Scene mode barcode.
        Step:
        1.Launch single capture activity
        2.Set scene mode barcode
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set scene mode barcode
        SM.setCameraSetting('single',5,1)
        self._confirmSettingMode('scenemode','barcode')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 16
    def testCaptureSingleImageWithFDFROn(self):
        """
        Summary:Capture image with FD/FR ON.
        Step:
        1.Launch single capture activity
        2.Set FD/FR ON
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set FD/FR ON, confirm fdfr is 'on' method is achieved in SM.setCameraSetting().
        SM.setCameraSetting('single','fdfr','on')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 17
    def testCaptureSingleImageWithFDFROff(self):
        """
        Summary:Capture image with FD/FR Off.
        Step:
        1.Launch single capture activity
        2.Set FD/FR Off
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set FD/FR Off, confirm fdfr is 'on' method is achieved in SM.setCameraSetting().
        SM.setCameraSetting('single','fdfr','off')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 18
    def testCaptureSingleImageWithPictureSizeWidescreen(self):
        """
        Summary:Capture image with Photo size 6M.
        Step:
        1.Launch single capture activity
        2.Set photo size 6M
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set photo size 6M
        SM.setCameraSetting('single',4,1)
        self._confirmSettingMode('picture_size','WideScreen')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 19
    def testCaptureSingleImageWithPictureSizeStandardScreen(self):
        """
        Summary:Capture image with Scene mode barcode.
        Step:
        1.Launch single capture activity
        2.Set photo size 13M
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set photo size 13M
        SM.setCameraSetting('single',5,2)
        self._confirmSettingMode('picture_size','StandardScreen')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 20
    def testCaptureSingleImageWithHitsOn(self):
        """
        Summary:Capture image with Hints ON.
        Step:
        1.Launch single capture activity
        2.Set Hints ON
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set Hints ON
        SM.setCameraSetting('single',2,2)
        self._confirmSettingMode('hints','on')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 21
    def testCaptureSingleImageWithHitsOff(self):
        """
        Summary:Capture image with Hints OFF.
        Step:
        1.Launch single capture activity
        2.Set Hints OFF
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set Hints OFF
        SM.setCameraSetting('single',2,1)
        self._confirmSettingMode('hints','off')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 22
    def testCaptureSingleImageWithSelfTimerOff(self):
        """
        Summary:Capture image with Self-timer off.
        Step:
        1.Launch single capture activity
        2.Set Self-timer off
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set Self-timer off
        SM.setCameraSetting('single',9,1)
        self._confirmSettingMode('delay','0')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 23
    def testCaptureSingleImageWithSelfTimerThree(self):
        """
        Summary:Capture image with Self-timer 3s.
        Step:
        1.Launch single capture activity
        2.Set Self-timer 3s
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set Self-timer 3s
        SM.setCameraSetting('single',9,2)
        self._confirmSettingMode('delay','3')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(5)

    # Testcase 24
    def testCaptureSingleImageWithSelfTimerFive(self):
        """
        Summary:Capture image with Self-timer 5s.
        Step:
        1.Launch single capture activity
        2.Set Self-timer 5s
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set Self-timer 5s
        SM.setCameraSetting('single',9,3)
        self._confirmSettingMode('delay','5')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(7)

    # Testcase 25
    def testCaptureSingleImageWithSelfTimerTen(self):
        """
        Summary:Capture image with Self-timer 10s.
        Step:
        1.Launch single capture activity
        2.Set Self-timer 10s
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set Self-timer 10s
        SM.setCameraSetting('single',9,4)
        self._confirmSettingMode('delay','10')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(12)

    # Testcase 26
    def testCaptureSingleImageWithISOAuto(self):
        """
        Summary:Capture image with ISO Setting Auto.
        Step:
        1.Launch single capture activity
        2.Set ISO Setting Auto
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set ISO Setting Auto
        SM.setCameraSetting('single',8,5)
        self._confirmSettingMode('iso','iso-auto')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 27
    def testCaptureSingleImageWithISOOneH(self):
        """
        Summary:Capture image with ISO Setting 100.
        Step:
        1.Launch single capture activity
        2.Set ISO Setting 100
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set ISO Setting 100
        SM.setCameraSetting('single',8,4)
        self._confirmSettingMode('iso','iso-100')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 28
    def testCaptureSingleImageWithISOTwoH(self):
        """
        Summary:Capture image with ISO Setting 200.
        Step:
        1.Launch single capture activity
        2.Set ISO Setting 200
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set ISO Setting 200
        SM.setCameraSetting('single',8,3)
        self._confirmSettingMode('iso','iso-200')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 29
    def testCaptureSingleImageWithISOFourH(self):
        """
        Summary:Capture image with ISO Setting 400.
        Step:
        1.Launch single capture activity
        2.Set ISO Setting 400
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set ISO Setting 400
        SM.setCameraSetting('single',8,2)
        self._confirmSettingMode('iso','iso-400')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 30
    def testCaptureSingleImageWithISOEightH(self):
        """
        Summary:Capture image with ISO Setting 800.
        Step:
        1.Launch single capture activity
        2.Set ISO Setting 800
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set ISO Setting 800
        SM.setCameraSetting('single',8,1)
        self._confirmSettingMode('iso','iso-800')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 31
    def testCaptureSingleImageWithWBAuto(self):
        """
        Summary:Capture image with White Balance Auto.
        Step:
        1.Launch single capture activity
        2.Set White Balance Auto
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Capture image with White Balance Auto.
        SM.setCameraSetting('single',7,5)
        self._confirmSettingMode('whitebalance','auto')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 32
    def testCaptureSingleImageWithWBIncandescent(self):
        """
        Summary:Capture image with White Balance Incandescent.
        Step:
        1.Launch single capture activity
        2.Set White Balance Incandescent
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Capture image with White Balance Incandescent.
        SM.setCameraSetting('single',7,4)
        self._confirmSettingMode('whitebalance','incandescent')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 33
    def testCaptureSingleImageWithWBDaylight(self):
        """
        Summary:Capture image with White Balance Daylight.
        Step:
        1.Launch single capture activity
        2.Set White Balance Daylight
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Capture image with White Balance Daylight.
        SM.setCameraSetting('single',7,3)
        self._confirmSettingMode('whitebalance','daylight')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 34
    def testCaptureSingleImageWithWBFluorescent(self):
        """
        Summary:Capture image with White Balance Fluorescent.
        Step:
        1.Launch single capture activity
        2.Set White Balance Fluorescent
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Capture image with White Balance Fluorescent.
        SM.setCameraSetting('single',7,2)
        self._confirmSettingMode('whitebalance','fluorescent')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()  

    # Testcase 35
    def testCaptureSingleImageWithWBCloudy(self):
        """
        Summary:Capture image with White Balance Cloudy.
        Step:
        1.Launch single capture activity
        2.Set White Balance Cloudy
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Capture image with White Balance Cloudy.
        SM.setCameraSetting('single',7,1)
        self._confirmSettingMode('whitebalance','cloudy')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()  

    # Testcase 36
    def testCaptureSingleImageWithLocationOn(self):
        """
        Summary:Capture image with Geo location on.
        Step:
        1.Launch single capture activity
        2.Set location on.
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 
        SM.setCameraSetting('single',3,2)
        self._confirmSettingMode('location','on')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 37
    def testCaptureSingleImageWithLocationOff(self):
        """
        Summary:Capture image with Geo location off.
        Step:
        1.Launch single capture activity
        2.Set location off.
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 
        SM.setCameraSetting('single',3,1)
        self._confirmSettingMode('location','off')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 38
    def testFrontCaptureSingleImageWithLocationOn(self):
        """
        Summary:Capture image with Geo location on front camera.
        Step:
        1.Launch single capture activity
        3.Switch to front camera
        3.Set location on.
        4.Touch shutter button to capture picture
        5.Exit  activity
        """
        TB.switchBackOrFrontCamera('front')
        # Step 2 
        SM.setCameraSetting('fsingle',1,2)
        self._confirmSettingMode('location','on')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 39
    def testFrontCaptureSingleImageWithLocationOff(self):
        """
        Summary:Capture image with Geo location off front camera.
        Step:
        1.Launch single capture activity
        3.Switch to front camera
        3.Set location off.
        4.Touch shutter button to capture picture
        5.Exit  activity
        """
        TB.switchBackOrFrontCamera('front')
        # Step 2
        SM.setCameraSetting('fsingle',1,1)
        self._confirmSettingMode('location','off')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 40
    def testFrontCaptureSingleImageWithFDFROn(self):
        """
        Summary:Capture image with FD/FR on front camera.
        Step:
        1.Launch single capture activity
        3.Switch to front camera
        3.Set FD/FR on.
        4.Touch shutter button to capture picture
        5.Exit  activity
        """
        TB.switchBackOrFrontCamera('front')
        # Step 2
        SM.setCameraSetting('fsingle','fdfr','on')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 41
    def testFrontCaptureSingleImageWithFDFROff(self):
        """
        Summary:Capture image with FD/FR off front camera.
        Step:
        1.Launch single capture activity
        3.Switch to front camera
        3.Set FD/FR off.
        4.Touch shutter button to capture picture
        5.Exit  activity
        """
        TB.switchBackOrFrontCamera('front')
        # Step 2
        SM.setCameraSetting('fsingle','fdfr','off')
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