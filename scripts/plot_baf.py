import pandas as pd

from plot_bins import plot_bins


def main(args):
    df = pd.read_csv(args.plasma_allele_counts, sep='\t')
    
    hap_data = df.groupby("hap_block")['allele_0_count', 'allele_1_count'].sum()
    hap_data['depth'] = hap_data['allele_0_count'] + hap_data['allele_1_count']
    hap_data['baf'] = hap_data['allele_0_count'] / hap_data['depth']
    
    hap_data_subset = hap_data[hap_data['depth'] > hap_data['depth'].quantile(0.01)] 
    df_bins = hap_data_subset[['hap_block_start', 'hap_block_end', 'baf']]  
    df_bins.rename(columns={'hap_block_start': 'Start', 'hap_block_end': 'End'}, inplace=True)
    
    plot_bins(df_bins, args.baf_plot, y_vars=['baf'])
    
    
    print("lol")

if __name__ == '__main__':
    from argparse import ArgumentParser
    
    default0 = "smoke-test-data/allele_counts.tsv.gz"
    default1 = "results/smoke-test/cnv/baf_plot.png"
    
    parser = ArgumentParser()
    parser.add_argument("--plasma-allele-counts", type=str, default=default0)
    parser.add_argument("--baf-plot", type=str, default=default1)
    cli_args = parser.parse_args()
    
    main(cli_args)