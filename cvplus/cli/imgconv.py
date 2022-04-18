from __future__ import annotations

import argparse
import pathlib
import cv2
from cvplus import cvt
import tqdm
from typing import Optional
from cvplus.utils.image_files import ImageFiles
from enum import IntEnum, auto


class Mode(IntEnum):
    error = auto()
    none = auto()
    base_scale = auto()
    base_width = auto()
    base_height = auto()
    base_fixed_size = auto()


def main(
    input_folder: str,
    output_folder: str,
    recursive: bool,
    fixed_width: Optional[int],
    fixed_height: Optional[int],
    scale: Optional[float],
    extension: Optional[str],
):
    mode = Mode.error
    if fixed_width is None and fixed_height is None and scale is None:
        mode = Mode.none
    elif fixed_width is None and fixed_height is None and scale is not None:
        mode = Mode.base_scale
    elif fixed_width is not None and scale is not None:
        raise Exception("You can select only fixed-width or scale")
    elif fixed_height is not None and scale is not None:
        raise Exception("You can select only fixed-height or scale")
    elif fixed_width is not None and fixed_height is not None:
        mode = Mode.base_fixed_size
    elif fixed_width is not None:
        mode = Mode.base_width
    elif fixed_height is not None:
        mode = Mode.base_height
    if mode is Mode.error:
        raise Exception("Resize option is failed")

    image_files = ImageFiles([input_folder], recursive=recursive)

    input_base_path = pathlib.Path(input_folder)
    output_base_path = pathlib.Path(output_folder)

    try:
        assert (
            str(input_base_path.relative_to(output_base_path)) != "."
        ), "input-folder and output-folder should be different"
    except:  # noqa: E722
        pass

    src_paths = []
    dest_paths = []

    for input_image_file in image_files:
        input_src_image_path = pathlib.Path(str(input_image_file))
        input_rel_path = input_src_image_path.relative_to(input_base_path)
        output_dest_image_path = output_base_path.joinpath(
            output_base_path, input_rel_path
        )

        if extension is not None:
            output_dest_image_path = output_dest_image_path.with_suffix(extension)

        if recursive:
            try:
                output_dest_image_path.relative_to(input_base_path)
            except ValueError:
                pass
            else:
                raise Exception("output folder overwrapping with input folder")

        src_paths.append(input_src_image_path)
        dest_paths.append(output_dest_image_path)

        for idx in tqdm.tqdm(range(len(src_paths))):
            src_path: pathlib.Path = src_paths[idx]
            dest_path: pathlib.Path = dest_paths[idx]
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            img: cv2.Mat = cvt.imread(src_path)

            new_img: cv2.Mat = None
            if mode is Mode.none:
                new_img = img
            elif mode is Mode.base_scale:
                h, w = img.shape[:2]
                new_h = int(h * scale)
                new_w = int(w * scale)
                new_img = cv2.resize(img, (new_w, new_h))
            elif mode is Mode.base_width:
                h, w = img.shape[:2]
                scale = fixed_width / w
                new_h = int(h * scale)
                new_img = cv2.resize(img, (fixed_width, new_h))
            elif mode is Mode.base_height:
                h, w = img.shape[:2]
                scale = fixed_height / h
                new_w = int(w * scale)
                new_img = cv2.resize(img, (new_w, fixed_height))
            elif mode is Mode.base_fixed_size:
                print(fixed_width, fixed_height)
                new_img = cv2.resize(img, (fixed_width, fixed_height))
            else:
                raise NotImplementedError(f"Mode is not recognized:{mode}")

            if new_img is not None:
                cvt.imwrite(dest_path, new_img)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input-folder", help="input folder", type=str, required=True)
    parser.add_argument(
        "--output-folder", help="output folder", type=str, required=True
    )
    parser.add_argument(
        "--recursive", help="search folder deeply", type=bool, default=False
    )
    parser.add_argument("--fixed-width", type=int)
    parser.add_argument("--fixed-height", type=int)
    parser.add_argument("--scale", type=float)
    parser.add_argument("--extension", type=str, choices=[".jpg", ".png"])

    args = parser.parse_args()

    main(
        args.input_folder,
        args.output_folder,
        args.recursive,
        args.fixed_width,
        args.fixed_height,
        args.scale,
        args.extension,
    )
