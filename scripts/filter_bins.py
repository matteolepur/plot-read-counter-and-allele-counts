import pandas as pd
import pyranges as pr

def read_blacklist_sites(blacklist_path):
    """Read blacklist sites from a file and return as a PyRanges object."""
    # Directly read the blacklist file into a DataFrame
    df = pd.read_csv(blacklist_path, sep=' ', skiprows=1, names=['Chromosome', 'Start', 'End', 'Width'])
    # Drop the 'Width' column as it's not needed for PyRanges
    df = df.drop(columns=['Width'])
    return pr.PyRanges(df)

def read_genomic_bins(corr_read_counts_path):
    """Read genomic bins from a .tsv file and return as a PyRanges object."""
    df = pd.read_csv(corr_read_counts_path, sep='\t')
    df = df[['chr', 'start', 'end', 'copy']]
    df = df.rename(columns={'chr': 'Chromosome', 'start': 'Start', 'end': 'End'}) 
    return pr.PyRanges(df)


def main(args):
    # Step 1: Read genomic bins into a PyRanges object
    genomic_bins = read_genomic_bins(args.corr_read_counts)  # Assuming BED format for simplicity
    
    # Step 2: Read blacklist sites into a PyRanges object
    blacklist_sites = read_blacklist_sites(args.blacklist_regions)
    
    # Step 3: Filter out blacklist sites from genomic bins
    filtered_bins = genomic_bins.subtract(blacklist_sites)
    
    # Step 4: Convert back to a DataFrame for output
    df_filtered_bins = filtered_bins.df
    df_filtered_bins.to_csv(args.filtered_corr_read_counts, sep='\t', index=False)
    
    
if __name__ == "__main__":
    from argparse import ArgumentParser
    
    default0 = 'numbers-runs/tfri-pair-4-clone-a/cnv/filtered_plasma_corr_read_counts.tsv'  
    default1 = 'numbers-runs/tfri-pair-4-clone-a/cnv/plasma_corr_read_counts.tsv'
    default2 = 'blacklist_2018.10.23.txt'
    
    parser = ArgumentParser()
    parser.add_argument("--filtered-corr-read-counts", type=str, default=default0)
    parser.add_argument("--corr-read-counts", type=str, default=default1)
    parser.add_argument("--blacklist-regions", type=str, default=default2)
    cli_args = parser.parse_args()
    
    main(cli_args)
    