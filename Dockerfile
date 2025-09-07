# 파이썬 공식 이미지를 기반으로 합니다.
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파이썬 패키지를 설치합니다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FFMpeg 설치
RUN apt-get update && apt-get install -y ffmpeg
# FFmpeg 경로를 확인하는 임시 명령어 추가
RUN which ffmpeg

# 애플리케이션 소스 코드 복사
COPY . .

# 컨테이너 포트 노출
EXPOSE 8080

# 애플리케이션 실행
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
