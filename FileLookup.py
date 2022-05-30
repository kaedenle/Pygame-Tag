#file gets path (excluding C:/Users) from current directory
#only works if needed file is in current directory of this file or is in a sub directory of current directory
import os
def find(name):
    #get name of dir of current file
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    for roots, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
        name_dir = roots
        for file in files:
            if(file == name):
                roots = roots.replace(ROOT_DIR, "")
                ret = roots[1:]
                return (ret + "/" + file) if len(ret) != 0 else file
    return ""


            
            
        
