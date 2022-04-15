# Development Notes

This document covers best practices for development of GRE2G.

## Programming Principles

### Parameters Validation

It is assumed that all functions and class methods follow
[precondition principle](https://en.wikipedia.org/wiki/Precondition), specifically demanding approach. Demanding
approach states, that part of function or class method logic should be a pre-section which does the validation of all
input parameters and prevents code to be injected by wrong arguments. This also offloads the responsibility from user to
the function / class method itself.

### Design Patterns

The code should respect following software design patterns.

#### Null Object Pattern

When a function or method is supposed to return a value, it is not allowed to return `None` in any case. For each 
function or method, there has to be a special Null Object class, inheriting from `NullObjectBase` class located in 
`shared/null_object_base` module. If it is not supposed to work with a return value, then `None` is an appropriate way, 
e.g. for typing.

## Python Guidelines

**Max Line Length**: It is set to 120 characters.

### Commits Validation

Every commit has to pass through and be compliant with following tools:

- *Black* (automatic styling formatting)
- *Pylint* (linter)
- *Flake8* (linter)
- *MyPy* (annotations check)
- *Bandit* (vulnerabilities check)

The default configuration/standards of the tools is slightly modified generally and occasionally, there is a particular
PEP message disabling on a line level in the code.

Tools could be installed manually by a user or **using *pre-commit*** tool which integrates all the tools.
**This is also the preferred way.** See [Project Installation](../docs/project_installation.md) for more details about
*pre-commit* installation and location of modified configuration files.

### Docstring

It is used Google format.

To improve docstring readability, following highlight types are assumed:

- `<>`: Used to highlight `<variable>`, `<class>`, `<class.method()>`, `<class.attribute>`, `<function()>`, etc...
- `**`: Used to highlight GRE2G's modules (e.g. `*Video Streamer*`) and terms to emphasize that wording represents a
  specific solution's piece.
- ``` `` ```: Used to highlight source code blocks and commands (
  e.g. `` `from GRE2G.utils import *` ``), values (e.g. `` `-1` ``, `` `1.44` ``
  or `` `"string_value"` ``) or paths (e.g. `` `docs/images` ``).

## Python Dependencies

GRE2G uses Poetry as dependency and management tool. Therefore, only Poetry should be used (`poetry add` command), no
Pip or other ways. Developer should distinguish between dependencies for development and usage by an end user. For
development purposes, add Python dependencies using `--dev` option (`poetry add --dev`).

## YAML Configs

### Comments

YAML comments convention should follow [Python docstring](#docstring) convention.

### Config Values Validation

GRE2G does not use any main all YAML config parameters validation routine. Hydra does validation of expected config
parameters and their type. In the code, configuration variable is accessed whenever is needed using specific decorator,
applied on a function or class method. It passes the configuration variable as the first parameter in the function /
class method. Therefore, the same principle as in [Parameters Validation](#parameters-validation) is followed. The
function / class method has to validate required config parameter values and if the requirements are not met,
raise `ValueError` with custom message referring to the particular YAML config parameter.