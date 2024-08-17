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

def read_genomic_bins(raw_data: str, data_type: str):
    """Read genomic bins from a .tsv file and return as a PyRanges object."""
    if data_type == 'read-counts':
        df = pd.read_csv(raw_data, sep='\t')
        df = df[['chr', 'start', 'end', 'copy']]
        df = df.rename(columns={'chr': 'Chromosome', 'start': 'Start', 'end': 'End'})
    elif data_type == 'hap-counts':
        df = pd.read_csv(raw_data, sep='\t')
        df = df[['chrom', 'hap_block_start', 'hap_block_end', 'allele_a_count', 'allele_b_count']]
        df = df.rename(columns={'chrom': 'Chromosome', 'hap_block_start': 'Start', 'hap_block_end': 'End'})
    return pr.PyRanges(df)


def main(args):
    # Step 1: Read genomic bins into a PyRanges object
    genomic_bins = read_genomic_bins(args.raw_data, args.data_type)  # Assuming BED format for simplicity
    
    # Step 2: Read blacklist sites into a PyRanges object
    blacklist_sites = read_blacklist_sites(args.blacklist_regions, args.reference_genome)
    
    # Step 3: Filter out blacklist sites from genomic bins
    filtered_bins = genomic_bins.subtract(blacklist_sites)
    
    # Step 4: Convert back to a DataFrame for output
    df_filtered_bins = filtered_bins.df
    if args.data_type == 'hap-counts':
        df_filtered_bins = df_filtered_bins.rename(columns={'Chromosome': 'chrom', 'Start':'hap_block_start', 'End':'hap_block_end'})
    df_filtered_bins.to_csv(args.filtered_data, sep='\t', index=False)
    
    
if __name__ == "__main__":
    from argparse import ArgumentParser
    
    default0 = '/home/matteo/Desktop/anything-cfClone/cfclone-repos/cfclone-allele-repos/generate-count-data/plot-data/numbers-runs/TNBC-CID0000391/cnv/filtered_plasma_corr_read_counts.tsv'  
    default1 = "/home/matteo/Desktop/anything-numbers-pulls/cfclone-pulls/pull036/numbers-runs/tnbc/CID0000391/F112602/allele_counts/results/counts/allele_counts.tsv.gz"
    default2 = '/home/matteo/Desktop/anything-cfClone/cfclone-repos/cfclone-allele-repos/generate-count-data/plot-data/references/blacklist_GRCh38.GCA_000001405.2_centromere_acen.txt'
    default3 = 'hg38'
    default4 = 'hap-counts'
    
    parser = ArgumentParser()
    parser.add_argument("--filtered-data", type=str, default=default0)
    parser.add_argument("--raw-data", type=str, default=default1)
    parser.add_argument("--blacklist-regions", type=str, default=default2)
    parser.add_argument("--reference-genome", type=str, default=default3)
    parser.add_argument("--data-type", type=str, default=default4)
    cli_args = parser.parse_args()
    
    main(cli_args)
    