
#constants imported on mainTrack.py
INITIAL_BUFFER_SIZE = 300        # quantity of in frames
TRASHOLD_CONTROLS = 40           # measure in pixels
SIZE_REFERENC_TO_INTENSITY = 40  # measure reference in pixels

#constants imported on forkUpSystem.py
# The output from tracker is:
# [intensityTurning # leftRight # intensityUpDown # upDown \n] here you can decide the tags separator
DELIMITER_TAGS = '#'                            #Char delimiter to separete tags reciveds from the mainTrack.py
PROCESS_TRACK_WAY = ["python3", "mainTrack.py"] #location of the mainTrack.py