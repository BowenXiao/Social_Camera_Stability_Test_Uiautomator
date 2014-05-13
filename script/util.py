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

##################################################################################################################
ADB = 'adb'
ADB_SHELL = ADB + ' shell'
ADB_DEVICES = ADB + ' devices'
ANDROID_SERIAL='ANDROID_SERIAL'
##################################################################################################################

MODE_LIST_BUTTON    = 'com.intel.camera22:id/mode_button'
MODE_ID             ={'single':'com.intel.camera22:id/mode_wave_photo',
                      'smile':'com.intel.camera22:id/mode_wave_smile',
                      'hdr':'com.intel.camera22:id/mode_wave_hdr',
                      'video':'com.intel.camera22:id/mode_wave_video',
                      'burstfast':'com.intel.camera22:id/mode_wave_burst',
                      'burstslow':'com.intel.camera22:id/mode_wave_burst',
                      'perfectshot':'com.intel.camera22:id/mode_wave_perfectshot',
                      'panorama':'com.intel.camera22:id/mode_wave_panorama'
                      }


RESULT              = r'^>\d<$'
HORI_LIST_BUTTON    = 'com.intel.camera22:id/hori_list_button'
FLASH_SETTING       = ['off','on','auto']


##################################################
#     Settings in each mode                      #
##################################################
SINGLE_SETTING      = ['testcamera','hits','location','picturesize','scencesmode','exposure','whitebalance','iso','delay']
SMILE_SETTING       = ['location','picturesize','sencesmode','exposure','whitebalance','iso']
HDR_SETTING         = ['location','picturesize','delay']
VIDEO_SETTING       = ['testcamera','location','videosize','exposure','whitebalance']
BURST_SETTING       = ['location','picturesize','sencesmode','exposure']
PERFECTSHOT_SETTING = ['location','scencesmode','exposure']
PANORAMA_SETTING    = ['location','exposure','iso']
SINGLE_SETTING_FRONT= ['location']
VIDEO_SETTING_FRONT = ['location']


MODE = {'single':SINGLE_SETTING,
        'smile':SMILE_SETTING,
        'hdr':HDR_SETTING,
        'video':VIDEO_SETTING,
        'burst':BURST_SETTING,
        'perfectshot':PERFECTSHOT_SETTING,
        'panorama':PANORAMA_SETTING,
        'fsingle':SINGLE_SETTING_FRONT,
        'fvideo':VIDEO_SETTING_FRONT
        }


XML_CONFIRM_LIST = {'hits': 'pref_camera_hints_key',
                    'location': 'pref_camera_geo_location_key',
                    'picturesize': 'pref_camera_picture_size_key',
                    'scencesmode': 'pref_camera_scenemode_key',
                    'exposure': 'pref_camera_exposure_key',
                    'whitebalance': 'pref_camera_whitebalance_key',
                    'iso': 'pref_camera_iso_key',
                    'delay': 'pref_camera_delay_shooting_key',
                    'videosize': 'pref_video_quality_key'
                    }
#################################################################################################################
CPTUREBUTTON_RESOURCEID ='com.intel.camera22:id/shutter_button'
FRONTBACKBUTTON_DESCR = 'Front and back camera switch'
CPTUREPOINT='adb shell input swipe 363 1145 359 1045 '
DRAWUP_CAPTUREBUTTON='adb shell input swipe 363 1145 359 1045 '
DRAWDOWN_MENU='adb shell input swipe 530 6 523 22'


CAMERA_ID = 'adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_camera_id_key'
#################################################################################################################

class Adb():

    '''
    This method support user execute adb commands,support push,pull,cat,refresh,ls,launch,rm

    usage:  adb=Adb()
    ------------------------------------------------------------------------------------------------------------
    | adb.cmd('cat','xxxx/xxx.xml')                 |  adb shell cat xxxx/xxx.xml,return cat result             | 
    ------------------------------------------------------------------------------------------------------------
    | adb.cmd('refresh','/sdcard/')                 |  refresh media file under path /sdcard/,return ture/false |
    ------------------------------------------------------------------------------------------------------------
    | adb.cmd('ls','/sdcard/')                      |  get the file number under path /sdcard/,return number    |                         
    ------------------------------------------------------------------------------------------------------------    
    | adb.cmd('rm','xxxx/xxxx.jpg')                 |  delete xxxx/xxx.jpg,return true/false                    |
    ------------------------------------------------------------------------------------------------------------ 
    | adb.cmd('launch','com.intel.camera22/.Camera')|  launch social camera app,return adb commands             |
    ------------------------------------------------------------------------------------------------------------
    '''
    def cmd(self,action,path,t_path=None):
        #export android serial
        if not os.environ.has_key(ANDROID_SERIAL):
            self._exportANDROID_SERIAL()
        #adb commands
        action1={
        'refresh':self._refreshMedia,
        'ls':self._getFileNumber,
        'cat':self._catFile,
        'launch':self._launchActivity,
        'rm':self._deleteFile,
        'pm':self._resetApp
        }
        action2=['pull','push']
        if action in action1:
            return action1.get(action)(path)
        elif action in action2:
            return self._pushpullFile(action,path,t_path)
        else:
            raise Exception('commands is unsupported,only support [push,pull,cat,refresh,ls,launch,rm] now')

    def _resetApp(self,path):
        p = self._shellcmd('pm clear ' + path)
        return p        

    def _refreshMedia(self,path):
        p = self._shellcmd('am broadcast -a android.intent.action.MEDIA_MOUNTED -d file://' + path)
        out = p.stdout.read().strip()
        if 'result=0' in out:
            return True
        else:
            return False

    def _getFileNumber(self,path):
        p = self._shellcmd('ls ' + path + ' | wc -l')
        out = p.stdout.read().strip()
        return string.atoi(out)


    def _launchActivity(self,component):
        p = self._shellcmd('am start -n ' + component)
        return p

    def _catFile(self,path):
        p = self._shellcmd('cat ' + path)
        out = p.stdout.read().strip()
        return out

    def _deleteFile(self,path):
        p = self._shellcmd('rm -r  ' + path)
        p.wait()
        number = self._getFileNumber(path)
        if number == 0 :
            return True
        else:
            return False

    def _pushpullFile(self,action,path,t_path):
        beforeNO = self._getFileNumber(t_path)
        p = self._t_cmd(action + ' ' + path + ' ' + t_path)
        p.wait()
        afterNO = self._getFileNumber(t_path)
        if afterNO > beforeNO:
            return True
        else:
            return False

    def _exportANDROID_SERIAL(self):
        #get device number
        device_number = self._getDeviceNumber()
        #export ANDROID_SERIAL=xxxxxxxx
        os.environ[ANDROID_SERIAL] = device_number

    def _getDeviceNumber(self):
        #get device number, only support 1 device now
        #show all devices
        cmd = ADB_DEVICES
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p.wait()
        out=p.stdout.read().strip()
        #out is 'List of devices attached /nRHBxxxxxxxx/t device'
        words_before = 'List of devices attached'
        word_after = 'device'
        #get device number through separate str(out)
        device_number = out[len(words_before):-len(word_after)].strip()
        if len(device_number) >= 15:
            raise Exception('more than 1 device connect,only suppport 1 device now')
        else:
            return device_number

    def _shellcmd(self,func):
        cmd = ADB_SHELL + ' ' + func
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    def _t_cmd(self,func):
        cmd = ADB + ' ' + func
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)


class SetMode():
    
    def switchcamera(self,mode):
        d(resourceId = MODE_LIST_BUTTON).click.wait()
        try:
            assert d(resourceId = 'com.intel.camera22:id/mode_wave_smile')
            self._touchmode(mode)
        except:
            d(resourceId = 'com.intel.camera22:id/mode_wave_photo').click()
            self._touchmode(mode)

    def _touchmode(self,mode):
        if mode == 'burstslow':
            d(resourceId = MODE_ID[mode]).click.wait()
            d(text = 'SLOW').click.wait()
        elif mode == 'burstfast':
            d(resourceId = MODE_ID[mode]).click.wait()
            d(text = 'FAST').click.wait()
        else:
            d(resourceId = MODE_ID[mode]).click.wait()


    def _setFlashMode(self,option):
        d(resourceId = 'com.intel.camera22:id/left_menus_flash_setting').click.wait()
        d(resourceId = 'com.intel.camera22:id/hori_list_button')[FLASH_SETTING.index(option)].click.wait()

    def _setFDFRMode(self,option):
        d(resourceId = 'com.intel.camera22:id/left_menus_face_tracking').click()
        FDFRStatus = commands.getoutput('adb shell cat /data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep pref_fdfr_key')
        if FDFRStatus.find(option) == -1:
            d(resourceId = 'com.intel.camera22:id/left_menus_face_tracking').click()
        else:
            pass

    def setCameraSetting(self,mode,sub_mode,option):
        '''
        This method is used to set camera to one mode, sub-mode, and do any operate of this sub-mode.
        7 = Max element count in screen.
        2 = Length of settings - Max screen count


        Please input index number as sub_mode, input index number of options as option
        Such as:
        setCameraSetting('single',3,2)
        'single' means mode
        3 means the index number of Location in sub_mode list
        2 means the index number of Location off option in options list
        '''
    
        settings = MODE[mode]
        if sub_mode== 'flash':
            self._setFlashMode(option)
        elif sub_mode == 'fdfr':
            self._setFDFRMode(option)
        else:
            d(resourceId = 'com.intel.camera22:id/left_menus_camera_setting').click.wait(timeout=2000)
            if sub_mode <= 7:
                d(resourceId = HORI_LIST_BUTTON)[sub_mode-1].click.wait()
                if len(settings) >= 7:
                    d(resourceId = HORI_LIST_BUTTON)[option+7-1].click.wait()
                else:
                    d(resourceId = HORI_LIST_BUTTON)[option+len(settings)-1].click.wait()
            else:
                d.swipe(680,180,100,180)
                d(resourceId = HORI_LIST_BUTTON)[sub_mode-2-1].click.wait()
                d(resourceId = HORI_LIST_BUTTON)[option+7-1].click.wait()

class TouchButton():

    def takePicture(self,status):
        # capture single image
        def _singlecapture():
            d(resourceId = CPTUREBUTTON_RESOURCEID).click.wait()
        # capture smile image
        def _smilecapture():
            d(resourceId = CPTUREBUTTON_RESOURCEID).click.wait()
            time.sleep(2)
            d(resourceId = CPTUREBUTTON_RESOURCEID).click.wait()
        # capture single image by press 2s
        def _longclickcapture():
            commands.getoutput(DRAWUP_CAPTUREBUTTON + '2000')
            time.sleep(2) 
        #Dictionary
        takemode={'single':_singlecapture,'smile':_smilecapture,'longclick':_longclickcapture}    
        takemode[status]()
     
    def takePictureCustomTime(self,status): 
        # capture image by press Custom Time
        commands.getoutput(DRAWUP_CAPTUREBUTTON+ (status+'000'))



    def takeVideo(self,status,capturetimes=0):
        # Start record video
        d(resourceId = CPTUREBUTTON_RESOURCEID).click.wait() 
        for i in range(0,capturetimes):
            #Tap on the center of the screen to capture image during taking video
            d(resourceId = 'com.intel.camera22:id/camera_preview').click.wait()
        # Set recording time, every capturing during record video takes about 3s
        time.sleep(status - capturetimes*3 -2)
        # Stop record video
        d(resourceId = CPTUREBUTTON_RESOURCEID).click.wait() 
        return True
        
    def switchBackOrFrontCamera(self,status):
        #Dictionary
        camerastatus = {'back': '0','front':'1'}  
        # Get the current camera status
        currentstatus = commands.getoutput(CAMERA_ID)
        # Confirm the current status of the user is required
        if currentstatus.find(camerastatus.get(status)) == -1:
            # draw down the menu
            commands.getoutput(DRAWDOWN_MENU)
            time.sleep(1)
            # set the camera status
            d(description = FRONTBACKBUTTON_DESCR).click.wait()
            time.sleep(3)
            # Get the current camera status
            currentstatus = commands.getoutput(CAMERA_ID)
            # check the result
            if currentstatus.find(camerastatus.get(status)) != -1:
                print ('set camera is '+status)
                return True
            else:
                print ('set camera is '+status+' fail')
                return False
        else:
            print('Current camera is ' + status)
