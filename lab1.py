import cv2

IMG_FILE_NAME_1 = "img_from_webcam.png"
IMG_FILE_NAME_2 = "img_grayscale.png"
IMG_SHOW_DELAY_MS = 10000

# Colors in BGR
COLOR_PURPLE = (0x6F, 0x25, 0x6f)
COLOR_GOLD = (0x39, 0xA0, 0xAB)

if __name__ == "__main__":

    # Read an image from webcam
    print("Reading an image from webcam.")
    capture = cv2.VideoCapture(0)
    return_value, image_webcam = capture.read()
    capture.release()
    print("Done.")

    cv2.startWindowThread()

    # Display the image
    print("Displaying the image.")
    cv2.namedWindow("Image Window", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Image Window", image_webcam)
    print("Done.")
    cv2.waitKey(IMG_SHOW_DELAY_MS)

    # Write the image to disk
    print("Writing image to disk.")
    cv2.imwrite(IMG_FILE_NAME_1, image_webcam)
    print("Done.")

    # Load image from disk
    print("Loading image from disk.")
    image_disk = cv2.imread(IMG_FILE_NAME_1)
    print("Done.")

    # Convert the image to grayscale
    print("Converting the image to grayscale.")
    image_grayscale = cv2.cvtColor(image_webcam, cv2.COLOR_BGR2GRAY)
    # Need to convert it back to be able to draw colored lines
    image_grayscale = cv2.cvtColor(image_grayscale, cv2.COLOR_GRAY2BGR)
    print("Done")

    # Draw a diagonal line
    print("Drawing a diagonal line.")
    height, width = image_grayscale.shape[:2]
    cv2.line(image_grayscale, (0, 0), (width, height), COLOR_PURPLE, 2)
    print("Done.")

    # Draw a rectangle
    print("Drawing a rectangle.")
    cv2.rectangle(image_grayscale, (width // 4, height // 4), (3 * width // 4, 3 * height // 4), COLOR_GOLD, 2)
    print("Done.")

    # Display the image
    print("Displaying the image.")
    cv2.namedWindow("Grayscale Window", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Grayscale Window", image_grayscale)
    cv2.waitKey(IMG_SHOW_DELAY_MS)
    print("Done.")

    # Write the second image to disk
    print("Writing image to disk.")
    cv2.imwrite(IMG_FILE_NAME_2, image_grayscale)
    print("Done.")

