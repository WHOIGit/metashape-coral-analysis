# Coral Photogrammetry Analysis

This repository contains tools for automated 3D reconstruction and morphometric analysis of coral specimens using Agisoft Metashape photogrammetry software.

## Overview

The workflow consists of two main steps:
1. **3D Model Generation** (`gen_models.py`) - Creates 3D models from coral photographs
2. **Statistical Analysis** (`get_stats.py`) - Extracts surface area and volume measurements

## Requirements

- Python 3.10+
- Agisoft Metashape Python 3 Module
- Required Python packages:
  - `argparse` (built-in)
  - `pathlib` (built-in)
  - `csv` (built-in)

## Installation

### Step 0: Install Python

If you don't already have Python installed:

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer and check "Add Python to PATH"
3. Verify installation: `python --version`

**macOS:**
```bash
# Using Homebrew (recommended)
brew install python

# Or download from python.org
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3 python3-pip
```

### Step 1: Install Agisoft Metashape Professional

1. Download the Agisoft Metashape Python 3 Module from the [official website](https://www.agisoft.com/downloads/installer/). Use the link corresponding to your operating system.

### Step 1.5: Configure License Server File

If you're using a floating license instead of a local license, you need to link your client machine to the license server.

Create a `server.lic` file with the following content:
```
[license_server]
host = <server_ip>
port = <port>
```

Place this file in the appropriate directory:

**Windows:**
```bash
# Create directory if it doesn't exist
mkdir "C:\ProgramData\Agisoft\Licensing\licenses"

# Place server.lic file in this directory
```

**macOS:**
```bash
# Create directory with proper permissions
sudo mkdir -p "/Library/Application Support/Agisoft/Licensing/licenses"
sudo chmod -R 777 "/Library/Application Support/Agisoft/Licensing"

# Place server.lic file in this directory
```

**Linux:**
```bash
# Create directory if it doesn't exist
sudo mkdir -p "/var/tmp/agisoft/licensing/licenses"

# Place server.lic file in this directory
```

**Note:** Default port is 5842 if not specified. This configuration is compatible with Metashape Professional 2.0.1+.

For detailed instructions, see the [official Agisoft documentation](https://agisoft.freshdesk.com/support/solutions/articles/31000169378--metashape-2-x-linking-client-machine-to-the-license-server).

### Step 2: Set Up Python Virtual Environment

Create an isolated Python environment for this project:

```bash
# Create a virtual environment
python -m venv metashape-env

# Activate the virtual environment
# On Windows:
metashape-env\Scripts\activate
# On macOS/Linux:
source metashape-env/bin/activate
```

### Step 3: Install Metashape Python API

The Metashape Python module needs to be installed from the Metashape installation directory:

**Windows:**
```bash
# Navigate to your Downloads folder where Metashape was downloaded
cd "%USERPROFILE%\Downloads"

# Install the Python module
pip install ./Metashape-2.1.0-cp37.cp38.cp39.cp310.cp311-none-win_amd64.whl
```

**macOS:**
```bash
# Navigate to your Downloads folder where Metashape was downloaded
cd ~/Downloads

# Install the Python module
pip install ./Metashape-2.1.0-cp37.cp38.cp39.cp310.cp311-none-macosx_10_12_x86_64.whl
```

**Linux:**
```bash
# Navigate to your Downloads folder where Metashape was downloaded
cd ~/Downloads

# Install the wheel file
pip install ./Metashape-2.1.0-cp37.cp38.cp39.cp310.cp311-none-linux_x86_64.whl
```

### Step 4: Clone This Repository

```bash
git clone https://github.com/WHOIGit/metashape-coral-analysis.git
cd metashape-coral-analysis
```

### Step 5: Verify Installation

Test that Metashape is properly installed:

```bash
python -c "import Metashape; print('Metashape version:', Metashape.app.version)"
```

## Usage

### Step 0: Organize Coral Images

Before running the 3D reconstruction, organize your coral photographs into the required directory structure. Each coral specimen should have its own subdirectory containing all the photographs for that specimen.

Create the following directory structure:
```
coral_photos/
├── coral_001/
│   ├── IMG_001.jpg
│   ├── IMG_002.jpg
│   ├── IMG_003.jpg
│   └── ...
├── coral_002/
│   ├── IMG_001.jpg
│   ├── IMG_002.jpg
│   ├── IMG_003.jpg
│   └── ...
├── coral_003/
│   └── ...
└── ...
```

**Important Notes:**
- Each coral specimen must be in its own subdirectory
- Only JPEG files (.jpg and .jpeg) will be processed
- Directory names will be used as coral identifiers in the output
- Ensure all images for a specimen are in the same subdirectory
- The script will recursively search for JPEG files in each subdirectory

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
