# 식단 관리 앱

한글 음식 이름을 입력하면 1회 제공량 기준으로 칼로리, 단백질, 탄수화물, 지방을 출력하는 간단한 앱입니다. Streamlit 웹 인터페이스와 CLI 두 가지 방법을 모두 지원합니다.

## 사용법

### Streamlit 웹앱

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

사이드바에서 지원 음식 목록을 선택하거나 직접 입력하면 표와 총합을 확인할 수 있습니다.

### CLI

```bash
python main.py 닭가슴살 고구마 브로콜리
```

지원 음식 목록만 보고 싶다면 `--list` 옵션을 사용하세요. 알 수 없는 음식이 포함되어 있으면 비슷한 이름을 제안합니다.
