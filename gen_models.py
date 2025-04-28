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
