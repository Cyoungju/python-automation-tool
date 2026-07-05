import qrcode
from qrcode.constants import ERROR_CORRECT_H

qr = qrcode.QRCode(
    version=1,
    error_correction=ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

data = "https://www.google.com"
qr.add_data(data)
qr.make(fit=True)


qr_image = qr.make_image(
    fill_color="darkblue",
    back_color="lightyellow",
)

qr_image.save("custom_qr.png")

print("커스텀 QR 코드가 생성 되었습니다.")