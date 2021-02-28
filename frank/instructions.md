# Installing pga tool

[Install pga - Public Git Archive Tool](https://github.com/src-d/datasets/tree/master/PublicGitArchive/pga)

1. Install Go 1.11+.
2. Set environment variable `GO111MODULE=on`.
3. Fetch and build: `go get github.com/src-d/datasets/PublicGitArchive/pga`
4. Find built binary in `%GOPATH%/bin`
5. Move binary to desired location, or modify path.

As of 2020, this tool is no [longer maintained / useable](https://github.com/src-d/datasets/issues/171). 

# Alternative Datasets

https://github.com/src-d/awesome-machine-learning-on-source-code#datasets

Promising candidate: https://github.com/github/CodeSearchNet
* Only has standalone functions?
* Actively maintained


[How the data directory is structured](https://github.com/github/CodeSearchNet/blob/master/resources/README.md)
[How the data is formatted](https://github.com/github/CodeSearchNet#schema--format)
[Data Exploration](https://github.com/github/CodeSearchNet/blob/master/notebooks/ExploreData.ipynb)

1. Download the achives from S3 server.
2. [Per the maintainers](https://github.com/github/CodeSearchNet#Data), code from the same repo can only appear in one of the training, validation, or test sets. 
3. We want the same number of data points across each of {python, ruby, java, javascript, go, php}.
4. For each language, we want 10000 examples. 
    * training -> 8000, validation -> 1000, test -> 1000
    * Above splits are tentative 
5. The dataset is already partitioned, so sampling will only take place within partitions for convenience. (e.g. we only sample )
6. Because the public data set is large (20 GB), we will pre-extract the 10000 examples per language to save time.