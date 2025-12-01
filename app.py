import streamlit as st                 # 用来快速做网页 UI（上传文件、显示结果）
from paddleocr import PaddleOCR        # OCR 主工具（文字检测 + 文字识别）
import re                              # 用于正则抽取字段（日期、金额、发票号等）
import numpy as np
import cv2

# 页面基础设置（标题、布局）
st.set_page_config(
    page_title="发票 OCR DEMO",
    layout="wide",
    page_icon="🦈"
)
st.title("发票 OCR + 字段抽取 DEMO")

# --------- OCR 初始化（只做一次，节省重复加载模型的时间） ----------
@st.cache_resource
def init_ocr():
    # PaddleOCR 初始化参数说明：
    # use_angle_cls=True -> 启用文字方向分类（识别竖排/旋转文本更稳）
    # lang='ch' -> 中文模型
    # show_log=False -> 关闭模型内部日志，终端更干净
    return PaddleOCR(use_angle_cls=True, lang='ch')

ocr = init_ocr()   # 调用缓存函数，第一次会加载模型并缓存（加速后续请求）

# --------- 字段抽取函数（把 OCR 的文本 list -> 结构化字段） ----------
def extract_fields(lines):
    text = "\n".join(lines)
    print(text)

    # 发票号码
    invoice_number = re.search(r"发票号码：(\d+)", text)
    if invoice_number:
        invoice_number = invoice_number.group()
    # 发票时间
    invoice_date = re.search(r'开票日期：(20\d{2}年\d{2}月\d{2}日)', text)
    if invoice_date:
        invoice_date = invoice_date.group()
    # 购买方，售卖方信息
    name = re.findall(r"名称：(.+)", text)
    print(name)
    purchase_name = name[0]
    support_name = name[1]

    number = re.findall(r"统一社会信用代码/纳税人识别号：([0-9A-Z]{18})", text)
    print(number)
    purchase_number = number[0]
    support_number = number[1]
    # 金额
    money_line = re.findall(r"￥(\d+\.\d{2})", text)
    print(money_line)
    money = money_line[2]

    # 开票人姓名
    drawer = re.search(r"开票人：(.+)", text)
    drawer_name = drawer.group(1)
    return {
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "purchase_name": purchase_name,
        "purchase_number": purchase_number,
        "support_name": support_name,
        "support_number": support_number,
        "money": money,
        "drawer": drawer_name
    }

# --------- Streamlit 文件上传控件 ----------
uploaded_file = st.file_uploader("上传发票图片(jpg/png)", type=["jpg", "png", "jpeg"])
print(uploaded_file)
# 如果用户上传了文件，进行展示 + 识别
if uploaded_file is not None:
    # 在网页上显示上传的图片
    st.image(uploaded_file, caption="上传的发票", use_column_width=True)

    # 显示识别进度指示器
    with st.spinner("识别中……"):
        # 注意：paddleocr 的 ocr() 可以接受文件路径、numpy 数组 或者二进制图像数据
        # uploaded_file.read() 返回字节；部分 paddleocr 版本可以直接接受 bytes 输入
        # 如果报错，可把 bytes 转为 numpy + cv2.imdecode
        data = uploaded_file.read()
        img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        res = ocr.predict(img)



    if not res:
        print("解析失败：这张图片没有识别出任何文本")
        exit()
    # 从复杂的 res 中拿文本列表（此处假设使用的 pipeline 返回 dict）
    lines = res[0]['rec_texts']

    # 抽取字段并显示
    fields = extract_fields(lines)

    st.subheader("抽取字段结果")
    st.json(fields)  # 以 JSON 形式漂亮展示

    st.subheader("全部OCR文本")
    st.code("\n".join(lines))
