import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


fig, ax = plt.subplots()


def getProfitBars():
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
    profitHistory.plot.bar(x='Symbol', y='Profit', ax=ax, width=0.9)

    annotation = ax.annotate(
        text='',
        xy=(0, 0),
        xytext=(-100, 15), # distance from x, y
        textcoords='offset points',
        bbox={'boxstyle': 'round', 'fc': 'w'},
        arrowprops={'arrowstyle': '->'},
        color="White"
    )
    annotation.set_visible(False)

    netProfitAnnotation = ax.annotate(
        text=f"Net Profits: {profitHistory['Profit'].sum()}",
        xy=(-0.5, 4),
        textcoords='offset points',
        bbox={'boxstyle': 'round', 'facecolor' : "purple"},
        color="White"
    )
    netProfitAnnotation.set_visible(True)

    lastHoverID = [None]
    def uniquePrint(id, text):
        if id == lastHoverID[0]: return 
        print(text)
        lastHoverID[0] = id

    def on_hover(event):
        showAnnotation = False
        for bar in ax.patches: 
            if bar.contains(event)[0]:
                x_pos = bar.get_x() + bar.get_width() / 2
                row = profitHistory.iloc[int(x_pos)]
                height = max(0, bar.get_height())
                displayText = f"Trading asset: {row['Symbol']}\nProfit: {row['Profit']}"
                annotation.set_text(displayText)
                uniquePrint(x_pos, f"Annotation text:\n{displayText}\n")
                annotation.xy = (x_pos, height + 0.1)
                annotation.get_bbox_patch().set_facecolor("#008080")
                annotation.set_visible(True)
                showAnnotation = True 
        if not showAnnotation: 
            annotation.set_visible(False)
        fig.canvas.draw_idle()
    fig.canvas.mpl_connect('motion_notify_event', on_hover)
    fig.set_size_inches(12, 8)


getProfitBars()


plt.tight_layout()
plt.subplots_adjust(top=0.9, right=0.9, left=0.1) 
plt.show()