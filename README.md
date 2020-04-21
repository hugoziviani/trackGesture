# Project Description
Here you have got two projects with a similar foundaments. Capture track of any region and capture track to control a robot simulation.

# trackGesture
This is a simple trackGesture using opencv and python3.
It is composed by two Classes TrackAndTransformFrames.py	and VideoCaptureClass.py which are called from mainTrack.py.

1-To run this simple project you need to install the requirements.txt.

2-python3 mainTrack.py.

OBS: Is optional make a virtual environment to install the requirements.txt and after all run the project.


# trackGesture + RoboComp
Inside the project there is a folder called /pycomp, if you want to run the hand tracker you must have installed the RoboComp framework. Below is it discribed:

1-Install the RoboComp framework available in: https://github.com/robocomp/robocomp

2-After installed RoboComp correctly, fell free to also download the examples avaliables on theyr installation page.

3-Start the Robocomp simple world simulation with:
        $ rcis ~/robocomp/files/innermodel/simpleworld.xml
        # the simulation simple world will be start and show two windows with different vision.

4-go insde the folder of /pycomp component downloaded from this project and run the command above to start tracking:
        $ python3  src/imageController.py --Ice.Config=etc/config
        # will open the image from your default webcam(camera installed on your computer) to you chose the region to control the robot.

5- To exit from the image controller, on the frames capture, you must to press the key 'q' on your keyboard.

link to video example: https://youtu.be/Iyi8i6xSaEU using RoboComp

Fill free to use this code and any doubts please contact me. Thanks for your attention.
