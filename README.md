# FastAPI Development Project

Dự án này là một ứng dụng RESTful API cơ bản được phát triển bằng **FastAPI** và kết nối cơ sở dữ liệu **PostgreSQL**. Dự án trình bày hai phương pháp kết nối dữ liệu: **SQL thuần (Raw SQL)** thông qua `psycopg2` và **ORM (Object-Relational Mapping)** thông qua `SQLAlchemy`.

---

## 🛠️ Công Nghệ Sử Dụng

* **Ngôn ngữ:** Python 3.13+
* **Framework:** FastAPI (REST API)
* **Xác thực dữ liệu:** Pydantic v2 (Schemas)
* **Cơ sở dữ liệu:** PostgreSQL
* **ORM:** SQLAlchemy (Object-Relational Mapping)
* **Driver DB:** Psycopg2 (Raw SQL connection)
* **Bảo mật cấu hình:** Pydantic Settings (`.env`)
* **Server chạy ứng dụng:** Uvicorn

---

## 📂 Cấu Trúc Dự Án

```text
fastAPI/
│
├── app/
│   ├── __init__.py      # Khai báo thư mục app là một Package
│   ├── config.py        # Nạp biến môi trường động từ file .env
│   ├── database.py      # Thiết lập kết nối SQLAlchemy (ORM)
│   ├── models.py        # Định nghĩa cấu trúc bảng trong PostgreSQL (ORM Model)
│   ├── main.py          # File chính khởi chạy ứng dụng & định nghĩa các API Endpoints
│   └── test.py          # Script chạy nhanh Uvicorn server ở port 5000
│
├── .env                 # File lưu trữ biến môi trường bảo mật (Chỉ lưu cục bộ)
├── .env.example         # File cấu hình mẫu làm ví dụ
├── .gitignore           # Cấu hình bỏ qua khi push git lên GitHub
└── README.md            # Tài liệu hướng dẫn sử dụng dự án
```

---

## ⚙️ Hướng Dẫn Cài Đặt

### 1. Kích hoạt môi trường ảo (Virtual Environment)
* **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
* **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 2. Cài đặt các thư viện cần thiết
```bash
pip install fastapi uvicorn psycopg2-binary sqlalchemy pydantic-settings python-dotenv
```

### 3. Cấu hình biến môi trường (`.env`)
Tạo một file tên `.env` ở thư mục gốc của dự án bằng cách sao chép từ file `.env.example` và điền mật khẩu PostgreSQL của bạn:
```bash
cp .env.example .env
```
Nội dung file `.env` cần thiết lập:
```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=mat_khau_cua_ban
DATABASE_NAME=fastAPI
DATABASE_USERNAME=postgres
```

---

## 🚀 Khởi Chạy Ứng Dụng

Chạy câu lệnh sau tại thư mục gốc của dự án để khởi động API:
```bash
uvicorn app.main:app --reload
```
Server sẽ chạy mặc định tại địa chỉ: `http://127.0.0.1:8000`

Bạn có thể truy cập tài liệu API tự động sinh bởi FastAPI (Swagger UI) tại: `http://127.0.0.1:8000/docs`

---

## 🛰️ Danh Sách API Endpoints (Tổng Quan)

| Phương thức | Đường dẫn (URL) | Mô tả | Xử lý bằng |
| :--- | :--- | :--- | :--- |
| **GET** | `/post` | Chào mừng / Kiểm tra server | FastAPI |
| **GET** | `/posts` | Lấy danh sách tất cả bài viết | SQL Thuần |
| **POST** | `/createposts` | Tạo mới một bài viết | SQLAlchemy ORM |
| **GET** | `/post/{id}` | Lấy chi tiết bài viết theo ID | SQLAlchemy ORM |
| **DELETE** | `/post/{id}` | Xóa một bài viết theo ID | SQLAlchemy ORM |
| **PUT** | `/post/{id}` | Cập nhật bài viết theo ID (Chỉ trường gửi lên) | SQLAlchemy ORM |
| **GET** | `/sqlalchemy` | Lấy danh sách tất cả bài viết | SQLAlchemy ORM |
| **POST** | `/createuser` | Tạo mới một người dùng | SQLAlchemy ORM |
| **GET** | `/getuser/{id}` | Lấy chi tiết người dùng theo ID | SQLAlchemy ORM |
| **GET** | `/allUser` | Lấy danh sách tất cả người dùng | SQLAlchemy ORM |
| **POST** | `/login` | Đăng nhập hệ thống | SQLAlchemy ORM + JWT |

---

## 🌐 Triển Khai Thực Tế (Production Deployment Setup)

Dự án đã được cấu hình triển khai thực tế trên môi trường Linux (WSL Ubuntu) kết hợp giữa **Gunicorn**, **Nginx** và **DuckDNS**. Dưới đây là mô tả chi tiết các thành phần cấu hình:

### 1. Đồng bộ hóa Mật khẩu PostgreSQL
- **Mục đích:** Đồng bộ thông tin truy cập cơ sở dữ liệu trên cả Windows và Linux.
- **Thực hiện:**
  - Cập nhật mật khẩu Linux user `postgres` và database user `postgres` thành `123456789`.
  - Cấu hình file `.env` trỏ về `127.0.0.1` để ứng dụng kết nối trực tiếp với PostgreSQL chạy trong WSL.

### 2. Chạy ngầm Ứng dụng bằng Gunicorn & Systemd
- **Mục đích:** Chạy ngầm FastAPI vĩnh viễn dưới nền và tự động khởi động cùng hệ thống khi bật máy ảo mà không cần mở Terminal thủ công.
- **Tệp cấu hình:** [gunicorn.service](file:///c:/Users/nhung/Downloads/fastAPI/gunicorn.service) (đã được lưu trong thư mục gốc dự án và liên kết vào hệ thống tại `/etc/systemd/system/gunicorn.service`).
- **Lệnh quản lý:**
  - Khởi động: `sudo systemctl start gunicorn`
  - Dừng: `sudo systemctl stop gunicorn`
  - Khởi động lại (khi cập nhật code): `sudo systemctl restart gunicorn`
  - Xem trạng thái: `sudo systemctl status gunicorn`

### 3. Cấu hình Nginx làm Reverse Proxy
- **Mục đích:** Nginx lắng nghe ở cổng mặc định `80`, nhận yêu cầu từ trình duyệt ngoài và chuyển tiếp vào Gunicorn (cổng `8000`). Giúp người dùng không cần gõ số cổng `:8000` trên trình duyệt và tăng tính bảo mật, hiệu năng phục vụ.
- **Tệp cấu hình hệ thống:** `/etc/nginx/sites-available/default`
- **Lệnh quản lý:**
  - Kiểm tra cú pháp: `sudo nginx -t`
  - Khởi động lại: `sudo systemctl restart nginx`

### 4. Tên miền phụ miễn phí qua DuckDNS
- **Mục đích:** Thay thế địa chỉ IP thô bằng tên miền dễ nhớ, hỗ trợ cấu hình HTTPS sau này.
- **Tên miền phụ:** `truongkietfastapi.duckdns.org` (đã được trỏ về IP của máy Linux `172.23.202.173`).
- **Cách truy cập:**
  - Trang tài liệu API: `http://truongkietfastapi.duckdns.org/docs`
  - Trang chủ: `http://truongkietfastapi.duckdns.org`

