# Getting Started

This module includes a set of three data processing scripts. They should be 
invoked on the command line using a python interpreter.

## Downloading the Dataset
`download_dataset.py` will download the public [CodeSearchNet](https://github.com/github/CodeSearchNet) 
dataset from an Amazon S3 server to a local directory. 
Please ensure you have **at least 5 GB of free space**. 
The dataset consists of 6 .zip archives, each corresponding to one of the following languages:

* python
* javascript
* java
* php
* go
* ruby

For an overview on how these archives are structured, see [here](https://github.com/github/CodeSearchNet/blob/master/resources/README.md).

Run `python download_dataset.py -h` for a detailed usage guide.

## Extracting and Indexing the Dataset
The CodeSearchNet dataset comes pre-partitioned, meaning that training, validation, and test sets are maintained in separate files.
`setup_dataset.py` respects this partitioning, and performs the following operations:

* Extract the jsonl files.
* Concatenate .jsonl files that belong to the same language and partition. This is neccesary because one partition can be stored in multiple parts. 
* Indexes each jsonl file. In .jsonl files, each line corresponds to one example / data point. 
    The seek position of each example in the concatenated .jsonl file is recorded so that each example can be randomly accessed
    using its index. This facilitates random sampling later. 

Run `python setup_dataset.py -h` for a detailed usage guide.

## Sampling the Dataset
Once the .jsonl files are extracted and indexed, we are ready to sample the dataset. 
Given a partition and number of examples, `sample_dataset.py` allows you to select a balanced sample from all languages, 
and writes the result to a new .jsonl file. You can also pass in the `--excerpt` flag to specifiy whether a random excerpt
of the original code string should be taken. Note that only the following json fields are kept:

* language
* repo
* original_string

The meaning of each field is explained [here](https://github.com/github/CodeSearchNet#schema--format).

Run `python sample_dataset.py -h` for a detailed usage guide.