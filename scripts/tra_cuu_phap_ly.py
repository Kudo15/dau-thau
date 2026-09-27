#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tra cứu nhanh điều khoản pháp lý đấu thầu Việt Nam.
Hỗ trợ: Luật Đấu thầu 2013, Nghị định 63/2014/NĐ-CP, Thông tư liên quan.

Mỗi file JSON trong references/phap_ly/ có thể chứa các khối sau:
- "dieu" | "dieu_quan_trong" | "dieu_quan_trong_thong_tu_07":
    danh sách điều {so, tieu_de, noi_dung}
- "muc_luc": [{"dieu": 1, "ten": "..."}]
- "danh_sach_thong_tu": [{so_hieu, ten, ngay_ban_hanh, noi_dung_chinh: [...]}]
- mô tả văn bản: ten_van_ban, so_hieu, ngay_ban_hanh, hieu_luc, ghi_chu
Script tự nhận diện khối có mặt trong file, không bắt buộc thống nhất schema.
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

SCRIPT_DIR = Path(__file__).parent
REF_DIR = SCRIPT_DIR.parent / "references" / "phap_ly"

VAN_BAN_MAP = {
    "luat_dau_thau_2013": "luat_dau_thau_2013.json",
    "nghi_dinh_63_2014": "nghi_dinh_63_2014.json",
    "thong_tu_ldtbxd": "thong_tu_ldtbxd.json",
    "luat_dau_thau_2023": "luat_dau_thau_2023.json",
    "nghi_dinh_214_2025": "nghi_dinh_214_2025.json",
    "nghi_dinh_349_2026": "nghi_dinh_349_2026.json",
    "thong_tu_79_2025": "thong_tu_79_2025.json",
    "thong_tu_134_2026": "thong_tu_134_2026.json",
}

VAN_BAN_LABELS = {
    "luat_dau_thau_2013": "Luật Đấu thầu 2013 (đã hết hiệu lực)",
    "nghi_dinh_63_2014": "Nghị định 63/2014/NĐ-CP (đã hết hiệu lực)",
    "thong_tu_ldtbxd": "Thông tư liên quan khung 2013",
    "luat_dau_thau_2023": "Luật Đấu thầu 2023 - 22/2023/QH15",
    "nghi_dinh_214_2025": "Nghị định 214/2025/NĐ-CP",
    "nghi_dinh_349_2026": "Nghị định 349/2026/NĐ-CP",
    "thong_tu_79_2025": "Thông tư 79/2025/TT-BTC",
    "thong_tu_134_2026": "Thông tư 134/2026/TT-BTC",
}

DIEU_KEYS = ("dieu", "dieu_quan_trong", "dieu_quan_trong_thong_tu_07")

# Các văn bản mới có thể là bản tóm tắt theo chủ đề, không có toàn văn điều khoản.
VAN_BAN_MOI = {"luat_dau_thau_2023", "nghi_dinh_214_2025", "nghi_dinh_349_2026", "thong_tu_79_2025", "thong_tu_134_2026"}


def load_van_ban(van_ban_key: str) -> Dict[str, Any]:
    """Load dữ liệu văn bản pháp luật từ file JSON."""
    file_path = REF_DIR / VAN_BAN_MAP[van_ban_key]
    if not file_path.exists():
        return {"error": f"File không tồn tại: {file_path}"}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_dieu(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Trích danh sách điều có nội dung đầy đủ (theo thứ tự ưu tiên khóa)."""
    for key in DIEU_KEYS:
        value = data.get(key)
        if isinstance(value, list) and value:
            return value
    return []


def extract_muc_luc(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Trích mục lục (danh sách điều tên ngắn)."""
    value = data.get("muc_luc")
    if isinstance(value, list):
        return value
    return []


def extract_danh_sach_thong_tu(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Trích danh sách thông tư."""
    value = data.get("danh_sach_thong_tu")
    if isinstance(value, list):
        return value
    return []


def extract_searchable_items(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Chuẩn hóa dữ liệu điều, chủ đề và nội dung chính để tìm kiếm."""
    items = list(extract_dieu(data))
    for key in ("dieu_quan_trong", "noi_dung_chinh"):
        value = data.get(key)
        if isinstance(value, list):
            items.extend(x if isinstance(x, dict) else {"noi_dung": str(x)} for x in value)
    return items


def _truncate(text: str, limit: int = 500) -> str:
    text = text or ""
    return text[:limit] + "..." if len(text) > limit else text


def tra_cuu_dieu(van_ban_key: str, dieu_so: int) -> Optional[Dict[str, Any]]:
    """Tra cứu nội dung một điều cụ thể."""
    data = load_van_ban(van_ban_key)
    if "error" in data:
        return None
    for dieu in extract_searchable_items(data):
        if dieu.get("so") == dieu_so:
            return dieu
    return None


def _search_dieu(data: Dict[str, Any], label: str, tu_khoa_lower: str) -> List[Dict[str, Any]]:
    ket_qua = []
    for dieu in extract_searchable_items(data):
        van_ban_text = json.dumps(dieu, ensure_ascii=False).lower()
        if tu_khoa_lower in van_ban_text:
            ket_qua.append({
                "van_ban": label,
                "nguon": f"Điều {dieu.get('so')}" if dieu.get('so') is not None else "Chủ đề",
                "tieu_de": dieu.get("tieu_de", dieu.get("chu_de", "")),

                "noi_dung": _truncate(dieu.get("noi_dung", "")),
            })
    return ket_qua


def _search_muc_luc(data: Dict[str, Any], label: str, tu_khoa_lower: str) -> List[Dict[str, Any]]:
    ket_qua = []
    for muc in extract_muc_luc(data):
        ten = muc.get("ten", "")
        if tu_khoa_lower in ten.lower():
            ket_qua.append({
                "van_ban": label,
                "nguon": f"Mục lục - Điều {muc.get('dieu')}",
                "tieu_de": ten,
                "noi_dung": "(chỉ có trong mục lục, chưa có nội dung đầy đủ)",
            })
    return ket_qua


def _search_danh_sach_thong_tu(data: Dict[str, Any], label: str, tu_khoa_lower: str) -> List[Dict[str, Any]]:
    ket_qua = []
    for tt in extract_danh_sach_thong_tu(data):
        van_ban_text = json.dumps(tt, ensure_ascii=False).lower()
        if tu_khoa_lower in van_ban_text:
            ket_qua.append({
                "van_ban": label,
                "nguon": tt.get("so_hieu", "?"),
                "tieu_de": tt.get("ten", ""),
                "noi_dung": _truncate(" | ".join(tt.get("noi_dung_chinh", []))),
            })
    return ket_qua


def tim_kiem_tu_khoa(van_ban_key: str, tu_khoa: str) -> List[Dict[str, Any]]:
    """Tìm kiếm từ khóa trong một văn bản (điều, mục lục, danh sách thông tư)."""
    data = load_van_ban(van_ban_key)
    if "error" in data:
        return []
    label = VAN_BAN_LABELS[van_ban_key]
    tu_khoa_lower = tu_khoa.lower()
    ket_qua: List[Dict[str, Any]] = []
    ket_qua.extend(_search_dieu(data, label, tu_khoa_lower))
    ket_qua.extend(_search_danh_sach_thong_tu(data, label, tu_khoa_lower))
    ket_qua.extend(_search_muc_luc(data, label, tu_khoa_lower))
    return ket_qua


def tim_kiem_toan_bo(tu_khoa: str) -> List[Dict[str, Any]]:
    """Tìm kiếm từ khóa trong tất cả văn bản."""
    ket_qua: List[Dict[str, Any]] = []
    for key in VAN_BAN_MAP:
        ket_qua.extend(tim_kiem_tu_khoa(key, tu_khoa))
    return ket_qua


def danh_sach_van_ban() -> List[Dict[str, Any]]:
    """Liệt kê các văn bản có sẵn kèm thống kê nội dung."""
    result = []
    for key, label in VAN_BAN_LABELS.items():
        data = load_van_ban(key)
        entry: Dict[str, Any] = {
            "key": key,
            "ten": label,
            "so_hieu": data.get("so_hieu", "") if "error" not in data else "",
            "ton_tai": "error" not in data,
            "so_dieu": len(extract_dieu(data)) if "error" not in data else 0,
            "so_thong_tu": len(extract_danh_sach_thong_tu(data)) if "error" not in data else 0,
        }
        result.append(entry)
    return result


def in_dieu(dieu: Dict[str, Any], van_ban_label: str) -> None:
    """In nội dung điều ra màn hình."""
    print(f"\n{'='*60}")
    print(f"📄 {van_ban_label} - Điều {dieu.get('so')}")
    print(f"{'='*60}")
    if dieu.get("tieu_de"):
        print(f"📌 {dieu['tieu_de']}")
    elif dieu.get("chu_de"):
        print(f"📌 {dieu['chu_de']}")
    print(f"\n{dieu.get('noi_dung', 'Không có nội dung')}")
    print(f"{'='*60}\n")


def chay_smoke_test() -> int:
    """Chạy smoke test, trả về mã lỗi (0 = đạt)."""
    loi = 0

    print("🧪 Running smoke test...")

    print("\n1. Kiểm tra file dữ liệu:")
    for vb in danh_sach_van_ban():
        status = "✅" if vb["ton_tai"] else "❌"
        if not vb["ton_tai"]:
            loi = 1
        extra = []
        if vb["so_dieu"]:
            extra.append(f"{vb['so_dieu']} điều")
        if vb["so_thong_tu"]:
            extra.append(f"{vb['so_thong_tu']} thông tư")
        extra_str = f" ({', '.join(extra)})" if extra else ""
        print(f"   {status} {vb['ten']} ({vb['key']}){extra_str}")

    print("\n2. Test tra cứu Điều 91 Luật Đấu thầu 2013 (giải quyết kiến nghị):")
    dieu = tra_cuu_dieu("luat_dau_thau_2013", 91)
    if dieu:
        print(f"   ✅ Tìm thấy Điều 91: {dieu.get('tieu_de', '')[:60]}")
    else:
        print("   ❌ Không tìm thấy Điều 91 - dữ liệu tra cứu hỏng")
        loi = 1

    print("\n3. Test tìm kiếm từ khóa 'khiếu nại' trên toàn bộ văn bản:")
    kq = tim_kiem_toan_bo("khiếu nại")
    if kq:
        print(f"   ✅ Tìm thấy {len(kq)} kết quả")
    else:
        print("   ❌ Không tìm thấy kết quả nào - dữ liệu tra cứu hỏng")
        loi = 1

    print("\n4. Test tìm kiếm từ khóa 'thẩm định':")
    kq2 = tim_kiem_toan_bo("thẩm định")
    print(f"   ✅ Tìm thấy {len(kq2)} kết quả")

    if loi:
        print("\n❌ Smoke test THẤT BẠI")
    else:
        print("\n✅ Smoke test hoàn tất")
    return loi


def main() -> None:
    parser = argparse.ArgumentParser(description="Tra cứu pháp lý đấu thầu Việt Nam")
    parser.add_argument("--van-ban", choices=list(VAN_BAN_MAP.keys()) + ["all"], default="all",
                        help="Văn bản pháp luật cần tra cứu")
    parser.add_argument("--dieu", type=int, help="Số điều cần tra cứu")
    parser.add_argument("--tim-kiem", type=str, help="Từ khóa tìm kiếm")
    parser.add_argument("--danh-sach-van-ban", action="store_true",
                        help="Liệt kê các văn bản có sẵn")
    parser.add_argument("--test", action="store_true", help="Chạy test smoke")
    parser.add_argument("--chi-hien-hanh", action="store_true", help="Chỉ liệt kê/tìm kiếm khung pháp lý mới hiện hành")

    args = parser.parse_args()

    if args.chi_hien_hanh:
        for key in VAN_BAN_MAP:
            if key in VAN_BAN_MOI:
                print(f"- {key}: {VAN_BAN_LABELS[key]}")
        return

    if args.test:
        sys.exit(chay_smoke_test())

    if args.danh_sach_van_ban:
        print("\n📚 Danh sách văn bản pháp luật:")
        for vb in danh_sach_van_ban():
            status = "✅ Có sẵn" if vb["ton_tai"] else "❌ Chưa có"
            so_hieu = f" - {vb['so_hieu']}" if vb["so_hieu"] else ""
            print(f"  - {vb['ten']} ({vb['key']}){so_hieu}: {status}")
        return

    if args.dieu is not None and args.van_ban != "all":
        dieu = tra_cuu_dieu(args.van_ban, args.dieu)
        if dieu:
            in_dieu(dieu, VAN_BAN_LABELS[args.van_ban])
        else:
            print(f"❌ Không tìm thấy Điều {args.dieu} trong {VAN_BAN_LABELS[args.van_ban]}")
            sys.exit(1)
        return

    if args.tim_kiem:
        if args.van_ban == "all":
            ket_qua = tim_kiem_toan_bo(args.tim_kiem)
        else:
            ket_qua = tim_kiem_tu_khoa(args.van_ban, args.tim_kiem)

        if ket_qua:
            print(f"\n🔍 Tìm thấy {len(ket_qua)} kết quả cho '{args.tim_kiem}':")
            for i, kq in enumerate(ket_qua[:20], 1):
                print(f"\n{i}. [{kq['van_ban']}] {kq['nguon']}: {kq['tieu_de']}")
                if kq["noi_dung"]:
                    print(f"   {kq['noi_dung']}")
            if len(ket_qua) > 20:
                print(f"\n... và {len(ket_qua) - 20} kết quả khác.")
        else:
            print(f"❌ Không tìm thấy kết quả cho '{args.tim_kiem}'")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
