# ==========================================================
# 🔑 gen_keys.py – TẠO CẶP KHÓA & CHỨNG CHỈ TỰ KÝ (SELF-SIGNED)
# 📜 Dành cho thử nghiệm ký số PDF (phiên bản hiển thị đẹp)
# 👩‍💻 Cá nhân hóa bởi: Hau Thanh Huyen
# ==========================================================

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
import os, time, sys

# === 🎨 Định nghĩa màu (ANSI console) ===
class Mau:
    RESET = "\033[0m"
    XANH = "\033[92m"
    DO = "\033[91m"
    VANG = "\033[93m"
    CYAN = "\033[96m"
    XAM = "\033[90m"
    TRANG = "\033[97m"
    TIM = "\033[95m"

# Windows CMD không hỗ trợ ANSI => tắt màu
if os.name == "nt" and "WT_SESSION" not in os.environ:
    for attr in dir(Mau):
        if not attr.startswith("__"):
            setattr(Mau, attr, "")

# === 🧾 Hàm in định dạng ===
def log(msg, color=Mau.TRANG, delay=0.0, indent=0):
    prefix = " " * indent
    print(prefix + color + msg + Mau.RESET)
    if delay:
        time.sleep(delay)

# === 💫 Tiêu đề chương trình ===
print(Mau.CYAN + "╔════════════════════════════════════════════════════════════╗")
print(Mau.CYAN + "║    🔑  GEN_KEYS – TẠO CẶP KHÓA & CHỨNG CHỈ TỰ KÝ (V2.0)    ║")
print(Mau.CYAN + "╚════════════════════════════════════════════════════════════╝" + Mau.RESET)

# === 🗂️ Cấu hình đường dẫn ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR = os.path.join(BASE_DIR, "..", "keys")
os.makedirs(KEYS_DIR, exist_ok=True)

PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, "signer_key.pem")
CERT_PATH = os.path.join(KEYS_DIR, "signer_cert.pem")

log("📁 Thư mục lưu trữ khóa:", Mau.VANG)
log(f"   → {KEYS_DIR}", Mau.TRANG)
time.sleep(0.5)

# === 1️⃣ Tạo khóa riêng RSA 2048-bit ===
log("🔐 Đang tạo khóa riêng RSA 2048-bit...", Mau.CYAN)
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
time.sleep(0.6)
log("✅ Hoàn tất tạo khóa riêng.", Mau.XANH)

# === 2️⃣ Tạo chứng chỉ tự ký ===
log("📜 Đang tạo chứng chỉ tự ký (Self-signed Certificate)...", Mau.CYAN)
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "VN"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Thai Nguyen"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Thai Nguyen"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Hau Thanh Huyen"),
    x509.NameAttribute(NameOID.COMMON_NAME, "Hau Thanh Huyen Signature Authority"),
    x509.NameAttribute(NameOID.EMAIL_ADDRESS, "hau.thanh.huyen@gmail.com"),
])
time.sleep(0.6)

# === 3️⃣ Xây dựng certificate ===
cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(private_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.utcnow())
    .not_valid_after(datetime.utcnow() + timedelta(days=730))  # 2 năm
    .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
    .add_extension(x509.SubjectAlternativeName([x509.DNSName("hau-thanh-huyen.dev")]), critical=False)
    .sign(private_key, hashes.SHA256())
)
log("✅ Chứng chỉ đã được tạo thành công.", Mau.XANH)

# === 4️⃣ Ghi private key ===
log("💾 Đang lưu private key...", Mau.VANG)
with open(PRIVATE_KEY_PATH, "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
log(f"   → Đã lưu tại: {PRIVATE_KEY_PATH}", Mau.TRANG)

# === 5️⃣ Ghi certificate ===
log("💾 Đang lưu certificate...", Mau.VANG)
with open(CERT_PATH, "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))
log(f"   → Đã lưu tại: {CERT_PATH}", Mau.TRANG)

# === 🎯 Hoàn tất ===
log("────────────────────────────────────────────────────────────", Mau.XAM)
log("🎉 TẠO CẶP KHÓA & CHỨNG CHỈ TỰ KÝ THÀNH CÔNG!", Mau.XANH)
log("👩‍💻 Thực hiện bởi: Hau Thanh Huyen", Mau.TRANG)
log("📆 Hiệu lực chứng chỉ: 2 năm kể từ ngày tạo", Mau.VANG)
log("════════════════════════════════════════════════════════════", Mau.CYAN)
