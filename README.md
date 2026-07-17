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
