import requests
import pandas as pd

url = f"https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol=sz301173&scale=240&ma=no&datalen=10"
response = requests.get(url)
data = response.json()
print(data)
df = pd.DataFrame(data)
print(df)
code = '301173'
if df.empty:
    print(f"股票{code}没有数据")
else:
    df['code'] = code
# 新增status字段
# df['status'] = df['close'].apply(lambda x: 'close' if x == '' else 'normal')
# df['day'] = pd.to_datetime(df['day'], format='%Y-%m-%d')
# df = df[(df['day'] >= start_date) & (df['day'] <= end_date)]
    df.to_csv(f'sina_stock_{stock_symbol}.csv', index=False)