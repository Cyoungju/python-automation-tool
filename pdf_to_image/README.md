# pdf_to_image

PDF 파일을 페이지별 PNG 이미지로 변환하는 개인 자동화 도구입니다.

[PyMuPDF](https://pymupdf.readthedocs.io/) 라이브러리를 사용하며, poppler 등 외부 프로그램 설치 없이 pip만으로 동작합니다.
(출처: PyMuPDF PyPI 페이지 https://pypi.org/project/PyMuPDF/)

## 폴더 구조

```
pdf_to_image\
├── venv\           # 가상환경 (Git 업로드 시 제외)
├── main.py         # 변환 스크립트
├── input\          # 변환할 PDF를 넣는 폴더 (자동 생성)
├── output\         # 변환된 이미지가 저장되는 폴더 (자동 생성)
├── done\           # 변환 완료된 원본 PDF가 이동되는 폴더 (자동 생성)
└── README.md
```

## 설치

가상환경 사용은 Python 공식 문서가 안내하는 표준 방식입니다.
(출처: https://docs.python.org/3/tutorial/venv.html)

```bash
# 1. 가상환경 생성
python -m venv venv

# 2. 가상환경 활성화 (Windows)
venv\Scripts\activate

# 3. 라이브러리 설치
pip install pymupdf
```

## 사용법

### 1. input 폴더 일괄 변환

`input` 폴더에 PDF 파일을 넣고 실행하면 모든 PDF가 변환됩니다.

```bash
python main.py
```

### 2. 특정 파일만 변환

```bash
python main.py "파일명.pdf"
```

파일명에 공백이 있으면 반드시 큰따옴표로 감싸야 합니다.
(명령줄 인자는 셸이 공백 기준으로 분리하기 때문입니다. 출처: Python 공식 문서 sys.argv https://docs.python.org/3/library/sys.html#sys.argv)

### 3. 화질(DPI) 지정

기본값은 150 DPI이며, 마지막 인자로 숫자를 넣으면 DPI로 인식합니다.

```bash
python main.py "파일명.pdf" 300
```

### 4. .bat 파일로 실행 (선택)

아래 내용을 `pdf변환.bat`으로 저장하면 더블클릭 또는 드래그 앤 드롭으로 사용할 수 있습니다.

```bat
@echo off
chcp 65001 >nul
"%~dp0venv\Scripts\python.exe" "%~dp0main.py" %*
pause
```

- **더블클릭**: input 폴더의 모든 PDF 일괄 변환
- **PDF 드래그 앤 드롭**: 해당 파일만 변환

가상환경은 활성화(activate) 없이 내부 인터프리터 경로를 직접 지정해 실행할 수 있습니다.
(출처: Python 공식 문서 venv https://docs.python.org/3/library/venv.html#how-venvs-work)

`%*`는 배치 파일에 전달된 모든 인자를 그대로 넘기는 문법입니다.
(출처: Microsoft Learn "Using batch parameters" https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/percent)

## 동작 방식

1. `input` 폴더의 PDF를 페이지별 PNG로 변환
2. 변환 결과는 `output\PDF이름\` 폴더에 저장
3. 변환이 끝난 원본 PDF는 `done` 폴더로 자동 이동
   - 파일 이동에는 `shutil.move`를 사용합니다.
     (출처: Python 공식 문서 shutil https://docs.python.org/3/library/shutil.html#shutil.move)
   - 단, `input` 폴더 안의 파일만 이동하며, 드래그 앤 드롭으로 변환한 외부 파일은 원래 위치에 그대로 둡니다.

## 출력 결과

```
output\
└── 문서이름\
    ├── page_001.png
    ├── page_002.png
    └── ...
```

## Git 업로드 시 참고

- `venv/`는 재생성 가능한 로컬 환경이므로 `.gitignore`에 추가하여 제외하는 것이 관례입니다.
  (출처: GitHub 공식 Python용 gitignore 템플릿 https://github.com/github/gitignore/blob/main/Python.gitignore)
- `input/`, `output/`, `done/`도 개인 파일이 포함되므로 제외를 권장합니다.
- `pip freeze > requirements.txt`로 패키지 목록을 저장하면 다른 환경에서 `pip install -r requirements.txt`로 재현할 수 있습니다.
  (출처: pip 공식 문서 https://pip.pypa.io/en/stable/reference/requirements-file-format/)

## 참고 문서

- PyMuPDF 공식 문서: https://pymupdf.readthedocs.io/
- Python venv 공식 문서: https://docs.python.org/3/library/venv.html
- Python shutil 공식 문서: https://docs.python.org/3/library/shutil.html
- Windows 배치 파일 명령어 (Microsoft Learn): https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands
