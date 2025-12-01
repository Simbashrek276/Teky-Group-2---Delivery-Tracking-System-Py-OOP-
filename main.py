#đây sẽ là file main.py để mọi người lập trình nhé
#Đề Tài 4: Ứng Dụng Quản Lý Giao Hàng Nhanh (Delivery
#Tracking System)
#Mục tiêu:
#- Mô phỏng quản lý đơn hàng, shipper, trạng thái giao hàng. Tập trung:
#State pattern cho trạng thái đơn, kế thừa đặt loại đơn hàng,
#polymorphism tính phí..
#Các chức năng bắt buộc: ( bắt buộc phải tự suy nghĩ ra thêm các phương
#thức khác để có tính sáng tạo + thực tế )
#- Tạo Order (Normal/Express), tính phí theo khoảng cách & khối lượng.
#- Quản lý Shipper: assign order, finish order, rating.
#- Trạng thái order: New → Assigned → Shipping → Completed →
#Cancelle
#- Thống kê doanh thu theo shipper..
#- Lưu / Đọc dữ liệu ra file ( json hoặc txt ).
#Giảng viên hướng dẫn: Nguyễn Đức Huy
#- Export hóa đơn ra .txt.
#Các class chính: ( Bắt buộc phải từ 5 class đổ lên )
#Dưới đây là gợi ý: Order, NormalOrder(Order), ExpressOrder(Order),
#OrderState, Shipper, DeliveryService.....
#Test Cases ( ít nhất , phải có để kiểm tra ngoại lệ):
#- Tạo ExpressOrder, kiểm tra phí > NormalOrder cho cùng
#khoảng cách.
#- Gán shipper: order status chuyển đúng.
#- Shipper hoàn thành: tính doanh thu cộng đúng.
#- Lưu / Load dữ liệu: dữ liệu phải đồng nhất sau load.

import random
import json
class shipper():

class orderState():
    
class order():
    def __init__(self,order_id,distance,weight,base_rate,fee,created_at):
        order_id=self.order_id
        distance=self.distance
        weight=self.weight
        base_rate=self.base_rate
        fee=self.fee
        status=self.status
        shipper_id=self.shipper_id
        shipper_name=self.shipper_name
        created_at=self.created_at
    def assign_shipper(self):
        shipper_list=[shipper(),shipper(),shipper(),shipper()]
        self.shipper_id=random.randint(1,4)
        self.shipper_name=shipper_list[self.shipper_id-1].name
    def export_invoice(self):
        filename=f"Invoice number {self.order_id}.json"
        invoice_data = {
            "order_id": self.order_id,
            "status": self.status,
            "distance_km": self.distance,
            "weight_kg": self.weight,
            "base_rate": self.base_rate,
            "fee": self.fee,
            "shipper": {
                "id": self.shipper_id,
                "name": self.shipper_name
            },
            "created_at": (
                self.created_at
            )
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(invoice_data, f, ensure_ascii=False, indent=4)
        return filename