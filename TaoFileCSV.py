import csv
import os
from Permissions_Android import AOSP_PERMISSIONS
from androguard.core.bytecodes.apk import APK

android_permissions = sorted(list(AOSP_PERMISSIONS.keys()))

# Thư mục chứa các file APK
apk_folder = "D:/BTL/BTL Python/FileAPK"

# Kiểm tra xem file CSV đã tồn tại hay chưa
csv_exists = os.path.exists('permissions1.csv')

# Tạo file CSV hoặc mở file CSV đã tồn tại ở chế độ append
with open('permissions1.csv', mode='a', newline='') as file:
    writer = csv.writer(file, delimiter=';')  # Thiết lập dấu phân tách là dấu chấm phẩy (;)

    # Nếu file CSV chưa tồn tại, viết tên cột (quyền và type) vào file CSV
    if not csv_exists:
        writer.writerow(android_permissions + ['Type'])

    # Lặp qua từng file trong thư mục
    for filename in os.listdir(apk_folder):
        if filename.endswith(".apk"):
            apk_file = os.path.join(apk_folder, filename)
            apk = APK(apk_file)

            # Trích xuất danh sách quyền từ file APK
            permissions = apk.get_permissions()

            row = []

            # Kiểm tra từng quyền trong danh sách quyền Android
            for permission in android_permissions:
                if permission in permissions:
                    row.append(1)  # Quyền có xuất hiện trong file APK
                else:
                    row.append(0)  # Quyền không xuất hiện trong file APK
                    
            row.append(1)  # Type là 0 (Malicious)

            writer.writerow(row)

print("Dữ liệu đã được thêm vào file CSV thành công.")
