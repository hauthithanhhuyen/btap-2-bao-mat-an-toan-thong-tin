# ==========================================================
# ✒️  TAMPER PRESERVE SIGNATURE TOOL – PREMIUM CONSOLE EDITION
# 👩‍💻  Developer: Hau Thanh Huyen
# ==========================================================
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib.colors import Color
from pikepdf import Pdf
from pathlib import Path
from datetime import datetime
from io import BytesIO
import sys, time, os

# === 🎨 Màu console (có kiểm tra hỗ trợ) ===
class Mau:
    RESET = "\033[0m"
    XANH = "\033[92m"
    DO = "\033[91m"
    VANG = "\033[93m"
    CYAN = "\033[96m"
    XAM = "\033[90m"
    TRANG = "\033[97m"
    DAM = "\033[95m"

if os.name == "nt" and "WT_SESSION" not in os.environ:
    for attr in dir(Mau):
        if not attr.startswith("__"):
            setattr(Mau, attr, "")

# === ⚙️ Cấu hình ===
SIGNED_PDF = Path(r"F:\chuky\pdf\signed.pdf")
TAMPERED_PDF = Path(r"F:\chuky\pdf\tampered.pdf")
SIGN_IMAGE = Path("anhky.jpg")

# === 🧾 Hàm in thông báo ===
def log(msg, color=Mau.TRANG, delay=0.0, indent=0):
    prefix = " " * indent
    print(prefix + color + msg + Mau.RESET)
    if delay:
        time.sleep(delay)

# === 🚀 Giao diện đầu ===
print(Mau.CYAN + "╔════════════════════════════════════════════════════════════╗")
print(Mau.CYAN + "║    ✒️  TAMPER PRESERVE SIGNATURE TOOL – V2.0 (No Temp)     ║")
print(Mau.CYAN + "╚════════════════════════════════════════════════════════════╝" + Mau.RESET)
log("📂 Đang chuẩn bị xử lý tài liệu...", Mau.VANG, 0.5)

# === 🧩 Kiểm tra file nguồn ===
if not SIGNED_PDF.exists():
    log(f"❌ Không tìm thấy file nguồn: {SIGNED_PDF}", Mau.DO)
    sys.exit(1)
else:
    log(f"✅ Đã tìm thấy file nguồn: {SIGNED_PDF.name}", Mau.XANH)

# === 🖋️ Đăng ký font ===
FONT_PATH = Path("C:/Windows/Fonts/arial.ttf")
FONT_NAME = "ArialUnicode"
try:
    if FONT_PATH.exists():
        pdfmetrics.registerFont(TTFont(FONT_NAME, str(FONT_PATH)))
    else:
        FONT_NAME = "Helvetica"
    log(f"🧠 Font đang sử dụng: {FONT_NAME}", Mau.CYAN)
except Exception as e:
    FONT_NAME = "Helvetica"
    log(f"⚠️ Không thể đăng ký font Arial ({e}), chuyển sang Helvetica.", Mau.VANG)

# === 📏 Lấy kích thước trang PDF ===
with Pdf.open(str(SIGNED_PDF)) as base_check:
    mb = base_check.pages[0].MediaBox
    llx, lly, urx, ury = [float(x) for x in mb]
    page_w, page_h = urx - llx, ury - lly
log(f"📄 Kích thước trang: {page_w:.0f} x {page_h:.0f} pt", Mau.TRANG)

# === ✨ Tạo overlay trong bộ nhớ ===
log("🎨 Đang tạo overlay dấu cá nhân...", Mau.VANG, 0.3)
overlay_buffer = BytesIO()
c = canvas.Canvas(overlay_buffer, pagesize=(page_w, page_h))
c.setFont(FONT_NAME, 14)
try:
    c.setFillAlpha(0.25)
except Exception:
    pass

# Màu nền dấu tròn mờ
stamp_color = Color(0.9, 0.1, 0.1, alpha=0.2)
c.setFillColor(stamp_color)
center_x, center_y = page_w - 70*mm, 40*mm
c.circle(center_x, center_y, 25*mm, fill=1, stroke=0)

# Chữ trong dấu
c.setFillColor(Color(0.8, 0, 0, alpha=0.7))
c.setFont(FONT_NAME, 13)
c.drawCentredString(center_x, center_y + 2*mm, "HẦU THANH HUYỀN")
c.setFont(FONT_NAME, 9)
c.drawCentredString(center_x, center_y - 6*mm, "Ký & xác nhận")

# Ảnh chữ ký nếu có
if SIGN_IMAGE.exists():
    c.drawImage(str(SIGN_IMAGE),
                x=center_x - 20*mm,
                y=center_y + 10*mm,
                width=40*mm,
                height=20*mm,
                mask='auto')
    log("🖼️  Ảnh chữ ký đã chèn vào overlay.", Mau.XANH)
else:
    log("⚠️  Không tìm thấy ảnh chữ ký cá nhân (anhky.jpg).", Mau.VANG)

# Timestamp
ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
c.setFillColor(Color(0.5, 0, 0, alpha=0.6))
c.setFont(FONT_NAME, 8)
c.drawCentredString(center_x, center_y - 15*mm, f"Modified on: {ts}")
c.save()
overlay_buffer.seek(0)
log("✅ Overlay dấu cá nhân đã tạo thành công!", Mau.XANH)

# === 🧷 Ghép overlay lên PDF đã ký ===
log("🔗 Đang ghép overlay vào tài liệu...", Mau.VANG)
with Pdf.open(str(SIGNED_PDF)) as base:
    with Pdf.open(overlay_buffer) as overlay:
        for i, page in enumerate(base.pages):
            page.add_overlay(overlay.pages[0])
            log(f"   → Đã áp dụng dấu lên trang {i+1}", Mau.TRANG, 0.05)
        base.save(str(TAMPERED_PDF))
log(f"💾 File mới đã lưu tại: {TAMPERED_PDF}", Mau.CYAN)
log("────────────────────────────────────────────────────────────", Mau.XAM)
log("🎉 HOÀN TẤT! Chữ ký gốc vẫn được bảo toàn.", Mau.XANH)
log("👩‍💻 Thực hiện bởi: Hau Thanh Huyen", Mau.TRANG)
log("════════════════════════════════════════════════════════════", Mau.CYAN)
