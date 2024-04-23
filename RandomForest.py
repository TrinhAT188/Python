import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Đọc dữ liệu từ tệp CSV
df = pd.read_csv("C:/Users/Admin/Downloads/train (1).csv", header=0, sep=';')

# Chuyển đổi dữ liệu thành kiểu số nguyên
df = df.astype(int)

# # Phân tích tĩnh: Lấy top 10 quyền được sử dụng cho mã độc
# malicious_permissions_top10 = pd.Series(df[df['type'] == 1].sum(axis=0)).sort_values(ascending=False)[1:11]

# # Hiển thị biểu đồ cho top 10 quyền độc hại
# malicious_permissions_top10.plot.bar(color="red")
# plt.title('Top 10 Malicious Permissions')
# plt.xlabel('Permission')
# plt.ylabel('Count')
# plt.show()

# # Hiển thị top 10 quyền cho ứng dụng không phải độc hại
# benign_permissions_top10 = pd.Series(df[df['type'] == 0].sum(axis=0)).sort_values(ascending=False)[:10]
# benign_permissions_top10.plot.bar()
# plt.title('Top 10 Benign Permissions')
# plt.xlabel('Permission')
# plt.ylabel('Count')
# plt.show()

# Mô hình học máy
X_train, X_test, y_train, y_test = train_test_split(df.iloc[:, 1:330], df['type'], test_size=0.20, random_state=42)

# Huấn luyện mô hình RandomForest
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Đánh giá mô hình
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:")
print(classification_report(y_test, y_pred))
