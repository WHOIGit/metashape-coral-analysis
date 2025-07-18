# Coral Photogrammetry Analysis

This repository contains tools for automated 3D reconstruction and morphometric analysis of coral specimens using Agisoft Metashape photogrammetry software.

## Overview

The workflow consists of two main steps:
1. **3D Model Generation** (`gen_models.py`) - Creates 3D models from coral photographs
2. **Statistical Analysis** (`get_stats.py`) - Extracts surface area and volume measurements

## Requirements

- Python 3.7+
- Agisoft Metashape Professional
- Required Python packages:
  - `argparse` (built-in)
  - `pathlib` (built-in)
  - `csv` (built-in)

## Installation

1. Install Agisoft Metashape Professional
2. Ensure Metashape Python API is available in your Python environment
3. Clone this repository

## Usage

### Step 1: Generate 3D Models

Use `gen_models.py` to create 3D reconstructions from coral photographs:

```bash
python gen_models.py --site_dir /path/to/coral/photos --projects_dir /path/to/output/projects --project_name reconstruction
```

**Parameters:**
- `--site_dir`: Directory containing subdirectories with JPEG images for each coral specimen
- `--projects_dir`: Directory where Metashape project files (.psx) will be saved
- `--project_name`: Name for the project files (default: 'reconstruction')

**Input Structure:**
```
coral_photos/
├── coral_001/
│   ├── IMG_001.jpg
│   ├── IMG_002.jpg
│   └── ...
├── coral_002/
│   ├── IMG_001.jpg
│   ├── IMG_002.jpg
│   └── ...
└── ...
```

### Step 2: Extract Statistics

Use `get_stats.py` to extract morphometric measurements from the generated 3D models:

```bash
python get_stats.py --projects_dir /path/to/output/projects --project_name reconstruction --output coral_stats.csv
```

**Parameters:**
- `--projects_dir`: Directory containing the Metashape project files
- `--project_name`: Name of the project files (default: 'reconstruction')
- `--output`: Output CSV filename (default: 'model_stats.csv')

**Output:**
Creates a CSV file with the following columns:
- Coral Number: Directory name/specimen identifier
- Surface Area: Surface area of the 3D model
- Volume: Volume of the 3D model (calculated after hole closure)

## Workflow Details

### 3D Reconstruction Pipeline

The `gen_models.py` script performs the following Metashape operations for each coral specimen:

1. **Photo Loading**: Imports all JPEG images from the specimen directory
2. **Photo Matching**: Identifies common features between photos (downscale=0 for highest quality)
3. **Camera Alignment**: Estimates camera positions and orientations
4. **Camera Optimization**: Refines camera parameters
5. **Depth Map Generation**: Creates depth maps (downscale=1 for high quality)
6. **Mesh Construction**: Builds 3D mesh from depth maps
7. **UV Mapping**: Creates texture coordinates (16384x16384 resolution)
8. **Texture Generation**: Applies photo textures to the 3D model (16384x16384 resolution)

### Statistical Analysis

The `get_stats.py` script:

1. Opens each Metashape project file
2. Accesses the first chunk and its 3D model
3. Calculates surface area using Metashape's built-in area calculation
4. Closes holes in the mesh (level=100) for accurate volume calculation
5. Calculates volume using Metashape's built-in volume calculation
6. Exports results to CSV format

## Example Complete Workflow

```bash
# Step 1: Generate 3D models from coral photos
python gen_models.py --site_dir ./coral_photos --projects_dir ./coral_projects

# Step 2: Extract morphometric statistics
python get_stats.py --projects_dir ./coral_projects --output coral_measurements.csv
```

## Output Files

- **Metashape Projects**: `.psx` files containing complete 3D reconstruction data
- **Statistics CSV**: Morphometric measurements for analysis and comparison
- **Console Output**: Real-time progress and measurement values
