from pathlib import Path
from typing import List


class ConfigManager:
    def __init__(self, config) -> None:
        self.config = config
        
    # Inputs: data files
    @property
    def plasma_read_counts(self) -> Path:
        return Path(self.config['plasma_read_counts']).resolve()
    
    @property
    def plasma_allele_counts(self) -> Path:
        return Path(self.config['plasma_allele_counts']).resolve() 
     
    # Inputs: gc-map correction
    @property
    def gc_file(self) -> Path:
        return Path(self.config['cnv']['gc_file']).resolve()
    
    @property
    def map_file(self) -> Path:
        return Path(self.config['cnv']['map_file']).resolve()
    
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
        return self.cnv_dir.joinpath("plasma_corr_read_counts.tsv")
    
    # Outputs: baf plots
    @property
    def baf_dir(self) -> Path:
        return self.out_dir.joinpath("baf")
        
        
    def get_pipeline_files(self) -> List[str]:
        outputs = []
        outputs.append(str(self.plasma_corr_read_counts))
        return outputs