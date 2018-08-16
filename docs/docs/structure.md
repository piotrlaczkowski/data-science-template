## Directory structure

```
├── LICENSE
├── Dockerfile            <- New project Dockerfile that sources from base ML dev image
├── docker-compose.yml    <- Docker Compose configuration file
├── docker_clean_all.sh   <- Helper script to remove all containers and images from your system
├── start.sh              <- Script to run docker compose and any other project specific initialization steps 
├── Makefile              <- Makefile with commands like `make data` or `make train`
├── README.md             <- The top-level README for developers using this project.
├── data
│   ├── external          <- Data from third party sources.
│   ├── interim           <- Intermediate data that has been transformed.
│   ├── processed         <- The final, canonical data sets for modeling.
│   └── raw               <- The original, immutable data dump.
│
├── docs                  <- A default Sphinx project; see sphinx-doc.org for details
│
├── models                <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks             <- Jupyter notebooks. Naming convention is a number (for ordering),
│                            the creator's initials, and a short `-` delimited description, e.g.
│                            `1.0-jqp-initial-data-exploration`.
│
├── references            <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports               <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures           <- Generated graphics and figures to be used in reporting
│
├── requirements.txt      <- The requirements file for reproducing the analysis environment, e.g.
│                            generated with `pip freeze > requirements.txt`
│
├── src                   <- Source code for use in this project.
│   ├── __init__.py       <- Makes src a Python module
│   │
│   ├── data              <- Scripts to download or generate data
│   │   └── make_dataset.py
│   │
│   ├── features          <- Scripts to turn raw data into features for modeling
│   │   └── build_features.py
│   │
│   ├── models            <- Scripts to train models and then use trained models to make
│   │   │                    predictions
│   │   ├── predict_model.py
│   │   └── train_model.py
│   │
│   └── visualization  <- Scripts to create exploratory and results oriented visualizations
│       └── visualize.py
│
└── tox.ini            <- tox file with settings for running tox; see tox.testrun.org
```

### Data is immutable

- Don't ever edit your raw data, especially not manually, and especially not in Excel. 

- Don't overwrite your raw data. 

- Don't save multiple versions of the raw data. 

- Treat the data (and its format) as immutable. 

The code you write should move the raw data through a pipeline to your final analysis. You shouldn't have to run all of the steps every time you want to make a new figure (see [Analysis is a DAG](#analysis-is-a-dag)), but anyone should be able to reproduce the final products with only the code in `src` and the data in `data/raw`.

Also, if data is immutable, it doesn't need source control in the same way that code does. Therefore, ***by default, the data folder is included in the `.gitignore` file.*** If you have a small amount of data that rarely changes, you may want to include the data in the repository. Github currently warns if files are over 50MB and rejects files over 100MB. Some other options for storing/syncing large data include [AWS S3](https://aws.amazon.com/s3/) with a syncing tool (e.g., [`s3cmd`](http://s3tools.org/s3cmd)), [Git Large File Storage](https://git-lfs.github.com/), [Git Annex](https://git-annex.branchable.com/), and [dat](http://dat-data.com/). Currently by default, we ask for an S3 bucket and use [AWS CLI](http://docs.aws.amazon.com/cli/latest/reference/s3/index.html) to sync data in the `data` folder with the server.

### Notebooks are for exploration and communication

Notebook packages like the [Jupyter notebook](http://jupyter.org/), [Beaker notebook](http://beakernotebook.com/), [Zeppelin](http://zeppelin-project.org/), and other literate programming tools are very effective for exploratory data analysis. However, these tools can be less effective for reproducing an analysis. When we use notebooks in our work, we often subdivide the `notebooks` folder. For example, `notebooks/exploratory` contains initial explorations, whereas `notebooks/reports` is more polished work that can be exported as html to the `reports` directory.

Since notebooks are challenging objects for source control (e.g., diffs of the `json` are often not human-readable and merging is near impossible), we recommended not collaborating directly with others on Jupyter notebooks. There are two steps we recommend for using notebooks effectively:

 1. **Follow a naming convention** that shows the owner and the order the analysis was done in. We use the format `<step_number>-<your_initials>-<description>.ipynb` (e.g., `1-PL-visualize-distributions.ipynb`).

 2. **Refactor the good parts!** Don't write code to do the same task in multiple notebooks. If it's a data preprocessing task, put it in the pipeline at `src/data/make_dataset.py` and load data from `data/interim`. If it's useful utility code, refactor it to `src` and import it into notebooks with a cell like the following. If updating the system path is picky to you, we'd recommend making a Python package (there is a [cookiecutter for that](https://github.com/audreyr/cookiecutter-pypackage) as well) and installing that as an editable package with `pip install -e`.

```
# Load the "autoreload" extension
%load_ext autoreload

# always reload modules marked with "%aimport"
%autoreload 1

import os
import sys

# add the 'src' directory as one where we can import modules
src_dir = os.path.join(os.getcwd(), os.pardir, 'src')
sys.path.append(src_dir)

# import my method from the source code
%aimport preprocess.build_features
from preprocess.build_features import remove_invalid_data
```

### Analysis is a DAG

Often in an analysis you have long-running steps that preprocess data or train models. If these steps have been run already (and you have stored the output somewhere like the `data/interim` directory), you don't want to wait to rerun them every time. We prefer [`make`](https://www.gnu.org/software/make/) for managing steps that depend on each other, especially the long-running ones. Make is a common tool on Unix-based platforms (and [is available for Windows]()). Following the [`make` documentation](https://www.gnu.org/software/make/), [Makefile conventions](https://www.gnu.org/prep/standards/html_node/Makefile-Conventions.html#Makefile-Conventions), and [portability guide](http://www.gnu.org/savannah-checkouts/gnu/autoconf/manual/autoconf-2.69/html_node/Portable-Make.html#Portable-Make) will help ensure your Makefiles work effectively across systems. Here are [some](http://zmjones.com/make/) [examples](http://blog.kaggle.com/2012/10/15/make-for-data-scientists/) to [get started](https://web.archive.org/web/20150206054212/http://www.bioinformaticszen.com/post/decomplected-workflows-makefiles/). A number of data folks use `make` as their tool of choice, including [Mike Bostock](https://bost.ocks.org/mike/make/).

There are other tools for managing DAGs that are written in Python instead of a DSL (e.g., [Paver](http://paver.github.io/paver/#), [Luigi](http://luigi.readthedocs.org/en/stable/index.html), [Airflow](http://pythonhosted.org/airflow/cli.html), [Snakemake](https://bitbucket.org/snakemake/snakemake/wiki/Home), [Ruffus](http://www.ruffus.org.uk/), or [Joblib](https://pythonhosted.org/joblib/memory.html)). Feel free to use these if they are more appropriate for your analysis.

### Build from the environment up

The first step in reproducing an analysis is always reproducing the computational environment it was run in. You need the same tools, the same libraries, and the same versions to make everything play nicely together.

One effective approach to this is use [virtualenv](https://virtualenv.pypa.io/en/latest/) (we recommend [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) for managing virtualenvs). By listing all of your requirements in the repository (we include a `requirements.txt` file) you can easily track the packages needed to recreate the analysis. Here is a good workflow:

 >1. Run `mkvirtualenv` when creating a new project
 2. `pip install` the packages that your analysis needs
 3. Run `pip freeze > requirements.txt` to pin the exact package versions used to recreate the analysis
 4. If you find you need to install another package, run `pip freeze > requirements.txt` again and commit the changes to version control.

If you have more complex requirements for recreating your environment, consider a virtual machine based approach such as [Docker](https://www.docker.com/) or [Vagrant](https://www.vagrantup.com/). Both of these tools use text-based formats (Dockerfile and Vagrantfile respectively) you can easily add to source control to describe how to create a virtual machine with the requirements you need.

### Keep secrets and configuration out of version control

You _really_ don't want to leak your AWS secret key or Postgres username and password on Github. Enough said — see the [Twelve Factor App](http://12factor.net/config) principles on this point. Here's one way to do this:

#### Store your secrets and config variables in a special file

Create a `.env` file in the project root folder. Thanks to the `.gitignore`, this file should never get committed into the version control repository. Here's an example:

```nohighlight
# example .env file
DATABASE_URL=postgres://username:password@localhost:5432/dbname
AWS_ACCESS_KEY=myaccesskey
AWS_SECRET_ACCESS_KEY=mysecretkey
OTHER_VARIABLE=something
```

#### Use a package to load these variables automatically.

If you look at the stub script in `src/data/make_dataset.py`, it uses a package called [python-dotenv](https://github.com/theskumar/python-dotenv) to load up all the entries in this file as environment variables so they are accessible with `os.environ.get`. Here's an example snippet adapted from the `python-dotenv` documentation:

```python
# src/data/dotenv_example.py
import os
from dotenv import load_dotenv, find_dotenv

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()

# load up the entries as environment variables
load_dotenv(dotenv_path)

database_url = os.environ.get("DATABASE_URL")
other_variable = os.environ.get("OTHER_VARIABLE")
```

#### AWS CLI configuration
When using Amazon S3 to store data, a simple method of managing AWS access is to set your access keys to environment variables. However, managing mutiple sets of keys on a single machine (e.g. when working on multiple projects) it is best to use a [credentials file](https://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html), typically located in `~/.aws/credentials`. A typical file might look like:
```
[default]
aws_access_key_id=myaccesskey
aws_secret_access_key=mysecretkey

[another_project]
aws_access_key_id=myprojectaccesskey
aws_secret_access_key=myprojectsecretkey
```
You can add the profile name when initialising a project; assuming no applicable environment variables are set, the profile credentials will be used be default.

