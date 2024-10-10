import tkinter as tk
from tkinter import filedialog
import osurender

# Class defining the main window's details and parameters
class circleStudio(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initializes empty strings for replay and beatmap file names
        self.replayFile = ''
        self.beatmapFile = ''

        # Sets window title
        self.title("osu! Replay Analyzer Indev")
        #self.geometry("450x50")

        # Text Labels
        self.label = tk.Label(self, text="Choose osu")
        self.label.grid(row="0",column="0")

        # Buttons
        self.button1 = tk.Button(self, text="Select Replay File", command=self.onReplayClick)
        self.button2 = tk.Button(self, text="Select Beatmap FIle", command=self.onBeatmapClick)
        self.button3 = tk.Button(self, text="View Replay", command=self.onViewClick)

        self.label1 = tk.Label(self, text="No Replay Selected!")
        self.label2 = tk.Label(self, text = "No Beatmap Selected!")

        self.button1.grid(row="1",column="0")
        self.button2.grid(row="2",column="0")
        self.button3.grid(row="3",column="0")

        self.label1.grid(row="1",column="1")
        self.label2.grid(row="2",column="1")

    # When select replay button is clicked, opens file dialog to allow user to choose a .osr file
    def onReplayClick(self):
        self.replayFile = filedialog.askopenfilename()
        self.label1.config(text=self.replayFile)
    
    # When select beatmap button is clicked, opens file dialog to allow user to choose a .osu file
    def onBeatmapClick(self):
        self.beatmapFile = filedialog.askopenfilename()
        self.label2.config(text=self.beatmapFile)

    # When the view replay button is clicked, calls upon osurender.display to open a pygame window and render the replay
    def onViewClick(self):
        osurender.display(self.replayFile,self.beatmapFile)

# If the file is main.py, begin the program    
if __name__ == "__main__":
    app = circleStudio()
    app.mainloop()