

import threading # Python Module to Run 2 task in parallel
import time # Python time module for sleep
import os # OS module to trigger any request from OS
from tkinter import * #Tkinter is used for GUI
from datetime import datetime # To get Current Date and Time
import systemcheck #To check if everything is fine in system

import speech_recognition # For speech recognition
import pyttsx3 # For Speaking the Detected Text

recogniser = speech_recognition.Recognizer() # Initialise Speech to Text Recognition 

mic_index = 0

list_of_punctuations = {'comma': ',', 'fullstop': '.', 'full stop': '.',
                        'new line': '\n', 'newline': '\n', 'colon': ':', "exclamation mark": '!', "semicolon": ';', 'question mark': '?', 'hyphen': '-', 'underscore': '_', 'hash': '#'}

fnt1 = ('Arial',12,'bold') #Font Sizes to show on GUI
fnt2 = ('Arial',20,'bold')

#Global Variables
btn1Anim = 0 #For controlling animation for Button 1
btn2Anim = 0 #For controlling animation for Button 2
rec = 0 # For controlling Recordings


lang = 'en-Us' #Variable to Hold Language value

def speakText(text): #A function to Speak the Given Text
    try:
        engine = pyttsx3.init() #Initialize Text to SPeech Module
        engine.setProperty('rate', 120)    # Speed percent (can go over 100)
        engine.setProperty('volume', 0.9)  # Volume 0-1
        engine.say("I Heard. "+text) # Speak the Text from Speaker
        engine.runAndWait() # Wait until Speech is finished
    except:
        pass

def stt(): # A function for recording Audio and Converting it to Text
    global btn1Anim, btn2Anim, rec, L2, lang 

    if(rec ==1): # If rec is 1
        print(speech_recognition.Microphone.list_working_microphones())
        L2.delete(0.0,END) # Clear the GUI TextBox
        L2.insert(0.0," "*5+"Calibrating Mic. Please Stay Silent for few Seconds") #show message on GUI TextBox
        print('Calibrating Microphone') #Print on Shell
        print('Please be silent for few seconds.') #Print on Shell
        time.sleep(1) # Wait for a second
        with speech_recognition.Microphone(device_index=mic_index) as source: #Initialize the Microphone
            recogniser.adjust_for_ambient_noise(source,duration=4) #Record Ambient Noise for 4 seconds
            L2.delete(0.0,END) # Clear the GUI Text Box
            if lang == 'en-Us': # If language is English
                L2.insert(0.0, " "*25+"             Speak Now in English") #show message on GUI TextBox
            else: # If language is Hindi
                L2.insert(0.0, " "*25+"             Speak Now in Hindi") #show message on GUI TextBox
            time.sleep(0.5) #small delay



        with speech_recognition.Microphone(device_index=mic_index) as source: # Renitialize the Microphone for recording Audio
            print("Say something!") # Print on shell
            try:
                audio = recogniser.listen(source,timeout = 10) # Record the audio, stop if no sound for 10 seconds
            except Exception as e: #Show if any error
                print("MIC ERROR : ",e)
                

        # recognize speech using Google Speech Recognition
        try:
            detected_text = recogniser.recognize_google(audio, language=lang) # Send the recorded audio for Voice to Text
            print('\n\n\n'+ detected_text) # Print the detected text
            for x in list_of_punctuations.keys(): #Check and replace symbols from detected text
                if x in detected_text:
                    detected_text = detected_text.replace(x, list_of_punctuations[x])           
            print('\n\n\n'+ detected_text) #Print updated text
            L2.delete(0.0,END)
            L2.insert(0.0, detected_text) # Show Detected text on GUI Text Box
            speakText(detected_text) # Call function to Speak the Detected text
            temp = str(datetime.now())[:-7] # Get current DateTime as String
            temp = temp.replace(" ", "_") #Replace all spaces with _ , as filename maynot support spaces
            temp = temp.replace(":", "_") #Replace all : with _ , as filename maynot support :
            file = open("VoiceToText_"+temp+".txt",'w') # Make and open a file
            file.write(detected_text) # Write the Detected Text in the File
            file.close() # Close the File
            print("Output Saved in storedText"+temp+".txt") #Print message on Shell

            if "open" in detected_text.lower(): # If open in detected text, means maybe some command came
                if "chrome" in detected_text.lower(): # If chrome word in Detected Text
                    os.system("start msedge") #Send command to OS for opening Chrome
                
                if "browser" in detected_text.lower(): # If chrome word in Detected Text
                    os.system("start msedge") #Send command to OS for opening Chrome
                
                if "edge" in detected_text.lower(): # If chrome word in Detected Text
                    os.system("start msedge") #Send command to OS for opening Chrome

                if "paint" in detected_text.lower(): # If Paint word in Detected Text
                    os.system("mspaint") #Send command to OS for opening Paint

                if "word" in detected_text.lower() and "pad" in detected_text.lower(): # If word pad word in Detected Text
                    os.system("start wordpad") #Send command to OS for opening Wordpad

                
            
            if "close" in detected_text.lower(): # If close in detected text, means maybe some command came
                if "chrome" in detected_text.lower() or "browser" in detected_text.lower() or "edge" in detected_text.lower(): # If chrome word in Detected Text
                    os.system("Taskkill /IM msedge.exe /f") #Send command to OS for closing Chrome

                if "paint" in detected_text.lower(): # If Paint word in Detected Text
                    os.system("Taskkill /IM mspaint.exe /f") #Send command to OS for closing Paint

                if "word" in detected_text.lower() and "pad" in detected_text.lower(): # If word pad word in Detected Text
                    os.system("Taskkill /IM wordpad.exe /f") #Send command to OS for closing Wordpad
                  
        except speech_recognition.UnknownValueError: # If Voice is not Clear Error
            print("Google Speech Recognition could not understand audio")
            L2.delete(0.0,END)
            L2.insert(0.0," Speech Recognition could not understand audio. Please Speak Clearly Again")
        except speech_recognition.RequestError as e:  # If Internet issue error
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            L2.delete(0.0,END)
            L2.insert(0.0,"Could not request results from Google Speech Recognition service. Please Check for Internet Connection ")

        time.sleep(2)
        print('\n\n')
        btn1Anim, btn2Anim, rec = 0,0,0 # Stop animation and recording
        
        
root = Tk() # Start GUI window
root.title("Advance Speech to Text") #Set Title of Window
root.geometry("500x500+400+10") #Set Size of the Window

N = 3 #change N value to exact number of frames your gif contains for full  play
frames = [PhotoImage(file='micrec.gif',format = 'gif -index  %i' %(i)) for i in range(N)] # Load the Gif Image

def update(ind): # Function to run Gif Image
    global btn1Anim, btn2Anim
    if(btn1Anim==1): # Start Animation for Button 1
            ind = ind%N
            frame = frames[ind] # Load the Image
            ind += 1
            B1.config(image=frame) # Show Gif Image on Button 
    
    elif btn2Anim == 1: # Start Animation for Button 2
        ind = ind%N
        frame = frames[ind] # Load the Image
        ind += 1
        B2.config(image=frame) # Show Gif Image on Button 

    root.after(100, update, ind) # Update animation Image
        

def multiThreading(): # Multithreading function to run Voice to Text parallely
    while True:
        stt()
        

t1 = threading.Thread(target = multiThreading)
t1.start() # Start Multithreading FUnctionto run Voice to Text parallely

def start1(): # Function to call when Button 1 Clicked
    global btn1Anim, rec, lang
    if rec == 0:
        btn1Anim = 1 # Start Animation for Button 1
        rec = 1 # Start Recording
        lang = 'en-Us' # Language as English

def start2():  # Function to call when Button 2 Clicked
    global btn2Anim, rec, lang
    if rec == 0:
        btn2Anim = 1 # Start Animation for Button 2
        rec = 1 # Start Recording
        lang = 'hi-In' # Language as Hindi
        
def stop(): # If stopped BUtton is Pressed
    global btn1Anim, btn2Anim, rec, lang, L2
    
    btn1Anim, btn2Anim, rec = 0, 0, 0 # Stop all animation and recording
    L2.delete(0.0,END) # Clear the GUI Text Box
    

win = Frame(root, bg ='powderblue') # Set Background color

L1 = Label(win,text="ADVANCE SPEECH TO TEXT") #A Label on Top
L1.config(font = fnt2,bg ='powderblue')
L1.place(x=25,y=10,height = 30,width = 450)

L2 = Text(win) # GUI Text Box to Show Messages
L2.config(font = fnt1)
L2.place(x=25,y=50,height = 200,width = 450)

B1 = Button(win) # Button 1 for English Recording
photo = PhotoImage(file = "micrec.gif")
B1.config(image=photo,relief = RAISED, command = start1)
B1.config(bg='red')
B1.place(x = 80, y = 260, height = 150, width = 150)

B2 = Button(win) # Button 2 for Hindi Recording
photo1 = PhotoImage(file = "micrec.gif")
B2.config(image=photo1,relief = RAISED, command = start2)
B2.config(bg='red')
B2.place(x = 280, y = 260, height = 150, width = 150)

L3 = Label(win,text="ENGLISH") # Write ENGLISH below Button 1
L3.config(font = fnt2,bg ='powderblue')
L3.place(x=90,y=430,height = 30,width = 150)

L4 = Label(win,text="HINDI") # Write HINDI below Button 2
L4.config(font = fnt2,bg ='powderblue')
L4.place(x=280,y=430,height = 30,width = 150)

B3 = Button(win) # Button 1 for Stopping Recording
B3.config(text = "STOP", relief = RAISED, command = stop)
B3.config(bg='green')
B3.place(x = 220, y = 470, height = 25, width = 70)


win.place(x=0,y=0,height = 500,width = 500)
root.after(0, update, 0)
mainloop()

