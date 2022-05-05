#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import os
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    logger.info("Downloading artifact")
    artifact = run.use_artifact(args.input_artifact)
    artifact_path = artifact.file()

    df = pd.read_csv(artifact_path)

    # Apply minimal data processing:
    # Drop outliers
    logger.info("Removing price outliers")
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    logger.info("Converting last_review to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    # Save data to csv
    logger.info("Generating CSV")
    filename = args.output_artifact
    df.to_csv(filename, index=False)

    # Upload cleaned data as artifact
    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(filename)

    logger.info("Logging/uploading artifact")
    run.log_artifact(artifact)

    # Cleanup
    logger.info("Removing CSV")
    os.remove(filename)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Input artifact name to use for cleaning from W&B",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Output artifact name for W&B",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Output artifact type for W&B",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description for output artifact for W&B",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Min price to allow in dataset",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Max price to allow in dataset",
        required=True
    )


    args = parser.parse_args()

    go(args)
