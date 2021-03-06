#! /usr/bin/env python

from subprocess import call, PIPE
from os import *
from shutil import *
from threading import Thread
import sys
import time

port = 5556
# FIXME: This must be the hostname and port of resin server.
metaserver = "http://localhost:8080/freecivmetaserve/metaserver.php"
logdir = "/tmp/"
savesdir = "~/freeciv-build/resin/webapps/ROOT/savegames/"
pubscript = "pubscript_single.serv"
servers_count = 80


class civserverproc(Thread):

    def __init__ (self, port):
        Thread.__init__(self)
        self.port = port

    def run(self):
        while 1:
            try:
                retcode = call("freeciv-web --port " + str(self.port) + " -q 20 -e "
                       + " -m -M " + metaserver  + " --type \"Singleplayer\" --read " + pubscript +  " --log " + logdir + "fcweb-" + str(self.port) + ".log --saves " + savesdir, shell=True)
                if retcode < 0:
                    print >>sys.stderr, "Freeciv-web was terminated by signal", -retcode
                else:
                    print >>sys.stderr, "Freeciv-web returned", retcode
            except OSError, e:
                print >>sys.stderr, "Execution failed:", e

            time.sleep(10)

def create_directory(d):
    if path.exists(d):
        rmtree(d)
        makedirs(d)
    else:
        makedirs(d)

for i in range(servers_count):
    current = civserverproc(port)
    port += 1
    current.start()


print("Freeciv-webs done!")
