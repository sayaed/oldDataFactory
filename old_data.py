import pandas as pd
import requests
import time
from get_and_insert_rds_data import select_all_stock_code_from_aliyun_rds, insert_sina_data


def get_sina_stock_data(symbol, start_date, end_date):
    url = f"https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={symbol}&scale=240&ma=no&datalen=1000"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df['day'] = pd.to_datetime(df['day'], format='%Y-%m-%d')
    df = df[(df['day'] >= start_date) & (df['day'] <= end_date)]
    return df

def get_sina_all_stock_data(start_date, end_date):
    stock_codes = select_all_stock_code_from_aliyun_rds()
    data = []
    for i, code in enumerate(stock_codes):
        if i >= 4629:  # 限制爬取数量
            if code.startswith('6'):
                stock_symbol = 'sh' + code
            elif code.startswith('0') or code.startswith('3'):
                stock_symbol ='sz' + code
            # 43, 82, 83, 87, 88, 92
            elif code.startswith('43') or code.startswith('82') or code.startswith('83') or code.startswith('87') or code.startswith('88') or code.startswith('92'):
                stock_symbol = 'bj' + code
            else:
                continue
            url = f"https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={stock_symbol}&scale=240&ma=no&datalen=1000"
            response = requests.get(url)
            data = response.json()
            df = pd.DataFrame(data)
            if df.empty:
                print(f"股票{code}没有数据")
            else:
                df['code'] = code
            # 新增status字段
            # df['status'] = df['close'].apply(lambda x: 'close' if x == '' else 'normal')
            # df['day'] = pd.to_datetime(df['day'], format='%Y-%m-%d')
            # df = df[(df['day'] >= start_date) & (df['day'] <= end_date)]
                df.to_csv(f'sina_stock_{stock_symbol}.csv', index=False)
                insert_sina_data(df)
                print(f"已爬取{i+1}/{len(stock_codes)}只股票{stock_symbol}数据")
                time.sleep(3)  # 防止请求过于频繁
        else:
            continue


def get_a_stock_codes():
    base_url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    markets = ['sh_a', 'sz_a', 'bj_a']  # 沪市A股、深市A股、北京A股
    codes = []
    symbol = []

    for node in markets:
        page = 1
        while True:
            params = {
                'page': page,
                'num': 100,  # 每页最大支持100条
                'sort': 'symbol',
                'asc': 1,
                'node': node
            }
            try:
                response = requests.get(base_url, params=params, headers=headers)
                response.raise_for_status()  # 检查HTTP错误
                data = response.json()

                if not data:
                    break  # 无数据时退出循环

                # 提取股票代码
                current_codes = [item.get('code') for item in data if item.get('code')]
                codes.extend(current_codes)

                symbol.extend([item.get('symbol') for item in data if item.get('symbol')])

                # 判断是否还有下一页
                if len(data) < params['num']:
                    break
                else:
                    page += 1
                    time.sleep(1)  # 防止请求过于频繁
            except Exception as e:
                print(f"请求失败: {e}")
                break

    # 去重并排序
    unique_codes = list(set(codes))
    unique_codes.sort()
    unique_symbol = list(set(symbol))
    unique_symbol.sort()
    return unique_codes, unique_symbol


if __name__ == "__main__":
    # # 示例：爬取平安银行（sz000001）数据
    # data = get_sina_stock_data("sz000001", "2023-01-01", "2025-2-13")
    # data.to_csv('sina_stock.csv', index=False)

    # stock_codes, symbol = get_a_stock_codes()
    # print(f"共获取到 {len(stock_codes)} 只A股股票代码")
    # print("示例代码:", stock_codes[:10])  # 打印前10个代码
    # print("示例代码:", symbol[:10])  # 打印前10个代码

    # start_date = "2024-01-01"
    start_date = "2025-02-12"
    end_date = "2025-02-13"
    get_sina_all_stock_data(start_date, end_date)