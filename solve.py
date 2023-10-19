import cv2
import numpy as np


class MazeSolver:
    def __init__(self, maze: np.ndarray):
        self._maze = maze
        self.contour1 = None
        self.contour2 = None
        self.dilation = None
        self.erosion = None
        self.difference = None
        self.mask = None
        self.res = None

        self._solve()

    def _solve(self):
        _, thresh = cv2.threshold(self._maze, 127, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        self.contour1 = cv2.drawContours(thresh, contours, 0, (255, 255, 255), 30)

        self.contour2 = cv2.drawContours(self.contour1, contours, 1, (0, 0, 0), 30)

        kernel = cv2.getStructuringElement(cv2.MORPH_OPEN, ksize=(20, 20))

        self.dilation = cv2.dilate(self.contour2, kernel, iterations=1)

        self.erosion = cv2.erode(self.dilation, kernel, iterations=1)

        self.difference = cv2.absdiff(self.dilation, self.erosion)

        self.mask = cv2.bitwise_not(self.difference)

        r, b = self._maze, self._maze
        r = cv2.bitwise_and(r, r, mask=self.mask)
        b = cv2.bitwise_and(b, b, mask=self.mask)

        self.res = cv2.merge((b, self._maze, r))

    def save_image(self, path: str):
        cv2.imwrite(path, self.res)
