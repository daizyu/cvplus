from __future__ import annotations

import argparse
import cv2
import numpy as np

from cvplus.cv2keycode import KeyCodes
from cvplus.utils.image_files import ImageFiles


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-images", nargs="*", help="input file", type=str, required=True
    )
    # parser.add_argument(
    #     "--scale", help="display scale(--scale 0.5)", type=float, default=0.5
    # )
    # parser.add_argument("--color-code", default="hsv", choices=list(color_codes.keys()))
    # parser.add_argument(
    #    "--start-range",
    #    nargs=6,
    #    type=int,
    #    default=[255, 255, 255, 0, 0, 0],
    #    help="initial range e.g. (--start-range 0 10 40 30 200 49)",
    # )
    args = parser.parse_args()

    # assert len(args.start_range) == 6, "--start-range should be 6 length"
    # start_range = np.array(args.start_range)
    # if np.any(np.array([255, 255, 255, 0, 0, 0]) != start_range):
    #    assert start_range.max() <= 255, "--start-range should be up to 255"
    #    assert start_range.max() >= 0, "--start-range should more than 0"
    #    assert np.all(
    #        start_range[:3] < start_range[3:]
    #    ), "--start-range first 3 values should be lower than last 3 values"

    main(args.input_images, args.scale, args.color_code, start_range)
