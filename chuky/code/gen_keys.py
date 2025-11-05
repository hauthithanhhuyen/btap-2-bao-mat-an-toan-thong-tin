# ==========================================
# gen_keys.py - Tạo cặp khóa RSA + chứng chỉ tự ký (self-signed)
# Dùng cho thử nghiệm ký số PDF (không dùng khóa thương mại)
# Cá nhân hóa bởi: Hau Thanh Huyen
# ==========================================

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
import os

# === 🗂️ Cấu hình đường dẫn lưu file ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR = os.path.join(BASE_DIR, "..", "keys")
os.makedirs(KEYS_DIR, exist_ok=True)

PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, "signer_key.pem")
CERT_PATH = os.path.join(KEYS_DIR, "signer_cert.pem")

# === 1️⃣ Tạo khóa riêng RSA 2048-bit ===
print("🔐 Đang tạo private key RSA 2048-bit...")
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# === 2️⃣ Tạo chứng chỉ tự ký (self-signed certificate) ===
print("📜 Đang tạo chứng chỉ tự ký (self-signed certificate)...")

# 👇 Thông tin định danh cá nhân hóa
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "VN"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Thai Nguyen"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Thai Nguyen"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Hau Thanh Huyen"),
    x509.NameAttribute(NameOID.COMMON_NAME, "Hau Thanh Huyen Signature Authority"),
    x509.NameAttribute(NameOID.EMAIL_ADDRESS, "hau.thanh.huyen@gmail.com"),
])

# === 3️⃣ Xây dựng certificate ===
cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(private_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.utcnow())
    .not_valid_after(datetime.utcnow() + timedelta(days=730))  # hiệu lực 2 năm
    .add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True,
    )
    .add_extension(
        x509.SubjectAlternativeName([x509.DNSName("hau-thanh-huyen.dev")]),
        critical=False,
    )
    .sign(private_key, hashes.SHA256())
)

# === 4️⃣ Ghi file private key ===
with open(PRIVATE_KEY_PATH, "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
print(f"✅ Đã lưu private key tại: {PRIVATE_KEY_PATH}")

# === 5️⃣ Ghi file certificate ===
with open(CERT_PATH, "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))
print(f"✅ Đã lưu certificate tại: {CERT_PATH}")

# === 🎯 Hoàn tất ===
print("\n🎉 Tạo cặp khóa & chứng chỉ tự ký thành công!")
print("📁 Khóa và chứng chỉ đã sẵn sàng để sử dụng cho quá trình ký số PDF.")
