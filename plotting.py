import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display, HTML


def add_labels_to_barplot(ax, values, rects, yshift, labels_font_size, fmt):
    for value, rect in zip(values, rects):
        ax.text(rect.get_x() + rect.get_width() / 2,
                rect.get_height() + yshift,
                fmt(value),
                size=labels_font_size,
                color = "black",
                ha='center', va='bottom')


def plot_counts(df : pd.DataFrame,
                column : str,
                ylabel : str,
                df_base : pd.DataFrame = None,
                ylim = None,
                xlabel : str = "",
                figsize=(20,10),
                font_scale=2,
                labels_font_size=26,
                sns_style : str = "whitegrid",
                ylog = False,
                yshift = 2,
                xlabels = None,
                display_counts=False,
                show_value_labels=True,
                fmt = str):

    counts = df[column].value_counts()

    if df_base is not None:
        counts_base = df_base[column].value_counts()
        counts = counts / counts_base

    if display_counts:
        display(counts)

    sns.set()
    sns.set(font_scale=font_scale, style=sns_style)
    f, ax= plt.subplots(1,1, figsize=figsize, sharex=True)

    names = counts.index if xlabels is None else xlabels
    values = counts.loc[names].values

    plot = sns.barplot(x=names, y=values, ax=ax)
    plot.set(xlabel = xlabel,
             ylabel=ylabel,
             ylim=ylim,
             yscale=("log" if ylog else "linear"))

    plot.spines["top"].set_visible(False)
    plot.spines["bottom"].set_visible(True)
    plot.spines["right"].set_visible(False)

    if show_value_labels:
        add_labels_to_barplot(ax, values, plot.patches,
                              yshift, labels_font_size, fmt)

    return plot
