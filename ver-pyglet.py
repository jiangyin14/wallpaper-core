import pyglet
import os
import sys

class VideoWallpaperApp:
    def __init__(self, video_path, play_audio=True):
        self.video_path = video_path
        self.play_audio = play_audio

        # 创建窗口
        self.window = pyglet.window.Window(fullscreen=True)

        # 设置视频文件路径
        self.video_file = os.path.abspath(self.video_path)

        # 加载视频
        self.video = pyglet.media.load(self.video_file)

        # 播放视频
        self.player = pyglet.media.Player()
        self.player.queue(self.video)
        self.player.play()

        # 如果设置了音频，加载并播放
        if self.play_audio:
            self.audio = pyglet.media.load(self.video_file, streaming=False)
            self.audio_player = pyglet.media.Player()
            self.audio_player.queue(self.audio)
            self.audio_player.play()

        # 设置事件处理
        self.window.on_draw = self.on_draw
        pyglet.clock.schedule_interval(self.update, 1/30.0)

        pyglet.app.run()

    def on_draw(self):
        self.window.clear()
        self.video.get_texture().blit(0, 0)

    def update(self, dt):
        if self.player.source and self.player.source.video_format:
            self.window.set_size(self.player.source.video_format.width, self.player.source.video_format.height)

    def cleanup(self):
        pyglet.app.exit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <video_path> [play_audio]")
        sys.exit(1)

    video_path = sys.argv[1]
    play_audio = True if len(sys.argv) < 3 or int(sys.argv[2]) == 1 else False

    app = VideoWallpaperApp(video_path, play_audio)
