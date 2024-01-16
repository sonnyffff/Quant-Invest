# 在 terminal里安装 pip install akshare --upgrade
import akshare as ak
import time
from openpyxl import load_workbook

# 数据类型
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
# 文档
# https://akshare.akfamily.xyz/data/stock/stock.html#id10
# 中小板为002 003开头
# 排名分计算规则
# https://guorn.com/stock/help#chapter2


if __name__ == '__main__':
    start_time = time.time()
    # read 成交额
    wb = load_workbook("成交额.xlsx")
    sheet = wb.worksheets[0]
    temp = dict()
    for i, row in enumerate(sheet):
        if i > 0:
            temp[row[1].value] = row[-1].value

    # 返回A股实时数据
    stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    print("get!")
    # 筛选

    for index, row in stock_zh_a_spot_em_df.iterrows():
        # 排除ST和退市股票
        if "*ST" in row['名称'] or "ST" in row['名称'] or '退' in row['名称'][1:] or \
                not(row['代码'][:3] == '002' or row['代码'][:3] == '003') or row['涨跌幅'] > 9.9:
                    # print(
                    #     f"名称: {row['名称']}, 代码: {row['代码']}, 总市值: {row['总市值']}, 涨跌幅: {row['涨跌幅']}")
                    stock_zh_a_spot_em_df = stock_zh_a_spot_em_df.drop(index)

    # 按照总市值排序
    stock_zh_a_spot_em_df.sort_values(by='总市值', ascending=True, inplace=True)
    ranking_score = []
    # （股票数– 股票排名 + 1） / 股票数 * 100
    for rank in range(1, len(stock_zh_a_spot_em_df) + 1):
        ranking_score.append((len(stock_zh_a_spot_em_df) - rank + 1) / len(stock_zh_a_spot_em_df) * 100)
    stock_zh_a_spot_em_df['总市值排名分'] = ranking_score

    # 按照流通市值排序
    stock_zh_a_spot_em_df.sort_values(by='流通市值', ascending=True, inplace=True)
    stock_zh_a_spot_em_df['流通市值排名分'] = ranking_score

    # 按照收盘价排序
    stock_zh_a_spot_em_df.sort_values(by='昨收', ascending=True, inplace=True)
    stock_zh_a_spot_em_df['收盘价排名分'] = ranking_score

    # 按照成交额排序
    deall = []
    for index, row in stock_zh_a_spot_em_df.iterrows():
        deall.append(temp[row['代码']])
    stock_zh_a_spot_em_df['成交额排名分'] = deall

    # 计算权重
    ranking_score = []
    for index, row in stock_zh_a_spot_em_df.iterrows():
        ranking_score.append(row['总市值排名分'] * 38 + row['流通市值排名分'] * 90 + row['收盘价排名分'] * 11 + + row['成交额排名分'] * 7)
    stock_zh_a_spot_em_df['总排名分'] = ranking_score


    stock_zh_a_spot_em_df.sort_values(by='总排名分', ascending=False, inplace=True)

    print(stock_zh_a_spot_em_df.head(23))

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"花费时间: {elapsed_time} seconds")

