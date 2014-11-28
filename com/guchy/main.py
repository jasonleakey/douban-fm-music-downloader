__author__ = 'jasonhuang'

import urllib.request as ur
import json, os, sys

os.chdir(sys.path[0])

t = r'http://douban.fm/j/mine/playlist?type=n&channel='

for i in range(24):
    url = t + str(i)
    print(url)
    a = ur.urlopen(url).read().decode().replace('\\', '')
    a = json.loads(a)
    for i in a['song']:
        filename = i['artist'] + '-' + i['title'] + '.mp3'
        filename = filename.replace('/', '-')
        print('Downloading:', 'Artist: ' + i['artist'], 'Song: ' + i['albumtitle'], 'URL: ' + i['url'],
              sep='\n', end = '\n\n')
        try:
            if os.path.exists(filename):
                print('Existing')
                break
            ur.urlretrieve(i['url'], filename)
            if os.path.getsize(filename) < 300:
                os.system('del ' + filename)
        except Exception as a:
            print (a)
            pass