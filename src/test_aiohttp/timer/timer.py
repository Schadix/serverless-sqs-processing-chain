# Copyright (c) 2017-present, Facebook, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################
#
# Based on:
# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""Timing related functions."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time

# TODO: generalize and make annotation
# TODO: use ndarray and get the mean, median, p99 etc from the data. Sometimes the first inference run takes longer, but subsequent ones are much faster. Format: time_taken diff (tic/toc)
class Timer(object):
    """A simple timer.
    You have to call .tic() to start a timing sessions which can then have multiple .toc()
    """

    def __init__(self):
        self.total_time = 0.
        self.calls = 0
        self.start_time = 0.
        self.diff = 0.
        self.average_time = 0.

    def tic(self):
        # using time.time instead of time.clock because time time.clock
        # does not normalize for multithreading
        self.start_time = time.time()
        self.last_toc = self.start_time

    # FIXME: add interval function, return diff between toc's, not only diff between now and start_time
    def toc(self, average=True):
        if not self.start_time:
            raise Exception('from timer, have to tic before toc.')
        now = time.time()
        last_toc_diff = now - self.last_toc
        self.last_toc = now
        self.diff = now - self.start_time
        self.total_time += last_toc_diff
        self.calls += 1
        self.average_time = self.total_time / self.calls
        if average:
            return self.average_time
        else:
            return self.diff

    def reset(self):
        self.total_time = 0.
        self.calls = 0
        self.start_time = 0.
        self.diff = 0.
        self.average_time = 0.

    def __str__(self):
        return "total_time: {:.2f} s, calls: {:.0f}, start_time: {}, diff: {:.4f} s, average_time: {:.4f} s".format(
            self.total_time, self.calls, time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime(self.start_time)), self.diff, self.average_time)
