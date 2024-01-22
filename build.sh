#! /bin/bash
pip install -r requirements.txt
cd src/automode-eval && maturin build
