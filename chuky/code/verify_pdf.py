# ==========================================
# 🔒 PDF SIGNATURE VALIDATION TOOL
# Người phát triển: Hau Thanh Huyen
# ==========================================
import os, io, hashlib, datetime, sys
from datetime import timezone, timedelta
from pyhanko.sign import validation
from pyhanko.sign.diff_analysis import ModificationLevel
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.keys import load_cert_from_pemder
from pyhanko_certvalidator import ValidationContext

# === 🎨 Màu chữ trong console ===
class Mau:
    RESET = "\033[0m"
    XANH = "\033[92m"
    DO = "\033[91m"
    VANG = "\033[93m"
    CYAN = "\033[96m"
    DAM = "\033[95m"
    XAM = "\033[90m"
    TRANG = "\033[97m"

# Windows CMD cũ có thể không hỗ trợ ANSI escape → bỏ màu
if os.name == "nt" and "WT_SESSION" not in os.environ:
    for attr in dir(Mau):
        if not attr.startswith("__"):
            setattr(Mau, attr, "")

# === ⚙️ Cấu hình ===
DUONG_DAN_PDF = r"F:\\chuky\\pdf\\signed.pdf"
DUONG_DAN_CHUNG_THU = r"F:\\chuky\\keys\\signer_cert.pem"
DUONG_DAN_LOG = r"F:\\chuky\\canhbao.txt"

# === ✍️ Hàm ghi log ===
def ghi_log(noi_dung, mau=Mau.TRANG, indent=0):
    prefix = " " * indent
    print(prefix + mau + noi_dung + Mau.RESET)
    with open(DUONG_DAN_LOG, "a", encoding="utf-8") as f:
        f.write(noi_dung + "\n")

# === 🚀 Giao diện đầu ===
if os.path.exists(DUONG_DAN_LOG):
    os.remove(DUONG_DAN_LOG)

print(Mau.CYAN + "╔════════════════════════════════════════════════════════════╗")
print(Mau.CYAN + "║          🔒  HỆ THỐNG KIỂM TRA CHỮ KÝ PDF  V1.0            ║")
print(Mau.CYAN + "╚════════════════════════════════════════════════════════════╝" + Mau.RESET)
ghi_log(f"📅  Thời điểm kiểm tra: {datetime.datetime.now()}", Mau.TRANG)
ghi_log(f"📄  File cần xác thực:  {DUONG_DAN_PDF}", Mau.TRANG)
ghi_log("────────────────────────────────────────────────────────────", Mau.XAM)

# === 🧾 Nạp chứng thư tin cậy ===
try:
    ghi_log("🔸 Đang tải chứng thư tin cậy...", Mau.VANG)
    chung_thu_tin_cay = load_cert_from_pemder(DUONG_DAN_CHUNG_THU)
    ngu_canh = ValidationContext(trust_roots=[chung_thu_tin_cay])
    ghi_log("✅  Chứng thư nạp thành công!", Mau.XANH, indent=2)
except Exception as loi:
    ghi_log(f"❌  Lỗi khi tải chứng thư: {loi}", Mau.DO)
    sys.exit(1)

# === 📄 Mở PDF và kiểm tra chữ ký ===
try:
    with open(DUONG_DAN_PDF, "rb") as tep_pdf:
        pdf_doc = PdfFileReader(tep_pdf, strict=False)
        ds_chu_ky = pdf_doc.embedded_signatures

        if not ds_chu_ky:
            ghi_log("❌  Không tìm thấy chữ ký nào trong PDF.", Mau.DO)
            sys.exit(1)

        chu_ky = ds_chu_ky[0]
        ten_truong = chu_ky.field_name or "Signature1"
        ghi_log("────────────────────────────────────────────────────────────", Mau.XAM)
        ghi_log("📑  THÔNG TIN CHỮ KÝ PHÁT HIỆN:", Mau.CYAN)
        ghi_log(f"   ✒️  Tên trường chữ ký: {ten_truong}", Mau.VANG)
        doi_tuong = chu_ky.sig_object
        byte_range = doi_tuong.get('/ByteRange')
        kich_thuoc = len(doi_tuong.get('/Contents'))
        ghi_log(f"   📦  Kích thước vùng ký: {kich_thuoc} byte", Mau.TRANG)
        ghi_log(f"   🔢  ByteRange: {byte_range}", Mau.TRANG)

        # === 🧮 Hash SHA256 ===
        tep_pdf.seek(0)
        du_lieu = tep_pdf.read()
        br = list(byte_range)
        du_lieu_ky = du_lieu[br[0]:br[0]+br[1]] + du_lieu[br[2]:br[2]+br[3]]
        sha256_val = hashlib.sha256(du_lieu_ky).hexdigest()
        ghi_log(f"   🔑  SHA256: {sha256_val[:64]}...", Mau.CYAN)

        # === Xác thực chữ ký ===
        ghi_log("────────────────────────────────────────────────────────────", Mau.XAM)
        ghi_log("🧩  ĐANG TIẾN HÀNH XÁC THỰC...", Mau.VANG)
        try:
            ket_qua = validation.validate_pdf_signature(chu_ky, ngu_canh)
            ghi_log("✅  Hoàn tất xác thực chữ ký.", Mau.XANH, indent=2)
        except Exception as e:
            ghi_log(f"⚠️  Không thể xác thực: {e}", Mau.DO)
            sys.exit(1)

        # === In kết quả ===
        ghi_log("────────────────────────────────────────────────────────────", Mau.XAM)
        ghi_log("📊  KẾT QUẢ CHI TIẾT:", Mau.DAM)
        ghi_log(ket_qua.pretty_print_details(), Mau.TRANG, indent=2)

        # === 👤 Thông tin người ký ===
        cert = getattr(ket_qua, "signing_cert", None)
        if cert:
            ghi_log("\n👤  THÔNG TIN NGƯỜI KÝ:", Mau.VANG)
            ghi_log(f"   • Chủ thể: {cert.subject.human_friendly}", Mau.TRANG)
            sha1 = cert.sha1_fingerprint
            sha256 = cert.sha256_fingerprint
            sha1 = sha1 if isinstance(sha1, str) else sha1.hex()
            sha256 = sha256 if isinstance(sha256, str) else sha256.hex()
            ghi_log(f"   • SHA1: {sha1}", Mau.XAM)
            ghi_log(f"   • SHA256: {sha256}", Mau.XAM)
        else:
            ghi_log("⚠️  Không thể đọc chứng thư người ký.", Mau.DO)

        # === 🕒 Thời gian ký ===
        thoi_gian = getattr(ket_qua, "signer_reported_dt", None)
        if thoi_gian:
            vn_time = thoi_gian.astimezone(timezone(timedelta(hours=7)))
            ghi_log(f"\n🕒  Thời gian ký (VN): {vn_time}", Mau.TRANG)
        else:
            ghi_log("⚠️  Không có timestamp.", Mau.VANG)

        # === Kiểm tra chỉnh sửa ===
        muc_do = getattr(ket_qua, "modification_level", None)
        ghi_log("\n🧭  TÌNH TRẠNG TÀI LIỆU:", Mau.CYAN)
        if muc_do == ModificationLevel.NONE:
            ghi_log("   ✅  Không phát hiện chỉnh sửa sau khi ký.", Mau.XANH)
        elif muc_do == ModificationLevel.FORM_FILLING:
            ghi_log("   ⚠️  Có chỉnh sửa nhẹ (biểu mẫu).", Mau.VANG)
        else:
            ghi_log("   ❌  Phát hiện chỉnh sửa nội dung!", Mau.DO)

        # === Tổng kết ===
        ghi_log("────────────────────────────────────────────────────────────", Mau.XAM)
        if getattr(ket_qua, "bottom_line", False):
            ghi_log("🎉  KẾT QUẢ CUỐI: CHỮ KÝ HỢP LỆ – FILE NGUYÊN VẸN.", Mau.XANH)
        else:
            ghi_log("💀  KẾT QUẢ CUỐI: CHỮ KÝ KHÔNG HỢP LỆ HOẶC FILE BỊ SỬA.", Mau.DO)

except Exception as loi:
    ghi_log(f"💥  Lỗi hệ thống: {loi}", Mau.DO)

ghi_log("────────────────────────────────────────────────────────────", Mau.XAM)
ghi_log("✅  Hoàn tất kiểm tra – kết quả lưu tại canhbao.txt", Mau.XANH)
ghi_log("👨‍💻  Người thực hiện: Hau Thanh Huyen", Mau.TRANG)
ghi_log("════════════════════════════════════════════════════════════", Mau.CYAN)
