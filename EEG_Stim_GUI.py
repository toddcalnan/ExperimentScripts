from __future__ import division
from psychopy import visual, core, event, sound, gui
import egi.simple as egi
import random

connectToNetStation = 0 #change to 0 if you don't want to connect to NetStation; for testing purposes

if connectToNetStation == 1:
    ns = egi.Netstation() #create NetStation object
    ns.connect('10.10.10.42', 55513) #connect to NetStation
    ns.BeginSession()
    ns.sync()
    ns.StartRecording() #start NetStation recording

win = visual.Window((1920, 1080), screen = 0, color='black')    #screen = 1 for the second monitor, 0 for the main monitor
key = ['0'] #initializing the user input list

movieList = ['[]', 'aToys2008B.mov', 'bSocial2008B.mov', 'cBubblesSized602.mov'] #file names of the three movies, empty brackets are to keep numbers the same as Matlab

while key[0] != 9:
    myDlg = gui.Dlg(title = 'Movie Picker')
    myDlg.addText(' 1 = Toys \n 2 = Social \n 3 = Bubbles \n 9 = Quit')
    myDlg.addField('Video to Play:')
    key = str(myDlg.show() ) # show dialog and wait for OK or Cancel
    if myDlg.OK:  # or if ok_data is not None
        key = key[3]
        print(key)
    else:
        print('user cancelled')
        key = '9'

    if key[0] == '1' or key[0] == 'num_1':
        stimToPlay = 1
        flag = 'Toys'
    if key[0] == '2' or key[0] == 'num_2':
        stimToPlay = 2
        flag = 'Socl'
    if key[0] == '3' or key[0] == 'num_3':
        stimToPlay = 3
        flag = 'Bubl'
    if key[0] == '9' or key[0] == 'num_9':
        stimToPlay = 9

    if stimToPlay == 9:
        if connectToNetStation ==1:
            ns.StopRecording()
            ns.EndSession()
            ns.disconnect()
        win.close()
        core.quit()

    eventNameStart = flag + 'Start'
    eventNameEnd = flag + 'End'

    mov = visual.MovieStim3(win, movieList[stimToPlay], size=(1920, 1080),
        flipVert=False, flipHoriz=False, loop=False)
    globalClock = core.Clock
    if connectToNetStation == 1:
        ns.send_event(flag, label=eventNameStart, timestamp=egi.ms_localtime()) #send the event flag to NetStation

    while mov.status != visual.FINISHED: #while the video is still playing
        mov.draw() #draw the next frame of the video
        win.flip() #show the next frame of the video
 
        if event.getKeys(['escape']): #adding in a graceful exit
            if connectToNetStation ==1:
                ns.send_event('evt_', label=eventNameEnd, timestamp=egi.ms_localtime())  # add in second event flag to denote end of segment
                core.wait(.5) # gives the system time to add in the second flag
                ns.StopRecording()
                ns.EndSession()
                ns.disconnect()
            win.close()
            core.quit()
            
    if mov.status == visual.FINISHED and connectToNetStation == 1:
        ns.send_event('evt_', label=eventNameEnd, timestamp=egi.ms_localtime())  # add in second event flag to denote end of segment