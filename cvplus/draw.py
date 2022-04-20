from __future__ import annotations

import cv2
import math
from enum import IntEnum, auto
from typing import Any


class ArrowShape(IntEnum):
    none = auto()
    normal = auto()
    side_a = auto()
    side_b = auto()


def arrow(
    img: cv2.Mat,
    pt1: Any,
    pt2: Any,
    color: Any,
    thickness: int = 1,
    line_type: int = cv2.LINE_8,
    shift: int = 0,
    arrow_size: float = 10,
    arrow_angle: float = 30,
    arrow_shape1: ArrowShape = ArrowShape.normal,
    arrow_shape2: ArrowShape = ArrowShape.none,
):
    """
    Draw arrow

    Parameters
    ----------
    img         : cv2.Mat
    pt1         : Any
    pt2         : Any
    color       : Any
    thickness   : int = 1,
    line_type   : int = cv2.LINE_8,
    shift       : int = 0
    arrow_size  : float = 10
    arrow_angle : float = 30
    arrow_shape1: ArrowShape = ArrowShape.normal
    arrow_shape2: ArrowShape = ArrowShape.none
    Returns
    -------
    img : cv2.Mat
    """

    cv2.line(
        img=img,
        pt1=pt1,
        pt2=pt2,
        color=color,
        thickness=thickness,
        lineType=line_type,
        shift=shift,
    )

    rad = math.radians(arrow_angle)
    if arrow_shape1 is not ArrowShape.none:
        rad1 = math.atan2(pt2[1] - pt1[1], pt2[0] - pt1[0])
        rad1_1 = rad1 + rad
        rad1_2 = rad1 - rad
        if arrow_shape1 is not ArrowShape.side_b:
            x = int(pt1[0] + math.cos(rad1_1) * arrow_size)
            y = int(pt1[1] + math.sin(rad1_1) * arrow_size)
            cv2.line(
                img,
                pt2,
                (x, y),
                color=color,
                thickness=thickness,
                lineType=line_type,
                shift=shift,
            )
        if arrow_shape1 is not ArrowShape.side_a:
            x = int(pt1[0] + math.cos(rad1_2) * arrow_size)
            y = int(pt1[1] + math.sin(rad1_2) * arrow_size)
            cv2.line(
                img,
                pt1,
                (x, y),
                color=color,
                thickness=thickness,
                lineType=line_type,
                shift=shift,
            )
    if arrow_shape2 is ArrowShape.normal:
        rad2 = math.atan2(pt1[1] - pt2[1], pt1[0] - pt2[0])
        rad2_1 = rad2 + rad
        rad2_2 = rad2 - rad
        if arrow_shape2 is not ArrowShape.side_a:
            x = int(pt2[0] + math.cos(rad2_1) * arrow_size)
            y = int(pt2[1] + math.sin(rad2_1) * arrow_size)
            cv2.line(
                img,
                pt2,
                (x, y),
                color=color,
                thickness=thickness,
                lineType=line_type,
                shift=shift,
            )
        if arrow_shape2 is not ArrowShape.side_b:
            x = int(pt2[0] + math.cos(rad2_2) * arrow_size)
            y = int(pt2[1] + math.sin(rad2_2) * arrow_size)
            cv2.line(
                img,
                pt2,
                (x, y),
                color=color,
                thickness=thickness,
                lineType=line_type,
                shift=shift,
            )
    return img
