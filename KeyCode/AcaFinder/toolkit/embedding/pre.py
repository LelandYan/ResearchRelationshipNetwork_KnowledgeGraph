import numpy as np
import pandas as pd

e_paper = pd.read_csv("e_paper.csv")
acm_data = pd.read_csv("acm_data.csv")
acm_data = acm_data[["title", "year", "abstract"]]
print(e_paper.head())

# 增加paperID
acm_data["paperID"] = range(len(e_paper) + 1, len(e_paper) + 1 + len(acm_data))

# 切分年限字符串
_, acm_data['year'] = acm_data['year'].str.split(' ', 1).str
# 转化年限类型
acm_data["year"] = acm_data["year"].str.replace(',', '')
acm_data["year"] = pd.to_numeric(acm_data["year"])
# print(acm_data["abstract"])
result = pd.concat([e_paper, acm_data])
result.to_csv(r"e_paper2.csv", sep=',', index=False)
