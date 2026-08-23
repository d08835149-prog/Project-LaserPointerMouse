import cv2
import pyautogui

from laser_detector import detect_green_laser
from coordinate_mapper import CoordinateMapper
from mouse_controller import MouseController


# -------------------------
# Camera setup
# -------------------------

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FPS, 60)

if not camera.isOpened():
    print("Camera could not be opened.")
    exit()


# -------------------------
# Screen size
# -------------------------

screen_width, screen_height = pyautogui.size()


# -------------------------
# Coordinate mapper
# -------------------------

mapper = CoordinateMapper(
    screen_width,
    screen_height
)


# -------------------------
# Mouse controller
# -------------------------

mouse_controller = MouseController(
    alpha=0.4,
    dead_zone=8
)


# -------------------------
# Calibration mouse callback
# -------------------------

def mouse_callback(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:

        if not mapper.add_calibration_point(x, y):
            print("Calibration already has 4 points.")


# -------------------------
# Camera window
# -------------------------

window_name = "LaserPointerMouse - Camera"

cv2.namedWindow(window_name)

cv2.setMouseCallback(
    window_name,
    mouse_callback
)


# -------------------------
# Main loop
# -------------------------

while True:

    ret, frame = camera.read()

    if not ret:
        print("Failed to read camera frame.")
        break


    # -------------------------
    # Laser detection
    # -------------------------

    laser_position, mask = detect_green_laser(
        frame
    )


    if laser_position is not None:

        x, y = laser_position

        frame_height, frame_width = frame.shape[:2]


        # -------------------------
        # Coordinate mapping
        # -------------------------

        screen_x, screen_y = mapper.map_point(
            x,
            y,
            frame_width,
            frame_height
        )


        # -------------------------
        # Mouse movement
        # -------------------------

        smooth_x, smooth_y = mouse_controller.move(
            screen_x,
            screen_y
        )


        print(
            f"Laser: x={x}, y={y} "
            f"-> Mouse: x={smooth_x}, y={smooth_y}"
        )


        # -------------------------
        # Draw laser marker
        # -------------------------

        cv2.circle(
            frame,
            (x, y),
            12,
            (0, 0, 255),
            2
        )

        cv2.putText(
            frame,
            f"Laser ({x}, {y})",
            (x + 15, y - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2
        )


    # -------------------------
    # Draw calibration points
    # -------------------------

    points = mapper.calibration_points

    for i, point in enumerate(points):

        cv2.circle(
            frame,
            point,
            8,
            (255, 0, 0),
            -1
        )

        cv2.putText(
            frame,
            str(i + 1),
            (
                point[0] + 10,
                point[1] - 10
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 0),
            2
        )


    # -------------------------
    # Draw calibration lines
    # -------------------------

    if len(points) >= 2:

        for i in range(
            len(points) - 1
        ):

            cv2.line(
                frame,
                points[i],
                points[i + 1],
                (255, 0, 0),
                2
            )


    if len(points) == 4:

        cv2.line(
            frame,
            points[3],
            points[0],
            (255, 0, 0),
            2
        )


    # -------------------------
    # Status text
    # -------------------------

    if mapper.is_calibrated():

        cv2.putText(
            frame,
            "CALIBRATED",
            (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    else:

        cv2.putText(
            frame,
            "Calibration: click TL -> TR -> BR -> BL",
            (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 0, 0),
            2
        )


    # -------------------------
    # Show windows
    # -------------------------

    cv2.imshow(
        window_name,
        frame
    )

    cv2.imshow(
        "Laser Mask",
        mask
    )


    # -------------------------
    # Keyboard controls
    # -------------------------

    key = cv2.waitKey(1) & 0xFF


    # Q = quit
    if key == ord("q"):
        break


    # R = reset calibration
    if key == ord("r"):

        mapper.reset()
        mouse_controller.reset()

        print("Mouse controller reset.")


# -------------------------
# Cleanup
# -------------------------

camera.release()
cv2.destroyAllWindows()
