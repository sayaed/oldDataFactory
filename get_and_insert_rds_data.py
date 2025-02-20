import pandas as pd
from flask import Flask, jsonify
import pymysql
from sqlalchemy import create_engine


app = Flask(__name__)

# 数据库配置信息
DB_HOST = 'your_db_host'
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_NAME = 'your_database'


@app.route('/api/stock_code/<string:stock_id>', methods=['GET'])
def get_stock_code(stock_id):
    try:
        # 连接到数据库
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     database=DB_NAME)

        with connection.cursor() as cursor:
            # SQL 查询
            sql = "SELECT stock_code FROM stocks WHERE stock_id = %s"
            cursor.execute(sql, (stock_id,))
            result = cursor.fetchone()

        if result:
            stock_code = result[0]
            return jsonify({'stock_code': stock_code})
        else:
            return jsonify({'error': 'Stock ID not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        connection.close()

# 配置参数
DB_CONFIG = {
    "host": "rm-uf6q7zsz3z0jkw53zzo.mysql.rds.aliyuncs.com",  # 数据库外网地址
    "port": 3306,
    "user": "cruyff_admin",
    "password": "W@ngyun123",
    "database": "stock_db",
    # 'ssl': {'ca': '/Users/wangyun/Downloads/ApsaraDB-CA-Chain/ApsaraDB-CA-Chain.pem'}
}

def test_ssl_connection():
    conn = None
    try:
        # 建立 SSL 连接
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            cursor.execute("SHOW STATUS LIKE 'Ssl_cipher'")
            result = cursor.fetchone()
            print(f"SSL 加密协议: {result[1]}")  # 应返回 TLS 协议名称
        print("SSL 连接成功！")
    except pymysql.Error as e:
        print(f"连接失败: {e}")
    finally:
        if conn:
            conn.close()

@app.route('/api/stock_code', methods=['GET'])
def select_all_stock_code_from_aliyun_rds():
    try:
        # 添加 client_flag 参数（可选）
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # SQL 查询
        sql = "select `stock_code` from `stock_db`.`stock_daily_data` where `from_date` = '2025-2-15' ORDER BY `stock_code`"
        cursor.execute(sql)
        result = cursor.fetchall()
        result = [item[0] for item in result]
    except pymysql.Error as e:
        print(f"阿里云数据库错误: {e.args[0]} - {e.args[1]}")
    finally:
        cursor.close()
        conn.close()

    print(len(result))
    return result

def insert_data_to_aliyun_rds():
    try:
        # 添加 client_flag 参数（可选）
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # SQL 插入
        sql = "INSERT INTO `stock_db`.`stock_daily_data` (`from_date`, `close_price`) VALUES (%s, %s, %s)"
        # 批量插入
        values = [
            ('000001', '2021-01-01', 10.0),
            ('000002', '2021-01-01', 20.0),
            ('000003', '2021-01-01', 30.0),
            ('000004', '2021-01-01', 40.0),
            ('000005', '2021-01-01', 50.0),
        ]
        cursor.executemany(sql, values)
        conn.commit()
    except pymysql.Error as e:
        print(f"阿里云数据库错误: {e.args[0]} - {e.args[1]}")
    finally:
        cursor.close()
        conn.close()


def insert_sina_data(df):
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("连接数据库成功！")
        # day,open,high,low,close,volume,code,status
        merge_sql = """
        INSERT INTO test_stock_daily_data (from_date, opening_price_today, highest_price_today, lowest_price_today, close_price_yesterday, volume_today, stock_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        data_tuples = [tuple(x) for x in df.values]
        cursor.executemany(merge_sql, data_tuples)
        conn.commit()
        print("数据插入成功！")
    except pymysql.Error as e:
        print(f"阿里云数据库错误: {e.args[0]} - {e.args[1]}")
    except pd.errors.EmptyDataError:
        print("CSV文件为空。")
    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    # app.run(debug=True)
    select_all_stock_code_from_aliyun_rds()
