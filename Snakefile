from utils import ConfigManager
config = ConfigManager(config)

rule all:
    input:
        config.get_pipeline_files()


rule step_1_correct_reads:
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


rule step_2_filter_genomic_regions:
    input:
        config.plasma_corr_read_counts
    output:
        config.filtered_plasma_corr_read_counts
    params:
        config.blacklist_regions_file
    conda:
        "envs/prep_reads.yaml"
    log:
        config.log_filtered_plasma_corr_read_counts
    shell:
        "python scripts/filter_bins.py "
        "--filtered-corr-read-counts {output} "
        "--corr-read-counts {input} "
        "--blacklist-regions {params} "
        "&> {log}"


rule step_2_plot_cnv:
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


rule step_3_plot_baf:
    input:
        config.plasma_allele_counts
    output:
        config.plasma_baf_plot
    conda:
        "envs/plot_cnv.yaml"
    log:
        config.log_plasma_baf_plot
    shell:
        "python scripts/plot_baf.py "
        "--plasma-allele-counts {input} "
        "--baf-plot {output} "
        "&> {log}"