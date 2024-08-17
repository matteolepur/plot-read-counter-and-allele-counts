import pandas as pd

from plot_bins import plot_bins


CHROM_ORDER = [str(c) for c in range(0,23)] + ['X', 'Y']


def main(args):
    df = pd.read_csv(args.plasma_allele_counts, sep='\t')
    
    # calculate BAF
    hap_data = df.groupby(["chrom", "hap_block_start", "hap_block_end"])['allele_a_count', 'allele_b_count'].sum()
    hap_data['depth'] = hap_data['allele_a_count'] + hap_data['allele_b_count']
    hap_data['baf'] = hap_data['allele_b_count'] / hap_data['depth']
    
    # drop bins with low depth
    hap_data_subset = hap_data[hap_data['depth'] > hap_data['depth'].quantile(0.1)] 
    
    # reindex
    df_bins = hap_data_subset.reset_index()
    df_bins.rename(columns={'chrom': 'Chromosome', 'hap_block_start': 'Start', 'hap_block_end': 'End'}, inplace=True)
    
    # reorder
    if args.reference_genome == 'hg38':
        df_bins['Chromosome'] = df_bins['Chromosome'].str[3:]
        df_bins['Chromosome'] = pd.Categorical(df_bins['Chromosome'], categories=CHROM_ORDER, ordered=True)
        df_bins = df_bins.sort_values(['Chromosome', 'Start'])
    
     
    plot_bins(df_bins, args.baf_plot, y_vars=['baf'])


if __name__ == '__main__':
    from argparse import ArgumentParser
    
    default0 = "/home/matteo/Desktop/anything-numbers-pulls/cfclone-pulls/pull036/numbers-runs/tnbc/CID0000391/F112602/allele_counts/results/counts/allele_counts.tsv.gz"
    default1 = "results/smoke-test/cnv/baf_plot.png"
    default2 = 'hg38'
    
    parser = ArgumentParser()
    parser.add_argument("--plasma-allele-counts", type=str, default=default0)
    parser.add_argument("--baf-plot", type=str, default=default1)
    parser.add_argument("--reference-genome", type=str, default=default2)
    cli_args = parser.parse_args()
    
    main(cli_args)