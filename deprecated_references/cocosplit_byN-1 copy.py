import json
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description='Divide COCO JSON dataset into n units with a specified file size limit')
    parser.add_argument('--input-json', type=str, required=True, help='Path to input COCO JSON file')
    parser.add_argument('--output-dir', type=str, required=True, help='Path to output directory')
    parser.add_argument('--unit-size', type=int, required=True, help='Size limit (in MB) for each output file')
    parser.add_argument('--num-units', type=int, required=True, help='Number of output files to create')
    args = parser.parse_args()

    input_json_path = args.input_json
    output_dir = args.output_dir
    unit_size_mb = args.unit_size
    num_units = args.num_units

    # Load the input COCO JSON file
    with open(input_json_path, 'r') as f:
        coco_json = json.load(f)

    # Divide the annotations into n units
    annotations = coco_json['annotations']
    num_annotations = len(annotations)
    unit_size_bytes = unit_size_mb * 1024 * 1024
    annotations_per_unit = (num_annotations + num_units - 1) // num_units
    units = [annotations[i:i + annotations_per_unit] for i in range(0, num_annotations, annotations_per_unit)]

    # Create the output files
    for i, unit in enumerate(units):
        output_json_path = os.path.join(output_dir, f'{i}.json')
        unit_dict = dict(images=coco_json['images'], annotations=unit, categories=coco_json['categories'])

        # Write the output file
        with open(output_json_path, 'w') as f:
            json.dump(unit_dict, f)

        # Check if the output file is within the size limit
        if os.path.getsize(output_json_path) > unit_size_bytes:
            raise ValueError(f"Output file {i} exceeds the size limit of {unit_size_mb} MB")


if __name__ == '__main__':
    """python divide_coco_json.py --input-json /path/to/input.json --output-dir /path/to/output --unit-size 100 --num-units 5
    
    This will divide the COCO JSON dataset in the input.json file into 5 units with a size limit of 100 MB each, and save the output files in the output directory.
     You can modify the --unit-size and --num-units options to change the size limit and the number of output files, respectively.
    """
    main()