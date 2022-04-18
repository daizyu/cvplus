from __future__ import annotations

import argparse
import cv2
import numpy as np

from cvplus.cv2keycode import KeyCodes
from cvplus.utils.color_range import ColorRange
from cvplus.utils.image_files import ImageFiles

color_codes = {
    "hsv": cv2.COLOR_BGR2HSV,
    "hsv_full": cv2.COLOR_BGR2HSV_FULL,
    "hls": cv2.COLOR_BGR2HLS,
    "hls_full": cv2.COLOR_BGR2HLS_FULL,
    "rgb": cv2.COLOR_BGR2RGB,
    "bgr": None,
}


def callback_picker(event, x, y, flags, param):

    display_item: DisplayItems = param[0]
    color_range: ColorRange = param[1]
    if event == cv2.EVENT_LBUTTONDOWN:

        picked = display_item.cvt_img[y, x, :]
        lower, upper = color_range.update(picked)
        display_range(lower, upper)


class ThrusterKey:
    def __init__(self, keycode: KeyCodes, is_lower: bool, idx: int, offset: int):
        self.keycode = keycode
        self.is_lower = is_lower
        self.idx = idx
        self.offset = offset


thruster_keys = [
    ThrusterKey(KeyCodes.key2, True, 0, 5),
    ThrusterKey(KeyCodes.key3, True, 1, 5),
    ThrusterKey(KeyCodes.key4, True, 2, 5),
    ThrusterKey(KeyCodes.w, True, 0, 1),
    ThrusterKey(KeyCodes.e, True, 1, 1),
    ThrusterKey(KeyCodes.r, True, 2, 1),
    ThrusterKey(KeyCodes.s, True, 0, -1),
    ThrusterKey(KeyCodes.d, True, 1, -1),
    ThrusterKey(KeyCodes.f, True, 2, -1),
    ThrusterKey(KeyCodes.x, True, 0, -5),
    ThrusterKey(KeyCodes.c, True, 1, -5),
    ThrusterKey(KeyCodes.v, True, 2, -5),
    ThrusterKey(KeyCodes.key5, False, 0, 5),
    ThrusterKey(KeyCodes.key6, False, 1, 5),
    ThrusterKey(KeyCodes.key7, False, 2, 5),
    ThrusterKey(KeyCodes.t, False, 0, 1),
    ThrusterKey(KeyCodes.y, False, 1, 1),
    ThrusterKey(KeyCodes.u, False, 2, 1),
    ThrusterKey(KeyCodes.g, False, 0, -1),
    ThrusterKey(KeyCodes.h, False, 1, -1),
    ThrusterKey(KeyCodes.j, False, 2, -1),
    ThrusterKey(KeyCodes.b, False, 0, -5),
    ThrusterKey(KeyCodes.n, False, 1, -5),
    ThrusterKey(KeyCodes.m, False, 2, -5),
]


class DisplayItems:
    def __init__(self, scale: float, color_code: str):
        self.scale = scale
        self.color_code = color_code

    def set_image(self, img: np.ndarray):
        self.img = img

        h, w = img.shape[:2]
        scaled_h = int(h * self.scale)
        scaled_w = int(w * self.scale)

        self.scaled_img = cv2.resize(img, (scaled_w, scaled_h))

        color_code_val = color_codes[self.color_code]
        if color_code_val is None:
            self.cvt_img = self.scaled_img
        else:
            self.cvt_img = cv2.cvtColor(self.scaled_img, color_code_val)


def display_usage():
    print("Esc : close application")
    print("q / a : change image")
    print("-- change lower range (adjust manually)")
    print("2 / 3 / 4 : +5")
    print("w / e / r : +1")
    print("s / d / f : -1")
    print("x / c / v : -5")
    print("-- change upper range (adjust manually)")
    print("5 / 6 / 7 : +5")
    print("t / y / u : +1")
    print("g / h / j : -1")
    print("b / n / m : -5")


def display_range(lower: np.ndarray, upper: np.ndarray) -> None:
    print(lower, "---", upper)


def main(
    input_images: list[str], scale: float, color_code: str, start_range: np.ndarray
):

    image_files = ImageFiles(input_images)
    assert image_files.get_num_files() > 0, "Input image files are empty."

    display_item = DisplayItems(scale, color_code)
    display_item.set_image(image_files.get_image())

    color_range = ColorRange(start_range)

    cv2.namedWindow("img")
    cv2.setMouseCallback("img", callback_picker, param=[display_item, color_range])

    cv2.namedWindow(color_code)
    cv2.setMouseCallback(color_code, callback_picker, param=[display_item, color_range])

    cv2.namedWindow("mask")
    cv2.setMouseCallback("mask", callback_picker, param=[display_item, color_range])

    while True:
        cv2.imshow("img", display_item.scaled_img)
        cv2.imshow(color_code, display_item.cvt_img)

        mask = None
        if color_range.has():
            lower, upper = color_range.get_prev()
            mask = cv2.inRange(display_item.cvt_img, lower, upper)

            masked_img = display_item.scaled_img.copy()
            masked_img[mask != 0] = [0, 255, 255]
            cv2.imshow("mask", masked_img)

        keycode = cv2.waitKey(1) & 0xFF
        if keycode == KeyCodes.backspace.value:
            color_range.remove_last()

        elif keycode == KeyCodes.q.value:
            display_item.set_image(image_files.get_next_image())

        elif keycode == KeyCodes.a.value:
            display_item.set_image(image_files.get_prev_image())

        elif keycode == KeyCodes.esc.value:
            break

        elif keycode != 255:
            for thruster_key in thruster_keys:

                if keycode == thruster_key.keycode.value:
                    if thruster_key.is_lower:
                        lower, upper = color_range.mod_lower(
                            thruster_key.idx, thruster_key.offset
                        )
                        display_range(lower, upper)
                        break
                    else:
                        lower, upper = color_range.mod_upper(
                            thruster_key.idx, thruster_key.offset
                        )
                        display_range(lower, upper)
                        break
            else:
                display_usage()

    cv2.destroyAllWindows()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-images", nargs="*", help="input file", type=str, required=True
    )
    parser.add_argument(
        "--scale", help="display scale(--scale 0.5)", type=float, default=0.5
    )
    parser.add_argument("--color-code", default="hsv", choices=list(color_codes.keys()))
    parser.add_argument(
        "--start-range",
        nargs=6,
        type=int,
        default=[255, 255, 255, 0, 0, 0],
        help="initial range e.g. (--start-range 0 10 40 30 200 49)",
    )
    args = parser.parse_args()

    assert len(args.start_range) == 6, "--start-range should be 6 length"
    start_range = np.array(args.start_range)
    if np.any(np.array([255, 255, 255, 0, 0, 0]) != start_range):
        assert start_range.max() <= 255, "--start-range should be up to 255"
        assert start_range.max() >= 0, "--start-range should more than 0"
        assert np.all(
            start_range[:3] < start_range[3:]
        ), "--start-range first 3 values should be lower than last 3 values"

    main(args.input_images, args.scale, args.color_code, start_range)
