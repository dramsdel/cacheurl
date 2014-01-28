#!/usr/bin/python
#from termcolor import colored
from multiprocessing import Pool
import urllib, urllib2, cookielib, os, sys, time, signal
            
def accessURL(url):
    "Downloads a URL, prints time it took"
    urlTime = time.time()
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        htmlData = response.read()
    except urllib2.HTTPError, error:
        sys.stdout.write(":: Caught a 500 error while fetching the url: " + url + '\n')
        return 1
    except urllib2.URLError, error:
        sys.stdout.write(":: Caught a connection error while fetching the url: " + url + '\n')
        return 1
    except IOError, error:
        sys.stdout.write(":: Caught a IOError error while fetching the url: " + url + '\n')
        return 1
    sys.stdout.write(":: URL: " + url.rstrip() + " took " + str(time.time() - urlTime) + " seconds" + '\n')
    return 0

def signal_handler(signal, frame):
    sys.stdout.write(":: Received kill signal" + '\n')
    os.system('killall ' + os.path.basename(__file__))

def main ():
    if len(sys.argv) < 3:
        print '''
cachesite.py - grabs a site via a url list to cache pages on that server

  Usage cachesite.py -t threads urllist
'''
        sys.exit(0)
    else:
        if sys.argv[1] == "-t":
            threads = int(sys.argv[2])
            filename = sys.argv[3]
        else:
            print "Invalid Argument"
            sys.exit(1)
    try:
        urlList = open(filename, "r")
    except:
        print ":: Cannot access url list file"
        sys.exit(1)

    startTime = time.time()
    sys.stdout.write(":: Starting URL caching process")

    signal.signal(signal.SIGINT, signal_handler)

    pool = Pool(processes=threads)
    pool.apply_async(accessURL, ["http://www.google.com"])

    # Read file into an array
    urlArray = []
    for line in urlList:
        urlArray.append(line)
    pool.map(accessURL, urlArray)
    sys.stdout.write(":: Process took "+str((time.time() - startTime) / 60 )+" minutes")
    exit(0)

if __name__ == '__main__':

    try:
        main()
    except Exception, e:
        print str(e)
        os._exit(1)
