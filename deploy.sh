#!/bin/bash

rsync -rtv \
	src/ \
	pi@raspberrypi:yarapibabot/
