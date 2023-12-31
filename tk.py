import tkinter as tk
import cv2
from PIL import Image, ImageTk
import win32gui

class VideoWallpaperApp:
    def __init__(self, video_path, play_audio=True):
        self.root = tk.Tk()
        self.root.geometry("+0+0")  # 使窗口置于屏幕最顶层
        self.root.overrideredirect(True)  # 隐藏标题栏和边框

        self.video_path = video_path
        self.play_audio = play_audio

        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack()

        self.cap = cv2.VideoCapture(self.video_path)

        # 获取视频帧率
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        if self.fps == 0:
            self.fps = 30  # 如果帧率为零，默认设置为30

        self.show_frame()

    def show_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img)

            # 将窗口置于最底层
            hwnd = self.root.winfo_id()
            win32gui.ShowWindow(hwnd, 9)  # SW_RESTORE
            win32gui.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0002 | 0x0001)  # 使用 0 替代 win32gui.HWND_BOTTOM

            self.root.after(int(1000 / self.fps), self.show_frame)
        else:
            self.cap.release()
            self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python script.py <video_path> [play_audio]")
        sys.exit(1)

    video_path = sys.argv[1]
    play_audio = True if len(sys.argv) < 3 or int(sys.argv[2]) == 1 else False

    app = VideoWallpaperApp(video_path, play_audio)
    app.run()
