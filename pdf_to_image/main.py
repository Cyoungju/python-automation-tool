"""
PDF → 이미지(PNG) 변환 도구 (input/output 폴더 분리 버전)

폴더 구조:
  pdf_to_image\
  ├── main.py
  ├── input\    ← 변환할 PDF를 여기에 넣기
  └── output\   ← 변환 결과가 여기에 저장됨
  └── done\   ← 변환 완료된 원본 PDF가 여기로 이동됨
사용법:
  1) python main.py                 → input 폴더 안의 모든 PDF 변환
  2) python main.py 파일.pdf        → 특정 PDF만 변환 (결과는 output에 저장)
  3) python main.py 파일.pdf 300    → DPI 지정 (화질 ↑)

필요 라이브러리: pip install pymupdf
(PyMuPDF 공식 문서: https://pymupdf.readthedocs.io/)
"""

import os
import sys
import shutil

try:
    import pymupdf  # PyMuPDF 1.24+ / 구버전은 import fitz
except ImportError:
    print("PyMuPDF가 설치되어 있지 않습니다.")
    print("설치 명령: pip install pymupdf")
    sys.exit(1)

# 스크립트 파일 기준 경로 (어디서 실행해도 동일하게 동작)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input_pdf")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_images")
DONE_DIR = os.path.join(BASE_DIR, "done")

def convert_pdf(pdf_path: str, dpi: int = 150) -> None:
    """PDF 한 개를 페이지별 PNG로 변환해 output 폴더에 저장한다."""
    if not os.path.isfile(pdf_path):
        print(f"[건너뜀] 파일을 찾을 수 없음: {pdf_path}")
        return
    if not pdf_path.lower().endswith(".pdf"):
        print(f"[건너뜀] PDF 파일이 아님: {pdf_path}")
        return

    doc = pymupdf.open(pdf_path)

    # output 폴더 안에 PDF 이름으로 하위 폴더 생성
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    out_dir = os.path.join(OUTPUT_DIR, pdf_name)
    os.makedirs(out_dir, exist_ok=True)

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        out_path = os.path.join(out_dir, f"page_{i + 1:03d}.png")
        pix.save(out_path)
        print(f"  - {i + 1}/{len(doc)} 페이지 저장")

    doc.close()
    print(f"[완료] {os.path.basename(pdf_path)} → {out_dir} ({dpi} DPI)")

    # 변환 완료된 원본을 done 폴더로 이동
    if os.path.dirname(os.path.abspath(pdf_path)) == INPUT_DIR:
        os.makedirs(DONE_DIR, exist_ok=True)
        shutil.move(pdf_path, os.path.join(DONE_DIR, os.path.basename(pdf_path)))
        print(f"  → 원본을 done 폴더로 이동\n")
    else:
        print()

def main() -> None:
    # input / output 폴더가 없으면 자동 생성
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(DONE_DIR, exist_ok=True)

    args = sys.argv[1:]

    # 마지막 인자가 숫자면 DPI로 인식
    dpi = 150
    if args and args[-1].isdigit():
        dpi = int(args.pop())

    if args:
        # 경로를 직접 전달한 경우: 해당 파일들 변환
        targets = [a.strip('"') for a in args]
    else:
        # 인자가 없으면 input 폴더의 모든 PDF 변환
        targets = [
            os.path.join(INPUT_DIR, f)
            for f in os.listdir(INPUT_DIR)
            if f.lower().endswith(".pdf")
        ]
        if not targets:
            print(f"input 폴더에 PDF가 없습니다: {INPUT_DIR}")
            input("Enter를 누르면 창이 닫힙니다.")
            return
        print(f"input 폴더에서 {len(targets)}개의 PDF를 발견했습니다.\n")

    for pdf_path in targets:
        convert_pdf(pdf_path, dpi)

    input("변환이 끝났습니다. Enter를 누르면 창이 닫힙니다.")


if __name__ == "__main__":
    main()