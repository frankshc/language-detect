import os
import random
import itertools
import json


def iter_sample_single_jsonl(root, language, partition, num_examples, random_seed=None, excerpt=False):
    """Randomly samples a single extracted and indexed jsonl file.

    Args:
        root: A directory containing the extracted and indexed master dataset.
        language: The language to sample from.
        partition: The partition to sample from.
        num_examples: The number of examples.
        excerpt: A flag that indicate whether the original code string should
            be excerpted.

    Note:
        Only the fields "language", "repo", and "original_string" are kept.

    Returns:
        An iterator that yields the sampled jsonl lines.
    """

    jsonl_path = os.path.join(root, f'{language}_{partition}.jsonl')
    index_path = os.path.join(root, f'{language}_{partition}.index')

    def generator():

        with open(index_path, 'rb') as index_file, \
                open(jsonl_path, 'rb') as jsonl:

            # The first 4 bytes in the index file contains the total number
            # of examples or lines in the jsonl file.
            total_examples = int.from_bytes(index_file.read(4), byteorder='big',
                                            signed=False)

            # Create standalone random instance so as to not affect global
            # random state.
            rand = random.Random(random_seed)

            example_indices = rand.sample(range(total_examples), num_examples)

            for i in example_indices:
                index_file.seek(i * 4, 0)

                # Special case if i == 0: the seek position is implicitly
                # 0 and stored in the index file.
                seek_begin = i and int.from_bytes(index_file.read(4),
                                                  byteorder='big',
                                                  signed=False)

                # The seek position of the next example, or the position of the
                # current example not inclusive.
                seek_end = int.from_bytes(index_file.read(4),
                                          byteorder='big',
                                          signed=False)

                # Go to the position in the jsonl file that contains the
                # example.
                jsonl.seek(seek_begin, 0)
                num_bytes = seek_end - seek_begin

                line = jsonl.read(num_bytes).decode('utf-8')
                d = json.loads(line)
                d = {key: d[key] for key in ('language', 'repo', 'original_string')}

                if excerpt:
                    lines = d['original_string'].splitlines()
                    begin, end = sorted(rand.sample(range(len(lines)), 2))
                    d['original_string'] = '\n'.join(lines[begin:end])

                yield json.dumps(d) + '\n'

    return generator()


def sample_partition(root, partition, num_examples, output_file, random_seed=None, excerpt=False):
    """Randomly samples and splits the master dataset.

    Given a partition {test, valid, train}, randomly sample the specified
    number of examples for each language. Each line of json example is
    written to stdout.

    Args:
        root: A directory containing the extracted and indexed master dataset.
        partition: The partition to sample from.
        num_examples: The number of examples per language.
        output_file: A file-like object to which string output will be written.
        random_seed: The random seed to use for sampling.
        excerpt: A flag that indicate whether the original code string should
            be excerpted.
    """
    languages = sorted(('go', 'java', 'javascript', 'php', 'python', 'ruby'))

    sampler = itertools.chain(*(iter_sample_single_jsonl(root, lang, partition,
                                                         num_examples,
                                                         random_seed,
                                                         excerpt)
                                for lang in languages))

    output_file.writelines(line for line in sampler)


if __name__ == '__main__':
    import argparse

    description = ('Sample the extracted and indexed .jsonl CodeSearchNet '
                   'dataset for a given partition.')

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('jsonl_root', help='A directory that contains the extracted and indexed jsonl files.')
    parser.add_argument('partition', help='One of {train, test, valid}.')
    parser.add_argument('num_examples', type=int, help='Number of examples to sample per language.')
    parser.add_argument('output_path', help='The path of the output jsonl file.')
    parser.add_argument('--random_seed', type=int, help='An integer random seed used for sampling.')
    parser.add_argument('--excerpt', default=False, action='store_true')

    args = parser.parse_args()

    valid_partitions = ('train', 'valid', 'test')

    if args.partition not in valid_partitions:
        err_msg = f'Partition name must be one of {{{", ".join(valid_partitions)}}}.'
        raise ValueError(err_msg)

    with open(args.output_path, 'w') as out:
        sample_partition(args.jsonl_root, args.partition, args.num_examples,
                         out, args.random_seed, args.excerpt)