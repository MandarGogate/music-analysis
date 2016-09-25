from Tkinter import *
from math import *
import numpy as np
import sounddevice as sd

import Tkinter as tk
def evaluate(event):
    res.configure(text = "Hearing ON : " + str(eval(entry.get())))
    
    sd.default.samplerate = 44100

    time = 2.0
    frequency = eval(entry.get())
    frequency2 = eval(entry2.get())

    # Generate time of samples between 0 and two seconds
    samples = np.arange(44100 * time) / 44100.0
    # Recall that a sinusoidal wave of frequency f has formula w(t) = A*sin(2*pi*f*t)
    wave = 20000 * np.sin(2 * np.pi * frequency * samples)
    wave2 = 10000 * np.sin(2 * np.pi * frequency2 * samples)
    # Country
    
def evaluate2(event):
    res.configure(text = "Hearing ON : " + str(eval(entry2.get())))
    
    sd.default.samplerate = 44100

    time = 2.0
    frequency = eval(entry2.get())
    frequency2 = eval(entry.get())

    # Generate time of samples between 0 and two seconds
    samples = np.arange(44100 * time) / 44100.0
    # Recall that a sinusoidal wave of frequency f has formula w(t) = A*sin(2*pi*f*t)
    wave = 10000 * np.sin(2 * np.pi * frequency * samples)
    wave2 = 10000 * np.sin(2 * np.pi * frequency2 * samples)
    # Convert it to wav format (16 bits)
    wav_wave = np.array(wave, dtype=np.int16)
    wav_wave2 = np.array(wave2, dtype=np.int16)

    sd.play(wav_wave)
    sd.stop()
    sd.play(wav_wave2)
    
fields = 'Last Name', 'First Name', 'Job', 'Country'

def fetch(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()
      print('%s: "%s"' % (field, text)) 

def makeform(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries
   
def keyup(e):
    print '+', e.char
def keydown(e):
    print '-', e.char
       
    
w = Tk()
root = tk.Tk()
root.geometry("300x200")

def func(event):
    print("You hit return.")
root.bind('<Return>', func)

def onclick():
    print("You clicked the button")

button = tk.Button(root, text="click me", command=onclick)
button.pack()

Label(w, text="Your Expression:").pack()
entry = Entry(w)
entry.bind("<Return>", evaluate)
entry.pack()
res = Label(w)
res.pack()


Label(w, text="Your Expression:").pack()
entry2 = Entry(w)
entry2.bind("<Return>", evaluate2)
entry2.pack()
res2 = Label(w)
res2.pack()


w.mainloop()