# btap-2-bao-mat-an-toan-thong-tin
Chữ kí số
# Các file cần có trong quá trình làm bài chữ kí số
<img width="372" height="426" alt="image" src="https://github.com/user-attachments/assets/1f1b4b1d-a00b-4c4c-b7ae-01334dde6dae" />

# Trước tiên trong quy trình chữ ký số là tạo khóa gen_keys.py.

## Mục đích: Tạo ra các thành phần bảo mật cốt lõi: Khóa Bí mật (signer_key.pem) và Chứng chỉ (signer_cert.pem).

<img width="1442" height="548" alt="image" src="https://github.com/user-attachments/assets/8db260f1-ed10-4ed5-857d-ecd3655c8658" />

# sign_pdf.py (Ký Tài liệu)
<img width="1919" height="690" alt="image" src="https://github.com/user-attachments/assets/6895c039-38d9-4e3d-ad7a-77ca1b45c606" />

## Mục đích: Dùng Khóa Bí mật vừa tạo để ký vào original.pdf, tạo ra signed.pdf.

<img width="1126" height="649" alt="image" src="https://github.com/user-attachments/assets/1b30d126-ce49-429a-9aa6-bfa287908dce" />

# verify_pdf.py hoặc tampered.py (Xác minh/Giả mạo)

## verify_pdf.py được dùng để kiểm tra tính hợp lệ của signed.pdf (cần Khóa Công khai trong signer_cert.pem).

<img width="1286" height="553" alt="image" src="https://github.com/user-attachments/assets/a3dcaf8b-bb37-4cab-809d-cbba374e768f" />

<img width="1567" height="570" alt="image" src="https://github.com/user-attachments/assets/2e638fd2-848f-4fb3-b612-49e58489e58a" />

## tampered.py được dùng để sửa đổi signed.pdf thành tampered.pdf để phục vụ cho việc kiểm thử tính năng phát hiện giả mạo của verify_pdf.py.

<img width="1387" height="656" alt="image" src="https://github.com/user-attachments/assets/0b3e7e1b-b8ca-48b3-8837-269d877f9fe0" />

<img width="1866" height="797" alt="image" src="https://github.com/user-attachments/assets/d44809db-10aa-4b69-853a-db5d69606b5b" />


