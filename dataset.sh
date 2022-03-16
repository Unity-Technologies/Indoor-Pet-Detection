#!/usr/bin/env bash

help()
{
	echo "Usage: $0 [init|validate]"
	echo ""
	echo "  - init:	initialize data directory"
	echo "  - validate:	validate the structure of data directory"
	echo ""
}

BASE_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
CMD=$1

DATA_DIRS=(
	"$BASE_DIR/data/synth/train-10k"
	"$BASE_DIR/data/real/test2017"
	"$BASE_DIR/data/real/train2017"
	"$BASE_DIR/data/real/val2017"
	)

ANNOTATIONS_DIR="annotations"
IMAGES_DIR="images"
ANNOTATIONS_FILE="coco.json"

validate_dir()
{
	if [ ! -d $1 ]; then
		echo "ERROR: missing directory: $1"
	elif [ ! -d "$1/$ANNOTATIONS_DIR" ]; then
		echo "ERROR: missing directory: $1/$ANNOTATIONS_DIR"
	elif [ ! -f "$1/$ANNOTATIONS_DIR/$ANNOTATIONS_FILE" ]; then
		echo "ERROR: missing file: $1/$ANNOTATIONS_DIR/$ANNOTATIONS_FILE"
	elif [ ! -d "$1/$IMAGES_DIR" ]; then
		echo "ERROR: missing directory: $1/$IMAGES_DIR"
	else
		echo "Validation success: $1"
	fi
}


if [[ $CMD == "init" ]]; then
	echo "Initializing data directories..."
	for dir in ${DATA_DIRS[@]}; do
		mkdir -p $dir
	done
	echo "Done"

elif [[ $CMD == "validate" ]]; then
	echo "Validating data directories..."
	for dir in ${DATA_DIRS[@]}; do
		validate_dir $dir
	done
	echo "Done"

else
	help
	exit 1
fi
