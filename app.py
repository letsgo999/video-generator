import streamlit as st
import requests

# 백엔드 서버의 URL을 여기에 입력하세요.
# Cloud Run 서비스 URL을 복사하여 붙여넣으세요.
BACKEND_URL = "https://your-cloud-run-service-url.run.app"

st.title("비디오 생성기")
st.write("이미지와 오디오를 업로드하여 비디오를 생성하세요.")

# 오디오 파일 업로드
audio_file = st.file_uploader("오디오 파일 선택", type=['mp3', 'wav'])

# 이미지 파일 여러 개 업로드
image_files = st.file_uploader("이미지 파일 선택", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)

if st.button("비디오 생성"):
    if audio_file and image_files:
        st.info("비디오를 생성 중입니다. 잠시만 기다려 주세요...")

        # 요청에 포함할 파일들을 준비
        files = {
            'audio': audio_file.getvalue()
        }
        for i, img_file in enumerate(image_files):
            files[f'images_{i}'] = img_file.getvalue()

        try:
            # POST 요청을 백엔드 서버로 보냄
            response = requests.post(BACKEND_URL, files=files, timeout=300)

            # 응답 확인
            if response.status_code == 200:
                st.success("비디오 생성이 완료되었습니다!")
                st.json(response.json())
            else:
                st.error(f"비디오 생성 실패: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"서버 연결 오류: {e}")
    else:
        st.warning("오디오 파일과 이미지를 모두 업로드해야 합니다.")
