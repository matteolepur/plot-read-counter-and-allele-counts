import pandas as pd
from pathlib import Path

from plot_bins import plot_bins

        
def preprocess_for_plotting(df_cor_rc: pd.DataFrame) -> pd.DataFrame:
    """
    Args:
        df_cor_rc: pd.DataFrame of corrected read counts
    
    Returns:
        pd.DataFrame: preprocessed data for plotting
    """
    df_bins = df_cor_rc.copy()
    df_bins.rename(columns={'chr': 'Chromosome', 'start': 'Start', 'end': 'End'}, inplace=True)
    return df_bins


def main(args):
    cnv_plot = Path(args.cnv_plot)
    cnv_plot.parent.mkdir(parents=True, exist_ok=True)
    
    df_cor_rc = pd.read_csv(args.plasma_corr_read_counts, sep='\t')
    df_bins = preprocess_for_plotting(df_cor_rc)
    plot_bins(df_bins, cnv_plot, y_vars=['copy'])


if __name__ == "__main__":
    from argparse import ArgumentParser
    
    default0 = "numbers-runs/tfri-pair-4-clone-a/cnv/plasma_corr_read_counts.tsv"
    default1 = "numbers-runs/tfri-pair-4-clone-a/cnv/plasma_cnv_plot.png"
    
    parser = ArgumentParser()
    parser.add_argument("--plasma-corr-read-counts", type=str, default=default0)
    parser.add_argument("--cnv-plot", type=str, default=default1)
    cli_args = parser.parse_args()
    
    main(cli_args) 