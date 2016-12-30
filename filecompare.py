# -*-coding:utf-8-*-

import os
import os.path
import sys
import platform
import getopt
import hashlib
from color_std_out import *
from getterminalsize import *
def usage():
    print '[ * ] use like "python filecompare.py -s d:/tree -d d:/tree2"'
    print '[ * ] or use like "python filecompare.py --src d:/tree --dst d:/tree2"'

def format_path(path):
	plat_sys=platform.system()
	if plat_sys == "Windows":
		path=path.strip("\\")
	elif plat_sys == "Linux":
		path=path.strip("/")
	return path

def get_tree(rootdir):
	stack=[]
	ret=[]
	stack.append(rootdir)
	while len(stack)>0:
		tmp=stack.pop(len(stack)-1)
		if os.path.isdir(tmp):
			tmp=os.path.normcase(tmp)
			ret.append(format_path(tmp.split(rootdir)[1]))
			for item in os.listdir(tmp):
				stack.append(os.path.join(tmp,item))
			#print tmp
		elif os.path.isfile(tmp):
			tmp=os.path.normcase(tmp)
			ret.append(format_path(tmp.split(rootdir)[1]))
			#print tmp
	return ret

def get_file_hash(file_path):
	if os.path.exists(file_path):
		sha1=hashlib.sha1()
		f=open(file_path,"rb")
		fdata=f.read()
		sha1.update(fdata)
		f.close()
		return sha1.hexdigest()
	else:
		return False


def file_compare(src_path_list, dst_path_list,dst_file_hash_dict):
	for path in src_path_list:
		width,height=getTerminalSize()
		full_path=os.path.join(src,path)
		if os.path.isdir(full_path):
			if path in dst_path_list:
				width=width-12-len(path)
				width="{:>"+str(width)+"}"
				print "[ DIR ] "+path+width.format("[ "),
				printGreen("*")
				print " ]"
				dst_path_list.remove(path)
			elif path not in dst_path_list:
				width=width-12-len(path)
				width="{:>"+str(width)+"}"
				print "[ DIR ] "+path+width.format("[ "),
				printBlue("+")
				print " ]"
		elif os.path.isfile(full_path):
			cur_file_sha1=get_file_hash(full_path)
			if cur_file_sha1 in dst_file_hash_dict.keys():
				if path==dst_file_hash_dict[cur_file_sha1]:
					width=width-13-len(path)
					width="{:>"+str(width)+"}"
					print "[ FILE ] "+path+width.format("[ "),
					printGreen("*")
					print " ]"
					dst_path_list.remove(path)
				else:
					width=width-24-len(path)-len(dst_file_hash_dict[cur_file_sha1])
					width="{:>"+str(width)+"}"
					print "[ FILE ] %s moved to %s" % (path,dst_file_hash_dict[cur_file_sha1]),
					print width.format("[ "),
					printSkyBlue(">")
					print " ]"
					dst_path_list.remove(dst_file_hash_dict[cur_file_sha1])
			elif path in dst_file_hash_dict.values():
				width=width-13-len(path)
				width="{:>"+str(width)+"}"
				print "[ FILE ] "+path+width.format("[ "),
				printYellow("m")
				print " ]"
				dst_path_list.remove(path)
			else:
				width=width-13-len(path)
				width="{:>"+str(width)+"}"
				print "[ FILE ] "+path+width.format("[ "),
				printBlue("+")
				print " ]"
		else:
			pass
	if dst_path_list:
		for path in dst_path_list:
			width,height=getTerminalSize()
			width=width-13-len(path)
			width="{:>"+str(width)+"}"
			print "[ FILE ] "+path+width.format("[ "),
			printRed("-")
			print " ]"

opts, args = getopt.getopt(sys.argv[1:], "hs:d:", ["help", "src=", "dst="])
if not opts:
    usage()
src=""
dst=""
for op, value in opts:
    if op == "-s" or op == "--src":
        src = value
        if not os.path.exists(src):
            print '[ * ] path "%s" does not exist,please check the param "-s"' % (src)
            sys.exit()
        else:
            src = os.path.normcase(src)
            src=src.rstrip("\\")
    elif op == "-d" or op == "--dst":
        dst = value
        if not os.path.exists(dst):
            print '[ * ] path "%s" does not exist,please check the param "-d"' % (dst)
            sys.exit()
        else:
            dst = os.path.normcase(dst)
            dst=dst.rstrip("\\")
    else:
        usage()
        sys.exit()

src_path_list=get_tree(src)
dst_path_list=get_tree(dst)
src_path_list.remove('')
dst_path_list.remove('')
dst_file_hash_dict={}
print dst
for item in dst_path_list:
	full_path=os.path.join(dst,item)
	if os.path.isfile(full_path):
		dst_file_hash_dict[get_file_hash(full_path)]=item
	else:
		pass
file_compare(src_path_list, dst_path_list,dst_file_hash_dict)
print dst_path_list