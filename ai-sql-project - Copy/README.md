# AI SQK Project

Uses Conda for environment management.

## Update Dependencies

Edit the `environment.yml` file manually and modify a dependency, packages downloaded through Pip should be added under the `pip`, as a subpackage.

After the edits have been made, run the following code to install everything from the environment again.
```
conda env update --file environment.yml  --prune
```

## Running The Code

Activate the environment.

```
conda activate ai-sql-project
```

Run the code.

```
python ./project/main.py
```