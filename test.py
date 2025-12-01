from pprint import pprint

from paddleocr import PaddleOCR
import streamlit as st
import json
import re
# import paddleocr
# print(paddleocr.__version__)
ocr = PaddleOCR(
    use_angle_cls=True,
    lang='ch'
)

# for line in result[0]['rec_texts']:
#     print(line)

# exts = [t for t in result[0]['rec_texts']]
# scores = [s for s in result[0]['rec_scores']]
# boxes = [b for b in result[0]['rec_polys']]
# print("*" * 200)
# print(exts)
# print(scores)
# print(boxes)

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

    number = re.findall(r"统一社会信用代码/纳税人识别号：([0-9A-Z]+)", text)
    print(number)
    purchase_number = number[0]
    support_number = number[1]

    # 项目名称
    project = re.findall(r"\*\S+\*\S+", text)
    print(project)

    # 金额
    money_line = re.findall(r"￥(\d+\.\d{2})", text)
    print(money_line)
    money = money_line[2]

    # 开票人姓名
    drawer = re.search(r"开票人：(\S{2,4})", text)
    drawer_name = drawer.group(1)
    print(drawer)
    return {
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "purchase_name": purchase_name,
        "purchase_number": purchase_number,
        "support_name": support_name,
        "support_number": support_number,
        "money": money,
        "drawer": drawer_name,
        "project_line": project
    }


result = ocr.predict("img.png")
print("+" * 100)
fields = extract_fields(result[0]['rec_texts'])
print("+" * 100)
pprint(fields, indent=4)
