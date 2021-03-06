import cv2
import numpy as np
import csv
import os
import time
import random
from metric import Metric

DATA_DIRECTORY = "resources/"
OUTPUT_DIRECTORY = "output/"
IMG_SHOW_DELAY_MS = 10000
MAX_IMAGE_HEIGHT = 800
MAX_IMAGE_WIDTH = 800
MIN_MATCH_COUNT = 10
IMAGE_SHOW_SAMPLING = 0.025
COLOR_MAGENTA = (0xff, 0x00, 0xff)


# Resize image so that width is MAX_IMAGE_WIDTH or less, keep ratio
def shrink_image(image):
    # image is a NumPy ndarray, so image.shape is (height, width, depth)
    (height, width) = image.shape[:2]

    if width > MAX_IMAGE_WIDTH:
        ratio = MAX_IMAGE_WIDTH / width
        # new size passed to resize() should be (width, height)
        image = cv2.resize(image, (MAX_IMAGE_WIDTH, int(height * ratio)))
        (height, width) = image.shape[:2]

    if height > MAX_IMAGE_HEIGHT:
        ratio = MAX_IMAGE_HEIGHT / height
        # new size passed to resize() should be (width, height)
        image = cv2.resize(image, (int(width * ratio), MAX_IMAGE_HEIGHT))

    return image


# Performs either SIFT for Ada, or BRISK for Vlada
def process_base_image(student, algo_name, algorithm):
    # Read the image we'll use as a base, make it grayscale and shrink it
    # If it's not grayscale, OpenCV crashes.
    # If it's too big, OpenCV crashes without mentioning that it ran out of memory (but it did).
    base = cv2.imread(DATA_DIRECTORY + student + "/base.jpg")
    base_gray = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
    base_gray_small = shrink_image(base_gray)
    cv2.imshow("Base gray", base_gray_small)

    # Find key points and compute the descriptor
    key_points, descriptor = algorithm.detectAndCompute(base_gray_small, None)

    # Show key points on image.
    # You have to pass the output image to cv2.drawKeyPoints, also you have to declare it first.
    base_key_points_img = base_gray_small
    base_key_points_img = cv2.drawKeypoints(base_gray_small, key_points, base_key_points_img)
    base_key_points_rich_img = base_gray_small
    base_key_points_rich_img = cv2.drawKeypoints(base_gray_small, key_points, base_key_points_rich_img,
                                                 flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow("Base with key points " + student.upper() + " " + algo_name.upper(), base_key_points_img)
    cv2.imwrite(OUTPUT_DIRECTORY + student + "/" + algo_name + "/base_key_points.jpg", base_key_points_img)
    cv2.imwrite(OUTPUT_DIRECTORY + student + "/" + algo_name + "/base_key_points_rich.jpg", base_key_points_rich_img)

    return base_gray_small, key_points, descriptor


def detect_object(query_kp, train_kp, matches):
    if len(matches) >= MIN_MATCH_COUNT:
        src_pts = np.float32([query_kp[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([train_kp[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        match_mask = mask.ravel().tolist()

        return M, match_mask

    else:
        return None, None


def process_test_image(output_dir, algo, norm, image, name):
    image_gray_small = shrink_image(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))

    time_start = time.perf_counter()
    key_points, descriptor = algo.detectAndCompute(image_gray_small, None)
    time_stop = time.perf_counter()

    bf = cv2.BFMatcher(norm, crossCheck=True)

    # Query goes first, train goes second. Same with cv2.drawMatches().
    matches = bf.match(descriptor, base_descriptor)

    metrics.append(Metric(name, image.shape[:2], time_stop - time_start, len(matches)))

    M, matches_mask = detect_object(key_points, base_key_points, matches)
    if M is not None:
        pts = np.float32([[0, 0], [0, base_height - 1], [base_width - 1, base_height - 1], [base_width - 1, 0]]) \
            .reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        moments = cv2.moments(dst)
        cx, cy = int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00'])

        image_gray_small = cv2.cvtColor(image_gray_small, cv2.COLOR_GRAY2BGR)
        cv2.circle(image_gray_small, (cx, cy), 15, COLOR_MAGENTA, -1)

        image_gray_small = cv2.polylines(image_gray_small, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

    match_img = cv2.drawMatches(image_gray_small, key_points, base_image, base_key_points, matches, None,
                                matchesMask=matches_mask, flags=2)

    if random.uniform(0, 1) < IMAGE_SHOW_SAMPLING:
        cv2.imshow(name, match_img)
    cv2.imwrite(output_dir + "match_" + name, match_img)


def save_metrics(directory):
    with open(directory + "metrics.csv", 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, metrics[0].__dict__.keys())
        writer.writeheader()
        writer.writerows([metric.__dict__ for metric in metrics])


if __name__ == '__main__':
    cv2.startWindowThread()
    sift = cv2.xfeatures2d.SIFT_create()
    brisk = cv2.BRISK_create()

    for student_name in ("ada", "vlada"):
        #  SIFT
        (base_image, base_key_points, base_descriptor) = process_base_image(student_name, "sift", sift)
        (base_height, base_width) = base_image.shape[:2]

        metrics = []

        for img_name in os.listdir(DATA_DIRECTORY + student_name + "/"):
            img = cv2.imread(DATA_DIRECTORY + student_name + "/" + img_name)
            # I used L1 because they say that "L1 and L2 norms are preferable choices for SIFT and SURF descriptors".
            process_test_image(OUTPUT_DIRECTORY + student_name + "/sift/", sift, cv2.NORM_L1, img, img_name)

        save_metrics(OUTPUT_DIRECTORY + student_name + "/sift/")

        # BRISK
        (base_image, base_key_points, base_descriptor) = process_base_image(student_name, "brisk", brisk)
        (base_height, base_width) = base_image.shape[:2]

        metrics = []

        for img_name in os.listdir(DATA_DIRECTORY + student_name + "/"):
            img = cv2.imread(DATA_DIRECTORY + student_name + "/" + img_name)
            process_test_image(OUTPUT_DIRECTORY + student_name + "/brisk/", brisk, cv2.NORM_HAMMING, img, img_name)

        save_metrics(OUTPUT_DIRECTORY + student_name + "/brisk/")

    cv2.waitKey()
