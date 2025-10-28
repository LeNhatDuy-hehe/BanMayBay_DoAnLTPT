# 🎮 GAME BẮN MÁY BAY 2D - PLANE SHOOTER

Trò chơi bắn máy bay 2D được xây dựng bằng Python và thư viện Pygame. Đây là đồ án môn học Lập trình Python của sinh viên Trường Đại học Nam Cần Thơ.

## 📋 Thông tin dự án

- **Tên dự án:** Lập trình Game Bắn Máy Bay
- **Ngôn ngữ:** Python 3.10+
- **Thư viện chính:** Pygame 2.5.0
- **Trường:** Đại học Nam Cần Thơ
- **Khoa:** Công Nghệ Thông Tin
- **Lớp:** DH22TIN04

## 👥 Nhóm thực hiện

| MSSV | Họ Tên | Vai trò |
|------|--------|---------|
| 223160 | Lê Nhật Duy | Trưởng nhóm - Game Loop, Utils |
| 225234 | Bùi Nhật Anh | UI/UX, HUD, Menu |
| 221355 | Hà Quốc Khởi | Player, Bullet, Item, Explosion |
| 221964 | Nguyễn Minh Khôi | Boss System |
| 223521 | Phạm Huỳnh Như | Enemy, Báo cáo |

## 🎯 Tính năng chính

### Gameplay
- ✈️ Điều khiển máy bay chiến đấu
- 🔫 Hệ thống vũ khí 5 cấp độ (đạn thẳng → xoắn ốc 360°)
- 👾 Nhiều loại địch với độ khó khác nhau
- 👹 2 Boss với 6 patterns tấn công đa dạng
- 🎁 Vật phẩm hỗ trợ (HP, Power-up)
- 💥 Hiệu ứng nổ particles chân thực

### Hệ thống
- 🏆 Lưu điểm cao (Top 5)
- 🎵 Nhạc nền và hiệu ứng âm thanh
- ⏸️ Pause/Resume
- 📊 HUD hiển thị điểm, mạng, cấp độ vũ khí
- 🎬 Màn hình kết thúc đặc biệt (Happy Ending)

## 🔧 Yêu cầu hệ thống

### Tối thiểu
- **OS:** Windows 7/10, Linux, macOS
- **Python:** 3.8+
- **RAM:** 2GB
- **CPU:** Intel Core i3 hoặc tương đương
- **GPU:** Tích hợp (Intel HD Graphics)

### Khuyến nghị
- **OS:** Windows 10/11
- **Python:** 3.10+
- **RAM:** 4GB+
- **CPU:** Intel Core i5 hoặc tương đương
- **GPU:** Dedicated (NVIDIA/AMD)

## 📦 Cài đặt

### Bước 1: Clone repository

```bash
git clone https://github.com/LeNhatDuy-hehe/BanMayBay_DoAnLTPT.git
cd BanMayBay_DoAnLTPT/PhanMem
```

### Bước 2: Cài đặt Python

Tải Python từ: https://www.python.org/downloads/

**Lưu ý:** Tích chọn "Add Python to PATH" khi cài đặt!

### Bước 3: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

Hoặc cài thủ công:

```bash
pip install pygame
```

## 🚀 Chạy game

### Cách 1: Chạy trực tiếp

```bash
cd src
python main.py
```

### Cách 2: Chạy từ thư mục gốc

```bash
python PhanMem/src/main.py
```

### Cách 3: Double-click (Windows)

1. Mở thư mục `PhanMem/src/`
2. Double-click file `main.py`
3. Chọn "Open with Python"

## 🎮 Hướng dẫn chơi

### Điều khiển

| Phím | Chức năng |
|------|-----------|
| **←** | Di chuyển trái |
| **→** | Di chuyển phải |
| **↑** | Di chuyển lên |
| **↓** | Di chuyển xuống |
| **SPACE** | Bắn đạn |
| **P / ESC** | Tạm dừng |

### Mục tiêu

1. Tiêu diệt kẻ địch để ghi điểm
2. Thu thập vật phẩm (HP, Power-up)
3. Đánh bại 2 Boss ở mốc 1000đ và 4000đ
4. Đạt điểm cao nhất có thể

### Gun Levels

- **Level 1:** 1 viên đạn thẳng
- **Level 2:** 2 viên song song
- **Level 3:** 3 viên tỏa (-1°, 0°, +1°)
- **Level 4:** 4 viên tỏa rộng
- **Level 5:** Xoắn ốc 360° + Aura vàng ✨

### Boss Patterns

**Boss 1 (1000 điểm):**
- 🔵 Circle Shot (Đạn tỏa tròn)
- 🌀 Spiral (Xoắn ốc)
- ⚡ Laser (5 tia)

**Boss 2 (4000 điểm):**
- Tất cả patterns của Boss 1
- 🌊 Energy Wave (Sóng năng lượng)
- 🔺 Triple Bullet (3 hướng)
- 🎲 Random Bullets (Ngẫu nhiên)

## 📂 Cấu trúc dự án

```
PhanMem/
├── src/                    # Mã nguồn Python
│   ├── main.py            # File chính
│   ├── player.py          # Người chơi
│   ├── enemy.py           # Kẻ địch
│   ├── boss.py            # Boss
│   ├── bullet.py          # Đạn
│   ├── item.py            # Vật phẩm
│   ├── explosion.py       # Hiệu ứng nổ
│   ├── hud.py             # Giao diện HUD
│   ├── menu.py            # Menu
│   ├── highscores.py      # Quản lý điểm
│   ├── settings.py        # Cấu hình
│   └── utils.py           # Tiện ích
│
├── assets/                 # Tài nguyên
│   ├── image/             # Hình ảnh
│   └── sound/             # Âm thanh
│
├── highscores.json        # Điểm cao
├── requirements.txt       # Thư viện
└── README.md             # File này
```

## 🐛 Xử lý lỗi thường gặp

### Lỗi: "pygame not found"
```bash
pip install pygame --upgrade
```

### Lỗi: "No module named 'src'"
Đảm bảo chạy lệnh từ đúng thư mục:
```bash
cd PhanMem/src
python main.py
```

### Lỗi: Thiếu file assets
Kiểm tra thư mục `assets/` có đầy đủ file image và sound

### Lỗi: FPS thấp
- Giảm số lượng enemies trong `settings.py`
- Tắt các ứng dụng nền đang chạy
- Update driver card màn hình

## 📊 Kết quả kiểm thử

| Chức năng | Trạng thái |
|-----------|------------|
| Di chuyển Player | ✅ Pass |
| Bắn đạn 5 cấp độ | ✅ Pass |
| Va chạm | ✅ Pass |
| Spawn Enemy | ✅ Pass |
| Boss 2 levels | ✅ Pass |
| Items (HP, Power) | ✅ Pass |
| Lưu điểm cao | ✅ Pass |
| Pause/Resume | ✅ Pass |
| FPS 60 | ✅ Pass |

**Hiệu năng:**
- FPS trung bình: 58-60
- RAM: ~170MB
- Thời gian load: 2s

## 🔮 Hướng phát triển

- [ ] Chế độ nhiều người chơi (Multiplayer)
- [ ] Thêm nhiều Boss (Level 3, 4, 5...)
- [ ] Hệ thống nhiệm vụ (Missions)
- [ ] Cửa hàng nâng cấp (Shop/Upgrades)
- [ ] Leaderboard online
- [ ] Port sang Android/iOS
- [ ] Thêm hiệu ứng particle nâng cao
- [ ] AI thông minh hơn cho Enemy

## 📄 License

Dự án này được phát triển cho mục đích học tập tại Trường Đại học Nam Cần Thơ.

## 📞 Liên hệ

- **Email:** lenhatduy@student.ncu.edu.vn
- **GitHub:** https://github.com/LeNhatDuy-hehe/BanMayBay_DoAnLTPT

---

## 🙏 Cảm ơn

Xin cảm ơn:
- Thầy **Đặng Mạnh Huy** - Giảng viên hướng dẫn
- Khoa Công Nghệ Thông Tin - Trường ĐH Nam Cần Thơ
- Cộng đồng Pygame
- Tất cả người chơi đã thử nghiệm game

---

**Made with ❤️ by Team DH22TIN04**

**Cần Thơ, Tháng 10 - 2025**
