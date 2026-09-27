---
name: dau-thau
description: Kỹ năng tư vấn đấu thầu cho chủ đầu tư tại Việt Nam theo khung pháp lý hiện hành: Luật Đấu thầu 2023 (22/2023/QH15), Nghị định 214/2025/NĐ-CP, Nghị định 349/2026/NĐ-CP, Thông tư 79/2025/TT-BTC và Thông tư 134/2026/TT-BTC; hỗ trợ thẩm định HSMT, đánh giá HSDT, lựa chọn nhà thầu, xử lý tình huống và trả lời kiến nghị. Có khu vực tham chiếu lịch sử Luật 2013/Nghị định 63.
---

# Skill Đấu Thầu (dau-thau)

Skill này hỗ trợ chủ đầu tư thực hiện các công tác đấu thầu đúng quy định pháp luật tại Việt Nam.

## Năng lực chính

1. **Thẩm định Hồ sơ mời thầu (HSMT)** – Kiểm tra tính đầy đủ, hợp lệ, phù hợp quy định pháp luật trước khi phát hành (Điều 7, 13, 105 Nghị định 63/2014).
2. **Đánh giá Hồ sơ dự thầu (HSDT)** – Kiểm tra hợp lệ, chấm điểm, xếp hạng theo tiêu chí đã công bố (Điều 18 Nghị định 63/2014; Điều 39, 40, 42, 43 Luật).
3. **Lựa chọn nhà thầu** – Hỗ trợ lập báo cáo thẩm định kết quả, quyết định phê duyệt/kết quả trúng thầu.
4. **Xử lý khiếu nại, kiến nghị** – Quy trình, thời hạn, mẫu phản hồi (Điều 88, 91, 92 Luật; Điều 117-120 Nghị định 63/2014).
5. **Ký kết và quản lý hợp đồng** – Điều kiện ký kết, bảo đảm thực hiện hợp đồng (Điều 62-66 Luật; Điều 89-99 Nghị định 63/2014).
6. **Tra cứu pháp lý nhanh** – Script tìm kiếm khung hiện hành và khung lịch sử; ưu tiên Luật 22/2023/QH15, Nghị định 214/2025/NĐ-CP đã cập nhật bởi Nghị định 349/2026/NĐ-CP, Thông tư 79/2025/TT-BTC và Thông tư 134/2026/TT-BTC.

## Cấu trúc thư mục

```
dau-thau/
├── SKILL.md
├── scripts/
│   └── tra_cuu_phap_ly.py
├── templates/
│   ├── hsmthau_checklist.md       # Checklist thẩm định HSMT trước phát hành
│   ├── hsmt_checklist.md          # Checklist đánh giá HSDT (hồ sơ dự thầu)
│   ├── kien_nghi_phan_hoi.md      # Mẫu phản hồi kiến nghị/khiếu nại
│   ├── bao_cao_tham_dinh.md       # Mẫu báo cáo thẩm định kết quả lựa chọn nhà thầu
│   └── quyet_dinh_trung_thau.md   # Mẫu quyết định trúng thầu
└── references/
    └── phap_ly/
        ├── luat_dau_thau_2013.json      # Luật Đấu thầu 2013 (điều, khoản, mục)
        ├── nghi_dinh_63_2014.json       # Nghị định 63/2014/NĐ-CP
        ├── thong_tu_ldtbxd.json         # Thông tư khung lịch sử 2013
        ├── luat_dau_thau_2023.json      # Luật 22/2023/QH15
        ├── nghi_dinh_214_2025.json      # Nghị định 214/2025/NĐ-CP
        ├── nghi_dinh_349_2026.json      # Nghị định 349/2026/NĐ-CP
        ├── thong_tu_79_2025.json        # Thông tư 79/2025/TT-BTC
        └── thong_tu_134_2026.json       # Thông tư 134/2026/TT-BTC
```

## Cách sử dụng

### 1. Tra cứu điều khoản pháp lý

```bash
python scripts/tra_cuu_phap_ly.py --van-ban "luat_dau_thau_2013" --dieu 30
python scripts/tra_cuu_phap_ly.py --tim-kiem "khiếu nại" --van-ban all
python scripts/tra_cuu_phap_ly.py --danh-sach-van-ban
```

### 2. Sử dụng checklist/mẫu biểu

- Mở file trong `templates/` tương ứng với giai đoạn đang thực hiện.
- Điền thông tin dự án, đối chiếu từng mục.
- Xuất PDF/Word để lưu hồ sơ.

### 3. Workflow thẩm định HSMT

1. Thu thập HSMT do đơn vị tư vấn lập gửi.
2. Kiểm tra điều kiện phát hành (Điều 7 Luật Đấu thầu 2013): kế hoạch đã duyệt, HSMT đã duyệt đủ nội dung, thông báo mời thầu đã đăng tải, vốn đã thu xếp, mặt bằng bảo đảm.
3. Mở `templates/hsmthau_checklist.md`, kiểm tra từng mục theo Luật Đấu thầu 2013, Nghị định 63/2014 (nội dung thẩm định tại Điều 105 Nghị định).
4. Ghi nhận kết quả: Đạt / Không đạt / Cần bổ sung.
5. Lập báo cáo thẩm định theo `templates/bao_cao_tham_dinh.md`, gửi đơn vị tư vấn chỉnh sửa nếu cần (thời gian thẩm định tối đa 20 ngày, Điều 12.1.h Luật).

### 4. Workflow đánh giá HSDT

1. Mở thầu trong vòng 01 giờ kể từ thời điểm đóng thầu (Điều 14.4 Nghị định 63/2014); lập biên bản mở thầu.
2. Sử dụng `templates/hsmt_checklist.md`: kiểm tra tính hợp lệ (screening), đánh giá chi tiết, xếp hạng theo tiêu chí đã công bố trong HSMT.
3. Thương thảo hợp đồng với nhà thầu xếp hạng thứ nhất (nếu áp dụng).
4. Trình, thẩm định (Điều 106 Nghị định), phê duyệt kết quả lựa chọn nhà thầu.
5. Lập báo cáo theo `templates/bao_cao_tham_dinh.md`; thông báo kết quả cho các nhà thầu trong 05 ngày làm việc (Điều 12.1.n Luật).

### 5. Xử lý khiếu nại/kiến nghị

1. Tiếp nhận kiến nghị đúng điều kiện (Điều 118 Nghị định 63/2014) và thời hạn: kiến nghị về kết quả trong 10 ngày kể từ ngày có thông báo kết quả (Điều 92.2.a Luật).
2. Trả lời bằng văn bản trong 07 ngày làm việc (Điều 92.1.b, 92.2.b Luật); không trả lời hoặc nhà thầu không đồng ý: nhà thầu được kiến nghị lên người có thẩm quyền trong 05 ngày làm việc; về kết quả lựa chọn còn có Hội đồng tư vấn giải quyết kiến nghị (Điều 92.2.c-e).
3. Sử dụng `templates/kien_nghi_phan_hoi.md` soạn phản hồi, gửi người kiến nghị và lưu hồ sơ.
4. Khiếu nại, tố cáo: theo pháp luật về khiếu nại, tố cáo (Điều 88 Luật); các bên có quyền yêu cầu Tòa án áp dụng biện pháp khẩn cấp tạm thời (Điều 94 Luật).

## ⚠️ Trạng thái pháp lý (quan trọng)

- **Luật Đấu thầu 2013 (số 43/2013/QH13) và Nghị định 63/2014/NĐ-CP hết hiệu lực từ 01/01/2025.**
- Hệ thống pháp lý hiện hành được cập nhật trong Skill: **Luật Đấu thầu 2023 (22/2023/QH15)**; **Nghị định 214/2025/NĐ-CP**, đã cập nhật bởi **Nghị định 349/2026/NĐ-CP ngày 09/09/2026**; **Thông tư 79/2025/TT-BTC ngày 04/08/2025** và **Thông tư 134/2026/TT-BTC ngày 09/09/2026**.
- Khi xử lý hồ sơ, phải xác định ngày phát hành/mốc pháp lý của gói thầu, kiểm tra điều khoản chuyển tiếp và ưu tiên văn bản sửa đổi mới nhất. Luật 2013/Nghị định 63 chỉ dùng để tham chiếu lịch sử hoặc hồ sơ thuộc giai đoạn cũ.
- Dữ liệu trong `references/phap_ly/` là bản tóm tắt tra cứu. Với các văn bản mới, phải đối chiếu toàn văn và phụ lục/mẫu hồ sơ trên Cổng thông tin điện tử Chính phủ, Hệ thống mạng đấu thầu quốc gia hoặc nguồn chính thức trước khi phát hành văn bản chính thức.

## Cập nhật dữ liệu pháp lý

> **Lưu ý**: Khi có văn bản mới (hoặc khi chuyển hẳn sang Luật Đấu thầu 2023 + NĐ 214/2025):
> 1. Cập nhật file JSON trong `references/phap_ly/`.
> 2. Chạy lại script tra cứu để kiểm tra.
> 3. Cập nhật checklist/mẫu biểu nếu quy trình thay đổi.

## Test

```bash
python scripts/tra_cuu_phap_ly.py --test
```