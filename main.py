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
        if order_id not in self.orders:
            print("Order không tồn tại.")
            return
        if shipper_id not in self.shippers:
            print("Shipper không tồn tại.")
            return

        order = self.orders[order_id]
        shipper = self.shippers[shipper_id]

        if order.status == "COMPLETED" or order.status == "CANCELLED":
            print("Không thể gán shipper cho order đã hoàn thành hoặc đã hủy.")
            return
        if shipper.current_order is not None:
            print("Shipper hiện đang có đơn khác, không thể gán.")
            return

        shipper.assign_order(order)
        shipper.current_order = order

    def complete_order(self, order_id, rating=None):
        if order_id not in self.orders:
            print("Order không tồn tại.")
            return
        order = self.orders[order_id]
        if order.status == "COMPLETED":
            print(f"Order {order_id} đã hoàn thành trước đó rồi, không thể hoàn thành lại.")
            return
        if order.shipper is None:
            print("Order chưa được gán shipper, không thể hoàn thành.")
            return
        if order.shipper.current_order is None:
            # shipper không còn current_order (có thể đã được hoàn thành trước) nên là kiểu ye
            print("Shipper không đang giao order này, kiểm tra lại trạng thái.")
            return

        order.shipper.finish_order()

        if rating:
            order.shipper.add_rating(rating)

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
            shipper.total_revenue = sdata.get("total_revenue", 0)
            shipper.completed_orders = sdata.get("completed_orders", 0)
            shipper.ratings = sdata.get("ratings", [])
            self.shippers[int(sid)] = shipper

        self.orders = {}
        for oid, odata in data["orders"].items():
            if odata["type"] == "NormalOrder":
                order = NormalOrder(int(odata["order_id"]), odata["distance"], odata["weight"], odata["base_rate"])
            else:
                order = ExpressOrder(int(odata["order_id"]), odata["distance"], odata["weight"], odata["base_rate"])

            order.fee = odata.get("fee", 0)
            order.status = odata.get("status", "NEW")
            order.shipper_id = odata.get("shipper_id")
            order.shipper_name = odata.get("shipper_name")
            state_name = odata.get("state", "NewState")
            if state_name == "NewState":
                order.state = NewState()
            elif state_name == "AssignedState":
                order.state = AssignedState()
            elif state_name == "ShippingState":
                order.state = ShippingState()
            elif state_name == "CompletedState":
                order.state = CompletedState()

            elif state_name == "CancelledState":
                order.state = CancelledState()
            else:
                order.state = NewState()

            self.orders[int(oid)] = order

        for oid, order in list(self.orders.items()):
            if order.shipper_id is not None:
                sid = int(order.shipper_id)
                if sid in self.shippers:
                    order.shipper = self.shippers[sid]
                    # nếu đơn đang ở trạng thái ASSIGNED hoặc SHIPPING, thì ae cập nhật current_order của shipper ye
                    if order.status in ("ASSIGNED", "SHIPPING"):
                        self.shippers[sid].current_order = order

        #cái counter của mình để tránh trùng ID (kiểu id order bị trùng ấy)
        if self.orders:
            self.order_counter = max(self.orders.keys()) + 1
        else:
            self.order_counter = 1
        if self.shippers:
            self.shipper_counter = max(self.shippers.keys()) + 1
        else:
            self.shipper_counter = 1

#menu của mình nhé ae :))
import tkinter as tk
from tkinter import messagebox, simpledialog

class DeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Delivery Tracking System")
        self.root.geometry("1200x700")

        self.service = DeliveryService()

        #menu trái đây (tớ đang để màu xanh dương)
        left_frame = tk.Frame(root, width=180, bg="#2c3e50")
        left_frame.pack(side="left", fill="y")

        def big_btn(text, cmd):
            return tk.Button(
                left_frame,
                text=text,
                command=cmd,
                height=2,
                font=("Arial", 11, "bold"),
                bg="#34495e",
                fg="white"
            )

        big_btn("Add Shipper", self.add_shipper).pack(fill="x", pady=5)
        big_btn("Create Order", self.create_order).pack(fill="x", pady=5)
        big_btn("Assign", self.assign_shipper).pack(fill="x", pady=5)
        big_btn("Complete", self.complete_order).pack(fill="x", pady=5)
        big_btn("Export", self.export_invoice).pack(fill="x", pady=5)
        big_btn("Save", self.save).pack(fill="x", pady=5)
        big_btn("Load", self.load).pack(fill="x", pady=5)

        #cả phần khung chính (phần diện tích bên phải của thanh menu bên trái ấy)
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        left_main = tk.Frame(main_frame, bg="#ecf0f1")
        left_main.pack(side="left", fill="both", expand=True, padx=(10,5), pady=10)

        right_main = tk.Frame(main_frame)
        right_main.pack(side="left", fill="both", expand=True, padx=(5,10), pady=10)

        #khung chính (dashboard)

        self.rank_box = tk.LabelFrame(left_main, text="Top Shippers")
        self.rank_box.pack(fill="x", pady=5)

        self.rank_label = tk.Label(self.rank_box, justify="left")
        self.rank_label.pack()

        stats_frame = tk.Frame(left_main)
        stats_frame.pack(fill="x")

        self.total_orders_box = tk.LabelFrame(stats_frame, text="Total Orders")
        self.total_orders_box.pack(side="left", expand=True, fill="both", padx=5)

        self.total_km_box = tk.LabelFrame(stats_frame, text="Total Distance")
        self.total_km_box.pack(side="left", expand=True, fill="both", padx=5)

        self.feedback_box = tk.LabelFrame(left_main, text="Ratings")
        self.feedback_box.pack(fill="both", expand=True, pady=5)

        self.feedback_label = tk.Label(self.feedback_box, justify="left")
        self.feedback_label.pack()

        # phần khung bên phải sẽ ntn

        # phần khung của ông chú shipper :))
        shipper_panel = tk.LabelFrame(right_main, text="Shipper")
        shipper_panel.pack(fill="both", expand=True, pady=10)

        self.shipper_list = tk.Listbox(shipper_panel, font=("Arial", 11))
        self.shipper_list.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Button(shipper_panel, text="+ Add", command=self.add_shipper).pack(fill="x")
        tk.Button(shipper_panel, text="Assign", command=self.assign_shipper).pack(fill="x")

        # ORDER PANEL
        order_panel = tk.LabelFrame(right_main, text="Order")
        order_panel.pack(fill="both", expand=True, pady=10)

        self.order_list = tk.Listbox(order_panel, font=("Arial", 11))
        self.order_list.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Button(order_panel, text="+ Create", command=self.create_order).pack(fill="x")
        tk.Button(order_panel, text="Complete", command=self.complete_order).pack(fill="x")
        tk.Button(order_panel, text="Export", command=self.export_invoice).pack(fill="x")

        self.refresh()

    #đây sẽ là các hàm của nhóm mình 
    def refresh(self):
        self.order_list.delete(0, tk.END)
        self.shipper_list.delete(0, tk.END)

        for o in self.service.orders.values():
            self.order_list.insert(tk.END,
                f"ID:{o.order_id} | {o.status} | {o.fee}")

        for s in self.service.shippers.values():
            avg = round(sum(s.ratings)/len(s.ratings),2) if s.ratings else "N/A"
            self.shipper_list.insert(tk.END,
                f"ID:{s.shipper_id} | {s.name} | Rev:{s.total_revenue} | ⭐{avg}")

        sorted_shippers = sorted(self.service.shippers.values(),
                                 key=lambda x: x.total_revenue,
                                 reverse=True)

        rank_text = ""
        for i, s in enumerate(sorted_shippers[:5], start=1):
            rank_text += f"{i}. {s.name} - {s.total_revenue}\n"

        self.rank_label.config(text=rank_text if rank_text else "No data")

        total_orders = len(self.service.orders)
        total_km = sum(o.distance for o in self.service.orders.values())

        for widget in self.total_orders_box.winfo_children():
            widget.destroy()
        tk.Label(self.total_orders_box, text=str(total_orders), font=("Arial", 16)).pack()

        for widget in self.total_km_box.winfo_children():
            widget.destroy()
        tk.Label(self.total_km_box, text=str(total_km), font=("Arial", 16)).pack()

        ratings_text = ""
        for s in self.service.shippers.values():
            if s.ratings:
                avg = round(sum(s.ratings)/len(s.ratings),2)
                ratings_text += f"{s.name}: {avg}\n"

        self.feedback_label.config(text=ratings_text if ratings_text else "No ratings")

    def add_shipper(self):
        name = simpledialog.askstring("Input", "Shipper name:")
        if name:
            self.service.add_shipper(name)
            self.refresh()

    def create_order(self):
        form = tk.Toplevel(self.root)
        form.title("Create Order")
        form.geometry("300x250")

        tk.Label(form, text="Order Type").pack()
        type_var = tk.StringVar(value="normal")
        tk.OptionMenu(form, type_var, "normal", "express").pack()

        tk.Label(form, text="Distance (km)").pack()
        distance_entry = tk.Entry(form)
        distance_entry.pack()

        tk.Label(form, text="Weight (kg)").pack()
        weight_entry = tk.Entry(form)
        weight_entry.pack()

        def submit():
            try:
                type_name = type_var.get()
                distance = float(distance_entry.get())
                weight = float(weight_entry.get())

                order = self.service.create_order(type_name, distance, weight)

                messagebox.showinfo("Success", f"Order {order.order_id} created!\nFee: {order.fee}")
                form.destroy()
                self.refresh()
            except:
                messagebox.showerror("Error", "Invalid input")

        tk.Button(form, text="Create", command=submit).pack(pady=10)

    def assign_shipper(self):
        form = tk.Toplevel(self.root)
        form.title("Assign Shipper")
        form.geometry("300x200")

        tk.Label(form, text="Order ID").pack()
        order_entry = tk.Entry(form)
        order_entry.pack()

        tk.Label(form, text="Shipper ID").pack()
        shipper_entry = tk.Entry(form)
        shipper_entry.pack()

        def submit():
            try:
                order_id = int(order_entry.get())
                shipper_id = int(shipper_entry.get())

                self.service.assign_shipper(order_id, shipper_id)
                self.refresh()
                form.destroy()
            except:
                messagebox.showerror("Error", "Invalid input")

        tk.Button(form, text="Assign", command=submit).pack(pady=10)

    def complete_order(self):
        form = tk.Toplevel(self.root)
        form.title("Complete Order")
        form.geometry("300x200")

        tk.Label(form, text="Order ID").pack()
        order_entry = tk.Entry(form)
        order_entry.pack()

        tk.Label(form, text="Rating (1-5 optional)").pack()
        rating_entry = tk.Entry(form)
        rating_entry.pack()

        def submit():
            try:
                order_id = int(order_entry.get())
                rating = rating_entry.get()
                rating = int(rating) if rating else None

                self.service.complete_order(order_id, rating)
                self.refresh()
                form.destroy()
            except:
                messagebox.showerror("Error", "Invalid input")

        tk.Button(form, text="Complete", command=submit).pack(pady=10)

    def export_invoice(self):
        try:
            order_id = int(simpledialog.askstring("Order ID", "Enter order ID"))
        except:
            return

        if order_id in self.service.orders:
            filename = self.service.orders[order_id].export_invoice_txt()
            messagebox.showinfo("Exported", f"Saved as {filename}")
        else:
            messagebox.showerror("Error", "Order not found")

    def save(self):
        self.service.save_json()
        messagebox.showinfo("Saved", "Data saved")

    def load(self):
        self.service.load_json()
        self.refresh()
        messagebox.showinfo("Loaded", "Data loaded")


if __name__ == "__main__":
    root = tk.Tk()
    app = DeliveryApp(root)
    root.mainloop()