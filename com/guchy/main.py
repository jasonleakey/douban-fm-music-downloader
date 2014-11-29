__author__ = 'jasonhuang'

import urllib.request as ur
import json, os, sys
import socket
import logging

def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stdout.write(s)
        if readsofar >= totalsize: # near the end
            sys.stdout.write("\n")
    else: # total size is unknown
        sys.stdout.write("read %d\n" % (readsofar,))

os.chdir(sys.path[0])
t = r'http://douban.fm/j/mine/playlist?from=mainsite&type=n&channel='
CHANNEL_CHINESE = 1
CHANNEL_ENGLISH = 2
CHANNEL_70 = 3
CHANNEL_80 = 4
CHANNEL_90 = 5
logging.basicConfig(filename="main.log", level=logging.DEBUG)


# set network timeout as 30 secs.
# download a file should not take that long.
socket.setdefaulttimeout(30)
for i in [ CHANNEL_CHINESE, CHANNEL_ENGLISH, CHANNEL_70, CHANNEL_80, CHANNEL_90 ]:
    url = t + str(i)
    logging.debug("\n")
    logging.debug(url)
    a = ur.urlopen(url).read().decode().replace('\\', '')
    a = json.loads(a)
    for i in a['song']:
        audio_url = i['url']
        extension = audio_url[audio_url.rfind("."):]
        filename = i['artist'] + '-' + i['title'] + extension
        filename = filename.replace('/', '-')
        logging.debug('Downloading:')
        logging.debug('Artist: ' + i['artist'])
        logging.debug('Song: ' + i['title'])
        logging.debug('URL: ' + i['url'])
        logging.debug("File:" + filename)
        try:
            if os.path.exists(filename):
                logging.warning('File exists')
                pass
            ur.urlretrieve(i['url'], filename, reporthook=reporthook)
            logging.info("done")
            if os.path.getsize(filename) < 300:
                os.system('del ' + filename)
        except Exception as a:
            logging.error(a)
            logging.info("fail")
            pass

