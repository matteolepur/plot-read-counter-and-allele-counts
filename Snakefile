"""
Two processes are being run here.
1) Correcting, filtering, and plotting count data from a wig file.
2) Filtering and plotting baf data from .tsv file.
"""

from utils import ConfigManager
config = ConfigManager(config)

rule all:
    input:
        config.get_pipeline_files()


rule process_1_step_1_correct_reads:
    input:
        c=config.plasma_read_counts,
        g=config.gc_file,
        m=config.map_file
    output:
        config.plasma_corr_read_counts
    conda:
        "envs/prep_reads.yaml"
    log:
        config.log_plasma_corr_read_counts
    resources:
        mem="8G"
    shell:
        "python scripts/correct_reads.py "
        "--corr-read-counts {output} "
        "--read-counts {input.c} "
        "--gc {input.g} "
        "--map {input.m} "
        "&> {log}"


rule process_1_step_2_filter_genomic_regions_for_wig:
    input:
        config.plasma_corr_read_counts
    output:
        config.filtered_plasma_corr_read_counts
    params:
        blist = config.blacklist_regions_file,
        ref = config.reference_genome
    conda:
        "envs/prep_reads.yaml"
    log:
        config.log_filtered_plasma_corr_read_counts
    shell:
        "python scripts/filter_bins.py "
        "--filtered-data {output} "
        "--raw-data {input} "
        "--blacklist-regions {params.blist} "
        "--reference-genome {params.ref} "
        "--data-type read-counts "
        "&> {log}"

rule process_1_step_3_plot_cnv_from_wig:
    input:
        config.filtered_plasma_corr_read_counts
    output:
        config.plasma_cnv_plot
    conda:
        "envs/plot_cnv.yaml"
    log:
        config.log_plasma_cnv_plot
    shell:
        "python scripts/plot_cnv.py "
        "--plasma-corr-read-counts {input} "
        "--cnv-plot {output} "
        "&> {log}"


rule process_2_step_1_filter_genomic_regions_for_count:
    input:
        config.plasma_allele_counts
    output:
        config.filtered_plasma_allele_counts
    params:
        blist = config.blacklist_regions_file,
        ref = config.reference_genome
    conda:
        "envs/prep_reads.yaml"
    log:
        config.log_filtered_plasma_allele_counts
    shell:
        "python scripts/filter_bins.py "
        "--filtered-data {output} "
        "--raw-data {input} "
        "--blacklist-regions {params.blist} "
        "--reference-genome {params.ref} "
        "--data-type hap-counts "
        "&> {log}"

rule step_3_plot_baf:
    input:
        config.filtered_plasma_allele_counts
    output:
        config.plasma_baf_plot
    conda:
        "envs/plot_cnv.yaml"
    params:
        ref = config.reference_genome
    log:
        config.log_plasma_baf_plot
    shell:
        "python scripts/plot_baf.py "
        "--plasma-allele-counts {input} "
        "--baf-plot {output} "
        "--reference-genome {params.ref} "
        "&> {log}"