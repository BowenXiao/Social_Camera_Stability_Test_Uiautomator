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
        SM.switchcamera('smile')


    def tearDown(self):
        super(CameraTest,self).tearDown()
        #4.Exit  activity
        self._pressBack(4)
        A.cmd('pm','com.intel.camera22')

    # Testcase 1
    def testCaptureSmileImageWithFlashOn(self):
        """
        Summary:Capture image with Flash ON.
        Step:
        1.Launch smile capture activity
        2.Set flash ON
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set flash ON
        SM.setCameraSetting('smile','flash','on')
        self._confirmSettingMode('flash','on')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 2
    def testCaptureSmileImageWithFlashOff(self):
        """
        Summary:Capture image with Flash OFF.
        Step:
        1.Launch smile capture activity
        2.Set flash OFF
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set flash OFF
        SM.setCameraSetting('smile','flash','off')
        self._confirmSettingMode('flash','off')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 3
    def testCaptureSmileImageWithFlashAuto(self):
        """
        Summary:Capture image with Flash AUTO.
        Step:
        1.Launch smile capture activity
        2.Set flash to AUTO mode
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set flash AUTO
        SM.setCameraSetting('smile','flash','auto')
        self._confirmSettingMode('flash','auto')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 4
    def testCaptureSmileImageWithExposureAuto(self):
        """
        Summary:Capture image with Exposure auto.
        Step:
        1.Launch smile capture activity
        2.Set exposure auto
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set exposure auto
        SM.setCameraSetting('smile',4,3)
        self._confirmSettingMode('exposure','0')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 5
    def testCaptureSmileImageWithExposurePlusOne(self):
        """
        Summary:Capture image with Exposure 1.
        Step:
        1.Launch smile capture activity
        2.Set exposure 1
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set exposure 1
        SM.setCameraSetting('smile',4,4)
        self._confirmSettingMode('exposure','3')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 6
    def testCaptureSmileImageWithExposurePlusTwo(self):
        """
        Summary:Capture image with Exposure 2.
        Step:
        1.Launch smile capture activity
        2.Set exposure 2
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set exposure 2
        SM.setCameraSetting('smile',4,5)
        self._confirmSettingMode('exposure','6')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 7
    def testCaptureSmileImageWithExposureRedOne(self):
        """
        Summary:Capture image with Exposure -1.
        Step:
        1.Launch smile capture activity
        2.Set exposure -1
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set exposure -1
        SM.setCameraSetting('smile',4,2)
        self._confirmSettingMode('exposure','-3')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 8
    def testCaptureSmileImageWithExposureRedTwo(self):
        """
        Summary:Capture image with Exposure -2.
        Step:
        1.Launch smile capture activity
        2.Set exposure -2
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set exposure -2
        SM.setCameraSetting('smile',4,1)
        self._confirmSettingMode('exposure','-6')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 9
    def testCaptureSmileImageWithSceneAuto(self):
        """
        Summary:Capture image with Scene mode AUTO.
        Step:
        1.Launch smile capture activity
        2.Set scene mode AUTO
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set scene mode AUTO
        SM.setCameraSetting('smile',3,7)
        self._confirmSettingMode('scenemode','auto')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 10
    def testCaptureSmileImageWithSceneSports(self):
        """
        Summary:Capture image with Scene mode Sports.
        Step:
        1.Launch smile capture activity
        2.Set scene mode Sports
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set scene mode Sports
        SM.setCameraSetting('smile',3,6)
        self._confirmSettingMode('scenemode','sports')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 11
    def testCaptureSmileImageWithSceneNight(self):
        """
        Summary:Capture image with Scene mode Night.
        Step:
        1.Launch smile capture activity
        2.Set scene mode Night
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set scene mode Night
        SM.setCameraSetting('smile',3,5)
        self._confirmSettingMode('scenemode','night')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 12
    def testCaptureSmileImageWithSceneLandscape(self):
        """
        Summary:Capture image with Scene mode Landscape.
        Step:
        1.Launch smile capture activity
        2.Set scene mode Landscape
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set scene mode Landscape
        SM.setCameraSetting('smile',3,4)
        self._confirmSettingMode('scenemode','landscape')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 13
    def testCaptureSmileImageWithScenePortrait(self):
        """
        Summary:Capture image with Scene mode Portrait.
        Step:
        1.Launch smile capture activity
        2.Set scene mode Portrait
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set scene mode Portrait
        SM.setCameraSetting('smile',3,3)
        self._confirmSettingMode('scenemode','portrait')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 14
    def testCaptureSmileImageWithSceneNightPortrait(self):
        """
        Summary:Capture image with Scene mode NightPortrait.
        Step:
        1.Launch smile capture activity
        2.Set scene mode NightPortrait
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set scene mode NightPortrait
        SM.setCameraSetting('smile',3,2)
        self._confirmSettingMode('scenemode','night-portrait')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 15
    def testCaptureSmileImageWithSceneBarcode(self):
        """
        Summary:Capture image with Scene mode barcode.
        Step:
        1.Launch smile capture activity
        2.Set scene mode barcode
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set scene mode barcode
        SM.setCameraSetting('smile',3,1)
        self._confirmSettingMode('scenemode','barcode')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 16
    def testCaptureSmileImageWithPictureSizeWidescreen(self):
        """
        Summary:Capture image with Photo size 6M.
        Step:
        1.Launch smile capture activity
        2.Set photo size 6M
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set photo size 6M
        SM.setCameraSetting('smile',2,1)
        self._confirmSettingMode('picture_size','WideScreen')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 17
    def testCaptureSmileImageWithPictureSizeStandardScreen(self):
        """
        Summary:Capture image with Scene mode barcode.
        Step:
        1.Launch smile capture activity
        2.Set photo size 13M
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2  Set photo size 13M
        SM.setCameraSetting('smile',2,2)
        self._confirmSettingMode('picture_size','StandardScreen')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm(2)

    # Testcase 18
    def testCaptureSingleImageWithLocationOn(self):
        """
        Summary:Capture image with Geo-tag ON.
        Step:
        1.Launch smile capture activity
        2.Set Ge0-tag ON
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set Ge0-tag ON.
        SM.setCameraSetting('smile',3,2)
        self._confirmSettingMode('location','on')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 19
    def testCaptureSingleImageWithLocationOff(self):
        """
        Summary:Capture image with Geo-tag OFF by front Face camera.
        Step:
        1.Launch smile capture activity
        2.Set Ge0-tag OFF
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set Ge0-tag OFF.
        SM.setCameraSetting('smile',3,1)
        self._confirmSettingMode('location','off')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 20
    def testCaptureSmileImageWithISOAuto(self):
        """
        Summary:Capture image with ISO Setting Auto.
        Step:
        1.Launch smile capture activity
        2.Set ISO Setting Auto
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set ISO Setting Auto
        SM.setCameraSetting('smile',6,5)
        self._confirmSettingMode('iso','iso-auto')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 21
    def testCaptureSmileImageWithISOOneH(self):
        """
        Summary:Capture image with ISO Setting 100.
        Step:
        1.Launch smile capture activity
        2.Set ISO Setting 100
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set ISO Setting 100
        SM.setCameraSetting('smile',6,4)
        self._confirmSettingMode('iso','iso-100')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 22
    def testCaptureSmileImageWithISOTwoH(self):
        """
        Summary:Capture image with ISO Setting 200.
        Step:
        1.Launch smile capture activity
        2.Set ISO Setting 200
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set ISO Setting 200
        SM.setCameraSetting('smile',6,3)
        self._confirmSettingMode('iso','iso-200')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 23
    def testCaptureSmileImageWithISOFourH(self):
        """
        Summary:Capture image with ISO Setting 400.
        Step:
        1.Launch smile capture activity
        2.Set ISO Setting 400
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set ISO Setting 400
        SM.setCameraSetting('smile',6,2)
        self._confirmSettingMode('iso','iso-400')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 24
    def testCaptureSmileImageWithISOEightH(self):
        """
        Summary:Capture image with ISO Setting 800.
        Step:
        1.Launch smile capture activity
        2.Set ISO Setting 800
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Set ISO Setting 800
        SM.setCameraSetting('smile',6,1)
        self._confirmSettingMode('iso','iso-800')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 25
    def testCaptureSmileImageWithWBAuto(self):
        """
        Summary:Capture image with White Balance Auto.
        Step:
        1.Launch smile capture activity
        2.Set White Balance Auto
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Capture image with White Balance Auto.
        SM.setCameraSetting('smile',5,5)
        self._confirmSettingMode('whitebalance','auto')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 26
    def testCaptureSmileImageWithWBIncandescent(self):
        """
        Summary:Capture image with White Balance Incandescent.
        Step:
        1.Launch smile capture activity
        2.Set White Balance Incandescent
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Capture image with White Balance Incandescent.
        SM.setCameraSetting('smile',5,4)
        self._confirmSettingMode('whitebalance','incandescent')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 27
    def testCaptureSmileImageWithWBDaylight(self):
        """
        Summary:Capture image with White Balance Daylight.
        Step:
        1.Launch smile capture activity
        2.Set White Balance Daylight
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Capture image with White Balance Daylight.
        SM.setCameraSetting('smile',5,3)
        self._confirmSettingMode('whitebalance','daylight')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()

    # Testcase 28
    def testCaptureSmileImageWithWBFluorescent(self):
        """
        Summary:Capture image with White Balance Fluorescent.
        Step:
        1.Launch smile capture activity
        2.Set White Balance Fluorescent
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Capture image with White Balance Fluorescent.
        SM.setCameraSetting('smile',5,2)
        self._confirmSettingMode('whitebalance','fluorescent')
        # Step 3 Touch shutter button to capture picture and confirm picture count + 1.
        self._capturePictureAndConfirm()  

    # Testcase 29
    def testCaptureSmileImageWithWBCloudy(self):
        """
        Summary:Capture image with White Balance Cloudy.
        Step:
        1.Launch smile capture activity
        2.Set White Balance Cloudy
        3.Touch shutter button to capture picture
        4.Exit  activity
        """
        # Step 2 Capture image with White Balance Cloudy.
        SM.setCameraSetting('smile',5,1)
        self._confirmSettingMode('whitebalance','cloudy')
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
        TB.takePicture('smile')
        time.sleep(timer)       
        afterC  = A.cmd('ls','/sdcard/DCIM/100ANDRO')
        if afterC == beforeC:
            self.fail('take picture failed !!')