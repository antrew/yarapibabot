#!/bin/bash

set -e
set -u

source deploy.settings

rsync -rtv \
	--delete \
	--exclude '*.pyc' \
	--exclude 'override.ini' \
	src/ \
	pi@$PI_HOSTNAME:yarapibabot/
