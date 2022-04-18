from __future__ import annotations

import argparse
import cv2
import os
from cvplus.cv2keycode import KeyCodes
from cvplus import cvt
import logging


camera_parameters = {
    "CAP_PROP_FRAME_WIDTH": cv2.CAP_PROP_FRAME_WIDTH,
    "CAP_PROP_FRAME_HEIGHT": cv2.CAP_PROP_FRAME_HEIGHT,
    "CAP_PROP_FOURCC": cv2.CAP_PROP_FRAME_HEIGHT,
    "CAP_PROP_BRIGHTNESS": cv2.CAP_PROP_BRIGHTNESS,
    "CAP_PROP_CONTRAST": cv2.CAP_PROP_CONTRAST,
    "CAP_PROP_SATURATION": cv2.CAP_PROP_SATURATION,
    "CAP_PROP_HUE": cv2.CAP_PROP_HUE,
    "CAP_PROP_GAIN": cv2.CAP_PROP_GAIN,
    "CAP_PROP_EXPOSURE": cv2.CAP_PROP_EXPOSURE,
    "CAP_PROP_FPS": cv2.CAP_PROP_FPS,
    "CAP_PROP_FORMAT": cv2.CAP_PROP_FORMAT,
    "CAP_PROP_MODE": cv2.CAP_PROP_MODE,
    "CAP_PROP_CONVERT_RGB": cv2.CAP_PROP_CONVERT_RGB,
    "CAP_PROP_GAMMA": cv2.CAP_PROP_GAMMA,
    "CAP_PROP_FOCUS": cv2.CAP_PROP_FOCUS,
    "CAP_PROP_PAN": cv2.CAP_PROP_PAN,
    "CAP_PROP_TILT": cv2.CAP_PROP_TILT,
    "CAP_PROP_ROLL": cv2.CAP_PROP_ROLL,
    "CAP_PROP_TEMPERATURE": cv2.CAP_PROP_TEMPERATURE,
    "CAP_PROP_TRIGGER": cv2.CAP_PROP_TRIGGER,
    "CAP_PROP_TRIGGER_DELAY": cv2.CAP_PROP_TRIGGER_DELAY,
    "CAP_PROP_SETTINGS": cv2.CAP_PROP_SETTINGS,
    "CAP_PROP_AUTO_EXPOSURE": cv2.CAP_PROP_AUTO_EXPOSURE,
    "CAP_PROP_AUTOFOCUS": cv2.CAP_PROP_AUTOFOCUS,
    "CAP_PROP_AUTO_WB": cv2.CAP_PROP_AUTO_WB,
}


def display_usage():
    logging.info("===== Key assignment")
    logging.info("s   : save(grab)")
    logging.info("esc : close application")


def main(
    output_folder: str, camera_id: int, extention: str, camera_parameters_settings: dict
) -> None:
    global camera_parameters

    logging.basicConfig(level=logging.INFO)

    os.makedirs(output_folder, exist_ok=True)

    capture = cv2.VideoCapture(camera_id)

    for key in camera_parameters.keys():

        if camera_parameters_settings[key] is not None:
            original_val = capture.get(camera_parameters[key])
            target_val = camera_parameters_settings[key]
            capture.set(camera_parameters[key], target_val)
            result_val = capture.get(camera_parameters[key])

            logging.info(f"{key}:<<== try to change value")
            logging.info(f"Original : {original_val}")
            if target_val == result_val:
                logging.info(f"Target   : {target_val}")
                logging.info(f"Result   : {result_val}")
            else:
                logging.warning(f"Target   : {target_val}")
                logging.warning(f"Result   : {result_val}")

        else:
            logging.info(f"{key}:{capture.get(camera_parameters[key])}")

    display_usage()

    saved_frame_idx = 0
    while True:

        ret, frame = capture.read()

        if not ret:
            keycode = cv2.waitKey(1) & 0xFF
            if keycode == KeyCodes.esc.value:
                break
            continue

        cv2.imshow("frame", frame)
        keycode = cv2.waitKey(1) & 0xFF
        if keycode == KeyCodes.esc.value:
            break
        elif keycode == KeyCodes.s.value:
            saved_frame_str = str(saved_frame_idx).zfill(10)
            new_filename = os.path.join(output_folder, f"{saved_frame_str}{extention}")
            ret = cvt.imwrite(new_filename, frame)
            if ret:
                logging.info(f"Saved : {new_filename}")
                saved_frame_idx += 1
            else:
                logging.error(f"Cannot save : {new_filename}")
        elif keycode != 255:
            display_usage()

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-folder", help="output folder", type=str, required=True
    )
    parser.add_argument("--camera-id", type=int, default=0)
    parser.add_argument(
        "--extention", type=str, choices=[".jpg", ".png"], default=".jpg"
    )
    parser.add_argument("--mask-range", type=int, nargs="*")
    parser.add_argument("--mask-color-bgr", type=int, default=[0, 255, 255])

    for key in camera_parameters.keys():
        parser.add_argument(f"--{key.lower()}", type=float, default=None)

    args = parser.parse_args()
    camera_parameters_settings = {
        "CAP_PROP_FRAME_WIDTH": args.cap_prop_frame_width,
        "CAP_PROP_FRAME_HEIGHT": args.cap_prop_frame_height,
        "CAP_PROP_FOURCC": args.cap_prop_frame_height,
        "CAP_PROP_BRIGHTNESS": args.cap_prop_brightness,
        "CAP_PROP_CONTRAST": args.cap_prop_contrast,
        "CAP_PROP_SATURATION": args.cap_prop_saturation,
        "CAP_PROP_HUE": args.cap_prop_hue,
        "CAP_PROP_GAIN": args.cap_prop_gain,
        "CAP_PROP_EXPOSURE": args.cap_prop_exposure,
        "CAP_PROP_FPS": args.cap_prop_fps,
        "CAP_PROP_FORMAT": args.cap_prop_format,
        "CAP_PROP_MODE": args.cap_prop_mode,
        "CAP_PROP_CONVERT_RGB": args.cap_prop_convert_rgb,
        "CAP_PROP_GAMMA": args.cap_prop_gamma,
        "CAP_PROP_FOCUS": args.cap_prop_focus,
        "CAP_PROP_PAN": args.cap_prop_pan,
        "CAP_PROP_TILT": args.cap_prop_tilt,
        "CAP_PROP_ROLL": args.cap_prop_roll,
        "CAP_PROP_TEMPERATURE": args.cap_prop_temperature,
        "CAP_PROP_TRIGGER": args.cap_prop_trigger,
        "CAP_PROP_TRIGGER_DELAY": args.cap_prop_trigger_delay,
        "CAP_PROP_SETTINGS": args.cap_prop_settings,
        "CAP_PROP_AUTO_EXPOSURE": args.cap_prop_auto_exposure,
        "CAP_PROP_AUTOFOCUS": args.cap_prop_autofocus,
        "CAP_PROP_AUTO_WB": args.cap_prop_auto_wb,
    }

    main(args.output_folder, args.camera_id, args.extention, camera_parameters_settings)
