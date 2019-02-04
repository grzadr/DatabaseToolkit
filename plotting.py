import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display, HTML


def plot_counts(df : pd.DataFrame,
                column : str,
                ylabel : str,
                ylim = None,
                figsize=(20,10),
                font_scale=2,
                labels_font_size=26,
                sns_style : str = "whitegrid",
                ylog = False,
                xlabels = None,
                display_counts=False):

    counts = df[column].value_counts()

    if display_counts:
        display(counts)

    sns.set()
    sns.set(font_scale=font_scale)
    sns.set_style(sns_style)
    f, ax= plt.subplots(1,1, figsize=figsize, sharex=True)

    names = counts.index if xlabels is None else xlabels
    values = counts.loc[names].values

    plot = sns.barplot(x=names, y=values, ax=ax)
    plot.set(xlabel = "",
             ylabel=ylabel,
             ylim=ylim,
             yscale=("log" if ylog else None))

    for value, rect in zip(values, plot.patches):
        ax.text(rect.get_x() + rect.get_width() / 2,
                rect.get_height() + 6,
                str(value),
                size=labels_font_size,
                color = "black",
                ha='center', va='bottom')
