import cv2
import numpy as np


class CoordinateMapper:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.calibration_points = []
        self.perspective_matrix = None

    def add_calibration_point(self, x, y):
        if len(self.calibration_points) >= 4:
            return False

        self.calibration_points.append((x, y))

        print(
            f"Calibration point "
            f"{len(self.calibration_points)}: ({x}, {y})"
        )

        if len(self.calibration_points) == 4:
            self._update_perspective_matrix()

        return True

    def _update_perspective_matrix(self):
        source_points = np.float32([
            self.calibration_points[0],
            self.calibration_points[1],
            self.calibration_points[2],
            self.calibration_points[3]
        ])

        destination_points = np.float32([
            [0, 0],
            [self.screen_width - 1, 0],
            [
                self.screen_width - 1,
                self.screen_height - 1
            ],
            [0, self.screen_height - 1]
        ])

        self.perspective_matrix = cv2.getPerspectiveTransform(
            source_points,
            destination_points
        )

        print("Calibration complete!")
        print("Perspective transform enabled.")

    def map_point(self, x, y, frame_width, frame_height):
        if self.perspective_matrix is not None:

            laser_point = np.array(
                [[[x, y]]],
                dtype=np.float32
            )

            transformed_point = cv2.perspectiveTransform(
                laser_point,
                self.perspective_matrix
            )

            screen_x = int(
                transformed_point[0][0][0]
            )

            screen_y = int(
                transformed_point[0][0][1]
            )

        else:
            screen_x = int(
                x / frame_width
                * self.screen_width
            )

            screen_y = int(
                y / frame_height
                * self.screen_height
            )

        screen_x = max(
            0,
            min(
                screen_x,
                self.screen_width - 1
            )
        )

        screen_y = max(
            0,
            min(
                screen_y,
                self.screen_height - 1
            )
        )

        return screen_x, screen_y

    def reset(self):
        self.calibration_points.clear()
        self.perspective_matrix = None

        print("Calibration reset.")

    def is_calibrated(self):
        return self.perspective_matrix is not None