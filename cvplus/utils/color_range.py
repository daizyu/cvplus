from __future__ import annotations

import numpy as np


class ColorRange:
    def __init__(self, start_range: np.ndarray):
        self.start_range = start_range
        self._reset()

    def _reset(self):
        self.lowers = np.vstack(self.start_range[:3].reshape([1, 3]))
        self.uppers = np.vstack(self.start_range[3:].reshape([1, 3]))

    def get_prev(self) -> list[np.ndarray]:
        prev_lower = self.lowers[-1]
        prev_upper = self.uppers[-1]
        return [prev_lower, prev_upper]

    def mod_lower(self, idx: int, offset: int):
        assert 0 <= idx <= 2
        prev_lower, prev_upper = self.get_prev()
        new_lower = prev_lower.copy()
        new_lower[idx] = new_lower[idx] + offset
        new_lower = np.max([np.array([0, 0, 0]), new_lower], axis=0)
        if np.any([prev_lower != new_lower]) and np.all(prev_upper > new_lower):
            self.lowers = np.vstack([self.lowers, new_lower])
            self.uppers = np.vstack([self.uppers, prev_upper])
        return self.get_prev()

    def mod_upper(self, idx: int, offset: int):
        assert 0 <= idx <= 2
        prev_lower, prev_upper = self.get_prev()
        new_upper = prev_upper.copy()
        new_upper[idx] = new_upper[idx] + offset
        new_upper = np.min([np.array([255, 255, 255]), new_upper], axis=0)
        if np.any([prev_lower != new_upper]) and np.all(prev_lower < new_upper):
            self.lowers = np.vstack([self.lowers, prev_lower])
            self.uppers = np.vstack([self.uppers, new_upper])
        return self.get_prev()

    def has(self):
        lower, upper = self.get_prev()

        if np.all(lower < upper):
            return True
        return False

    def remove_last(self):
        if self.lowers.shape[0] <= 1:
            return
        self.lowers = self.lowers[:-1]
        self.uppers = self.uppers[:-1]
        return

    def history_length(self):
        return self.lowers.shape[0]

    def update(self, lst: list[int]) -> list[np.ndarray]:
        assert len(lst) == 3
        ary = np.array(lst, np.float32)

        prev_lower, prev_upper = self.get_prev()

        new_lower = np.min([ary, prev_lower], axis=0)

        new_upper = np.max([ary, prev_upper], axis=0)

        if self.history_length() == 1:
            new_lower = new_lower - np.array([1, 1, 1])
            new_lower = np.max([new_lower, np.array([0, 0, 0])], axis=0)
            new_upper = new_upper + np.array([1, 1, 1])
            new_upper = np.min([new_upper, np.array([255, 255, 255])], axis=0)
            self.lowers = np.vstack([self.lowers, new_lower])
            self.uppers = np.vstack([self.uppers, new_upper])

        elif np.any(prev_lower != new_lower) or np.any(prev_upper != new_upper):
            self.lowers = np.vstack([self.lowers, new_lower])
            self.uppers = np.vstack([self.uppers, new_upper])

        return self.get_prev()


if __name__ == "__main__":
    color_range = ColorRange(np.array([255, 255, 255, 0, 0, 0]))
    print(color_range.history_length())
    color_range.update([200, 30, 23])
    print(color_range.get_prev())
    color_range.mod_lower(1, -4)
    print(color_range.get_prev())
    color_range.mod_lower(1, -30)
    print(color_range.get_prev())
    color_range.mod_lower(0, 30)
    print(color_range.get_prev())
    color_range.mod_upper(0, -30)
    print(color_range.get_prev())
    color_range.mod_upper(2, -1)
    print(color_range.get_prev())
