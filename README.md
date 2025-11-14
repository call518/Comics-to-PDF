# 📚 Comics2PDF

> Convert comic book image folders to high-quality PDF files  
> 만화책 이미지 폴더를 고품질 PDF로 변환하는 Python 도구

## ✨ 기능

- **다양한 이미지 형식 지원**: JPG, PNG, BMP, GIF, TIFF, WebP (6가지 형식)
- **알파벳 순 정렬**: 폴더 내 이미지들을 파일명 순으로 자동 정렬
- **이미지 비율 유지**: 원본 비율을 유지하면서 페이지에 맞게 자동 크기 조정
- **중앙 정렬 배치**: 이미지를 페이지 중앙에 배치
- **페이지 방향 선택**: 가로/세로 페이지 설정 가능 (만화책은 가로 권장)
- **실시간 진행률**: 처리 상황을 10장마다 표시
- **기본 경로 자동 생성**: 입출력 폴더가 없으면 자동 생성

## 🚀 설치 및 설정

### 1. Python 환경 설정
```bash
# Python 3.7+ 필요
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는 venv\Scripts\activate  # Windows

# 필요한 라이브러리 설치
pip install Pillow reportlab
```

### 2. 폴더 구조
```
프로젝트 폴더/
├── convert_to_pdf.py          # 메인 스크립트
├── images-input/              # 입력 폴더 (기본값)
│   ├── comic_volume_01/       # 만화책 1권 이미지들
│   │   ├── page_001.jpg
│   │   ├── page_002.png
│   │   └── ...
│   ├── comic_volume_02/       # 만화책 2권 이미지들
│   │   ├── page_001.jpg
│   │   └── ...
│   └── ...
└── images-output/             # 출력 폴더 (기본값, 자동 생성)
    ├── comic_volume_01.pdf
    ├── comic_volume_02.pdf
    └── ...
```

## 📖 사용법

### 기본 사용법 (권장)
```bash
python convert_to_pdf.py
```
- 기본적으로 `images-input` 폴더의 하위 디렉토리들을 처리
- PDF 파일들은 `images-output` 폴더에 저장
- 기본 페이지 방향: 가로 (landscape) - 만화책에 최적화
- 각 폴더 처리 전 사용자 확인

### 자동 실행 (확인 없이)
```bash
python convert_to_pdf.py --auto
```
- 확인 메시지 없이 즉시 처리 시작
- 대량 처리에 유용

### 페이지 방향 선택
```bash
python convert_to_pdf.py --orientation landscape    # 가로 페이지 (기본값, 만화책 권장)
python convert_to_pdf.py --orientation portrait     # 세로 페이지
```

### 사용자 지정 경로
```bash
python convert_to_pdf.py -i ./my_images -o ./my_pdfs
```

### 기존 파일 덮어쓰기
```bash
python convert_to_pdf.py --force
```

## 🎛️ 옵션 설명

| 옵션 | 단축형 | 설명 | 기본값 |
|------|--------|------|---------|
| `--input` | `-i` | 이미지 폴더들이 있는 입력 디렉토리 | `images-input` |
| `--output` | `-o` | PDF 파일들이 저장될 출력 디렉토리 | `images-output` |
| `--orientation` | - | PDF 페이지 방향 (portrait/landscape) | `landscape` |
| `--auto` | - | 확인 없이 자동 실행 | `false` |
| `--force` | - | 기존 PDF 파일 덮어쓰기 | `false` |
| `--help` | `-h` | 도움말 표시 | - |

## 💻 지원 형식

### 입력 이미지 형식
- JPG, JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`) 
- BMP (`.bmp`)
- GIF (`.gif`)
- TIFF (`.tiff`, `.tif`)
- WebP (`.webp`)

### 출력 형식
- PDF (A4 크기, 고품질)

## 📚 사용 예시

### 단일 폴더 처리
```bash
# 기본 설정으로 처리 (가로 페이지)
python convert_to_pdf.py

# 세로 페이지로 처리
python convert_to_pdf.py --orientation portrait
```

### 다량의 폴더 처리
```bash
# 자동 처리 (확인 없이)
python convert_to_pdf.py --auto

# 기존 파일 덮어쓰기 허용
python convert_to_pdf.py --auto --force
```

### 경로 지정
```bash
# 입력/출력 경로 지정
python convert_to_pdf.py -i /path/to/comics -o /path/to/pdfs

# 출력 경로만 변경
python convert_to_pdf.py -o ~/Documents/converted_comics
```

## ⚡ 성능 및 품질

- **처리 속도**: 이미지 크기와 수량에 따라 변동
- **이미지 품질**: JPEG 압축률 85% (고품질 유지)
- **페이지 크기**: A4 (210×297mm)
- **메모리 효율**: 이미지별 순차 처리로 메모리 사용량 최적화

## 🛠️ 문제 해결

### 라이브러리 설치 오류
```bash
pip install --upgrade pip
pip install Pillow reportlab
```

### 메모리 부족
- 대용량 이미지는 미리 리사이징 권장
- 한 번에 처리할 폴더 수 조정

### 권한 오류  
- 출력 디렉토리 쓰기 권한 확인
- 다른 출력 경로 지정

### 이미지 파일 인식 안됨
- 지원 형식 확인 (JPG, PNG, BMP, GIF, TIFF, WebP)
- 파일명에 특수문자나 공백 확인

## 📝 개발 정보

- **언어**: Python 3.7+
- **종속성**: Pillow, reportlab
- **라이센스**: MIT
- **저자**: GitHub Copilot

## 🎯 만화책 최적화 팁

1. **가로 페이지 권장**: `--orientation landscape` (기본값)
2. **대량 처리**: `--auto` 옵션으로 자동 처리
3. **폴더명 정리**: 숫자 순서대로 정렬되도록 폴더명 설정
4. **이미지 형식**: JPG 권장 (파일 크기 vs 품질 균형)

---

> 💡 **Tip**: 만화책 스캔본의 경우 가로 페이지(landscape)로 설정하면 상하 여백이 줄어들어 더 좋은 결과를 얻을 수 있습니다.