#!/bin/sh
pyro4-ns & (sleep 1 && (python pyro_mcp23017.py & python pyro_bmp180.py)) & (sleep 2 && ./run.py) & (sleep 3 && ./flask/bin/python updater.py)
