import cv2

DATA_DIRECTORY = "resources/"
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


if __name__ == '__main__':

    cv2.startWindowThread()
    sift = cv2.xfeatures2d.SIFT_create()

    # Read the image we'll use as a base, make it grayscale and shrink it
    # If it's not grayscale, OpenCV crashes.
    # If it's too big, OpenCV crashes without mentioning that it ran out of memory (but it did).
    base = cv2.imread(DATA_DIRECTORY + "base.jpg")
    base_gray = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
    base_gray_small = shrink_image(base_gray)
    cv2.imshow("Base gray", base_gray_small)
    cv2.waitKey(IMG_SHOW_DELAY_MS)

    # Find key points and compute the descriptor
    key_points, descriptor = sift.detectAndCompute(base_gray_small, None)

    # Show key points on image.
    # You have to pass the output image to cv2.drawKeyPoints, also you have to declare it first.
    base_key_points = base_gray_small
    base_key_points = cv2.drawKeypoints(base_gray_small, key_points, base_key_points)
    cv2.imshow("Base with key points", base_key_points)
    cv2.waitKey(IMG_SHOW_DELAY_MS)
