
mkdir -p data/synth/train2017
mkdir -p data/real/train2017
mkdir -p data/real/val2017
mkdir -p data/real/test

# real images for fine tuning [1200]
gsutil -m cp gs://dog_detection_data/formatted-datasets/coco-real-indoor-dog/train/train2017.zip data/real/train2017
unzip data/real/train/train2017.zip data/real/train/train2017.zip

# real images for validation [138]
gsutil -m cp gs://dog_detection_data/formatted-datasets/coco-real-indoor-dog/val/val2017.zip data/real/val2017
unzip data/real/val2017/val2017.zip data/real/val2017/

# real images for test [200]
gsutil -m cp gs://dog_detection_data/formatted-datasets/coco-real-indoor-dog/test/test.zip data/real/test
unzip data/real/test/test.zip data/real/test/

# synthetic images for training [5k]
gsutil -m cp gs://dog_detection_data/formatted-datasets/coco-synth-indoor-dog/train-5k/train2017.zip data/synth/train2017
unzip data/synth/train/train2017.zip data/synth/train/

