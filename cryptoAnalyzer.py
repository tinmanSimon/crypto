import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def getTradeProfits():
    tradingHistory = pd.read_csv("./logs/paper-trading-history-all-2024-04-13T15_59_37.071Z.csv")
    uniqueSymbols = list(set(tradingHistory['Symbol']))
    tradingHistory = tradingHistory[tradingHistory['Status'] != 'Cancelled']
    tradingHistory = tradingHistory.groupby(by='Symbol').apply(lambda df: df.reset_index().drop('index', axis=1).sort_values(by=["Closing Time"]), include_groups=False)
    newRows = []
    print(tradingHistory)
    for symbol in uniqueSymbols:
        curHistory = tradingHistory.loc[symbol]
        curRowLength = curHistory.shape[0]
        accumulatedQuantities, accumulatedProfits = 0, 0
        print(f"symbol: {symbol}, curHistory:\n{curHistory}")
        for i in range(curRowLength):
            curRow = curHistory.iloc[i]
            accumulatedQuantities += curRow['Qty'] if curRow['Side'] == 'Buy' else -curRow['Qty']
            accumulatedProfits += -curRow['Qty'] * curRow['Fill Price'] if curRow['Side'] == 'Buy' else curRow['Qty'] * curRow['Fill Price']
            print(f"accumulatedQuantities: {accumulatedQuantities}, accumulatedProfits: {accumulatedProfits}")
            if accumulatedQuantities == 0:
                newRows.append({
                    'Symbol': symbol,
                    'Profit': round(accumulatedProfits, 2),
                    'ads' : [1,2,3]
                })
                accumulatedProfits = 0
                print("\n")
    if not newRows: 
        print("Didn't found any completed trades, return")
        return
    profitHistory = pd.DataFrame(newRows, columns=newRows[0].keys()).sort_values(by='Profit')
    print(profitHistory)
    print(profitHistory['Profit'].sum())
    ax = profitHistory.plot.bar(use_index=True, y='Profit')
    for p in ax.patches:
        x_pos = p.get_x() + p.get_width() / 2
        row = profitHistory.iloc[int(x_pos)]
        tmp = "\n".join([str(val) for val in row['ads']])
        ax.annotate(tmp, (p.get_x() * 1.005, p.get_height() * 1.005))


getTradeProfits()





plt.show()