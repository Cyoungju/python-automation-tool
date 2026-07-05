import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
qr = qrcode.QRCode(
    version=3,
    error_correction=ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

data = "https://github.com/Cyoungju"

qr.add_data(data)
qr.make(fit=True)

qr_image = qr.make_image(
    fill_color="#000000",
    back_color="#ffffff"
).convert("RGB")

try: 
    logo = Image.open("logo.jpg")
    qr_width, qr_height = qr_image.size
    logo_size = qr_width // 4
    logo = logo.resize((logo_size, logo_size))

    logo_x = (qr_width - logo_size) //2
    logo_y = (qr_height - logo_size) //2

    qr_image.paste(logo, (logo_x, logo_y))

    print("✅ 로고가 포함된 QR코드가 생성되었습니다!")


except FileNotFoundError:
    print("⚠️ logo.png 파일이 없어서 로고 없이 생성합니다.")
    print("💡 같은 폴더에 logo.png 파일을 넣고 다시 실행해보세요!")

# 8. 저장
qr_image.save("logo_qr.png")
print("📁 저장 완료: logo_qr.png")