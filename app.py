import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import cv2

import VideoIndexer
import VideoRetriever

DB_FILE = "lcLihsJnwlIt.json"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Search Engine")

        self.video_widgets = []

        if not os.path.exists(DB_FILE):
            self.show_init_screen()
        else:
            self.show_search_screen()

    def show_init_screen(self):
        self.clear()

        tk.Label(self.root, text="No video database found. Initialize:").pack()
        tk.Button(self.root, text="Choose Video Folder", command=self.init_db).pack()

    def init_db(self):
        folder = filedialog.askdirectory()
        if folder:
            VideoIndexer.createDB(folder)
            messagebox.showinfo("Done", "Video DB created!")
            self.show_search_screen()

    def show_search_screen(self):
        self.clear()

        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack()

        tk.Button(self.root, text="Search", command=self.do_search).pack()
        tk.Button(self.root, text="Rebuild DB", command=self.show_init_screen).pack()

        self.frame = tk.Frame(self.root)
        self.frame.pack()

    def do_search(self):
        query = self.entry.get()

        video_paths = VideoRetriever.search(query, DB_FILE, top=1)

        for w in self.video_widgets:
            w["frame"].destroy()
        self.video_widgets.clear()

        for path in video_paths:
            container = tk.Frame(self.frame)
            container.pack(side="left", padx=10)

            tk.Label(container, text=path, wraplength=200).pack()

            video_label = tk.Label(container)
            video_label.pack()

            cap = cv2.VideoCapture(path)

            widget = {
                "frame": container,
                "label": video_label,
                "cap": cap
            }

            self.video_widgets.append(widget)

            self.play_video(widget)

    def play_video(self, widget):
        cap = widget["cap"]
        label = widget["label"]

        ret, frame = cap.read()

        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = img.resize((200, 150))

            tk_img = ImageTk.PhotoImage(img)

            label.config(image=tk_img)
            label.image = tk_img

        self.root.after(30, lambda: self.play_video(widget))

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
