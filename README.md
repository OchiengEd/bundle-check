# bundle-check

Bundle Check project provides two components. A certbundle python package which provides tools to check an operator bundle for 
completenes and correctness and a main.py which uses the certbundle package and runs checks against an operator bundle.

## Installation

To build the certbundle package and install it in your environment, follow the steps below:

1. Setup a python virtual environment for testing  
` ➜ bundle-check git:(main) ✗ python -m venv pyenv`
1. Activate the newly created python virtual environment  
` ➜ bundle-check git:(main) ✗ source pyenv/bin/activate`
1. Upgrade the python pip package  
`(pyenv) ➜ bundle-check git:(main) ✗ python -m pip install --upgrade pip`
1. Install the python build package  
`(pyenv) ➜  bundle-check git:(main) ✗ python -m pip install build`
1. Build the certbundle package using the build package  
`(pyenv) ➜  bundle-check git:(main) ✗ python -m build`
1. Install the newly build python package  
`(pyenv) ➜  bundle-check git:(main) ✗ python -m pip install dist/certbundle-0.0.1.tar.gz`

``
## Usage
You can then run the checks using the format below.

```
(pyenv) ➜  bundle-check git:(main) ✗ python3 main.py bundle -d ~/operators/test-operator/bundle
```

For more detailed output, you can append the `--debug` flag to the above command.
