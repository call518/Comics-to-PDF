#!/usr/bin/env python3
"""
만화책 이미지 폴더를 PDF로 변환하는 통합 프로그램
기본 모드와 배치 모드를 지원합니다.
"""

import os
import sys
import argparse
import time
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
import tempfile


def get_jpg_files(folder_path):
    """폴더에서 JPG 파일들을 알파벳 순으로 가져옵니다."""
    jpg_extensions = ['.jpg', '.JPG', '.jpeg', '.JPEG']
    jpg_files = []
    
    for file in os.listdir(folder_path):
        if any(file.endswith(ext) for ext in jpg_extensions):
            jpg_files.append(os.path.join(folder_path, file))
    
    # 알파벳 순으로 정렬
    jpg_files.sort()
    return jpg_files


def create_pdf_from_images(image_files, output_pdf_path, folder_name, page_size=landscape(A4), verbose=True):
    """이미지 파일들로부터 PDF를 생성합니다."""
    if not image_files:
        if verbose:
            print(f"  경고: {folder_name}에 이미지 파일이 없습니다.")
        return False
    
    try:
        # PDF 캔버스 생성
        c = canvas.Canvas(str(output_pdf_path), pagesize=page_size)
        page_width, page_height = page_size
        
        total_images = len(image_files)
        start_time = time.time()
        
        for i, img_path in enumerate(image_files):
            try:
                # 이미지 열기
                with Image.open(img_path) as img:
                    # RGBA 이미지를 RGB로 변환 (필요시)
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')
                    
                    img_width, img_height = img.size
                    
                    # 이미지를 페이지에 맞게 스케일링
                    width_ratio = page_width / img_width
                    height_ratio = page_height / img_height
                    scale_ratio = min(width_ratio, height_ratio)
                    
                    new_width = img_width * scale_ratio
                    new_height = img_height * scale_ratio
                    
                    # 중앙 정렬을 위한 위치 계산
                    x = (page_width - new_width) / 2
                    y = (page_height - new_height) / 2
                    
                    # 임시 파일로 이미지 저장
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                        img.save(tmp_file.name, 'JPEG', quality=85)
                        c.drawImage(tmp_file.name, x, y, width=new_width, height=new_height)
                        os.unlink(tmp_file.name)
                
                # 다음 페이지로
                if i < len(image_files) - 1:
                    c.showPage()
                
                # 진행률 표시 (10장마다)
                if verbose and (i + 1) % 10 == 0:
                    elapsed = time.time() - start_time
                    avg_time = elapsed / (i + 1)
                    remaining = avg_time * (total_images - i - 1)
                    print(f"    진행: {i+1}/{total_images} ({(i+1)/total_images*100:.1f}%) 예상 남은 시간: {remaining:.1f}초")
                    
            except Exception as e:
                if verbose:
                    print(f"    오류 - {os.path.basename(img_path)}: {e}")
                continue
        
        # PDF 저장
        c.save()
        
        if verbose:
            total_time = time.time() - start_time
            print(f"    완료: {total_images}장, {total_time:.1f}초 소요")
        
        return True
        
    except Exception as e:
        if verbose:
            print(f"  PDF 생성 실패: {e}")
        return False


def process_folders(input_dir, output_dir, orientation='landscape', skip_existing=True):
    """폴더들을 처리하여 PDF로 변환합니다."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # 출력 디렉토리가 없으면 생성
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 입력 디렉토리가 없으면 생성 (빈 폴더라도 생성)
    if not input_path.exists():
        print(f"입력 디렉토리가 없어서 생성합니다: {input_dir}")
        input_path.mkdir(parents=True, exist_ok=True)
        if input_dir == './images-input':
            print("생성된 'images-input' 폴더에 만화책 폴더들을 넣어주세요.")
            print("예: images-input/드래곤볼_무수정판_01/, images-input/드래곤볼_무수정판_02/, ...")
        return
    
    # 페이지 방향 설정
    if orientation == 'portrait':
        page_size = A4
        orientation_name = "세로"
    else:  # landscape
        page_size = landscape(A4)
        orientation_name = "가로"
    
    # 하위 디렉토리들을 가져오기
    subdirs = [d for d in input_path.iterdir() if d.is_dir()]
    subdirs.sort()
    
    if not subdirs:
        print(f"오류: {input_dir}에 하위 디렉토리가 없습니다.")
        return
    
    print(f"페이지 방향: {orientation_name}")
    print(f"=== 배치 처리 시작 ===")
    print(f"총 {len(subdirs)}개의 폴더를 처리합니다.")
    print(f"입력: {input_path.absolute()}")
    print(f"출력: {output_path.absolute()}")
    if skip_existing:
        print("기존 PDF 파일은 건너띙니다.")
    else:
        print("기존 PDF 파일을 덮어쒕니다.")
    print()
    
    success_count = 0
    skip_count = 0
    fail_count = 0
    total_start_time = time.time()
    
    for idx, subdir in enumerate(subdirs, 1):
        folder_name = subdir.name
        pdf_filename = f"{folder_name}.pdf"
        output_pdf_path = output_path / pdf_filename
        
        print(f"[{idx}/{len(subdirs)}] {folder_name}")
        
        # 이미 존재하는 파일 확인
        if skip_existing and output_pdf_path.exists():
            print(f"  건너뜀: PDF 파일이 이미 존재합니다.")
            skip_count += 1
            continue
        
        # JPG 파일들 가져오기
        jpg_files = get_jpg_files(str(subdir))
        
        if not jpg_files:
            print(f"  건너뜀: JPG 파일이 없습니다.")
            fail_count += 1
            continue
        
        print(f"  {len(jpg_files)}장의 이미지 처리 중...")
        
        # PDF 생성
        if create_pdf_from_images(jpg_files, output_pdf_path, folder_name, page_size, verbose=True):
            success_count += 1
            file_size = output_pdf_path.stat().st_size / 1024 / 1024  # MB
            print(f"  ✅ 완료: {pdf_filename} ({file_size:.1f}MB)")
        else:
            fail_count += 1
            print(f"  ❌ 실패: {pdf_filename}")
        
        print()  # 빈 줄
    
    # 결과 요약
    total_time = time.time() - total_start_time
    
    print("=== 처리 완료 ===")
    print(f"성공: {success_count}개")
    print(f"건너띠: {skip_count}개")
    print(f"실패: {fail_count}개")
    print(f"총 소요 시간: {total_time/60:.1f}분")
    
    print(f"PDF 파일 위치: {output_path.absolute()}")


def main():
    parser = argparse.ArgumentParser(
        description="만화책 이미지 폴더들을 PDF로 변환합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  # 기본 사용
  python convert_to_pdf.py                                          
  
  # 자동 처리 (확인 없이)
  python convert_to_pdf.py --auto                          
  
  # 페이지 방향 지정
  python convert_to_pdf.py --orientation portrait                   
  
  # 경로 지정
  python convert_to_pdf.py -i ./my-images -o ./my-pdfs --auto     
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        default='./images-input',
        help='이미지 폴더들이 있는 입력 디렉토리 (기본값: ./images-input)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='./images-output',
        help='PDF 파일들이 저장될 출력 디렉토리 (기본값: ./images-output)'
    )
    
    parser.add_argument(
        '--orientation',
        choices=['portrait', 'landscape'],
        default='landscape',
        help='PDF 페이지 방향: portrait(세로), landscape(가로) (기본값: landscape)'
    )
    

    
    parser.add_argument(
        '--auto',
        action='store_true',
        help='확인 없이 자동으로 처리 시작'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='기존 PDF 파일을 덮어쓰기'
    )
    
    args = parser.parse_args()
    
    print("=== 만화책 이미지 → PDF 변환기 ===")
    print(f"입력 디렉토리: {args.input}")
    print(f"출력 디렉토리: {args.output}")
    print(f"페이지 방향: {'세로' if args.orientation == 'portrait' else '가로'}")
    print(f"덮어쓰기: {'예' if args.force else '아니오'}")
    print()
    
    # 폴더 개수 미리 확인
    input_path = Path(args.input)
    if input_path.exists():
        subdirs = [d for d in input_path.iterdir() if d.is_dir()]
        print(f"처리할 폴더 수: {len(subdirs)}개")
        
        if len(subdirs) > 10:
            estimated_time = len(subdirs) * 2  # 폴더당 약 2분 예상
            print(f"예상 처리 시간: 약 {estimated_time//60}시간 {estimated_time%60}분")
    else:
        print(f"경고: 입력 디렉토리가 존재하지 않습니다: {args.input}")
    
    print()
    
    # 확인 메시지 (auto 모드가 아닌 경우)
    if not args.auto:
        response = input("처리를 시작하시겠습니까? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("작업이 취소되었습니다.")
            return
        print()
    
    process_folders(
        args.input, 
        args.output, 
        args.orientation, 
        skip_existing=not args.force
    )


if __name__ == "__main__":
    main()