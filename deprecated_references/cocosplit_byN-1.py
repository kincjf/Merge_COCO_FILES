import os
import json
import argparse

def split_coco_dataset(annotations_file, output_dir, num_parts=None, file_size=None):
    with open(annotations_file, 'r') as f:
        dataset = json.load(f)

    if num_parts:
        num_images = len(dataset['images'])
        images_per_part = num_images // num_parts
        for i in range(num_parts):
            start_index = i * images_per_part
            end_index = (i+1) * images_per_part if i < num_parts-1 else num_images
            part_dataset = {
                'info': dataset['info'],
                'licenses': dataset['licenses'],
                'images': dataset['images'][start_index:end_index],
                'annotations': [a for a in dataset['annotations'] if a['image_id'] in [img['id'] for img in dataset['images'][start_index:end_index]]],
                'categories': dataset['categories']
            }
            with open(os.path.join(output_dir, f'part{i}.json'), 'w') as f:
                json.dump(part_dataset, f, indent=2)
                
    elif file_size:
        file_num = 1
        file_size_bytes = 0
        part_dataset = {
            'info': dataset['info'],
            'licenses': dataset['licenses'],
            'images': [],
            'annotations': [],
            'categories': dataset['categories']
        }
        for image in dataset['images']:
            image_path = os.path.join(os.path.dirname(annotations_file), image['file_name'])
            image_size = os.path.getsize(image_path)
            if file_size_bytes + image_size > file_size:
                with open(os.path.join(output_dir, f'part{file_num}.json'), 'w') as f:
                    json.dump(part_dataset, f, indent=2)
                part_dataset = {
                    'info': dataset['info'],
                    'licenses': dataset['licenses'],
                    'images': [],
                    'annotations': [],
                    'categories': dataset['categories']
                }
                file_num += 1
                file_size_bytes = 0
            part_dataset['images'].append(image)
            part_dataset['annotations'].extend([a for a in dataset['annotations'] if a['image_id'] == image['id']])
            file_size_bytes += image_size

        with open(os.path.join(output_dir, f'part{file_num}.json'), 'w') as f:
            json.dump(part_dataset, f, indent=2)

if __name__ == '__main__':
    """python split_coco.py annotations.json --num-parts 5 --output-dir parts/
    """
    parser = argparse.ArgumentParser(description='Split COCO dataset')
    parser.add_argument('annotations_file', help='path to COCO annotations file')
    parser.add_argument('--output-dir', default='./', help='output directory')
    parser.add_argument('--num-parts', type=int, help='number of parts to split the dataset')
    parser.add_argument('--file-size', type=float, help='maximum file size (in GB) for each part')
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    split_coco_dataset(args.annotations_file, args.output_dir, num_parts=args.num_parts, file_size=args.file_size)