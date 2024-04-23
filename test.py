import pandas as pd
from androguard.core.bytecodes.apk import APK
from Permissions_Android import AOSP_PERMISSIONS
from RandomForest import df, model

android_permissions = sorted(list(AOSP_PERMISSIONS.keys()))

def extract_permissions(apk_file):
    """Trích xuất danh sách quyền từ tệp APK."""
    apk = APK(apk_file)
    return apk.get_permissions()

def generate_feature_vector(permissions):
    """Biểu diễn quyền dưới dạng vector đặc trưng."""
    feature_vector = []
    for permission in android_permissions:
        if permission in permissions:
            feature_vector.append(1)
        else:
            feature_vector.append(0)
    return feature_vector
new_apk_file = input("Input directory of apk: ")

try:
    permissions = extract_permissions(new_apk_file)
    feature_vector = generate_feature_vector(permissions)
    apk_features_to_check = pd.DataFrame([feature_vector], columns=df.columns[1:331])
    apk_features_to_check = apk_features_to_check.drop(columns=['type'])
    # Dự đoán nhãn cho mẫu mới
    predicted_label = model.predict(apk_features_to_check)

    print("Predicted label for the new sample:", predicted_label)
except:
    print(f"File not found!\nPlease check the directory")
