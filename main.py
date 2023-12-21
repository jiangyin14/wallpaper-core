import os
from pydub import AudioSegment
import win32api
import win32con
import win32gui
import configparser

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

def readConfig(config_path='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_path)
    video_path = config.get('WallpaperSettings', 'video_path')
    play_audio = config.getboolean('WallpaperSettings', 'play_audio')
    return video_path, play_audio

if __name__ == '__main__':
    config_path = 'config.ini'
    video_path, play_audio = readConfig(config_path)
    setVideoWallpaper(video_path, play_audio)
