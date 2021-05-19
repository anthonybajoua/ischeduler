#!/usr/bin/env python
import os
import tkinter as tk
import datetime
from threading import Timer
from csv import reader

global textbox
global timers


def sendCallback():
	try:
	    msg = e1.get("1.0", tk.END)
	    comp = e2.get()
	    time = e3.get().split(":")

	    e1.delete("1.0", tk.END)
	    e2.delete(0, tk.END)
	    e3.delete(0, tk.END)

	    delta = datetime.timedelta(hours=int(time[0])) + datetime.timedelta(minutes=int(time[1]))

	    laterDate = (datetime.datetime.now() + delta).strftime("%m/%d/%Y, %H:%M:%S")
	    secondsLater = delta.seconds
	    
	    textbox.config(state="normal")
	    textbox.insert(tk.END, f"Sending {msg} to {comp} at {laterDate}\n")
	    textbox.config(state=tk.DISABLED)

	    timer = Timer(secondsLater, send, args=[msg, comp])
	    timer.start()
	    timers.append(timer)
	except:
		print("Unexpected error")


def sendFile():
	filename = e4.get()
	e4.delete(0, tk.END)
	try:
		if filename[-4:] == ".csv":
			with open(filename, 'r') as read_obj:
				csv_reader = reader(read_obj)

				next(csv_reader)

				for row in csv_reader:
					if len(row) == 3:
						msg, name, time = row[0], row[1], row[2]

						time = time.split(":")


						delta = datetime.timedelta(hours=int(time[0])) + datetime.timedelta(minutes=int(time[1]))
						laterDate = (datetime.datetime.now() + delta).strftime("%m/%d/%Y, %H:%M:%S")
						secondsLater = delta.seconds

						textbox.config(state="normal")
						textbox.insert(tk.END, f"Sending {msg} to {name} at {laterDate}\n")
						textbox.config(state=tk.DISABLED)
						
						print(secondsLater, msg, name)
						timer = Timer(secondsLater, send, args=[msg, name])
						timer.start()
						timers.append(timer)
	except:
		print("Unexpected error")


def send(msg, usr):
    cmd=f"osascript -e \"tell application \\\"Messages\\\" to send \\\"{msg}\\\" to buddy \\\"{usr}\\\"\""
    os.popen(cmd)

def on_closing():
    for t in timers:
        t.cancel()
    root.destroy()


if __name__ == "__main__":
    try:
        timers = []

        root = tk.Tk()
        root.title("iScheduler")

        tk.Grid.rowconfigure(root,0,weight=1)        
        tk.Grid.rowconfigure(root,2,weight=0)
        tk.Grid.rowconfigure(root,3,weight=0)
        tk.Grid.rowconfigure(root,4,weight=4)


        tk.Grid.columnconfigure(root,0,weight=1)        
        tk.Grid.columnconfigure(root,1,weight=1)


        tk.Label(root, text="Message").grid(row=0,column=0)
        tk.Label(root, text="Contact Name (exact match)").grid(row=1, column=0)
        tk.Label(root, text="Delay format: hours:minutes").grid(row=2,column=0)
        tk.Label(root, text="Filename (optional), leave all other fields blank if using this. \nSupports .csv or .xslx with schema {msg}, {contactName}, {delay}").grid(row=3,column=0)


        e1 = tk.Text(root, height=5, width=30)
        e2 = tk.Entry(root)
        e3 = tk.Entry(root)
        e4 = tk.Entry(root)


        e1.grid(row=0,column=1,sticky="NSEW")
        e2.grid(row=1,column=1,sticky="EW")
        e3.grid(row=2,column=1,sticky="EW")
        e4.grid(row=3,column=1,sticky="EW")


        sendButton = tk.Button(root, text ="Send", command = sendCallback)
        sendButton.grid(row=4,column=1)

        fileButton = tk.Button(root, text ="Send (file)", command = sendFile)
        fileButton.grid(row=4,column=2)

        textbox = tk.Text(root, height=5, width=50)
        textbox.grid(row=4,column=0, sticky="nsew")
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
    
    except KeyboardInterrupt as e:
        for t in timers:
            t.cancel()