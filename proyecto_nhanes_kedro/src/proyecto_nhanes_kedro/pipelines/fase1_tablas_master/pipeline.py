from kedro.pipeline import Pipeline, node
import re
from pathlib import Path
from .nodes import standarize_columns, build_section_master

def create_pipeline(**kwargs) -> Pipeline:
    # Leer el documento para saber qué datasets componen qué secciones
    # Se debe ignorar esto si el doc es eliminado, pero como FASE 1 depende
    # del doc para construir dinámicamente, en vez de usar el doc,
    # vamos a mapear los datasets de una vez.
    
    sections = {
        "demographics": ["demo_j"],
        "dietary": [
            "dr1ff_j", "dr2ff_j", "dr1tot_j", "dr2tot_j", "drxfcd_j",
            "dsbi", "dsii", "dspi", "ds1ids_j", "ds2ids_j", "ds1tot_j",
            "ds2tot_j", "dsqids_j", "dsqtot_j"
        ],
        "examination": [
            "aux_j", "auxar_j", "auxtym_j", "auxwbr_j", "bpx_j", "bpxo_j",
            "bmx_j", "dxxag_j", "dxxfem_j", "dxxspn_j", "dxx_j", "lux_j",
            "ohxden_j", "ohxref_j"
        ],
        "laboratory": [
            "alb_cr_j", "ssagp_j", "utas_j", "uas_j", "hdl_j", "trigly_j",
            "tchol_j", "ucm_j", "crco_j", "cbc_j", "cot_j", "ucot_j",
            "cmv_j", "ethox_j", "fastqx_j", "fertin_j", "fr_j", "ssfr_j",
            "folate_j", "folfms_j", "ghb_j", "ssglyp_j", "hepa_j", "hepbd_j",
            "hepb_s_j", "hepc_j", "hepe_j", "hscrp_j", "hiv_j", "ins_j",
            "uio_j", "fetib_j", "pbcd_j", "uhg_j", "ihgem_j", "um_j",
            "ssneon_j", "uni_j", "opd_j", "pernt_j", "pfas_j", "sspfas_j",
            "ephpp_j", "phthte_j", "glu_j", "pah_j", "uphopm_j", "sstst_j",
            "biopro_j", "tfr_j", "ucflow_j", "ucpreg_j", "vitaec_j", "vic_j",
            "vid_j", "uvoc_j", "ssuvoc_j", "ssuvcm_j", "vocwb_j"
        ]
    }
    
    nodes = []
    
    for section, datasets in sections.items():
        intermediate_datasets = []
        
        for ds in datasets:
            nodes.append(
                node(
                    func=standarize_columns,
                    inputs=f"{ds}_raw",
                    outputs=f"{ds}_intermediate",
                    name=f"standarize_{ds}"
                )
            )
            intermediate_datasets.append(f"{ds}_intermediate")
            
        if intermediate_datasets:
            nodes.append(
                node(
                    func=build_section_master,
                    inputs=intermediate_datasets,
                    outputs=f"{section}_master",
                    name=f"build_{section}_master"
                )
            )
            
    return Pipeline(nodes)
