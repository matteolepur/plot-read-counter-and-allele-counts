import pandas as pd
import pyranges as pr

def hg19_read_blacklist_sites(blacklist_path):
    """Read blacklist sites from a file and return as a PyRanges object."""
    # Directly read the blacklist file into a DataFrame
    df = pd.read_csv(blacklist_path, sep=' ', skiprows=1, names=['Chromosome', 'Start', 'End', 'Width'])
    # Drop the 'Width' column as it's not needed for PyRanges
    df = df.drop(columns=['Width'])
    return pr.PyRanges(df)

def hg38_read_blacklist_sites(blacklist_path):
    """Read blacklist sites from a file and return as a PyRanges object."""
    # Directly read the blacklist file into a DataFrame
    df = pd.read_csv(blacklist_path, sep='\t', skiprows=1, names=['Chromosome', 'Start', 'End', 'GapType'])
    # Drop the 'Width' column as it's not needed for PyRanges
    df = df.drop(columns=['GapType'])
    return pr.PyRanges(df)

def read_blacklist_sites(blacklist_path: str, reference_genome: str):
    if reference_genome == 'hg19':
        return hg19_read_blacklist_sites(blacklist_path)
    elif reference_genome == 'hg38':
        return hg38_read_blacklist_sites(blacklist_path)
    else:
        raise ValueError(f"Unsupported reference genome: {reference_genome}")

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
    blacklist_sites = read_blacklist_sites(args.blacklist_regions, args.reference_genome)
    
    # Step 3: Filter out blacklist sites from genomic bins
    filtered_bins = genomic_bins.subtract(blacklist_sites)
    
    # Step 4: Convert back to a DataFrame for output
    df_filtered_bins = filtered_bins.df
    df_filtered_bins.to_csv(args.filtered_corr_read_counts, sep='\t', index=False)
    
    
if __name__ == "__main__":
    from argparse import ArgumentParser
    
    default0 = '/home/matteo/Desktop/anything-cfClone/cfclone-repos/cfclone-allele-repos/generate-count-data/plot-data/numbers-runs/TNBC-CID0000391/cnv/filtered_plasma_corr_read_counts.tsv'  
    default1 = '/home/matteo/Desktop/anything-cfClone/cfclone-repos/cfclone-allele-repos/generate-count-data/plot-data/numbers-runs/TNBC-CID0000391/cnv/plasma_corr_read_counts.tsv'
    default2 = '/home/matteo/Desktop/anything-cfClone/cfclone-repos/cfclone-allele-repos/generate-count-data/plot-data/references/blacklist_GRCh38.GCA_000001405.2_centromere_acen.txt'
    default3 = 'hg38'
     
    parser = ArgumentParser()
    parser.add_argument("--filtered-corr-read-counts", type=str, default=default0)
    parser.add_argument("--corr-read-counts", type=str, default=default1)
    parser.add_argument("--blacklist-regions", type=str, default=default2)
    parser.add_argument("--reference-genome", type=str, default=default3)
    cli_args = parser.parse_args()
    
    main(cli_args)
    