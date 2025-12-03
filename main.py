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
#- Trạng thái order: New → Assigned → Shipping → Completed → Canceled
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
from datetime import datetime

class Shipper():
    pass

class Order():
    def __init__(self,order_id,distance,weight,base_rate,created_at):
        self.order_id = order_id
        self.distance = distance
        self.weight = weight
        self.base_rate = base_rate
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.fee = 0

        self.status = "NEW"

        self.shipper_id = None
        self.shipper_name = None

    def set_fee(self,fee):
        self.fee=fee
        #cái này dùng cho Normal Order hoặc express order nhé mn
    
    def set_shipper(self, shipper_id, shipper_name):
        self.shipper_id = shipper_id
        self.shipper_name = shipper_name
        self.status = "ASSIGNED"

    def assign_shipper(self):
        shipper_list=[shipper(),shipper(),shipper(),shipper()]
        self.shipper_id=random.randint(1,4)
        self.shipper_name=shipper_list[self.shipper_id-1].name

    def export_invoice(self):
        filename = f"Invoice_{self.order_id}.json"

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
            "created_at": self.created_at
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(invoice_data, f, ensure_ascii=False, indent=4)

        return filename
    
    
    def to_dict(self): #cái này để phục vụ cho thằng save của delivery service bên dưới của tớ nhé
        return {
            "order_id": self.order_id,
            "distance": self.distance,
            "weight": self.weight,
            "base_rate": self.base_rate,
            "created_at": self.created_at,
            "fee": self.fee,
            "status": self.status,
            "shipper_id": self.shipper_id,
            "shipper_name": self.shipper_name
        }
class normalorder(Order):
    def __init__(self,order_id,distance,weight,created_at):
        super().__init__(order_id,distance,weight,created_at)
        self.base_rate=5000
    def set_fee(self,fee):
        fee = self.base_rate*self.distance + self.weight*3000
        self.fee=fee
class expressorder(Order):
    def __init__(self,order_id,distance,weight,created_at):
        super().__init__(order_id,distance,weight,created_at)
        self.base_rate=10000
    def set_fee(self,fee):
        fee = self.base_rate*self.distance + self.weight*3000
        self.fee=fee
class OrderState(): #cái này để print ra trạng thái hiện tại của đơn hàng nhé ae
    def state_name(self):
        return self.__class__.__name__

    def assign(self, order, shipper):
        raise Exception(f"Không thể gán shipper khi đang ở trạng thái {self.state_name()}.")

    def start_shipping(self, order):
        raise Exception(f"Không thể bắt đầu giao khi đang ở trạng thái {self.state_name()}.")

    def complete(self, order):
        raise Exception(f"Không thể hoàn thành khi đang ở trạng thái {self.state_name()}.")

    def cancel(self, order):
        raise Exception(f"Không thể hủy đơn khi đang ở trạng thái {self.state_name()}.")

#tớ làm phần này nó sẽ define mỗi OrderState kế thừa 
class NewState(OrderState):
    def assign(self, order, shipper):
        order.shipper = shipper
        order.shipper_id = shipper.shipper_id
        order.shipper_name = shipper.name
        order.status = "ASSIGNED"
        order.state = AssignedState()

class AssignedState(OrderState):
    def start_shipping(self, order):
        order.status = "SHIPPING"
        order.state = ShippingState()

    def cancel(self, order):
        order.status = "CANCELLED"
        order.state = CancelledState()

class ShippingState(OrderState):
    def complete(self, order):
        order.status = "COMPLETED"
        order.state = CompletedState()

class CompletedState(OrderState):
    pass

class CancelledState(OrderState):
    pass

class DeliveryService():
    def __init__(self):
        self.orders = {}
        self.shippers = {}
        self.order_counter = 1
        self.shipper_counter = 1

    def add_shipper(self, name):
        shipper = Shipper(self.shipper_counter, name)
        self.shippers[self.shipper_counter] = shipper
        self.shipper_counter += 1

    def create_order(self, type_name, distance, weight):
        oid = self.order_counter
        if type_name == "normal":
            order = NormalOrder(oid, distance, weight)
        else:
            order = ExpressOrder(oid, distance, weight)
        self.orders[oid] = order
        self.order_counter += 1
        return order

    def assign_shipper(self, order_id, shipper_id):
        self.shippers[shipper_id].assign_order(self.orders[order_id])

    def complete_order(self, order_id):
        shipper = self.orders[order_id].shipper
        shipper.finish_order()

    def save(self, filename):
        data = {
            "orders": {oid: o.to_dict() for oid, o in self.orders.items()},
            "shippers": {
                sid: {
                    "id": s.shipper_id,
                    "name": s.name,
                    "total_revenue": s.total_revenue,
                    "completed_orders": s.completed_orders,
                    "ratings": s.ratings,
                }
                for sid, s in self.shippers.items()
            }
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
