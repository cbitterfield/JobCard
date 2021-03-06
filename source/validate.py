'''
Created on 7:07:52 PM

@author: colin
'''

#===============================================================================
# Import 
#===============================================================================

import os
from string import Template
import logging
logger = logging.getLogger(__name__)

#===============================================================================
# Setup Commnands for Produce and Exists
#===============================================================================

CMD_PRODUCE = ''

CMD_EXISTS = ''

#===============================================================================
# Module Global Variables
#===============================================================================

MESSAGE = ''
ERROR = ''
NEWLINE = '\n'
Error = False



def main (source, output, component, jobcard, config, noexec):
    #===============================================================================
    # Module Global Variables
    #===============================================================================
    
    CURL=config['locations']['curl']
    CONVERT=config['locations']['convert']
    FFMPEG=config['locations']['ffmpeg']
    FFPROBE=config['locations']['ffprobe']
    MOGRIFY=config['locations']['mogrify']
    FONT=config['boxcover']['font']
    
    logger.debug("CURL = " + CURL)
    logger.debug("CONVERT = " + CONVERT)
    logger.debug("FFMPEG = " + FFMPEG)
    logger.debug("FFPROBE = " + FFPROBE)
    logger.debug("MOGRIFY = " + MOGRIFY)
    logger.debug("FONT = " + FONT)
    
    logger.info("Produce - Module Main - Start")
    # Start Code here
    
    
    logger.info("Produce - Module Main - Start")
    
    return(Error)

def produce(source, output, component, jobcard, config, noexec):
    Error = False
    logger.info("Produce - Start")
    logger.info("Validate Volumes from Configuration")
    
    for volume in config['default']: 
        if os.path.isdir(config['default'][volume]):
            logger.info('\t' + volume + " : " + str(config['default'][volume]) + " -- exists")
        else:
            logger.error('\t' + volume + " : " + str(config['default'][volume]) + " -- does not exist: FAIL")
            Error = True
     
    
    logger.info("Validate programs are installed and have valid pathnames from Configuration")
    
    for program in config['locations']:
        if os.path.isfile(config['locations'][program]):
            logger.info( '\t' + program +" : " + str(config['locations'][program]) + " -- exists")
        else:
            logger.error('\t' + program +" : " + str(config['locations'][program]) + " -- does not exist: FAIL")
            Error = True
    
    for key in config:
        for item in config[key]:
            if item.endswith('font'):
                if os.path.isfile(config[key][item]):
                    logger.info("Test if font exists:" + str(item) + ":Valid")
                else:
                    Error = True    
                    logger.error("Test if font exists:" + str(item) + ":Missing")
    
    
    for component in jobcard['component']:
    
        if jobcard['component'][component] == 'produce':
            logger.info(str(component) + " will be produced")
            for value in jobcard[component]:
                logger.info('\t' + value + ":" + str(jobcard[component][value]))
                if value == 'src': 
                    logger.info("Test Source file or directory")
                    test_desc = str(jobcard[component][value])
                    #Determine Absolute or Relative Path/File Descriptor               
                    
                    if test_desc[0] != "/":                       
                        logger.info("\tsource is realtive to Source")    
                        file_desc = str(config['default']['source']) + "/" +  str(jobcard[component][value])
                    else:
                        logger.debug("\tsource is an absolute path")
                        file_desc = str(jobcard[component][value])
                    
                    logger.info("\tFILE_DESC = " + file_desc) 
                            
                    if os.path.exists(file_desc):
                        logger.info('\t\texists[' + file_desc + "]")
                        if os.path.isdir(file_desc):
                            logger.info('\t\is directory[' + file_desc + "]")
                        elif os.path.isfile(file_desc):
                            logger.info('\t\tis file[' + file_desc + "]")    
                    else:
                        logger.error('\t\tfailed[' + file_desc + "]")   
                        Error = True 
        
        
        elif jobcard['component'][component] == 'exists':
            logger.info(str(component) + " will be copied from existing files")
            for value in jobcard[component]:
                logger.info('\t' + value + ":" + str(jobcard[component][value]))
                if value == 'src': 
                    test_desc = str(jobcard[component][value])
                    #Determine Absolute or Relative Path/File Descriptor               
                    
                    if test_desc[0] != "/":                       
                        logger.debug("Relative Path")    
                        file_desc = str(config['default']['finish']) + "/" +  str(jobcard[component][value])
                    else:
                        logger.debug("Absolute Path")
                        file_desc = str(jobcard[component][value])
                    
                    logger.debug("\tFILE_DESC = " + file_desc) 
                            
                    if os.path.exists( file_desc ):
                        logger.info('\t\texists[' + file_desc + "]")
                        if os.path.isdir(file_desc):
                            logger.info('\t\tis directory[' + file_desc + "]")
                        elif os.path.isfile(file_desc):
                            logger.info('\t\tis file[' + file_desc + "]")    
                    else:
                        logger.error('\t\tfailed[' + file_desc + "]")   
                        Error = True 
        else:        
            logger.info(str(component) +" is ignored")
     
             
    # Validate all products
    for product in jobcard['product']:
        logger.info("Validate " + product)
        
        if jobcard['product'][product] == 'produce':
            logger.info(product + " will be produced")
        
            for component in jobcard[product]:
                
                if component == 'out_dir':
                    logger.info("Scratch work will be written to\n")
                    logger.info("\t: " + config['default']['scratch'])
                    logger.info("\t: out_dir:" + str(jobcard[product][component]))
                else:
                    logger.info("including component " + str(component))
                    
        elif jobcard['product'][product] == 'exists':   
            logger.info(product + " will be copied from existing files")
             
             
        else:
            logger.info(product +" is ignored")     
    
    logger.info("Produce - End")
    return(Error)


def exists(source, output, component, jobcard, config, noexec):
    logger.info("Produce - Start")
    
    
    
    logger.info("Produce - End")
    return(Error)



def ignore(source, output, component, jobcard, config, noexec):
    logger.info("Produce - Start")
    
    
    
    logger.info("Produce - End")
    return(Error)