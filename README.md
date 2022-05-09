# Build an ML Pipeline for Short-Term Rental Prices in NYC

This project was completed as part of the [Udacity Machine Learning DevOps Engineer NanoDegree](https://www.udacity.com/course/machine-learning-dev-ops-engineer-nanodegree--nd0821). The starter template code was forked from [the course repo](https://github.com/udacity/nd0821-c2-build-model-workflow-starter).

The setup for this project:

```
You are working for a property management company renting rooms and properties for short periods of 
time on various rental platforms. You need to estimate the typical price for a given property based 
on the price of similar properties. Your company receives new data in bulk every week. The model needs 
to be retrained with the same cadence, necessitating an end-to-end pipeline that can be reused.

In this project you will build such a pipeline.
```

## Final Pipeline Results
* [Github](https://github.com/jeffgerlach/mlops-nyc-rental-prices-pipeline)
* [Weights & Balances (W&B) Project Page](https://wandb.ai/jg06/nyc_airbnb)
* [W&B Test Regression Model Run](https://wandb.ai/jg06/nyc_airbnb/runs/2266xopv/overview)
* [Final Production Model Artifact](https://wandb.ai/jg06/nyc_airbnb/artifacts/model_export/random_forest_export/423fa0cdda5cf694d5b0)

## Pipeline Graph View
![Pipeline](pipeline.png?raw=true)

## Using MLFlow to Run the Pipeline

Make sure you are in the root directory in your terminal.

To run the entire pipeline:
```bash
>  mlflow run .
```

Pipeline steps:
- download
- basic_cleaning
- data_check
- data_split
- train_random_forest
- test_regression_model (requires model artifact with prod tag in W&B)

To run selected steps:
```bash
> mlflow run . -P steps=download,basic_cleaning
```

The pipeline utilizes hydra to pass in default parameters (stored in the top level `config.yaml` file and allows for overriding via the command line:
```bash
> mlflow run . \
  -P steps=basic_cleaning,train_random_forest \
  -P hydra_options="modeling.random_forest.max_features=0.5 etl.min_price=50"
```
