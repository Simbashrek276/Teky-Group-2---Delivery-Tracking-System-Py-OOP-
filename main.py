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

print('a')