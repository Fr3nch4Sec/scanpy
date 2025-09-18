#!/usr/bin/python3
# help.py

import argparse
import shlex
import sys



def get_parsed_args():
    
    parser = argparse.ArgumentParser(description="Port scanner")
    
    parser.add_argument('-u', required=True, help="ip or hostname (ex: 127.0.0.1 , yoann.org)")
    parser.add_argument('-pS', type=int, default=1, help="start port (default: 1)")
    parser.add_argument('-pE', type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument('-m', choices=['basic', 'advanced', 'concurrent'], default='basic', help="Scan mode: basic (sequential), advanced (threaded), concurrent (pool) (default: basic)")
    parser.add_argument('-b', action='store_true', help="Grab service banners for open ports")
    
    print("Entrer les parametres (ex: -u 127.0.0.1 -pS 1 -pE 1500 -m advanced -b) : 🙈 🙉 🐌 ")
    
    params_str = input().strip()
    
    argv = shlex.split(params_str)
    
    return parser.parse_args(argv)