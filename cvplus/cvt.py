from __future__ import annotations


import cv2
import base64

import numpy as np
import os

from PIL import Image  # type: ignore


def imread(
    filepath: str, flags: int = cv2.IMREAD_COLOR, dtype: type = np.uint8
) -> cv2.Mat:
    """
    Read image file  ( enable contains non-ascill code file and directory name )

    Parameters
    ----------
    filepath : str
        File Name ( enable contains non-ascill code file and directory name )
    flags : int
        color mode
    dtype : Array type

    Returns
    -------
    image : cv2.Mat
        CV2 Image ( Null : Error )
    """
    try:
        n: np.ndarray = np.fromfile(filepath, dtype)
        img = cv2.imdecode(n, flags)
    except Exception as e:
        print(e)
        return None
    return img


def imwrite(filepath: str, img: cv2.Mat) -> bool:
    """
    Write image file  ( enable contains non-ascill code file and directory name )

    Parameters
    ----------
    filepath : str
        File Name ( enable contains non-ascill code file and directory name )
    img : cv2.Mat
        CV2 image

    Returns
    -------
    result : bool
        True >> Successful
        False >> Error
    """
    ret, ary = cv2.imencode(os.path.splitext(filepath)[1], img)
    if not ret:
        return False

    ary.tofile(filepath)

    return True


def imnew(w: int, h: int, d: int = 3, dtype: type = np.uint8) -> cv2.Mat:
    """
    Create new image file

    Parameters
    ----------
    w       : int
            width
    h       : int
            height
    d       : depth
            1 : Gray scale
            3 : Color
            4 : Color + alpha channel
    dtype   : np.uint8
            image array data type

    Returns
    -------
    img : cv2.Mat
    """
    assert d in [1, 3, 4]
    return np.zeros([h, w], dtype)


def to_pil(img: cv2.Mat) -> Image.Image:
    if img.ndim == 2:
        return Image.fromarray(img)
    elif img.shape[2] == 3:
        return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    elif img.shape[2] == 4:
        return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA))

    Exception(f'Incorrect image format shape="{img.shape}"')


def from_pil(pil_img: Image.Image) -> cv2.Mat:
    ary = np.array(pil_img, dtype=np.uint8)
    if ary.ndim == 2:
        return ary

    if ary.shape[2] == 3:
        return cv2.cvtColor(ary, cv2.COLOR_RGB2BGR)
    elif ary.shape[2] == 4:
        return cv2.cvtColor(ary, cv2.COLOR_RGBA2BGRA)

    raise Exception(f'Incorrect image format shape="{ary.shape}"')


def to_html_img_tag(img: cv2.Mat, attributes: dict = {}) -> str:
    attributes_str = ""
    for key, val in attributes.items():
        if type(val) is str:
            attributes_str += f' {key}="{val}"'
        elif type(val) is float or type(val) is int:
            attributes_str += f" {key}={val}"
        else:
            raise Exception("Incorrect type attributes")

    cnt = cv2.imencode(".png", img)[1]
    dat: str = base64.encodebytes(cnt).decode("utf-8")
    return f'<img src="data:image/png;base64,{dat}"{attributes_str}>'


if __name__ == "__main__":
    import cvplus.cvt

    img = cvplus.cvt.imnew(200, 100)

    pil_img = to_pil(img)

    img2 = from_pil(pil_img)

    img_tag = to_html_img_tag(img2, {"alt": "test code", "title": "Test"})
    # with codecs.open(r"test.html", "w+", "utf8") as f:
    #    f.write(f"<html>{img_tag}</html>")
