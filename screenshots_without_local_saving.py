# -*- coding: utf-8 -*-

import os.path
import subprocess
import time

import config


def makeScreenShot( screenShotPath ):
    command = 'DISPLAY=:0 /usr/bin/scrot -q 80 '+screenShotPath+' && /usr/bin/convert -crop 1920x1080+0+0 ' + screenShotPath + ' ' + screenShotPath

    subprocess.call( command, shell=True, stderr=subprocess.STDOUT )
    
def uploadScreenshot( screenShotPath, configs ):
    command = ' /usr/bin/curl -i \
 -F cmd=terminals.upload_screenshot \
 -F id_terminal=' + configs['ID_TERMINAL'] + ' \
 -F name=file \
 -F file=@' + screenShotPath + ' ' + configs['GATEWAY_UPLOAD_URL']
    
    subprocess.call( command, shell=True, stderr=subprocess.STDOUT )

def reportScreenshotNotChanged( configs ):
    command = ' /usr/bin/curl -i \
 -F cmd=terminals.screenshot_not_changed \
 -F id_terminal=' + configs['ID_TERMINAL'] + ' ' + configs['GATEWAY_API_URL']
 
    subprocess.call( command, shell=True, stderr=subprocess.STDOUT )
      
def run( configs ):
    screenShotPath = configs['SCREENSHOT_PATH'];
    
    sizeOld = 0
    
    if ( os.path.isfile( screenShotPath ) ):
        sizeOld = os.path.getsize( screenShotPath )
        os.remove( screenShotPath )
    
    makeScreenShot( screenShotPath )
    
    if ( os.path.isfile( screenShotPath ) ):
        sizeNew = os.path.getsize( screenShotPath )     
            
        if ( sizeNew != sizeOld ):
            uploadScreenshot( screenShotPath, configs )
        else:
            reportScreenshotNotChanged( configs )           

def runScreenshotsLoop( configs ):
    if (configs['IS_SCREENSHOT_ENABLED'].lower() == 'true'):
        while True:
            start = time.time()  
            run( configs )
            finish = time.time()
            
            timeOut =  int( configs['SCREENSHOT_TIMEOUT'] ) - (finish-start)
            
            if( timeOut > 0.1 ):
                time.sleep(timeOut)
###############################################################################    
         
initFilePath = '/etc/terminal/osago.ini'

configs = config.readConfigFile( initFilePath )

runScreenshotsLoop( configs )
    
    
    
    
    

