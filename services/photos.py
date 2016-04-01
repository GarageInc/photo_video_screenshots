# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 10:03:06 2016

@author: RinatF
"""

import os.path
import subprocess
import time

import config

def makePhoto( photoPath ):

    command = '/usr/bin/streamer -s 1920x1080 -f jpeg -o ' + photoPath

    subprocess.call( command, shell=True, stderr=subprocess.STDOUT)
    
def uploadPhoto( photoPath, configs ):
    
    command = ' /usr/bin/curl -i \
 -F cmd=terminals.upload_photo \
 -F id_terminal=' + configs['ID_TERMINAL'] + ' \
 -F name=file \
 -F file=@' + photoPath + ' ' + configs['GATEWAY_UPLOAD_URL']
    
    subprocess.call( command, shell=True, stderr=subprocess.STDOUT )

def reportPhotoNotChanged( configs ):
    command = ' /usr/bin/curl -i \
 -F cmd=terminals.photo_not_changed \
 -F id_terminal=' + configs['ID_TERMINAL'] + ' ' + configs['GATEWAY_API_URL']
 
    subprocess.call( command, shell=True, stderr=subprocess.STDOUT )
    
def run( configs ):

    if (configs['IS_PHOTO_ENABLED'].lower() == 'true'):
        photoPath = configs['PHOTO_PATH'];
    
        sizeOld = 0
    
        if ( os.path.isfile( photoPath ) ):
            sizeOld = os.path.getsize( photoPath )
            os.remove( photoPath )
    
        makePhoto( photoPath )
    
        if ( os.path.isfile( photoPath ) ):
            sizeNew = os.path.getsize( photoPath )     
            
            if ( sizeNew != sizeOld ):
                uploadPhoto( photoPath, configs )
            else:
                reportPhotoNotChanged( configs )
                
                    
###############################################################################    
                    
initFilePath = '/etc/osago/terminal'

configs = config.readConfigFile( initFilePath )

while True:
    start = time.time()  
    run( configs )
    finish = time.time()
    
    timeOut =  int( configs['PHOTO_TIMEOUT'] ) - (finish-start)
    if( timeOut > 0.1 ):
        time.sleep(timeOut)
