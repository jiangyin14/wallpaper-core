import os
import sys
import cv2
import time
from pydub import AudioSegment
import win32api
import win32con
import win32gui

def clear_temp_image_folder(folder):
    # 删除 temp_image 文件夹中的所有文件
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def setVideoWallpaper(video_path, play_audio=True, interval=0.3):
    # 打开注册表
    regKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(regKey, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    win32api.RegSetValueEx(regKey, "TileWallpaper", 0, win32con.REG_SZ, "0")

    # 创建 temp_image 文件夹并清空其中的文件
    temp_image_folder = os.path.join(os.path.dirname(video_path), "temp_image")
    os.makedirs(temp_image_folder, exist_ok=True)
    clear_temp_image_folder(temp_image_folder)

    # 获取视频帧率
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    # 读取视频并保存每一帧为图片
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        image_path = os.path.join(temp_image_folder, f"frame_{frame_count}.jpg")
        cv2.imwrite(image_path, frame)

    cap.release()

    # 刷新屏幕并设置每一帧为桌面壁纸
    for frame_number in range(1, frame_count + 1):
        image_path = os.path.join(temp_image_folder, f"frame_{frame_number}.jpg")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, image_path, win32con.SPIF_SENDWININICHANGE)
        time.sleep(1 / fps)  # 使用视频的帧率来控制切换间隔

    # 设置音频
    if play_audio:
        audio_path = os.path.splitext(video_path)[0] + ".wav"
        audio_segment = AudioSegment.from_file(video_path, format="mp4")
        audio_segment.export(audio_path, format="wav")
        win32api.RegSetValueEx(regKey, "SoundOn", 0, win32con.REG_SZ, audio_path)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script.py <video_path> <play_audio> [interval]")
        sys.exit(1)

    video_path = sys.argv[1]
    play_audio = bool(int(sys.argv[2]))

    interval = 0.3  # 默认间隔为0.3秒
    if len(sys.argv) >= 4:
        interval = float(sys.argv[3])

    setVideoWallpaper(video_path, play_audio, interval)
