import os
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import CircleModuleDrawer, RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageFont


LOGO_FILE = "logo.jpg"

qr = qrcode.QRCode(
    error_correction=ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

data = "https://github.com/Cyoungju"
qr.add_data(data)
qr.make(fit=True)

kwargs = {
    "image_factory": StyledPilImage,
    "module_drawer": CircleModuleDrawer(),
    "eye_drawer": RoundedModuleDrawer(),
}

if os.path.isfile(LOGO_FILE):
    kwargs["embedded_image_path"] = LOGO_FILE
    print("✅ 로고가 포함된 점묘 QR코드를 생성합니다!")
else:
    print(f"⚠️ {LOGO_FILE} 파일이 없어서 로고 없이 생성합니다.")

# QR 생성
qr_image = qr.make_image(**kwargs).convert("RGB")

# 하단에 표시할 텍스트
footer_text = "github.com/Cyoungju"

# 하단 영역 높이
footer_height = 80

# 최종 이미지 생성
result_image = Image.new(
    "RGB",
    (qr_image.width, qr_image.height + footer_height),
    "white",
)

# QR 붙이기
result_image.paste(qr_image, (0, 0))

draw = ImageDraw.Draw(result_image)

# 폰트
try:
    font = ImageFont.truetype("malgun.ttf", 22)  # Windows
except OSError:
    font = ImageFont.load_default()

# 구분선
line_y = qr_image.height + 15
line_margin = 40

draw.line(
    (line_margin, line_y, result_image.width - line_margin, line_y),
    fill=(210, 210, 210),
    width=2,
)

# 텍스트 가운데 정렬
bbox = draw.textbbox((0, 0), footer_text, font=font)
text_width = bbox[2] - bbox[0]

draw.text(
    (
        (result_image.width - text_width) // 2,
        line_y + 15,
    ),
    footer_text,
    fill=(70, 70, 70),
    font=font,
)

# 저장
result_image.save("logo_qr_dot.png")
print("📁 저장 완료: logo_qr_dot.png")