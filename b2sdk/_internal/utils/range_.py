######################################################################
#
# File: b2sdk/_internal/utils/range_.py
#
# Copyright 2020 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################
from __future__ import annotations

import dataclasses


@dataclasses.dataclass(eq=True, order=True)
class Range:
    """
    HTTP ranges use an *inclusive* index at the end.
    """
    __slots__ = ['start', 'end']

    start: int
    end: int

    def __post_init__(self):
        assert 0 <= self.start <= self.end

    @classmethod
    def from_header(cls, raw_range_header: str) -> Range:
        """
        Factory method which returns an object constructed from Range http header.

        raw_range_header example: 'bytes=0-11'
        """
        offsets = tuple(
            int(i) for i in raw_range_header.replace('bytes', '').strip('= ').split('-')
        )
        return cls(*offsets)

    def size(self) -> int:
        return self.end - self.start + 1

    def subrange(self, sub_start, sub_end) -> Range:
        """
        Return a range that is part of this range.

        :param sub_start: index relative to the start of this range.
        :param sub_end: (Inclusive!) index relative to the start of this range.
        :return: a new Range
        """
        assert 0 <= sub_start <= sub_end < self.size()
        return self.__class__(self.start + sub_start, self.start + sub_end)

    def as_tuple(self) -> tuple[int, int]:
        return self.start, self.end

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.start}, {self.end})'
