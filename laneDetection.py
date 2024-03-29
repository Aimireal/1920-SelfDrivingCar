import numpy as np
import cv2
import utils

######################################################################################################
# laneDetection.py: Uses utils.py to process video feeds for lane detection and steering prediction
######################################################################################################

cameraFeed = False
videoPath = 'testdata/videos/dashcamdark.mp4'
cameraNo = 1
frameWidth = 640
frameHeight = 480

# Set up our predefined distortion map co-ordinates
if cameraFeed:
    initialTrackPoint = [24, 55, 12, 100]
else:
    initialTrackPoint = [42, 47, 16, 77]

if cameraFeed:
    cap = cv2.VideoCapture(cameraNo)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
else:
    cap = cv2.VideoCapture(videoPath)

count = 0
noOfArrayValues = 10
global arrayCurve, arrayCounter
arrayCounter = 0
arrayCurve = np.zeros([noOfArrayValues])
myVals = []
utils.initializeTrackPoints(initialTrackPoint)

while True:
    success, img = cap.read()
    if not cameraFeed:
        img = cv2.resize(img, (frameWidth, frameHeight), None)
    imgWarpPoints = img.copy()
    imgFinal = img.copy()
    imgCanny = img.copy()

    imgUndis = utils.remove_distortion(img)
    imgThres, imgCanny, imgColor = utils.thresholding(imgUndis)
    src = utils.valTrackPoints()
    imgWarp = utils.perspective_warp(imgThres, dst_size=(frameWidth, frameHeight), src=src)
    imgWarpPoints = utils.drawPoints(imgWarpPoints, src)
    imgSliding, curves, lanes, ploty = utils.sliding_window(imgWarp, draw_windows=True)

    try:
        curverad = utils.get_curve(imgFinal, curves[0], curves[1])
        lane_curve = np.mean([curverad[0], curverad[1]])
        imgFinal = utils.draw_lanes(img, curves[0], curves[1], frameWidth, frameHeight, src=src)

        # Average the lane curvature
        currentCurve = lane_curve // 50
        if int(np.sum(arrayCurve)) == 0:
            averageCurve = currentCurve
        else:
            averageCurve = np.sum(arrayCurve) // arrayCurve.shape[0]
        if abs(averageCurve - currentCurve) > 200:
            arrayCurve[arrayCounter] = averageCurve
        else:
            arrayCurve[arrayCounter] = currentCurve

        arrayCounter += 1
        if arrayCounter >= noOfArrayValues:
            arrayCounter = 0

        cv2.putText(imgFinal, str(int(averageCurve)), (frameWidth // 2 - 70, 70), cv2.FONT_HERSHEY_DUPLEX, 1.75,
                    (255, 0, 255), 2, cv2.LINE_AA)

    except:
        lane_curve = 00
        pass

    imgFinal = utils.drawLines(imgFinal, lane_curve)
    imgThres = cv2.cvtColor(imgThres, cv2.COLOR_GRAY2BGR)
    imgBlank = np.zeros_like(img)

    # Show every process of what we do
    # imgStacked = utils.stackImages(0.7, ([img, imgUndis, imgWarpPoints],
    # [imgColor, imgCanny, imgThres],
    # [imgWarp, imgSliding, imgFinal]
    #  ))
    # cv2.imshow("Result", imgFinal)

    # Show our interface and set up an exit condition on Q
    imgStacked = utils.stackImages(0.9, ([imgWarpPoints, imgSliding, imgFinal]))
    cv2.imshow("PipeLine", imgStacked)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
