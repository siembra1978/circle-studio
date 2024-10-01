import tkinter as tk
from tkinter import filedialog
import osurender

class circleStudio(tk.Tk):
    def __init__(self):
        super().__init__()

        self.replayFile = ''
        self.beatmapFile = ''

        self.title("osu! Replay Analyzer Indev")
        #self.geometry("450x50")

        self.label = tk.Label(self, text="Choose osu")
        self.label.grid(row="0",column="0")

        #self.list = tk.Listbox(self, height=10, width=50)
        #self.list.pack(pady=20)

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

    def onReplayClick(self):
        self.replayFile = filedialog.askopenfilename()
        self.label1.config(text=self.replayFile)
        
    def onBeatmapClick(self):
        self.beatmapFile = filedialog.askopenfilename()
        self.label2.config(text=self.beatmapFile)

    def onViewClick(self):
        osurender.display(self.replayFile,self.beatmapFile)
	    
if __name__ == "__main__":
    app = circleStudio()
    app.mainloop()