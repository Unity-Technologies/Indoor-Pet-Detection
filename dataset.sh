#!/usr/bin/env bash

set -e

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

SYNTH_DIR="$BASE_DIR/data/synth"
SYNTH_TRAIN_DIR="$SYNTH_DIR/train-10k"
REAL_DIR="$BASE_DIR/data/real"
REAL_TRAIN_DIR="$REAL_DIR/train"
REAL_VAL_DIR="$REAL_DIR/val"
REAL_TEST_DIR="$REAL_DIR/test"

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
	if [ -d "$BASE_DIR/data" ]; then
		echo "WARNING: The 'data/' directory has already exist. Please remove it before initialization"
		exit 0
	fi

	echo "Initializing real datasets directories..."
	mkdir -p $SYNTH_DIR
	mkdir -p $REAL_DIR

	echo "Downloading real datasets"
	TMP_DIR="$BASE_DIR/tmp_datasets"
	if [ ! -d $TMP_DIR ]; then
		mkdir $TMP_DIR
		gsutil cp -r gs://indoor-pet-detection/data/real $TMP_DIR
	fi
	unzip -o -q "$TMP_DIR/real/train.zip" -d $REAL_DIR \
		&& mv "$REAL_DIR/train2017" $REAL_TRAIN_DIR \
		&& mv "$REAL_TRAIN_DIR/annotations_coco" "$REAL_TRAIN_DIR/$ANNOTATIONS_DIR" \
		&& mv "$REAL_TRAIN_DIR/$ANNOTATIONS_DIR/train_dog_coco.json" "$REAL_TRAIN_DIR/$ANNOTATIONS_DIR/$ANNOTATIONS_FILE"
	unzip -o -q "$TMP_DIR/real/val.zip" -d $REAL_DIR \
		&& mv "$REAL_DIR/val2017" $REAL_VAL_DIR \
		&& mv "$REAL_VAL_DIR/annotations_coco" "$REAL_VAL_DIR/$ANNOTATIONS_DIR" \
		&& mv "$REAL_VAL_DIR/$ANNOTATIONS_DIR/val_dog_coco.json" "$REAL_VAL_DIR/$ANNOTATIONS_DIR/$ANNOTATIONS_FILE"
	unzip -o -q "$TMP_DIR/real/test.zip" -d $REAL_DIR \
		&& mv "$REAL_TEST_DIR/annotations_coco" "$REAL_TEST_DIR/$ANNOTATIONS_DIR" \
		&& mv "$REAL_TEST_DIR/$ANNOTATIONS_DIR/test_dog_coco.json" "$REAL_TEST_DIR/$ANNOTATIONS_DIR/$ANNOTATIONS_FILE"

	rm -rf $TMP_DIR

	echo "Done"

elif [[ $CMD == "validate" ]]; then
	echo "Validating data directories..."
	validate_dir $SYNTH_TRAIN_DIR
	validate_dir $REAL_TRAIN_DIR
	validate_dir $REAL_VAL_DIR
	validate_dir $REAL_TEST_DIR
	echo "Done"

else
	help
	exit 1
fi
