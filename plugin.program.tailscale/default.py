#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import xbmcaddon
import xbmcgui

from resources.lib.addon import TailscaleAddon

if __name__ == '__main__':
    addon = TailscaleAddon()
    addon.run()
