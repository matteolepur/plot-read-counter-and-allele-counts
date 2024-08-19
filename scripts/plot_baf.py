import pandas as pd

from plot_bins import plot_bins


CHROM_ORDER = [str(c) for c in range(0,23)] + ['X', 'Y']

def calculate_baf(df_allele_counts: pd.DataFrame) -> pd.DataFrame:
    df_hap_counts = df_allele_counts.groupby(["chrom", "hap_block_start", "hap_block_end"])['allele_a_count', 'allele_b_count'].sum()
    df_hap_counts['depth'] = df_hap_counts['allele_a_count'] + df_hap_counts['allele_b_count']
    df_hap_counts['baf'] = df_hap_counts['allele_b_count'] / df_hap_counts['depth']
    return df_hap_counts

def clean_dataframe_for_plotting(df_hap_data: pd.DataFrame, reference_genome: str) -> pd.DataFrame:
    # reindex
    df_bins = df_hap_data.reset_index()
    df_bins.rename(columns={'chrom': 'Chromosome', 'hap_block_start': 'Start', 'hap_block_end': 'End'}, inplace=True)
    
    # reorder
    if reference_genome == 'hg38':
        df_bins['Chromosome'] = df_bins['Chromosome'].str[3:]
        df_bins['Chromosome'] = pd.Categorical(df_bins['Chromosome'], categories=CHROM_ORDER, ordered=True)
        df_bins = df_bins.sort_values(['Chromosome', 'Start'])
        
    return df_bins


def main(args):
    df_allele_counts = pd.read_csv(args.plasma_allele_counts, sep='\t')
    df_hap_data = calculate_baf(df_allele_counts)
    df_hap_data = df_hap_data[df_hap_data['depth'] > df_hap_data['depth'].quantile(0.1)] 
    df_bins = clean_dataframe_for_plotting(df_hap_data, args.reference_genome) 
    plot_bins(df_bins, args.baf_plot, y_vars=['baf'])


if __name__ == '__main__':
    from argparse import ArgumentParser
    
    default0 = "/home/matteo/Desktop/anything-cfClone/cfclone-repos/cfclone-allele-repos/generate-count-data/plot-data/runs/tnbc/CID0000220/E01889/baf/filtered_plasma_allele_counts.tsv"
    default1 = "/home/matteo/Desktop/anything-cfClone/cfclone-repos/cfclone-allele-repos/generate-count-data/plot-data/runs/tnbc/CID0000220/E01889/baf/plasma_baf_plot.png"
    default2 = 'hg38'
    
    parser = ArgumentParser()
    parser.add_argument("--plasma-allele-counts", type=str, default=default0)
    parser.add_argument("--baf-plot", type=str, default=default1)
    parser.add_argument("--reference-genome", type=str, default=default2)
    cli_args = parser.parse_args()
    
    main(cli_args)