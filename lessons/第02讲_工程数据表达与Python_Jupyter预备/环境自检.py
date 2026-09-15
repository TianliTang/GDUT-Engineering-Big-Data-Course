"""第2讲命令行环境与数据路径自检。"""

from __future__ import annotations

import platform
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import sklearn


TARGET_PYTHON = "3.12.10"
root = Path(__file__).resolve().parent
data_path = root / "data" / "构件检查示例数据.csv"

print("目标Python:", TARGET_PYTHON)
print("当前Python:", platform.python_version())
print("Python executable:", sys.executable)
print("pandas:", pd.__version__)
print("NumPy:", np.__version__)
print("Matplotlib:", matplotlib.__version__)
print("scikit-learn:", sklearn.__version__)
print("data path:", data_path)

if platform.python_version() != TARGET_PYTHON:
    print("WARNING: 当前Python补丁版本与机房目标版本不同，请核对是否已激活课程venv。")

if not data_path.exists():
    raise FileNotFoundError(f"缺少数据文件：{data_path}")

frame = pd.read_csv(data_path)
assert frame.shape == (18, 12), frame.shape
assert frame["inspection_id"].notna().all()
assert frame["inspection_id"].is_unique
assert frame["result"].value_counts().to_dict() == {"通过": 11, "复核": 4, "整改": 3}

print("PASS: 解释器、软件包、数据路径与关键结构检查通过。")
