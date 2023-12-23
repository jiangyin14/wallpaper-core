import pygame
import os
import sys

class VideoWallpaperApp:
    def __init__(self, video_path, play_audio=True):
        pygame.init()

        self.video_path = video_path
        self.play_audio = play_audio

        # 设置屏幕大小
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # 设置视频文件路径
        self.video_file = os.path.abspath(self.video_path)

        # 加载视频
        self.video = pygame.movie.Movie(self.video_file)

        # 播放视频
        self.video.play()

        # 如果设置了音频，加载并播放
        if self.play_audio:
            pygame.mixer.music.load(self.video_file)
            pygame.mixer.music.play()

        self.run()

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.cleanup()
                    sys.exit()

            if not self.video.get_busy():
                self.cleanup()
                sys.exit()

            # 更新显示
            self.screen.blit(self.video.get_surface(), (0, 0))
            pygame.display.flip()

            clock.tick(30)

    def cleanup(self):
        pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <video_path> [play_audio]")
        sys.exit(1)

    video_path = sys.argv[1]
    play_audio = True if len(sys.argv) < 3 or int(sys.argv[2]) == 1 else False

    app = VideoWallpaperApp(video_path, play_audio)
