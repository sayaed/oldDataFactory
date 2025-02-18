import pandas as pd


def read(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


# 假设df是包含股票K线数据的DataFrame，包含'high', 'low', 'open', 'close'列
def find_top_bottom(df):
    tops = []
    bottoms = []

    for i in range(1, len(df) - 1):
        prev, current, next_ = df.iloc[i - 1], df.iloc[i], df.iloc[i + 1]

        # 顶分型
        if current['high'] > prev['high'] and current['high'] > next_['high'] and \
                current['low'] > prev['low'] and current['low'] > next_['low']:
            tops.append(current)

        # 底分型
        if current['low'] < prev['low'] and current['low'] < next_['low'] and \
                current['high'] < prev['high'] and current['high'] < next_['high']:
            bottoms.append(current)

    return tops, bottoms

# 示例使用
# df = pd.read_csv('stock_data.csv')  # 加载股票数据
# tops, bottoms = find_top_bottom(df)
# print("顶分型:", tops)
# print("底分型:", bottoms)

# 导入必要的模块
import ast


# 读取本地txt文件的内容
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


# 计算字典中的键数量
def count_dict_keys(content):
    try:
        # 将字符串内容转换为字典
        data_dict = ast.literal_eval(content)

        # 检查是否为字典
        if isinstance(data_dict, dict):
            # 计算字典中的键数量
            key_count = len(data_dict.keys())
            return key_count
        else:
            print("文件内容不是有效的字典格式。")
            return None
    except (ValueError, SyntaxError):
        print("文件内容格式错误，无法解析为字典。")
        return None


# 主函数
if __name__ == "__main__":
    # 文件路径
    file_path = '/Users/wangyun/Documents/stock_info1.txt'  # 请确保文件路径正确

    # 读取文件内容
    file_content = read_file(file_path)

    # 计算字典中的键数量
    keys_count = count_dict_keys(file_content)

    # 打印结果
    if keys_count is not None:
        print(f"字典中的键数量为: {keys_count}")
