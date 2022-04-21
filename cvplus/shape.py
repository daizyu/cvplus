from __future__ import annotations

import cv2
import numpy as np
from enum import IntEnum, auto
from typing import Any


class CROP_AFFIN(IntEnum):
    ccw_from_left_top = auto()
    cw_from_left_top = auto()
    left_top_down_right_top_down = auto()
    top_left_right_down_left_right = auto()


def crop_simple_affin(
    img: cv2.Mat,
    pts: Any,
    size: tuple | list[int] = (500, 500),
    mode: CROP_AFFIN = CROP_AFFIN.ccw_from_left_top,
):
    """
    Cropping rect by 4 points using affine transformation.
    img  : cv2.Mat
            Image
    pts  : Any
            4 points list or 4 points counter
    size : tuple | list[int],
            width , height
    mode : CROP_AFFIN = CROP_AFFIN.ccw_from_left_top,
            Points orders.
            ccw_from_top_left :
                Counter clock wise from top left
            cw_from_top_left  :
                Clock wise from top left
            left_top_down_right_top_down :
                Left Top, Left Down, Right Top, RIght Down
            top_left_right_down_left_right:
                Left Top, Right Top, Left Down, Right Down

    Returns
    -------
    img : cv2.Mat
    """

    ary = np.array(pts, np.float32)
    if ary.ndim == 2:  # Normal
        new_ary = ary
    elif ary.ndim == 3:
        if ary.shape[1] == 1:  # Countour Mode
            new_ary = ary.reshape([ary.shape[0], ary.shape[2]])
        else:
            raise NotImplementedError()
    else:
        raise NotImplementedError()

    w, h = size
    src_pts = np.array(new_ary, np.float32)
    if mode is CROP_AFFIN.ccw_from_left_top:
        dst_pts = np.array([[0, 0], [0, h], [w, h], [w, 0]], dtype=np.float32)
    elif mode is CROP_AFFIN.cw_from_left_top:
        dst_pts = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=np.float32)
    elif mode is CROP_AFFIN.left_top_down_right_top_down:
        dst_pts = np.array([[0, 0], [0, h], [w, 0], [w, h]], dtype=np.float32)
    elif mode is CROP_AFFIN.top_left_right_down_left_right:
        dst_pts = np.array([[0, 0], [w, 0], [0, h], [w, h]], dtype=np.float32)
    else:
        raise NotImplementedError

    mat = cv2.getPerspectiveTransform(src_pts, dst_pts)
    img2 = cv2.warpPerspective(img, mat, (w, h))
    return img2


if __name__ == "__main__":
    from cvplus import cvt, shape

    img = cvt.imread("test1.jpg")
    pts = [[9, 9], [52, 194], [235, 252], [375, 139]]
    img2 = shape.crop_simple_affin(img, pts, [200, 200])
    cvt.imwrite("test2.jpg", img2)
