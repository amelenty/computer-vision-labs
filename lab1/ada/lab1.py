import cv2

DATA_DIRECTORY = "resources/"
IMG_SHOW_DELAY_MS = 10000
MAX_IMAGE_WIDTH = 800


# sometimes I hate Python
def shrink_image(image):
    (height, width) = image.shape[:2]
    if width > MAX_IMAGE_WIDTH:
        ratio = MAX_IMAGE_WIDTH / width
        # return cv2.resize(image, (int(height * ratio), MAX_IMAGE_WIDTH))
        return cv2.resize(image, (MAX_IMAGE_WIDTH, int(height * ratio)))
    return image


if __name__ == '__main__':
    cv2.startWindowThread()
    sift = cv2.xfeatures2d.SIFT_create()
    base = cv2.imread(DATA_DIRECTORY + "base.jpg")
    base_gray = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
    base_gray_small = shrink_image(base_gray)
    cv2.imshow("Base gray", base_gray_small)
    cv2.waitKey(IMG_SHOW_DELAY_MS)
    key_points, descriptor = sift.detectAndCompute(base_gray_small, None)

    base_key_points = base_gray_small
    base_key_points = cv2.drawKeypoints(base_gray_small, key_points, base_key_points)
    cv2.imshow("Base with key points", shrink_image(base_key_points))
    cv2.waitKey(IMG_SHOW_DELAY_MS)
