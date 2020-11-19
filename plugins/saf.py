#! /usr/bin/env python

import os, sys, shutil

os.system("echo %cd%")

class arginfo:
	def __init__(self):
		self.filenames = []

args = arginfo()

def visit(filelist, dirname, names):
	for n in names:
		fullname = dirname + "/" + n
		if os.path.isfile(fullname):
			filelist.append((os.path.getsize(fullname), fullname))

def bundle(src, dst):
	filelist = []

	for fn in src:
		if os.path.isfile(fn):
			filelist.append((os.path.getsize(fn), fn))
			print(fn)
		else:
			os.walk(fn, visit, filelist)

	dfp = open(dst, "wb")

	if not dfp:
		raise "Can't open output file %s" % (dst)

	for f in filelist:
		(sz, fn) = f
		fn = fn.replace("\\", "/")
		dfp.write(f"{sz} {fn}\n".encode())

	dfp.write("-\n".encode())

	for f in filelist:
		(sz, fn) = f
		sfp = open(fn, "rb")
		if not sfp:
			raise "Can't open input file %s" % (fn)
		shutil.copyfileobj(sfp, dfp)
		sfp.close()

	dfp.close()

def parseargs(a):
	usage = "usage: saf.py" + \
	 " <input files> <output file>"
	if len(a) == 0:
		return usage
	while len(a) > 0:
		s = a.pop(0)
		if s == "--help":
			return usage
		elif s[0] == "-":
			return "invalid option '"  + s + "'"
		else:
			args.filenames.append(s)
	if len(args.filenames) < 2:
		return "You must give at least an input and output file"
	return

errormsg = parseargs(sys.argv[1:])
if errormsg:
	sys.stderr.write(errormsg + "\n")
	sys.exit(1)

bundle(args.filenames[0:-1], args.filenames[-1])
