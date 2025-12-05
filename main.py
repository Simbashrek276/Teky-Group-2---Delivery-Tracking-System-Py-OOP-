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

import os
import random
import json
from datetime import datetime

class Shipper:
    def __init__(self, shipper_id, name):
        self.shipper_id = shipper_id
        self.name = name
        self.total_revenue = 0
        self.completed_orders = 0
        self.ratings = []
        self.current_order = None

    def assign_order(self, order):
        self.current_order = order
        order.shipper = self   
        order.set_shipper(self.shipper_id, self.name)
        order.state = AssignedState()

    def finish_order(self):
        if self.current_order:
            self.total_revenue += self.current_order.fee
            self.completed_orders += 1
            self.current_order.state = CompletedState()
            self.current_order.status = "COMPLETED"
            self.current_order = None

    def complete_order(self, order_id, rating=None):
        order = self.orders[order_id]

        if order.status == "COMPLETED":
            print(f"Order {order_id} đã hoàn thành trước đó rồi, ko hoàn thành lại đc nữa")
            return
        order.shipper.finish_order()
        if rating:
            order.shipper.add_rating(rating)

    def add_rating(self, rating):
        self.ratings.append(rating)

    def to_dict(self):
        return {
            "shipper_id": self.shipper_id,
            "name": self.name,
            "total_revenue": self.total_revenue,
            "completed_orders": self.completed_orders,
            "ratings": self.ratings
        }

class Order():
    def __init__(self, order_id, distance, weight, base_rate=5):
        self.order_id = order_id
        self.distance = distance
        self.weight = weight
        self.base_rate = base_rate
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.fee = 0
        self.status = "NEW"

        self.shipper = None #cái này lưu nguyên cả cái object shipper cho tí gọi cho dễ như kiểu là "shipper.asign_order() cho tiện"
        self.shipper_id = None
        self.shipper_name = None #cai này lưu tên mấy chú ship dạng string nhé nên khác nhau (nên minh châu phân biệt lưu ý với self.shipper ở trên nhem)

        self.state = NewState()

    def set_fee(self,fee):
        self.fee=fee
        #cái này dùng cho Normal Order hoặc express order nhé mn
    
    def set_shipper(self, shipper_id, shipper_name):
        self.shipper_id = shipper_id
        self.shipper_name = shipper_name
        self.status = "ASSIGNED"

    def export_invoice_txt(self): #nchung la cais nay export hoa don ra txt cho dễ đọc
        filename = f"Invoice_{self.order_id}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("===== DELIVERY INVOICE (hóa đơn) =====\n")
            f.write(f"Order ID      : {self.order_id}\n")
            f.write(f"Status        : {self.status}\n")
            f.write(f"Created At    : {self.created_at}\n")
            f.write("\n--- SHIPPING INFO ---\n")
            f.write(f"Distance (km) : {self.distance}\n")
            f.write(f"Weight (kg)   : {self.weight}\n")
            f.write(f"Base Rate     : {self.base_rate}\n")
            f.write(f"Fee (VND)     : {self.fee}\n")
            f.write("\n--- SHIPPER ---\n")
            f.write(f"Shipper ID    : {self.shipper_id}\n")
            f.write(f"Shipper Name  : {self.shipper_name}\n")
            f.write("\n====================================\n")
        return filename
    
    def to_dict(self): 
        #cái này để phục vụ cho thằng save của delivery service bên dưới của tớ nhé
        return {
            "order_id": self.order_id,
            "distance": self.distance,
            "weight": self.weight,
            "base_rate": self.base_rate,
            "created_at": self.created_at,
            "fee": self.fee,
            "status": self.status,
            "shipper_id": self.shipper_id,
            "shipper_name": self.shipper_name,
            "type": self.__class__.__name__,
            "state": self.state.state_name()
        }
    
class NormalOrder(Order):
    def calculate_fee(self):
        self.fee = self.base_rate * self.distance + self.weight * 2

class ExpressOrder(Order):
    def calculate_fee(self):
        self.fee = (self.base_rate * self.distance + self.weight * 2) * 1.5

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

class DeliveryService:
    def __init__(self):
        self.orders = {}
        self.shippers = {}
        self.order_counter = 1
        self.shipper_counter = 1

    def add_shipper(self, name):
        shipper = Shipper(self.shipper_counter, name)
        self.shippers[self.shipper_counter] = shipper
        self.shipper_counter += 1
        return shipper

    def create_order(self, type_name, distance, weight):
        oid = self.order_counter
        if type_name == "normal":
            order = NormalOrder(oid, distance, weight)
        else:
            order = ExpressOrder(oid, distance, weight)

        order.calculate_fee()
        self.orders[oid] = order
        self.order_counter += 1
        return order

    def assign_shipper(self, order_id, shipper_id):
        shipper = self.shippers[shipper_id]
        shipper.assign_order(self.orders[order_id])
        shipper.current_order = self.orders[order_id]

    def complete_order(self, order_id, rating=None):
        order = self.orders[order_id]
        order.shipper.finish_order()

        if rating:
            order.shipper.add_rating(rating)

    #tớ lưu du liệu ra file json để load
    #chắc tớ nghĩ json cần thiết (cái này thầy Huy bảo trọ giúp AI một phần ok nhé nên ở đây tớ làm json)
    def save_json(self, filename="data.json"):
        data = {
            "shippers": {sid: s.to_dict() for sid, s in self.shippers.items()},
            "orders": {oid: o.to_dict() for oid, o in self.orders.items()}
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_json(self, filename="data.json"):
        if not os.path.exists(filename):
            print("File data.json chưa tồn tại! Hãy dùng chức năng 6 (Lưu dữ liệu) trước.")
            return

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.shippers = {}
        for sid, sdata in data["shippers"].items():
            shipper = Shipper(int(sdata["shipper_id"]), sdata["name"])
            shipper.total_revenue = sdata["total_revenue"]
            shipper.completed_orders = sdata["completed_orders"]
            shipper.ratings = sdata["ratings"]
            self.shippers[int(sid)] = shipper

        self.orders = {}
        for oid, odata in data["orders"].items():
            if odata["type"] == "NormalOrder":
                order = NormalOrder(int(odata["order_id"]), odata["distance"], odata["weight"], odata["base_rate"])
            else:
                order = ExpressOrder(int(odata["order_id"]), odata["distance"], odata["weight"], odata["base_rate"])

            order.fee = odata["fee"]
            order.status = odata["status"]
            order.shipper_id = odata["shipper_id"]
            order.shipper_name = odata["shipper_name"]
            self.orders[int(oid)] = order

#menu của mình nhé ae :))
def main():
    service = DeliveryService()

    while True:
        print("\n===== DELIVERY SYSTEM MENU =====")
        print("1. Thêm shipper")
        print("2. Tạo order")
        print("3. Gán shipper cho order")
        print("4. Hoàn thành order")
        print("5. Xuất hóa đơn order")
        print("6. Lưu dữ liệu ra JSON")
        print("7. Load dữ liệu từ JSON")
        print("0. Thoát")
        choice = input("Chọn chức năng: ")

        if choice == "1":
            name = input("Tên shipper: ")
            shipper = service.add_shipper(name)
            print(f"Đã thêm shipper {shipper.name} với ID {shipper.shipper_id}")

        elif choice == "2":
            type_name = input("Loại order (normal/express): ")
            distance = float(input("Khoảng cách (km): "))
            weight = float(input("Khối lượng (kg): "))
            order = service.create_order(type_name, distance, weight)
            print(f"Đã tạo order với ID {order.order_id} với phí {order.fee}K VND")

        elif choice == "3":
            order_id = int(input("ID order: "))
            shipper_id = int(input("ID shipper: "))
            service.assign_shipper(order_id, shipper_id)
            print(f"Đã gán shipper {shipper_id} cho order ID {order_id}")

        elif choice == "4":
            order_id = int(input("ID order: "))
            rating_input = input("Đánh giá shipper (1-5, bỏ trống nếu không có): ")
            rating = int(rating_input) if rating_input else None
            service.complete_order(order_id, rating)
            print(f"Order {order_id} đã hoàn thành")

        elif choice == "5":
            order_id = int(input("ID order: "))
            if order_id not in service.orders:
                print("Order không tồn tại. Check again bro")
            else:
                filename = service.orders[order_id].export_invoice_txt()
                print(f"Đã xuất hóa đơn: {filename}")

        elif choice == "6":
            service.save_json()
            print("Đã lưu dữ liệu ra data.json")

        elif choice == "7":
            service.load_json()
            print("Đã load dữ liệu từ data.json")

        elif choice == "0":
            print("Thoát chương trình.")
            break

        else:
            print("Chức năng không hợp lệ, vui lòng chọn lại.")

if __name__ == "__main__":
    main()