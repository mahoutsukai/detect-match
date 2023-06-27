import argparse
import datetime
import os
import sys

import cv2 as cv
import pandas as pd

from detectron2.data.datasets import register_coco_instances
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

# Clear the metadata cache
MetadataCatalog.clear()

annotation_file_path = os.path.expanduser("~/coco-annotator/datasets/Matches/.exports/coco-1684684967.4248435.json")
image_files_path = os.path.expanduser("~/coco-annotator/datasets/Matches/images")

register_coco_instances("match", {},
                        annotation_file_path,
                        image_files_path)

# Create predictor
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_match.pth")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.6
cfg.MODEL.DEVICE = "cpu"
predictor = DefaultPredictor(cfg)


def predection_match(imgPath, filename, sibling_directory):
    im = cv.imread(imgPath)

    # Get the metadata for the "match" dataset
    match_metadata = MetadataCatalog.get("match")

    # Create a custom color map where the "match" class has a different color than the other classes
    match_metadata.thing_classes = ["match"]
    match_metadata.thing_colors = [(255, 0, 0)]

    outputs = predictor(im)

    v = Visualizer(im[:, :, ::-1],
                   metadata=match_metadata,
                   scale=1.0
                   )

    v = v.draw_instance_predictions(outputs["instances"].to("cpu"))

    # Save results as JPEG file
    file_name = os.path.basename(filename)
    base_name = os.path.splitext(file_name)[0]
    new_filename = base_name + "_prediction_match.jpg"
    new_path = os.path.join(sibling_directory, new_filename)

    result_image = v.get_image()[:, :, ::-1]
    resize_image = cv.resize(result_image, (0, 0), fx=0.75, fy=0.75)
    cv.imwrite(new_path, resize_image, [cv.IMWRITE_JPEG_QUALITY, 60])
    print("saved {}".format(new_filename))

    # Save results as CSV file
    result = []
    var = [result.extend((x,
                          outputs["instances"][x].pred_classes.item(),
                          [match_metadata.thing_classes[x] for x in outputs["instances"][x].pred_classes][0],
                          outputs["instances"][x].scores.item(),
                          outputs["instances"][x].pred_boxes.tensor.cpu().numpy()[0][0],
                          outputs["instances"][x].pred_boxes.tensor.cpu().numpy()[0][1],
                          outputs["instances"][x].pred_boxes.tensor.cpu().numpy()[0][2],
                          outputs["instances"][x].pred_boxes.tensor.cpu().numpy()[0][3])
                         for x in range(len(outputs["instances"])))]
    df = pd.DataFrame(result, columns=['id', 'class-id', 'class', 'score', 'x-min', 'y-min', 'x-max', 'y-max'])
    csv_filename = new_filename + ".csv"
    csv_path = os.path.join(sibling_directory, csv_filename)
    df.to_csv(csv_path)
    print("saved {}".format(csv_filename))

    # Preview the results
    # cv.imshow("test", v.get_image()[:, :, ::-1])
    # cv.waitKey(0)


def process_jpg_files(directory, grandchild_directory_name):
    for root, dirs, files in os.walk(directory):
        dirs.sort()

        for dir_name in dirs:
            grandchild_directory = os.path.join(root, dir_name, grandchild_directory_name)

            # check if "grandchild_directory_name" directory exists
            if not os.path.exists(grandchild_directory):
                print('"{}" not exist in {}'.format(grandchild_directory_name, dir_name))
                continue

            if os.path.isdir(grandchild_directory):
                # Get the parent directory of "grandchild_directory_name" directory
                parent_directory = os.path.dirname(grandchild_directory)

                # Get size of first image
                for dirpath, dirnames, filenames in os.walk(grandchild_directory):
                    # just take the even ones
                    filenames = sorted(filenames)

                for dirpath, dirnames, filenames in os.walk(grandchild_directory):
                    filenames.sort()

                    # just take the even ones
                    filenames = sorted(filenames)

                    print(len(filenames))

                    now = datetime.datetime.now()
                    timestamp = now.strftime('%Y%m%d_%H%M%S')

                    sibling_directory_name = '_prediction_match_' + timestamp
                    sibling_directory = os.path.join(parent_directory, sibling_directory_name)

                    if not os.path.exists(sibling_directory):
                        os.mkdir(sibling_directory)

                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)

                        print()
                        print('filename: {}'.format(filename))

                        predection_match(filepath, filename, sibling_directory)

    sys.exit()


def main():
    parser = argparse.ArgumentParser(description='Detic to detect rect and caption')
    parser.add_argument('--directory_path', metavar='directory_path', type=str,
                        help='directory path to process')
    parser.add_argument('--grandchild_directory_name', metavar='grandchild_directory_name', type=str,
                        help='JPEG, JPEG_XXX')
    args = parser.parse_args()

    process_jpg_files(args.directory_path, args.grandchild_directory_name)


if __name__ == "__main__":
    main()
