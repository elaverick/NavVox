#!/usr/bin/env bash

cd waze-voicepack-links
git pull origin main
cd ..
git add waze-voicepack-links
git commit -m "Update waze-voicepack-links submodule"