#!/bin/bash

rsync -rtv \
	--delete \
	--exclude '*.pyc' \
	--exclude 'override.ini' \
	src/ \
	pi@raspberrypi:yarapibabot/
