import sys
import os
import ConfigParser
import time

env = ConfigParser.RawConfigParser()
env.read('C:/Users/Przemek/Desktop/arqonia/backend/resources/env.properties')
rest = env.get('Backend', 'catalog.rest');

fn = open(rest+'jsonBuilder.py', 'a')
fn.write(" ")
fn.seek(-1, os.SEEK_END)
fn.truncate()
fn.close()