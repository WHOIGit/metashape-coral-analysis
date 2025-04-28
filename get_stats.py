import csv
import argparse
from pathlib import Path

import Metashape


def get_stats(project_dir, project_name, output_file_path):
    project_file = (project_dir / project_name).with_suffix('.psx')
    doc = Metashape.Document()
    doc.open(str(project_file))

    chunk = doc.chunks[0]
    model = chunk.model

    area = model.area()       
    print(f'Surface Area: {model.area()}')

    model.closeHoles(level=100)
    volume = model.volume()
    print(f'Volume: {model.volume()}')

    with open(output_file_path, 'a') as output_file:
        writer = csv.writer(output_file)
        writer.writerow([project_dir.stem, area, volume])       

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--projects_dir', type=str)
    parser.add_argument('--project_name', type=str, default='reconstruction')
    parser.add_argument('--output', type=str, default='model_stats.csv')
    args = parser.parse_args()

    # Write header
    header = ['Coral Number', 'Surface Area', 'Volume']
    with open(args.output, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header)

    for dir_path in Path(args.projects_dir).iterdir():
        if dir_path.is_dir():
            project_dir = Path(args.projects_dir) / dir_path.name
            get_stats(project_dir, args.project_name, args.output)


if __name__ == '__main__':
    main()
