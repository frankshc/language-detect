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
