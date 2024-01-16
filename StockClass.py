import akshare as ak
from openpyxl import load_workbook
if __name__ == '__main__':
    # l = ak.stock_zh_a_hist(symbol = '603777', period = 'daily')[-5:]['成交额'].values.tolist()
    # print(l)
    # stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    # print("get!")
    # # 筛选
    # i = 0
    # for index, row in stock_zh_a_spot_em_df.iterrows():
    #     # 排除ST和退市股票
    #     if "*ST" in row['名称'] or "ST" in row['名称'] or '退' in row['名称'][1:] or \
    #             not (row['代码'][:3] == '002' or row['代码'][:3] == '003') or row['涨跌幅'] > 9.9:
    #         # print(
    #         #     f"名称: {row['名称']}, 代码: {row['代码']}, 总市值: {row['总市值']}, 涨跌幅: {row['涨跌幅']}")
    #         stock_zh_a_spot_em_df = stock_zh_a_spot_em_df.drop(index)
    #         i += 1
    # print(stock_zh_a_spot_em_df)
    wb = load_workbook("成交额.xlsx")
    sheet = wb.worksheets[0]
    temp = dict()
    for i, row in enumerate(sheet):
        if i > 0:
            temp[row[1].value] = row[-1].value
    print(temp)

