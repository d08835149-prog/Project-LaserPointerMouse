import math
import pyautogui


class MouseController:
    def __init__(self, alpha=0.4, dead_zone=8):
        self.alpha = alpha
        self.dead_zone = dead_zone

        self.smooth_x = None
        self.smooth_y = None

        self.last_mouse_x = None
        self.last_mouse_y = None

    def move(self, screen_x, screen_y):
        # Smoothing
        if self.smooth_x is None:
            self.smooth_x = screen_x
            self.smooth_y = screen_y
        else:
            self.smooth_x = int(
                self.alpha * screen_x
                + (1 - self.alpha) * self.smooth_x
            )

            self.smooth_y = int(
                self.alpha * screen_y
                + (1 - self.alpha) * self.smooth_y
            )

        # Dead zone
        should_move = True

        if self.last_mouse_x is not None:
            distance = math.sqrt(
                (self.smooth_x - self.last_mouse_x) ** 2
                +
                (self.smooth_y - self.last_mouse_y) ** 2
            )

            if distance < self.dead_zone:
                should_move = False

        # Move Windows mouse
        if should_move:
            pyautogui.moveTo(
                self.smooth_x,
                self.smooth_y,
                duration=0
            )

            self.last_mouse_x = self.smooth_x
            self.last_mouse_y = self.smooth_y

        return self.smooth_x, self.smooth_y

    def reset(self):
        self.smooth_x = None
        self.smooth_y = None

        self.last_mouse_x = None
        self.last_mouse_y = None