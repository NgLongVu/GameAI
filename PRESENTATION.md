---
marp: true
theme: default
class: lead
backgroundColor: '#f8f9fa'
paginate: true
---

# BÁO CÁO BÀI TẬP LỚN: MÔN TRÍ TUỆ NHÂN TẠO 
## Đề tài: Trò chơi Catch The Thief (Cảnh sát bắt cướp)

**Nhóm thực hiện: Nhóm 05**
1. Nguyễn Quốc Hiệu - 232631001
2. Vũ Khánh Minh
3. Vũ (Nguyễn Long Vũ - *tên repository*)

**Giảng viên hướng dẫn:** [Tên Giảng Viên]

---

# MỤC LỤC
1. Tổng quan đề tài & Mục tiêu dự án
2. Cơ chế & Phân tích luật chơi
3. Thuật toán Trí tuệ nhân tạo (AI) đã áp dụng
4. Cấu trúc chương trình & Giải pháp kỹ thuật
5. Tính năng bổ trợ & Vật phẩm
6. Chạy thử nghiệm (Demo)
7. Tổng kết & Định hướng phát triển

---

# 1. TỔNG QUAN ĐỀ TÀI & MỤC TIÊU DỰ ÁN

**Catch The Thief** là một tựa game chiến thuật theo lượt (Turn-based strategy) được phát triển bằng ngôn ngữ Python (thư viện Pygame).

- **Khái quát:** Game mô phỏng cuộc rượt đuổi nghẹt thở giữa Đội Cảnh Sát (do người chơi điều khiển) và Tên Trộm (do hệ thống AI điều khiển) trên một bản đồ hình mạng lưới đồ thị.
- **Mục tiêu của môn học:** 
  - Áp dụng các thuật toán tìm kiếm trên không gian trạng thái (Graph Search, Pathfinding).
  - Xây dựng hệ thống Heuristic để Bot (AI) biết cách đưa ra quyết định thông minh nhất nhằm trốn thoát hoặc kéo dài thời gian sinh tồn.
- **Vai trò:**
  - **Người chơi:** Huy động lực lượng cảnh sát vây bắt.
  - **AI Bot:** Trốn thoát tới điểm ra (Exit node) hoặc tránh xa cảnh sát nhất có thể.

---

# 2. CƠ CHẾ & PHÂN TÍCH LUẬT CHƠI

Môi trường trò chơi là một **Đồ thị vô hướng (Undirected Graph)** gồm các Node (điểm đứng) và Edge (đường nối).

### Điều kiện thắng thua
- **Người chơi (Cảnh sát) thắng:** Bắt được tên trộm (cùng đứng trên 1 node) hoặc dồn tên trộm vào bước đường cùng không còn node liền kề nào để đi.
- **AI (Tên trộm) thắng:** Đi trót lọt đến các điểm "Exit Nodes" (Điểm thoát hiểm) đã được đánh dấu sẵn trên bản đồ.

### Luật di chuyển
- **Turn-based:** Cảnh sát đi 1 bước (chỉ 1 cảnh sát trong đội được di chuyển mỗi lượt) -> Tên trộm đi 1 bước.
- Mỗi nhân vật chỉ được phép đi tới các Node kề cạnh (Neighbor Nodes) thông qua các Edge.

---

# 3. THUẬT TOÁN AI ĐƯỢC ÁP DỤNG (1/2)

Hệ thống AI của Tên trộm đóng vai trò là "bộ não" của dự án, đánh giá tính khả thi dựa trên hàm **Heuristic** và các giải thuật duyệt đồ thị:

- **Pathfinding (Tìm đường):**
  - AI sử dụng thuật toán Duyệt theo chiều rộng (BFS) để tìm ra đường đi ngắn nhất từ vị trí hiện tại của mình tới tất cả các điểm Exit.
  - BFS cũng được dùng để đo khoảng cách ngắn nhất từ tên trộm đến từng viên cảnh sát.

- **Đánh giá Node kề (Heuristic Function):**
  Khi tới lượt, AI sẽ duyệt qua tất cả các Node kề (hợp lệ, không bị cảnh sát chặn) và gán điểm (Score) cho từng Node. Node nào có điểm cao nhất sẽ được chọn làm nước đi.

---

# 4. THUẬT TOÁN AI ĐƯỢC ÁP DỤNG (2/2)

Tiêu chí tính điểm của AI (Heuristic Factors):
1. **Khoảng cách tới Cảnh sát (Ưu tiên Sống còn):** Node càng xa đội cảnh sát thì điểm càng cao.
2. **Khoảng cách tới Lối thoát (Ưu tiên Trốn thoát):** Node càng gần điểm Exit thì điểm càng cao.
3. **Mức độ "Tự do" (Tránh góc chết):** AI kiểm tra xem Node tiếp theo có bao nhiêu lối rẽ. Nếu Node đó đi vào ngõ cụt (Dead end), AI sẽ trừ điểm nặng hoặc né tránh.
4. **Cơ chế Rerouting:** Nếu lối thoát bị cảnh sát chặn hoàn toàn, AI sẽ chuyển trạng thái sang "Cố thủ" – chạy vòng quanh để câu giờ, đợi người chơi đi sai nước.

---

# 5. CẤU TRÚC CHƯƠNG TRÌNH & KỸ THUẬT

Dự án được triển khai theo mô hình lập trình hướng đối tượng (OOP) sạch, với các module chức năng riêng biệt:

- `core/board.py & entities.py`: Khởi tạo bản đồ đồ thị từ file JSON, định nghĩa các thuộc tính cốt lõi của Cảnh sát và Trộm.
- `ai/bot.py & pathfinding.py`: Chứa các hàm xử lý thuật toán tính toán đường đi, gán điểm và ra quyết định.
- `ui/`: Các thành phần giao diện (Main Menu sinh động, Chọn Level, Cài đặt).
- **Hệ thống Save/Load (`save_manager.py`):** Theo dõi quá trình chơi, lưu trữ số Vàng (Coins) và số Level (Map) đã mở khóa vào file `player_save.json`.
- **Dynamic Resolution:** Tự động scale cửa sổ hiển thị theo kích thước màn hình người dùng, hỗ trợ Responsive UI hoàn chỉnh.

---

# 6. TÍNH NĂNG BỔ TRỢ & VẬT PHẨM (POWER-UPS)

Để tăng tính chiến thuật và thú vị cho Game, nhóm tích hợp hệ thống kinh tế (Coins) và vật phẩm phụ trợ:

- **Hệ thống phần thưởng:** Khi chiến thắng một level, người chơi nhận được tiền vàng.
- **Sử dụng Vàng để kích hoạt kỹ năng:**
  - 🔄 **UNDO (Hoàn tác - Tốn 10 Coins):** Quay ngược lại 1 lượt đi nếu lỡ đi nhầm (thuật toán sẽ lấy lại state từ lịch sử `history`).
  - ❄️ **FREEZE (Đóng băng - Tốn 15 Coins):** Đóng băng tên trộm trong 1 lượt (AI bị mất lượt), giúp đội cảnh sát rút ngắn khoảng cách bao vây. 

---

# 7. THIẾT KẾ CÁC MÀN CHƠI (LEVEL DESIGN)

Trò chơi sở hữu 8 bản đồ đồ thị (Map) được cấu hình dưới dạng tệp `JSON`.

- **Màn 1 -> Màn 3:** Đồ thị đơn giản, ít cảnh sát, là các vòng hướng dẫn cơ bản.
- **Màn 4 -> Màn 6:** Đồ thị phức tạp hơn, nhiều điểm thắt cổ chai (bottlenecks), yêu cầu người chơi phối hợp nhiều cảnh sát để khóa đường.
- **Màn 7 & Màn 8:** Đồ thị mạng nhện quy mô lớn. AI có quá nhiều phương án lựa chọn, đòi hỏi người chơi vận dụng tối đa các kỹ năng Undo và Freeze để bao vây.

---

# 8. TỔNG KẾT & ĐỊNH HƯỚNG PHÁT TRIỂN

### Kết quả đạt được:
- Nhóm đã hiện thực hóa thành công bài toán Cảnh sát bắt cướp trên lý thuyết đồ thị.
- Trải nghiệm game mượt mà, giao diện đẹp, AI có khả năng lẩn trốn gây khó dễ thực sự cho người chơi.

### Định hướng tương lai:
1. Nâng cấp thuật toán AI (Áp dụng thuật toán **Minimax** với Alpha-Beta Pruning để tên trộm có khả năng tính toán trước 3-4 nước đi của cảnh sát).
2. Tích hợp tính năng tạo bản đồ (Map Builder) để người chơi tự vẽ đồ thị của riêng mình.
3. Chế độ PvP (Người vs Người).

---

# XIN CHÂN THÀNH CẢM ƠN!
## Q&A (Hỏi Đáp)

**Thành viên Nhóm 05 sẵn sàng trả lời các câu hỏi từ thầy cô và các bạn.**

*(1) Nguyễn Quốc Hiệu - 232631001*
*(2) Vũ Khánh Minh*
*(3) Vũ*
