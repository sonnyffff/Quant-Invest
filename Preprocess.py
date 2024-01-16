import akshare as ak
import time


def preprocess():
    start_time = time.time()
    # 返回A股实时数据
    stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    print("get!")
    # 筛选

    for index, row in stock_zh_a_spot_em_df.iterrows():
        # 排除ST和退市股票
        if "*ST" in row['名称'] or "ST" in row['名称'] or '退' in row['名称'][1:] or \
                not (row['代码'][:3] == '002' or row['代码'][:3] == '003') or row['涨跌幅'] > 9.9:
            # print(
            #     f"名称: {row['名称']}, 代码: {row['代码']}, 总市值: {row['总市值']}, 涨跌幅: {row['涨跌幅']}")
            stock_zh_a_spot_em_df = stock_zh_a_spot_em_df.drop(index)

    temp = []
    length = len(stock_zh_a_spot_em_df)
    i = 1
    for index, row in stock_zh_a_spot_em_df.iterrows():
            l = ak.stock_zh_a_hist(symbol=row['代码'], period='daily')[-5:]['成交额'].values.tolist()
            print(str(i) + "/" + str(length))
            temp.append(sum(l)/5)
            i+=1
    stock_zh_a_spot_em_df['近五日平均成交额'] = temp
    # 排序
    stock_zh_a_spot_em_df.sort_values(by='近五日平均成交额', ascending=True, inplace=True)

    ranking_score = []
    # （股票数– 股票排名 + 1） / 股票数 * 100
    for rank in range(1, len(stock_zh_a_spot_em_df) + 1):
        ranking_score.append((len(stock_zh_a_spot_em_df) - rank + 1) / len(stock_zh_a_spot_em_df) * 100)
    stock_zh_a_spot_em_df['成交额排名分'] = ranking_score

    stock_zh_a_spot_em_df.to_excel('成交额.xlsx', index=False)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"花费时间: {elapsed_time} seconds")

if __name__ == '__main__':
    preprocess()