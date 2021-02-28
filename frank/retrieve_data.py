import zipfile
import gzip
import json
import itertools
import os
import collections
import random


def sample_dataset(output_dir: str, num_train: int, num_valid: int, num_test: int):
    """Takes a sample of the primary dataset archive.

    Args:
        train: Number of training examples.
        valid: Number of validation examples.
        test: Number of test examples.
    """
    languages = ('go', 'python', 'ruby', 'javascript', 'php', 'java')

    for lang in languages:
        with zipfile.ZipFile(f'data/{lang}.zip', 'r') as archive:
            # We are only interested in .gz files in the archive.
            paths = (path for path in archive.namelist() if
                     os.path.splitext(path)[1] == '.gz')

            # A dictionary that maps partitions names to paths.
            partition_paths = collections.defaultdict(list)

            for path in paths:
                # Extract the file name.
                _, name = os.path.split(path)
                # Ignore ".jsonl.gz" extension.
                name, _ = name.split('.', 1)
                # Extract partition and file index.
                _, part, index = name.split('_')
                partition_paths[part].append(path)

            # The number of samples to take for each partition.
            num_samples = {'train': num_train, 'valid': num_valid,
                           'test': num_test}

            for part, paths in partition_paths.items():

                def iter_data():
                    for path in paths:
                        with archive.open(path) as gz:
                            with gzip.open(gz) as file:
                                file = list(file)
                                for line in file:
                                    data = json.loads(line)
                                    yield data['original_string']

                num_total = sum(1 for _ in iter_data())
                indices = random.sample(range(num_total), num_samples[part])
                indices.sort(reverse=True)

                sequential_id = itertools.count().__next__

                for i, data in enumerate(iter_data()):
                    if not indices:
                        continue
                    elif i == indices[-1]:
                        indices.pop()

                        filename = os.path.join(output_dir, part, lang,
                                                str(sequential_id()) + '.txt')

                        os.makedirs(os.path.dirname(filename), exist_ok=True)
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(data)

                        print(f'Wrote data to {filename}.')


if __name__ == '__main__':
    sample_dataset('sample_data', 8000, 1000, 1000)