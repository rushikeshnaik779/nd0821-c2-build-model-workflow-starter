#!/usr/bin/env python
"""
Perform basic cleaning on the data and save the results in W&B
"""
import argparse
import logging
import wandb
import pandas as pd 
import os 


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################


    artifact_local_path = run.use_artifact(args.input_artifact).file()

    dataframe = pd.read_csv(artifact_local_path, index_col="id")
    min_price = args.min_price
    max_price = args.max_price 
    idx = dataframe['price'].between(min_price, max_price)
    dataframe = dataframe[idx].copy()
    logger.info(f"Dataset price outliers removal outside range: {min_price} - {max_price}")


    tmp_artifact_path = os.path.join(args.temp_directory, args.output_artifact)
    dataframe.to_csv(tmp_artifact_path)

    logger.info(f"Temporary artifact saved {tmp_artifact_path}")

    artifact = wandb.Artifact(
        args.output_artifact, 
        type=args.output_type, 
        description=args.output_description
    )

    artifact.add_file(tmp_artifact_path)
    run.log_artifact(artifact)
    artifact.wait()
    logger.info("Cleaned dataset is uploaded to W&B")





if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data ")


    parser.add_argument(
        "--temp_directory", 
        type=str,
        help="Temporary directory for dataset storage",
        required=True
    )

    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Input artifact name",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Output artifact name",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="output artifact type",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Output artifact description",
        required=True

    )

    parser.add_argument(
        "--min_price",
        type=int,
        help="minimum price limit",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=int, 
        help="Maximum price limit",
        required=True
    )

    args = parser.parse_args()

    go(args)
