import os
import re
from pathlib import Path

docs_path = Path("c:/Users/alarc/OneDrive/Escritorio/Proyecto_Nhanes_Kedro/proyecto_nhanes_kedro/docs/Documentacion_Variables.txt")
catalog_path = Path("c:/Users/alarc/OneDrive/Escritorio/Proyecto_Nhanes_Kedro/proyecto_nhanes_kedro/conf/base/catalog.yml")

with open(docs_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

sections = {}
current_section = None

for line in lines:
    line = line.strip()
    if not line:
        continue
    
    # Check if section
    if line.startswith('--') and line.endswith('--'):
        if "DEMOGRAPHICS" in line:
            current_section = "demographics"
        elif "DIETARY" in line:
            current_section = "dietary"
        elif "EXAMINATION" in line:
            current_section = "examination"
        elif "LABORATORY" in line:
            current_section = "laboratory"
        sections[current_section] = []
        continue
        
    # Check if dataset
    match = re.match(r"^([A-Z0-9_]+):\s*(http.*)", line)
    if match and current_section:
        ds_name = match.group(1).lower()
        sections[current_section].append(ds_name)

# Generate catalog entries
catalog_additions = "\n# --- AUTOMATICALLY GENERATED FASE 1 NHANES ---\n"

# Add masters
masters = ["demographics_master", "dietary_master", "examination_master", "laboratory_master"]
for master in masters:
    catalog_additions += f"""
{master}:
  type: pandas.ParquetDataset
  filepath: data/03_primary/{master}.parquet
"""

for section, datasets in sections.items():
    catalog_additions += f"\n# --- SECTION: {section.upper()} ---\n"
    for ds in datasets:
        # Raw entry
        catalog_additions += f"""
{ds}_raw:
  type: pandas.GenericDataset
  filepath: data/01_raw/{ds.upper()}.xpt
  file_format: sas
  load_args:
    format: xport

{ds}_intermediate:
  type: pandas.ParquetDataset
  filepath: data/02_intermediate/{ds.upper()}.parquet
"""

# Append to catalog
with open(catalog_path, 'a', encoding='utf-8') as f:
    f.write(catalog_additions)

print(f"Catalog updated successfully with datasets from {len(sections)} sections.")
