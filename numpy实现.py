import numpy as np
import cv2 as cv
#
# # 创建一个 3x3x3 的三维数组
# array = np.array([
#     [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
#     [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
#     [[19, 20, 21], [22, 23, 24], [25, 26, 27]]
# ])
# print(array)
# print("*" * 100)
# print(array[:, :, 0])
# print("*" * 100)
# print(array[:, 0, :])
# print("*" * 100)
# print(array[0, :, :])
#
# img = cv.imread("c000019.jpg")
# cv.imshow("照片", img)
# cv.imshow("中值", cv.medianBlur(img, 5))
# cv.imshow("高斯", cv.GaussianBlur(img, (5, 5), 0))
# cv.imshow("均值", cv.blur(img, (5, 5)))
# cv.waitKey()

capture = cv.VideoCapture(0)

while True:
    ret, frame = capture.read()
    cv.imshow("camero", frame)
    key = cv.waitKey(1)
    if key != -1 & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()