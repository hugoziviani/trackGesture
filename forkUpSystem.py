from generalConfig import *
import subprocess
import sys

cmd = PROCESS_TRACK_WAY

p = subprocess.Popen(cmd, -1, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # -1 is the buffer size

while True:
    nextline = p.stdout.readline()
    decodedLine = nextline.decode('utf-8')

    if decodedLine == '' or p.poll() is not None:
        print("Tracker is turning off...")
        break

    if (decodedLine.find(DELIMITER_TAGS)):
        print(decodedLine.split(DELIMITER_TAGS))

    else:
        print(decodedLine)

    # sys.stdout.write(decodedLine) # if this part is up from other process
    sys.stdout.flush()
