import Data
from multidict import MultiDict
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# import csv


# Distribution graphs (histogram/bar graph) of column data
def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = df.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]] # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df.shape
    columnNames = list(df)
    nGraphRow = (nCol + nGraphPerRow - 1) / nGraphPerRow
    plt.figure(num = None, figsize = (3 * nGraphPerRow, 4 * nGraphRow), dpi = 100)
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1, facecolor ='#ECE9E9')
        columnDf = df.iloc[:, i]
        if (not np.issubdtype(type(columnDf.iloc[0]), np.number)):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar(color='grey', edgecolor='blue', linewidth=1.5)
        else:
            columnDf.hist(color='grey', edgecolor='blue', linewidth=1.5)
            columnDf
        plt.ylabel('counts')
        plt.xticks(rotation = 90)
        plt.grid(False)

        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad = 1.0, w_pad = 1.0, h_pad = 1.0)
    plt.show()


def plotheatmap(df):
    df = df.dropna('columns')  # drop columns with NaN
    df = df[[col for col in df if df[col].nunique() > 1]]  # keep columns where there are more than 1 unique values
    if df.shape[1] < 2:
        print(
            f'No correlation plots shown: The number of non-NaN or constant columns ({df.shape[1]}) is less than 2')
        return
    plt.figure(figsize=(40, 40))
    # play with the figsize until the plot is big enough to plot all the columns
    # of your dataset, or the way you desire it to look like otherwise
    print(df.head(5))
    corr = df.corr()
    print(corr.head(5))
    # plot the heatmap
    sns.heatmap(corr,
                xticklabels=corr.columns,
                yticklabels=corr.columns)
    plt.show()



# Scatter and density plots
def plotScatterMatrix(df, plotSize, textSize):
    df = df.select_dtypes(include =[np.number]) # keep only numerical columns
    # Remove rows and columns that would lead to df being singular
    df = df.dropna('columns')
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    columnNames = list(df)
    if len(columnNames) > 10: # reduce the number of columns for matrix inversion of kernel density plots
        columnNames = columnNames[:10]
    df = df[columnNames]
    ax = pd.plotting.scatter_matrix(df, alpha=0.75, figsize=[plotSize, plotSize], diagonal='kde')
    corrs = df.corr().values
    for i, j in zip(*plt.np.triu_indices_from(ax, k = 1)):
        ax[i, j].annotate('Corr. coef = %.3f' % corrs[i, j], (0.8, 0.2), xycoords='axes fraction', ha='center', va='center', size=textSize)
    plt.suptitle('Scatter and Density Plot')
    plt.show()



# testData = Data.readCSV('test-CarData.csv')
data = pd.read_csv('test-CarData.csv')
plotPerColumnDistribution(data, 10, 5)
# plotheatmap(data)
# plotScatterMatrix(data, 9, 10)