import cv2
import numpy as np
import matplotlib.pyplot as plt


def create_coordinates(image, line_parameters):
    # Read 3/5ths up the cameras position
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * (3 / 5))

    # Calculate coordinates
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, asiline):
    # Get the slope and intercept to optimise the lines from hough transform
    left_fit = []
    right_fit = []
    for line in asiline:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]

        # Work out if we are on the left or right and create coordinates
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)

    left_line = create_coordinates(image, left_fit_average)
    right_lane = create_coordinates(image, right_fit_average)
    return np.array([left_line, right_lane])


def canny_edge_detection(image):
    # Copy the frame and convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Gaussian Filter and edge detection
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny


def region_of_interest(image):
    # Define our area of interest where road fits
    height = image.shape[0]
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)]
    ])
    mask = np.zeros_like(image)

    # Use openCV to fill mask and return
    cv2.fillPoly(mask, polygons, 255)
    apply_mask = cv2.bitwise_and(image, mask)
    return apply_mask


def draw_hough(image, hough_lines):
    # Take calculated hough lines and draw into numpy array as image
    hough_transformed_image = np.zeros_like(image)
    if hough_lines is not None:
        for x1, y1, x2, y2 in hough_lines:
            cv2.line(hough_transformed_image, (x1, y1), (x2, y2), (0, 255, 0), 5)
        return hough_transformed_image


# Video processing
video = cv2.VideoCapture("testdata/videos/dashcam.mp4")
while video.isOpened():
    _, frame = video.read()

    # Running functions
    canny_image = canny_edge_detection(frame)
    roi_image = region_of_interest(canny_image)

    # Hough Line transform algorithm
    lines = cv2.HoughLinesP(roi_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average_slope_intercept(frame, lines)
    hough_image = draw_hough(frame, averaged_lines)

    # Combine our copied frame and hough line applied image to show road markings
    weighted_image = cv2.addWeighted(frame, 0.8, hough_image, 1, 1)

    # Run our processing on each frame displaying for 1ms per frame
    cv2.imshow("output", weighted_image)
    cv2.waitKey(1)
