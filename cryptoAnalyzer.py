import pandas as pd
import matplotlib.pyplot as plt

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
    profitHistory = pd.DataFrame(newRows, columns=['Symbol', 'Profit']).sort_values(by='Profit')
    print(profitHistory)
    print(profitHistory['Profit'].sum())
    profitHistory.plot.bar(x='Symbol', y='Profit')

getTradeProfits()





plt.show()
