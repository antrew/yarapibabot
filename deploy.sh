#!/bin/bash

rsync -rtv \
	--delete \
	--exclude '*.pyc' \
	src/ \
	pi@raspberrypi:yarapibabot/
