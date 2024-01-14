# 在 terminal里安装 pip install akshare --upgrade
import akshare as ak


# 数据类型
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
# 文档
# https://akshare.akfamily.xyz/data/stock/stock.html#id10
# 中小板为002 003开头


if __name__ == '__main__':
    # 返回A股实时数据
    stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    # 按照总市值排序
    stock_zh_a_spot_em_df.sort_values(by='总市值', ascending=True, inplace=True)
    for index, row in stock_zh_a_spot_em_df.iterrows():
        # 排除ST和退市股票
        if "*ST" not in row['名称'] and "ST" not in row['名称'] and '退'not in row['名称'][1:]:
            # 排除科创板
            if row['代码'][:3] != '688':
                # 中小板为002 003开头
                if row['代码'][:3] == '002' or row['代码'][:3] == '003':
                    print(f"名称: {row['名称']}, 代码: {row['代码']}, 总市值: {row['总市值']}")
