**flight_tickets_analysis**
==============================

It is a data science project for predicting the lowest ticket price in a certain period of time.

1. Scraped from tcharter.ir

2. Pre-processing of data I gathered.

3. Phase of training model and predicting.

**Project Organization Hierarchy**
------------

    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── development        <- The deployment files like requirements.txt or docker-compose.yml can be here.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── source_codes       <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate dataset
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
--------

**How to run this project:**

1- Create virtual environment

2- Go to development dir and install dependencies with:
```
$ pip install -r requirements.txt
```

3- Go to data/common_utils and install it with:
```
$ pip install .
```

> [!NOTE]
> this is my common utils between flight_ticket_preprocessing and flight_tickets_scraper



<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
