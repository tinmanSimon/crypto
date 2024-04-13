import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

def getTradeProfits():
    fig, ax = plt.subplots()
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
    profitHistory.plot.bar(use_index=True, y='Profit', ax=ax)


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

    def on_hover(event):
        showAnnotation = False
        for bar in ax.patches: 
            if bar.contains(event)[0]:
                x_pos = bar.get_x() + bar.get_width() / 2
                height = bar.get_height()
                displayText = "i sdaijfsadfjhiuwefundsafn waeuihf dsia nfjksdahfhjdasbaif nd"
                annotation.set_text(displayText)
                print(f"Annotation text:\n {displayText}")
                annotation.xy = (x_pos, height + 0.1)
                annotation.get_bbox_patch().set_facecolor("#008080")
                annotation.set_visible(True)
                showAnnotation = True 
        if not showAnnotation: 
            annotation.set_visible(False)
        fig.canvas.draw_idle()
    fig.canvas.mpl_connect('motion_notify_event', on_hover)

getTradeProfits()





plt.show()