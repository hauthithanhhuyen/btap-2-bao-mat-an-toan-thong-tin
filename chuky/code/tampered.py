# tamper_preserve_signature.py
# Phiên bản có dấu cá nhân, không tạo file tạm overlay_temp.pdf

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib.colors import Color
from pikepdf import Pdf
from pathlib import Path
from datetime import datetime
from io import BytesIO
import sys

# === Cấu hình ===
SIGNED_PDF = Path(r"F:\chuky\pdf\signed.pdf")         # File PDF đã ký
TAMPERED_PDF = Path(r"F:\chuky\pdf\tampered.pdf")     # File PDF đầu ra
SIGN_IMAGE = Path("anhky.jpg")                          # Ảnh chữ ký cá nhân (tùy chọn)

# === Kiểm tra file nguồn ===
if not SIGNED_PDF.exists():
    print(f"❌ Không tìm thấy file nguồn: {SIGNED_PDF}")
    sys.exit(1)

# === Đăng ký font ===
FONT_PATH = Path("C:/Windows/Fonts/arial.ttf")
FONT_NAME = "ArialUnicode"
if FONT_PATH.exists():
    try:
        pdfmetrics.registerFont(TTFont(FONT_NAME, str(FONT_PATH)))
    except Exception:
        FONT_NAME = "Helvetica"
else:
    FONT_NAME = "Helvetica"

# === Lấy kích thước trang ===
with Pdf.open(str(SIGNED_PDF)) as base_check:
    mb = base_check.pages[0].MediaBox
    llx, lly, urx, ury = [float(x) for x in mb]
    page_w = urx - llx
    page_h = ury - lly

# === Tạo overlay trực tiếp trong bộ nhớ ===
overlay_buffer = BytesIO()
c = canvas.Canvas(overlay_buffer, pagesize=(page_w, page_h))
c.setFont(FONT_NAME, 14)
try:
    c.setFillAlpha(0.25)  # chữ mờ, không che nội dung
except Exception:
    pass

# Màu nền dấu (mờ nhẹ)
stamp_color = Color(0.9, 0.1, 0.1, alpha=0.2)  # đỏ nhạt trong suốt
c.setFillColor(stamp_color)

# --- Dấu cá nhân ---
# Nền tròn nhẹ làm dấu (hình ellipse)
center_x = page_w - 70*mm
center_y = 40*mm
c.circle(center_x, center_y, 25*mm, fill=1, stroke=0)

# Chữ trong dấu
c.setFillColor(Color(0.8, 0, 0, alpha=0.7))
c.setFont(FONT_NAME, 13)
c.drawCentredString(center_x, center_y + 2*mm, "HẦU THANH HUYỀN")
c.setFont(FONT_NAME, 9)
c.drawCentredString(center_x, center_y - 6*mm, "Ký & xác nhận")

# Thêm ảnh chữ ký nếu có
if SIGN_IMAGE.exists():
    c.drawImage(str(SIGN_IMAGE),
                x=center_x - 20*mm,
                y=center_y + 10*mm,
                width=40*mm,
                height=20*mm,
                mask='auto')

# Thêm timestamp nhỏ bên dưới
c.setFillColor(Color(0.5, 0, 0, alpha=0.6))
c.setFont(FONT_NAME, 8)
ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
c.drawCentredString(center_x, center_y - 15*mm, f"Modified on: {ts}")

c.save()
overlay_buffer.seek(0)

print("✅ Overlay dấu cá nhân đã tạo trong bộ nhớ.")

# === Ghép overlay với PDF gốc ===
with Pdf.open(str(SIGNED_PDF)) as base:
    with Pdf.open(overlay_buffer) as overlay:
        for i, page in enumerate(base.pages):
            page.add_overlay(overlay.pages[0])
            print(f"  → Đã áp dụng dấu cá nhân lên trang {i+1}")

        base.save(str(TAMPERED_PDF))
        print(f"💾 Đã lưu file chỉnh sửa tại: {TAMPERED_PDF}")

print("✅ Hoàn tất, không tạo file tạm overlay_temp.pdf nào.")
