from __future__ import division
from psychopy import visual, core, event, sound
import egi.simple as egi
import random

connectToNetStation = 0 #change to 0 if you don't want to connect to NetStation; for testing purposes

if connectToNetStation == 1:
    ns = egi.Netstation() #create NetStation object
    ns.connect('10.10.10.42', 55513) #connect to NetStation
    ns.BeginSession()
    ns.sync()
    ns.StartRecording() #start NetStation recording

win = visual.Window((1024, 1024),  fullscr= 'False', screen = 0, color='black')    #screen = 1 for the second monitor, 0 for the main monitor
count = 0 #initializing
chessboard1 = visual.ImageStim(win, image='chessboard1.png',  flipHoriz=False)
chessboard2 = visual.ImageStim(win, image='chessboard2.png',  flipHoriz=False)

while count < 200:
    chessboard1.draw()
    win.flip()
    #count+=1
    core.wait(.45)  #change the value based on how fast this actually goes. We want ~200 trials to take 3 minutes (180000 milliseconds)
    chessboard2.draw()
    win.flip()
    count+=1
    core.wait(.45) #change the value based on how fast this actually goes
    
    if event.getKeys(['escape']): #adding in a graceful exit
            if connectToNetStation ==1:
                core.wait(.5) # gives the system time to add in the second flag
                ns.StopRecording()
                ns.EndSession()
                ns.disconnect()
            win.close()
            core.quit()