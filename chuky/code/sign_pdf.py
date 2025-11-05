# ==========================================
# sign_pdf.py - Ký số tài liệu PDF bằng chứng chỉ tự ký (self-signed)
# Cá nhân hóa bởi: Hau Thanh Huyen
# ==========================================

from datetime import datetime
from pyhanko.sign import signers, fields
from pyhanko.stamp.text import TextStampStyle
from pyhanko.pdf_utils import images
from pyhanko.pdf_utils.text import TextBoxStyle
from pyhanko.pdf_utils.layout import SimpleBoxLayoutRule, AxisAlignment, Margins
from pyhanko.sign.general import load_cert_from_pemder, SigningError
from pyhanko_certvalidator import ValidationContext
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign.fields import SigFieldSpec
import os

# === 🗂️ CẤU HÌNH ĐƯỜNG DẪN ===
BASE_DIR = r"F:\chuky"
PDF_IN = os.path.join(BASE_DIR, "pdf", "original.pdf")
PDF_OUT = os.path.join(BASE_DIR, "pdf", "signed.pdf")
KEY_FILE = os.path.join(BASE_DIR, "keys", "signer_key.pem")
CERT_FILE = os.path.join(BASE_DIR, "keys", "signer_cert.pem")
SIG_IMG = os.path.join(BASE_DIR, "anhky", "anhky.jpg")

print("==========================================")
print("🖋️  BẮT ĐẦU QUÁ TRÌNH KÝ SỐ TÀI LIỆU PDF")
print("==========================================")
print("Bước 1️⃣: Chuẩn bị file PDF gốc:", PDF_IN)

# --- 🔑 Tạo signer và ValidationContext ---
signer = signers.SimpleSigner.load(KEY_FILE, CERT_FILE, key_passphrase=None)
vc = ValidationContext(trust_roots=[load_cert_from_pemder(CERT_FILE)])

# --- ✍️ Bắt đầu tiến trình ký ---
try:
    with open(PDF_IN, "rb") as inf:
        # ⚙️ Cho phép hybrid xref bằng cách tắt strict mode
        writer = IncrementalPdfFileWriter(inf, strict=False)

        # 🟢 Xác định số trang trong PDF
        try:
            pages = writer.root["/Pages"]
            num_pages = int(pages.get("/Count", 1))
        except Exception:
            num_pages = 1

        target_page = num_pages - 1
        print(f"Bước 2️⃣: Thêm trường chữ ký ở trang {target_page + 1}...")

        # 🟩 Thêm vùng chữ ký ở góc phải dưới
        fields.append_signature_field(
            writer,
            SigFieldSpec(
                sig_field_name="Signature_HauThanhHuyen",
                box=(240, 50, 550, 150),
                on_page=target_page
            )
        )

        # 🖼️ Hình ảnh chữ ký tay
        background_img = images.PdfImage(SIG_IMG)

        # --- 📐 Bố cục khung chữ ký ---
        bg_layout = SimpleBoxLayoutRule(
            x_align=AxisAlignment.ALIGN_MIN,
            y_align=AxisAlignment.ALIGN_MID,
            margins=Margins(right=20)
        )
        text_layout = SimpleBoxLayoutRule(
            x_align=AxisAlignment.ALIGN_MIN,
            y_align=AxisAlignment.ALIGN_MID,
            margins=Margins(left=150)
        )
        text_style = TextBoxStyle(font_size=13)

# 🕒 Thông tin chữ ký hiển thị trong tem
        ngay_ky = datetime.now().strftime("%d/%m/%Y")
        stamp_text = (
            "Hau Thanh Huyen"
            "\nSDT: 0199999999"
            "\nMSSV: k225480106027"
            "\ndiachi: Phu Luong"
            f"\nNgày ký: {ngay_ky}"
        )

        # --- 🪶 Cấu trúc khung hiển thị chữ ký ---
        stamp_style = TextStampStyle(
            stamp_text=stamp_text,
            background=background_img,
            background_layout=bg_layout,
            inner_content_layout=text_layout,
            text_box_style=text_style,
            border_width=1,
            background_opacity=1.0,
        )

        # --- 🧾 Thông tin metadata của chữ ký ---
        meta = signers.PdfSignatureMetadata(
            field_name="Signature_HauThanhHuyen",
            reason="Bài tập: Ký số PDF bằng Python - Lớp K58",
            location="Vietnam",
            md_algorithm="sha256",
        )

        # --- 🧑‍💻 Khởi tạo signer ---
        pdf_signer = signers.PdfSigner(
            signature_meta=meta,
            signer=signer,
            stamp_style=stamp_style,
        )

        print("Bước 3️⃣: Tạo PKCS#7 (messageDigest, signingTime, contentType)...")
        print("Bước 4️⃣: Tiến hành ký...")

        # --- ✨ Tiến hành ký số tài liệu ---
        with open(PDF_OUT, "wb") as outf:
            pdf_signer.sign_pdf(writer, output=outf)

        print("\n✅ HOÀN TẤT KÝ SỐ!")
        print("📄 File đã lưu tại:", PDF_OUT)
        print("🧾 Có thể kiểm tra chữ ký bằng verify_check_vn.py")

except SigningError as e:
    print("\n❌ LỖI KHI KÝ:", e)
    print("👉 Nếu PDF gốc có hybrid xref, hãy normalize lại bằng pikepdf trước khi ký.")
except Exception as e:
    print("\n❌ LỖI KHÔNG XÁC ĐỊNH:", e)
    print("⚠️ Kiểm tra lại đường dẫn file hoặc định dạng PDF.")

print("==========================================")
print("🏁 HOÀN TẤT QUÁ TRÌNH KÝ PDF")
print("==========================================")
