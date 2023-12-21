from flask import Flask, request, jsonify
import configparser

app = Flask(__name__)

@app.route('/set_wallpaper', methods=['POST'])
def set_wallpaper():
    data = request.get_json()

    # 获取视频路径和是否播放音频的值
    video_path = data.get('video_path', '')
    play_audio = data.get('play_audio', False)

    # 写入配置文件
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set('WallpaperSettings', 'video_path', video_path)
    config.set('WallpaperSettings', 'play_audio', str(play_audio))

    with open('config.ini', 'w') as config_file:
        config.write(config_file)

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
