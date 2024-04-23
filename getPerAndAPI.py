import os
import pandas as pd
from androguard.core.bytecodes.apk import APK
from androguard.misc import AnalyzeAPK, get_default_session
from Permissions_Android import AOSP_PERMISSIONS

# Hàm trích xuất cuộc gọi API từ một tệp APK
def EXTRACT_API_CALLS(apk):
    res = []
    sess = get_default_session()
    app, list_of_dex, dx = AnalyzeAPK(apk, session=sess)
    for method in dx.get_methods():
        for _, call, _ in method.get_xref_to():
            temp_list = call.class_name.split('/')
            if temp_list[0] == "Landroid" and temp_list[1] in ["content", "app", "bluetooth", "location", "media", "net", "nfc", "provider", "telecom", "telephony"]:
                res.append(temp_list[-1] + call.name)
    sess.reset()
    return list(set(res))

# Thư mục chứa các file APK
apk_folder = "D:/BTL/BTL Python/FileAPK"

# Danh sách tên các permissions Android
android_permissions = sorted(list(AOSP_PERMISSIONS.keys()))

# Tạo DataFrame để lưu dữ liệu
result_df = pd.DataFrame(columns=android_permissions)

# Lặp qua từng file trong thư mục
for filename in os.listdir(apk_folder):
    if filename.endswith(".apk"):
        apk_file = os.path.join(apk_folder, filename)
        apk = APK(apk_file)

        # Trích xuất danh sách quyền từ file APK
        permissions = apk.get_permissions()

        # Trích xuất danh sách API từ file APK
        apk_api = EXTRACT_API_CALLS(apk_file)

        # Tạo một hàng mới trong DataFrame và gán giá trị 1 cho các permission và API có trong tệp APK
        row = {permission: 1 if permission in permissions else 0 for permission in android_permissions}
        row.update({api: 1 if api in apk_api else 0 for api in apk_api})
        
        # Thêm hàng mới vào DataFrame
        result_df = result_df.append(row, ignore_index=True)

# Lưu DataFrame vào file CSV
output_csv = "D:/BTL/BTL Python/permissions_and_api.csv"
result_df.to_csv(output_csv, sep=",", index=False)
print(f"Results saved to: {output_csv}")
