# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 09:57:38 2016

@author: RinatF
"""

import os.path

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

    else:
        raise Exception('не удалось открыть файл: ' + filePath)
    
    return config;
