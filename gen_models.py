import argparse
from pathlib import Path

import Metashape


def get_absolute_jpeg_file_paths(directory):
    """
    Recursively gather absolute paths of JPEG files in a directory.
    
    Args:
    - directory (pathlib.Path): The path to the directory to traverse.
    
    Returns:
    - file_paths (list): The list of absolute JPEG paths.
    """
    jpeg_files = list(directory.rglob("*.jpg")) + list(directory.rglob("*.jpeg"))
    return [file.resolve() for file in jpeg_files]


def reconstruct(project_dir, project_name, jpeg_files):
    """Performs 3D reconstruction using Metashape photogrammetry pipeline.
    
    Creates a complete 3D model from JPEG photos using the Metashape workflow
    including photo alignment, depth map generation, mesh construction, and
    texture mapping.
    
    Args:
        project_dir (pathlib.Path): Directory where the project file will be saved.
        project_name (str): Name of the project (without extension).
        jpeg_files (list): List of pathlib.Path objects pointing to JPEG image files.
    
    Returns:
        None: Saves the completed project to disk.
    """
    project_file = (project_dir / project_name).with_suffix('.psx')
    doc = Metashape.Document()
    doc.save(str(project_file))
    chunk = doc.addChunk()
    images = [str(jpeg_file) for jpeg_file in jpeg_files]    

    chunk.addPhotos(images)
    chunk.matchPhotos(downscale=0)
    chunk.alignCameras()
    chunk.optimizeCameras()
    chunk.buildDepthMaps(downscale=1)
    chunk.buildModel()
    chunk.buildUV(texture_size=16384)
    chunk.buildTexture(texture_size=16384)
    doc.save()


def reconstruct_site():
    """Batch processes multiple coral sites for 3D reconstruction.
    
    Iterates through all subdirectories in a site directory and performs
    3D reconstruction for each one using the Metashape photogrammetry pipeline.
    Each subdirectory is treated as a separate coral site.
    
    Args:
        None: Uses command-line arguments for configuration.
            --site_dir: Directory containing subdirectories with JPEG images.
            --projects_dir: Directory where project files will be saved.
            --project_name: Name for the project files (default: 'reconstruction').
    
    Returns:
        None: Creates reconstruction projects for each site directory.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--site_dir', type=str)
    parser.add_argument('--projects_dir', type=str)
    parser.add_argument('--project_name', type=str, default='reconstruction')
    args = parser.parse_args()

    for dir_path in Path(args.site_dir).iterdir():
        if dir_path.is_dir():
            jpeg_files = get_absolute_jpeg_file_paths(dir_path)
            project_dir = Path(args.projects_dir) / dir_path.name
            reconstruct(project_dir, args.project_name, jpeg_files)


if __name__ == '__main__':
    reconstruct_site()
