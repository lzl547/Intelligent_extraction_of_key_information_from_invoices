import re
print(re.match('www', 'www.runoob.com'))  # 在起始位置匹配
print(re.match('com', 'www.runoob.com'))
lines = ["第一行", "第二行", "第三行"]
text = "\n".join(lines)
print(text)
# 不在起始位置匹配