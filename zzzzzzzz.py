#!/usr/bin/env python
import os
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if __name__ == '__main__':
    zipf = zipfile.ZipFile('D:\PIP\Dropbox\XBMC_Apps\kodi\plugin.gxx.film\plugin.gxx.film-.zip', 'w')
    zipdir('plugin.gxx.film', zipf)
    zipf.close()
    
    
    zipf = zipfile.ZipFile('D:\PIP\Dropbox\XBMC_Apps\kodi\repository.gxx\repository.gxx-.zip', 'w')
    zipdir('repository.gxx', zipf)
    zipf.close()

    zipf = zipfile.ZipFile('D:\PIP\Dropbox\XBMC_Apps\kodi\plugin.gxx.music\plugin.gxx.music-.zip', 'w')
    zipdir('plugin.gxx.music', zipf)
    zipf.close()    