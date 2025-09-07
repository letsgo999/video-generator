# CUDA(GPU) 지원용 공식 파이썬 이미지를 사용
FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04

# 파이썬 설치
RUN apt-get update && apt-get install -y python3 python3-pip

# 작업 디렉토리 설정
WORKDIR /app

# ... 나머지 `requirements.txt` 및 ffmpeg 설치 과정은 동일 ...

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
