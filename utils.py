from pathlib import Path
from typing import List


class ConfigManager:
    def __init__(self, config) -> None:
        self.config = config
        
    @property
    def plot_cnv(self) -> bool:
        return self.config['out_plots']['cnv']
        
    @property
    def plot_baf(self) -> bool:
        return self.config['out_plots']['baf']
    
    # Inputs: data files
    @property
    def plasma_read_counts(self) -> Path:
        return Path(self.config['data']['plasma_read_counts']).resolve()
    
    @property
    def plasma_allele_counts(self) -> Path:
        return Path(self.config['data']['plasma_allele_counts']).resolve() 
     
    # Inputs: gc-map correction
    @property
    def gc_file(self) -> Path:
        return Path(self.config['cnv']['gc_file']).resolve()
    
    @property
    def map_file(self) -> Path:
        return Path(self.config['cnv']['map_file']).resolve()
    
    @property
    def blacklist_regions_file(self) -> Path:
        return Path(self.config['blacklist_regions_file']).resolve()
    
    @property
    def reference_genome(self) -> str:
        return self.config['reference_genome']
    
    # Outputs: gc-map correction plots
    @property
    def out_dir(self) -> Path:
        return Path(self.config['out_dir']).resolve()
    
    @property
    def cnv_dir(self) -> Path:
        return self.out_dir.joinpath("cnv")
    
    @property
    def plasma_corr_read_counts(self) -> Path:
        return self.cnv_dir.joinpath("plasma_corr_read_counts.tsv")
    
    @property
    def log_plasma_corr_read_counts(self) -> Path:
        return self.cnv_dir.joinpath("plasma_corr_read_counts.log")
    
    
    # Outputs: filtered data outputs
    @property
    def filtered_plasma_corr_read_counts(self) -> Path:
        return self.cnv_dir.joinpath("filtered_plasma_corr_read_counts.tsv")
    
    @property
    def log_filtered_plasma_corr_read_counts(self) -> Path:
        return self.cnv_dir.joinpath("filtered_plasma_corr_read_counts.log")
    
    @property
    def baf_dir(self) -> Path:
        return self.out_dir.joinpath("baf")
    
    @property
    def filtered_plasma_allele_counts(self) -> Path:
        return self.cnv_dir.joinpath("filtered_allele_counts.tsv")
    
    @property
    def log_filtered_plasma_allele_counts(self) -> Path:
        return self.cnv_dir.joinpath("filtered_plasma_allele_counts.log")
    
    # Outputs: plots
    @property
    def plasma_cnv_plot(self) -> Path:
        return self.cnv_dir.joinpath("plasma_cnv_plot.png")
    
    @property
    def log_plasma_cnv_plot(self) -> Path:
        return self.cnv_dir.joinpath("plasma_cnv_plot.log")
    
    @property
    def plasma_baf_plot(self) -> Path:
        return self.baf_dir.joinpath("plasma_baf_plot.png")
    
    @property
    def log_plasma_baf_plot(self) -> Path:
        return self.baf_dir.joinpath("plasma_baf_plot.log")
        
    def get_pipeline_files(self) -> List[str]:
        outputs = []
        outputs.append(str(self.plasma_corr_read_counts))
        if self.plot_cnv:
            outputs.append(str(self.plasma_cnv_plot))
        if self.plot_baf:
            outputs.append(str(self.plasma_baf_plot))
        return outputs