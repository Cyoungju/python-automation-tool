import qrcode

data = "https://www.google.com"

qr_image = qrcode.make(data)

qr_image.save("basic_qr.png")

print("QR code가 생성 되었습니다.")