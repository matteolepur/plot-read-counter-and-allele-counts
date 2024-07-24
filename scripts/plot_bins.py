import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from statistics import median

from pathlib import Path

from typing import Union, List


def plot_bins(df_bins: pd.DataFrame, png_path: Path, y_vars: List[str]) -> None:
    """
    Args:
        df_bins: pd.DataFrame of genomic data in bed format 
        png_path: path to save output
    
    Notes:
        Columns of df_bins must be in the following form:
            Chromosome, Start, End, yvar0, yvar1, yvar2, ...
    """
    # create sup figure
    num_rows = len(y_vars)
    fig = plt.figure(figsize=(16, num_rows * 4))
    grid = fig.add_gridspec(nrows=num_rows, ncols=1, hspace=0.5)

    # plot copy in sub fig
    for row_idx, y_var in enumerate(y_vars):
        df_bins_yvar = df_bins[['Chromosome', 'Start', 'End', y_var]]
        chrms = df_bins_yvar['Chromosome'].unique()
        chrms_sizes = df_bins_yvar['Chromosome'].value_counts()
        width_ratios = [chrms_sizes[x] for x in chrms]
        sub_grid = grid[row_idx].subgridspec(nrows=1, ncols=len(chrms), width_ratios=width_ratios, wspace=0.01)
        _plot_bins(df_bins_yvar, sub_grid, title=y_var)

    # store sup figure
    grid.tight_layout(fig)
    fig.savefig(png_path, bbox_inches='tight')


def _plot_bins(df_bins: pd.DataFrame, sub_grid, title: Union[None, str] = None) -> None:
    """
    Args:
        df_bins: pd.DataFrame of genomic data in .bed format
        sub_grid: subgrid to plot genomic data

    Returns:
        None

    Notes:
        .bed format has columns Chromosome, Start, End, AnyGenomicData
    """
    sub_fig = plt.gcf()
    added_axes = []
    for i, chrm in enumerate(df_bins['Chromosome'].unique()):
        chrom_bins = df_bins[df_bins['Chromosome'] == chrm]
        num_bins = chrom_bins.shape[0]
        chrom_bins['idx'] = np.arange(num_bins)

        ax = sub_fig.add_subplot(sub_grid[0, i])
        added_axes.append(ax)
        ax.scatter(np.arange(num_bins), chrom_bins['copy'], s=1)

        sns.despine(ax=ax, offset=1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        if i != 0:
            ax.spines['left'].set_visible(False)
            ax.set_yticks([])
            ax.set_yticklabels([])
        else:
            ax.tick_params(axis='x', which='major', labelsize=12)

        ax.set_xticks([num_bins / 2])
        ax.set_xticklabels([chrm], fontsize=12)
        
    all_min_y, all_max_y = [], []
    for a in added_axes:  # only use axes that correspond to chroms.
        y_lims = a.get_ylim()
        all_min_y.append(y_lims[0])
        all_max_y.append(y_lims[1])
        
    common_ylim = [median(all_min_y), median(all_max_y)]
    for a in added_axes:
        a.set_ylim(common_ylim)
    
    if title is not None:
        ax = sub_fig.add_subplot(sub_grid[:])
        ax.axis("off")
        ax.set_title(title)
        