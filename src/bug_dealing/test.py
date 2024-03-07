import os

# 定义目录路径
directory_path = "../../data/data_by_ocean/Eclipse_raw"

# 检查目录是否存在
if os.path.exists(directory_path):
    print("目录 {directory_path} 存在。")
else:
    print("目录 {directory_path} 不存在。")
