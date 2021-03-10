import os
import zipfile
import gzip
import collections


def extract_jsonl_files(master_dataset_root, jsonl_root):

    os.makedirs(jsonl_root, exist_ok=True)

    languages = ('go', 'java', 'javascript', 'php', 'python', 'ruby')

    for lang in languages:

        zip_file_path = os.path.join(master_dataset_root, f'{lang}.zip')

        with zipfile.ZipFile(zip_file_path, 'r') as archive:
            partitions = collections.defaultdict(list)

            for path in archive.namelist():
                _, name = os.path.split(path)
                if name.endswith('.jsonl.gz'):
                    name, _ = name.split('.', 1)
                    _, part, i = name.split('_')
                    partitions[part].append((int(i), path))

            for part in partitions:

                # Order each file path in each partition by its index.
                gz_paths = sorted(path for _, path in partitions[part])

                # Set up output jsonl file to extract to.
                jsonl_path = os.path.join(jsonl_root, f'{lang}_{part}.jsonl')

                # Keep track of how many lines are in the output jsonl file.
                num_lines = 0

                # Use an index file to keep track of the seek positions of each
                # data item in the jsonl file. This is neccesary to improve
                # random access performance later on.
                index_path = os.path.join(jsonl_root, f'{lang}_{part}.index')

                with open(jsonl_path, 'wb') as jsonl, \
                        open(index_path, 'wb') as index:

                    # Offset the index pointer by 4 bytes to reserve space,
                    # which we will later use to store the number of lines
                    # in the jsonl file.
                    index.seek(4)

                    for path in gz_paths:
                        with archive.open(path) as gz, gzip.open(gz) as lines:
                            for i, line in enumerate(lines, 1):
                                jsonl.write(line)

                                # Record the ending seek position of the json
                                # line just written.
                                index.write(jsonl.tell()
                                            .to_bytes(4, byteorder='big'))

                            num_lines += i

                        # Unfortunately, the .jsonl.gz files do not have a
                        # newline character at the end of the file. We must
                        # manually add it.
                        jsonl.write(b'\n')

                        # The last json line written did not account for the
                        # added newline. As such, we must update the last 4
                        # bytes in the index file. Assume that there is enough
                        # offset to seek -4.
                        index.seek(-4, 1)
                        index.write(jsonl.tell().to_bytes(4, byteorder='big'))

                    # Write the total number of json lines into the reserved
                    # 4 bytes at the start of the index file.
                    index.seek(0)
                    index.write(num_lines.to_bytes(4, byteorder='big'))

                    print(f'Wrote {num_lines} lines to {jsonl_path}.')
                    print(f'Created index at {index_path}.')


if __name__ == '__main__':
    import argparse

    description = 'Extract and index the downloaded CodeSearchNet dataset.'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('dataset_root', help='The directory that contains the downloaded CodeSearchNet dataset.')
    parser.add_argument('jsonl_root', help='The directory to output the extracted and indexed jsonl files.')

    args = parser.parse_args()
    extract_jsonl_files(args.dataset_root, args.jsonl_root)
