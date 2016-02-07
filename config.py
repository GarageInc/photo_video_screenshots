# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 09:57:38 2016

@author: RinatF
"""

import os.path


'''
ID_TERMINAL

GATEWAY_UPLOAD_URL
GATEWAY_API_URL

IS_SCREENSHOT_ENABLED = true false
SCREENSHOT_PATH
SCREENSHOT_SAVING_TIMEOUT
SCREENSHOT_UPLOADING_TIMEOUT
SCREENSHOTS_SAVING_DIR = /etc/terminal/screenshots/

PHOTO_TIMEOUT
IS_PHOTO_ENABLED = true false
PHOTO_PATH

VIDEO_PATH
IS_VIDEO_ENABLED = true false

ORIGINAL_INPUT_DEVICE
PHOTO_INPUT_DEVICE
VIDEO_INPUT_DEVICE

VIDEO_RECORD_TIME = 3600
INPUT_WIDTH = 1280
INPUT_HEIGHT = 720

VIDEO_OUTPUT_WIDTH = 640
VIDEO_OUTPUT_HEIGHT = 320

'''


def isConfigLine( line ):
    return len( line ) > 0 and line[ 0 ] != '[' and line[ 0 ] != '#'
    
def readConfigFile( filePath ):
       
    config = dict()

    if( os.path.isfile ( filePath ) ):
        file = open(filePath)
        
        lines = file.readlines()

        for item in lines:

            line = str( item ).strip()
            
            if( isConfigLine( line ) ):
                params = line.split( '=' )
                                
                key = str( params[ 0 ] ).strip()
		
                value = str( params[ 1 ] ).strip()

                config.update( { key: value } )
        
        file.close()

    else:
        raise Exception('не удалось открыть файл: ' + filePath)
    
    return config;
