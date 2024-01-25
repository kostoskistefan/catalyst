# Catalyst

Catalyst is a python script to generate a C project from my personalized templates. The generated project uses Meson as a build system and generates initial quick start files.

For a more straightforward usage, add the `catalyst.py` file to your PATH.

## Script arguments

| Argument         | Description                                            | Default values       |
| ---              | ---                                                    | ---                  |
| **name**         | Name of the project                                    | No default, required |
| **type**         | Type of the project (library or executable)            | executable           |
| **license**      | Which license to use for the project (MIT or GPL)      | MIT                  |
| **enable-tests** | Whether to enable test file generation (true or false) | false                |

## Example Usage

#### MIT library without tests

`python catalyst.py --name my_lib --type library`

or more explicitly:

`catalyst.py --name my_lib --type library --license MIT --enable-tests false`


#### GPL application with tests

`catalyst.py --name my_app --type executable --license GPL --enable-tests true`
