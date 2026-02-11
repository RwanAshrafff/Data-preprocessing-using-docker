#!/bin/bash

# Define the container name
CONTAINER_NAME="vibrant_wescoff"

# Define the source and destination paths
SOURCE="/home/doc-bd-a2/service-result"
DEST="./bd-a1/service-result"

# Create the destination directory if it doesn't exist
mkdir -p $DEST

# Copy the files from the container to the local machine
docker cp $CONTAINER_NAME:$SOURCE $DEST

# Stop the container
docker stop $CONTAINER_NAME
