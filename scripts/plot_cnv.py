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
    plots_dir = Path(args.plots_dir)
    plots_dir.mkdir(parents=True, exist_ok=True)
    
    df_cor_rc = pd.read_csv(args.plasma_corr_read_counts, sep='\t')
    df_bins = preprocess_for_plotting(df_cor_rc)
    
    cnv_plot_path = plots_dir.joinpath("plasma_cnv_plot.png")
    plot_bins(df_bins, cnv_plot_path, y_vars=['copy'])


if __name__ == "__main__":
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument("--plasma-corr-read-counts", type=str, required=True)
    parser.add_argument("--plots-dir", type=str, required=True)
    cli_args = parser.parse_args()
    
    main(cli_args) 