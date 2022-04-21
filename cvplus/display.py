from __future__ import annotations

import cv2


def imshow_on_jupyter(img, format: str = ".jpg", options: dict = None):
    """
    Display Open CV image on the jupyter

    Parameters
    ----------
    img : cv2.Mat
        Open CV image
    format : str
        Image formatn ( .jpg / .png )

    Returns
    -------
    """
    from IPython.display import display, Image  # type: ignore

    decoded_bytes = cv2.imencode(format, img, options)[1].tobytes()
    display(Image(data=decoded_bytes))
