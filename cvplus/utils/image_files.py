from __future__ import annotations

import glob
import os

from cvplus import cvt
import cv2
import numpy as np
from typing import Optional


class _ImageFile_Item_:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def __str__(self):
        return self.filepath

    def get_image(self, flags: int = cv2.IMREAD_COLOR, dtype: type = np.uint8):
        self.img = cvt.imread(self.filepath, flags, dtype)


class _ImageFiles_Iter_:
    def __init__(self, all_files: list[str]):
        self.idx = 0
        self.all_files = all_files

    def __next__(self):
        if self.idx >= len(self.all_files):
            raise StopIteration()

        ret = self.all_files[self.idx]
        self.idx += 1
        return _ImageFile_Item_(ret)


class ImageFiles:
    cv2_image_exts = [
        ".jpg",
        ".jpeg",
        ".jp2",
        ".jpe",
        ".png",
        ".gif",
        ".bmp",
        ".dib",
        ".pbm",
        ".pgm",
        ".ppm",
        ".pnm",
        ".sr",
        ".ras",
        ".tiff",
        ".tif",
    ]

    def __iter__(self):
        return _ImageFiles_Iter_(self.all_files)

    def __init__(self, image_files: list[str], recursive=False):
        self.all_files: list[str] = []
        for image_file in image_files:
            if os.path.isdir(image_file):
                if recursive:
                    files = glob.glob(
                        os.path.join(image_file, "**/*.*"), recursive=True
                    )
                else:
                    files = glob.glob(os.path.join(image_file, "*.*"), recursive=False)

                files = [
                    file
                    for file in files
                    if os.path.splitext(file)[1].lower() in self.cv2_image_exts
                ]
                self.all_files += files
            else:
                if os.path.exists(image_file):
                    self.all_files.append(image_file)
        self.idx: int | None = None
        self.prev_idx: int | None = None
        self.img: np.ndarray | None = None

    def get_next_filename(self):
        self.prev_idx = self.idx
        if self.idx is None:
            self.idx = 0
        else:
            self.idx += 1
            self.idx %= len(self.all_files)
        return self.all_files[self.idx]

    def get_prev_filename(self):
        self.prev_idx = self.idx
        if self.idx is None:
            self.idx = len(self.all_files) - 1
        else:
            self.idx -= 1
            if self.idx < 0:
                self.idx = len(self.all_files) - 1
        return self.all_files[self.idx]

    def get_filename(self):
        if self.idx is None:
            self.idx = 0
        return self.all_files[self.idx]

    def get_image(
        self, flags: int = cv2.IMREAD_COLOR, dtype: type = np.uint8
    ) -> Optional[np.ndarray]:

        if self.img is None:
            self.img = cvt.imread(self.get_filename(), flags, dtype)
        elif self.idx != self.prev_idx:
            self.img = cvt.imread(self.get_filename(), flags, dtype)

        return self.img

    def get_next_image(
        self, flags: int = cv2.IMREAD_COLOR, dtype: type = np.uint8
    ) -> (np.ndarray | None):
        self.get_next_filename()
        return self.get_image(flags, dtype)

    def get_prev_image(
        self, flags: int = cv2.IMREAD_COLOR, dtype: type = np.uint8
    ) -> (np.ndarray | None):
        self.get_prev_filename()
        return self.get_image(flags, dtype)

    def get_num_files(self):
        return len(self.all_files)
