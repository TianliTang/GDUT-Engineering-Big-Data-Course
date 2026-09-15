# 第2讲学生操作包

## 用途

本包配套“工程数据表达与Python／Jupyter预备”的上机部分。学生Notebook不预留运行输出；课堂从第一个单元开始顺序运行。

目标环境：Windows 64位、Python 3.12.10、`D:\EngineeringBigData\venv`、JupyterLab。课程环境由管理员课前统一配置，课堂不安装Anaconda或临时下载软件包。

## 当堂练习与完成标准

教师演示结束后，学生独立完成约15分钟的操作：

1. 运行到缺失检查，核对18行×12列以及两个各缺失1项的字段；
2. 将`FOCUS_RESULT`设为“复核”，核对4条筛选结果；
3. 将`GROUP_FIELD`设为`result`，核对通过11、复核4、整改3；
4. 生成分组统计图，再执行Restart Kernel and Run All；
5. 保存Notebook，并确认自检结果为PASS。

完成后应保留三个结果：保存后的`第02讲_学生操作.ipynb`、`outputs/分组统计图.png`和`outputs/自检结果.txt`。

## 文件

- `第02讲_学生操作.ipynb`：读取、检查、筛选、分组、绘图与自检；
- `环境自检.py`：在命令行核对解释器、软件包和数据路径；
- `data/构件检查示例数据.csv`：18行构件检查事件教学合成数据；
- `data/数据字典.md`：字段含义、一行粒度、键、尺度和预期分布；
- `outputs/`：运行后保存分组统计图和自检结果。

## 启动

在Windows命令提示符中运行：

```text
D:
cd \EngineeringBigData
venv\Scripts\activate
python --version
jupyter lab
```

命令行前应出现`(venv)`，Python版本应为3.12.10。使用JupyterLab期间保留命令窗口。

## 操作

1. 将完整操作包放入`D:\EngineeringBigData\L02`，不要移动`data`目录；
2. 在JupyterLab中打开`第02讲_学生操作.ipynb`，右上角选择Python 3内核；
3. 从上到下运行，确认数据为18行、12列；
4. 将`FOCUS_RESULT`设为“复核”，应得到4条记录；
5. 将`GROUP_FIELD`设为`result`，应得到通过11、复核4、整改3；
6. 执行Restart Kernel and Run All；
7. 确认`outputs/分组统计图.png`和`outputs/自检结果.txt`已经生成。

Notebook最后设有“当堂记录与课后复做”，学生需要回答缺失字段、时间字段存储类型和统计单位三个问题。

出现问题时，记录电脑编号、当前命令、失败单元格、报错第一行和最后一行，不在课堂上自行安装软件包。
