from androguard.misc import AnalyzeAPK, get_default_session
import os 
import time
import shutil
import csv
import pandas as pd

# Hàm trích xuất cuộc gọi API từ một tệp APK
def EXTRACT_API_CALLS(apk_file):
    res = []
    sess = get_default_session()
    app, list_of_dex, dx = AnalyzeAPK(apk_file, session=sess)
    for method in dx.get_methods():
        for _, call, _ in method.get_xref_to():
            temp_list = call.class_name.split('/')
            if temp_list[0] == "Landroid":
                if temp_list[1] in ["content", "app", "bluetooth", "location", "media", "net", "nfc", "provider", "telecom", "telephony"]:
                    res.append(temp_list[-1] + call.name)
    sess.reset()
    return list(set(res))

# Đọc danh sách API từ tệp Excel
filename = "../apilist.xlsx"
df = pd.read_excel(filename)

# Đường dẫn đến thư mục chứa các tệp APK
apk_directory = "./uploaded_files"

# Tạo một DataFrame trống để lưu kết quả
result_df = pd.DataFrame(columns=df.columns)

# Lặp qua các tệp APK trong thư mục
for apk in os.listdir(apk_directory):
    apk_path = os.path.join(apk_directory, apk)
    res = []
    start = time.time()
    apkapi = EXTRACT_API_CALLS(apk_path)
    for api in df.columns:
        if api in apkapi:
            res.append(1)
        else:
            res.append(0)
    result_df = result_df.append(pd.Series(res, index=df.columns), ignore_index=True)
    print(result_df)

# Lưu kết quả vào một tệp CSV
result_df.to_csv("../apioutput.csv", sep=",", index=True)
