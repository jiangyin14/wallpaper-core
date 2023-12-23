import os
import sys
from pydub import AudioSegment
import win32api
import win32con
import win32gui

def setVideoWallpaper(video_path, play_audio=True):
    # 打开注册表
    regKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(regKey, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    win32api.RegSetValueEx(regKey, "TileWallpaper", 0, win32con.REG_SZ, "0")

    # 刷新屏幕
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, video_path, win32con.SPIF_SENDWININICHANGE)

    # 设置音频
    if play_audio:
        audio_path = os.path.splitext(video_path)[0] + ".wav"
        audio_segment = AudioSegment.from_file(video_path, format="mp4")
        audio_segment.export(audio_path, format="wav")
        win32api.RegSetValueEx(regKey, "SoundOn", 0, win32con.REG_SZ, audio_path)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script.py <video_path> <play_audio>")
        sys.exit(1)

    video_path = sys.argv[1]
    play_audio = bool(int(sys.argv[2]))

    setVideoWallpaper(video_path, play_audio)
