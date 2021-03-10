from urllib.request import urlopen
from shutil import copyfileobj
import os


def download_master_dataset(root):
    languages = ('go', 'java', 'javascript', 'php', 'python', 'ruby')

    os.makedirs(root, exist_ok=True)

    for lang in languages:

        url = (f'https://s3.amazonaws.com/code-search-net/'
               f'CodeSearchNet/v2/{lang}.zip')

        print(f'Downloading {lang} dataset from {url}... ', end='')

        output_path = os.path.join(root, f'{lang}.zip')
        req = urlopen(url)

        with open(output_path, 'wb') as f:
            copyfileobj(req, f)

        print('Done!')


if __name__ == '__main__':
    import argparse

    description = 'Download the public CodeSearchNet dataset.'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('root', help='A directory to hold the downloaded '
                                     'files.')

    args = parser.parse_args()
    download_master_dataset(args.root)