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
        "python scripts/correct_reads.py {input.g} {input.m} {input.c} {output}"

# step 2 plot cnv
# step 3 plot baf