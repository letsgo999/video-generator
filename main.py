import os
import moviepy.config as mpy_config

# FFmpeg 경로 설정
mpy_config.change_settings({"FFMPEG_BINARY": "/usr/bin/ffmpeg"})

import tempfile
import uuid
import moviepy.editor as mp
from PIL import Image
from flask import Flask, request, jsonify

# Flask 앱을 생성합니다.
app = Flask(__name__)

# MoviePy와 Pillow 라이브러리가 로컬에 설치되어 있는지 확인합니다.
print("MoviePy and Pillow libraries are ready.")

@app.route('/', methods=['POST'])
def generate_video():
    try:
        # 1. 파일 받기
        # Streamlit에서 업로드된 파일 받기
        audio_file = request.files['audio']
        image_files = request.files.getlist('images')

        with tempfile.TemporaryDirectory() as tmpdir:
            # 2. 임시 저장소에 파일 저장 및 이미지 리사이징
            image_paths = []
            for img_file in image_files:
                img_path = os.path.join(tmpdir, img_file.filename)
                img_file.save(img_path)

                # 이미지 크기 최적화 (1920x1080)
                img = Image.open(img_path)
                resized_img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
                resized_path = os.path.join(tmpdir, f"resized_{uuid.uuid4()}.jpg")
                resized_img.save(resized_path)
                image_paths.append(resized_path)

            audio_path = os.path.join(tmpdir, audio_file.filename)
            audio_file.save(audio_path)

            # 3. 비디오 생성 로직
            # MoviePy를 사용하여 비디오를 생성하는 코드를 여기에 배치합니다.

            clips = [mp.ImageClip(path).set_duration(3) for path in image_paths]
            final_clip = mp.concatenate_videoclips(clips)
            final_clip = final_clip.set_audio(mp.AudioFileClip(audio_path))

            output_filename = f"output_{uuid.uuid4()}.mp4"
            output_path = os.path.join(tmpdir, output_filename)
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

            # 4. 결과물 반환
            # 여기서는 최종 비디오를 Google Cloud Storage에 업로드하고 URL을 반환하는 로직이 필요합니다.
            # 초보자용 예제이므로 간단한 성공 메시지를 반환합니다.

            return jsonify({"status": "Video generation successful!"})

    

    except Exception as e:
        return jsonify({"status": "An error occurred", "error": str(e)})

@app.route('/', methods=['GET'])
def health_check():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Cloud Run의 PORT 환경 변수를 사용하거나 기본 8080
    app.run(host='0.0.0.0', port=port)  # 서버를 모든 IP에서 듣게 함 (debug=True는 테스트용)



