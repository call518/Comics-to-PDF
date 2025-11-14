# 만화책 이미지 → PDF 변환기

이 프로그램은 만화책을 스캔한 이미지 폴더들을 각각 하나의 PDF 파일로 변환합니다.

## 기능

- 각 폴더의 JPG 이미지들을 알파벳 순으로 정렬하여 PDF로 변환
- 이미지 비율을 유지하면서 페이지에 맞게 자동 크기 조정
- 중앙 정렬된 이미지 배치
- 입력/출력 경로 사용자 지정 가능
- 처리 진행 상황 실시간 표시

## 설치

Python 3.6 이상이 필요합니다.

### 1. 가상환경 생성 및 활성화 (권장)
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 또는
.venv\Scripts\activate     # Windows
```

### 2. 필요한 라이브러리 설치
```bash
pip install Pillow reportlab
```

## 사용법

### 기본 사용법
```bash
python convert_to_pdf.py
```
- 기본적으로 `./images-input` 폴더의 하위 디렉토리들을 처리
- PDF 파일들은 `./images-output` 폴더에 저장
- 기본 페이지 방향: 가로 (landscape)
- 일반 모드: 각 이미지 처리 상황을 상세히 표시

### 자동 실행 (확인 없이)
```bash
python convert_to_pdf.py --auto
```
- 확인 메시지 없이 즉시 처리 시작
- 42권 같은 대량 처리에 유용

### 페이지 방향 선택
```bash
python convert_to_pdf.py --orientation landscape    # 가로 페이지 (기본값)
python convert_to_pdf.py --orientation portrait     # 세로 페이지
```

### 사용자 지정 경로
```bash
python convert_to_pdf.py -i ./my_images -o ./my_pdfs --orientation landscape
```

### 전체 옵션
```bash
python convert_to_pdf.py --input /path/to/images --output /path/to/pdfs --orientation portrait --batch --force
```

## 폴더 구조 예시

### 입력 폴더 구조:
```
images-input/
├── 드래곤볼_무수정판_01/
│   ├── a-1.JPG
│   ├── raprnb_001.JPG
│   ├── raprnb_002.JPG
│   └── ...
├── 드래곤볼_무수정판_02/
│   ├── image001.jpg
│   ├── image002.jpg
│   └── ...
└── 드래곤볼_무수정판_03/
    └── ...
```

### 출력 결과:
```
images-output/
├── 드래곤볼_무수정판_01.pdf
├── 드래곤볼_무수정판_02.pdf
└── 드래곤볼_무수정판_03.pdf
```

## 지원 파일 형식

- `.jpg`, `.JPG`, `.jpeg`, `.JPEG` 파일만 처리
- 다른 확장자 파일들은 자동으로 무시됨

## 특징

- **알파벳 순 정렬**: 각 폴더 내 이미지들을 파일명 기준으로 알파벳 순 정렬
- **비율 유지**: 원본 이미지의 가로세로 비율을 유지하면서 페이지에 맞게 조정
- **중앙 정렬**: 이미지를 페이지 중앙에 배치
- **고품질**: JPEG 품질 85%로 압축하여 파일 크기와 품질의 균형 유지
- **안전한 처리**: 잘못된 이미지 파일은 건너뛰고 계속 진행

## 옵션 설명

| 옵션 | 단축형 | 설명 | 기본값 |
|------|--------|------|---------|
| `--input` | `-i` | 이미지 폴더들이 있는 입력 디렉토리 | `./images-input` |
| `--output` | `-o` | PDF 파일들이 저장될 출력 디렉토리 | `./images-output` |
| `--orientation` | - | PDF 페이지 방향 (portrait/landscape) | `landscape` |
| `--auto` | - | 확인 없이 자동 실행 | `false` |
| `--force` | - | 기존 PDF 파일 덮어쓰기 | `false` |
| `--help` | `-h` | 도움말 표시 | - |

## 사용 예시

### 현재 프로젝트의 경우:
```bash
# 기본 설정으로 실행 (images-input 폴더 → images-output 폴더, 가로 페이지)
python convert_to_pdf.py

# 세로 페이지로 변환
python convert_to_pdf.py --orientation portrait

# 자동 실행 (확인 없이)
python convert_to_pdf.py --auto

# 출력 경로만 변경
python convert_to_pdf.py -o /home/user/Documents/comics

# 입력과 출력 경로 모두 지정 (가로 페이지)
python convert_to_pdf.py -i /path/to/scanned/comics -o /path/to/output/pdfs --orientation landscape
```

### 42권 모두 처리:
현재 `images-input` 폴더에 드래곤볼 1~42권이 있으므로, 다음 명령으로 모든 권을 PDF로 변환할 수 있습니다:

```bash
# 가로 페이지로 자동 처리 (만화책에 최적화, 추천)
python convert_to_pdf.py --auto

# 세로 페이지로 자동 처리
python convert_to_pdf.py --auto --orientation portrait

# 확인 후 처리 (안전한 방법)
python convert_to_pdf.py
```

이 명령은:
- `images-input` 폴더의 42개 하위 폴더를 모두 처리
- 각 폴더마다 하나의 PDF 파일 생성 (예: `드래곤볼_무수정판_01.pdf`)
- `images-output` 폴더에 42개의 PDF 파일이 생성됨
- 가로 페이지로 생성하여 만화 이미지에 최적화된 레이아웃 제공
- 42권 전체 처리 시 약 1시간 20분 예상 소요

## 주의사항

- 처리 시작 전에 확인 메시지가 표시됩니다 (`y` 입력 시 시작)
- 이미지가 많은 경우 처리 시간이 오래 걸릴 수 있습니다
- 출력 디렉토리가 없으면 자동으로 생성됩니다
- 기존에 같은 이름의 PDF 파일이 있으면 덮어씁니다

## 문제 해결

### 라이브러리 설치 오류
```bash
# pip 업그레이드 후 재시도
pip install --upgrade pip
pip install Pillow reportlab
```

### 메모리 부족 오류
- 이미지 파일이 너무 큰 경우 발생할 수 있습니다
- 이미지를 미리 리사이징하거나 한 번에 적은 수의 폴더를 처리해보세요

### 권한 오류
- 출력 디렉토리에 쓰기 권한이 있는지 확인하세요
- 다른 출력 경로를 지정해보세요

## 개발 정보

- Python 3.6+
- 라이브러리: Pillow (이미지 처리), reportlab (PDF 생성)
- 페이지 크기: A4 (210×297mm)
- JPEG 품질: 85%