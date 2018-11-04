import cv2

DATA_DIRECTORY = "resources/"
OUTPUT_DIRECTORY = "output/"
IMG_SHOW_DELAY_MS = 10000
MAX_IMAGE_WIDTH = 800


# Resize image so that width is MAX_IMAGE_WIDTH or less, keep ratio
def shrink_image(image):
    # image is a NumPy ndarray, so image.shape is (height, width, depth)
    (height, width) = image.shape[:2]
    if width > MAX_IMAGE_WIDTH:
        ratio = MAX_IMAGE_WIDTH / width
        # new size passed to resize() should be (width, height)
        return cv2.resize(image, (MAX_IMAGE_WIDTH, int(height * ratio)))
    return image


def process_base_image():
    # Read the image we'll use as a base, make it grayscale and shrink it
    # If it's not grayscale, OpenCV crashes.
    # If it's too big, OpenCV crashes without mentioning that it ran out of memory (but it did).
    base = cv2.imread(DATA_DIRECTORY + "base.jpg")
    base_gray = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
    base_gray_small = shrink_image(base_gray)
    cv2.imshow("Base gray", base_gray_small)

    # Find key points and compute the descriptor
    key_points, descriptor = sift.detectAndCompute(base_gray_small, None)

    # Show key points on image.
    # You have to pass the output image to cv2.drawKeyPoints, also you have to declare it first.
    base_key_points_img = base_gray_small
    base_key_points_img = cv2.drawKeypoints(base_gray_small, key_points, base_key_points_img)
    base_key_points_rich_img = base_gray_small
    base_key_points_rich_img = cv2.drawKeypoints(base_gray_small, key_points, base_key_points_rich_img,
                                             flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow("Base with key points", base_key_points_img)
    cv2.imwrite(OUTPUT_DIRECTORY + "base_key_points.jpg", base_key_points_img)
    cv2.imwrite(OUTPUT_DIRECTORY + "base_key_points_rich.jpg", base_key_points_rich_img)

    return base_gray_small, key_points, descriptor


def process_test_image(image, name):
    image_gray_small = shrink_image(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    key_points, descriptor = sift.detectAndCompute(image_gray_small, None)

    # I used L1 because they say that "L1 and L2 norms are preferable choices for SIFT and SURF descriptors".
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

    # Query goes first, train goes second. Same with cv2.drawMatches().
    matches = bf.match(descriptor, base_descriptor)
    match_img = cv2.drawMatches(image_gray_small, key_points, base_image, base_key_points, matches, None)
    cv2.imshow(name, match_img)


if __name__ == '__main__':
    cv2.startWindowThread()
    sift = cv2.xfeatures2d.SIFT_create()

    (base_image, base_key_points, base_descriptor) = process_base_image()

    img_names = ['001+.jpg', '003-.jpg', '010+.jpg', '020+.jpg', '021-.jpg']

    for img_name in img_names:
        img = cv2.imread(DATA_DIRECTORY + img_name)
        process_test_image(img, img_name)

    cv2.waitKey()
