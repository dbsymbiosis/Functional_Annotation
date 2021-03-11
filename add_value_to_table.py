#!/usr/bin/env python2
DESCRIPTION = '''
add_value_to_table - Will add values into a table (via a new end column)
                     given key:value pairs. 

NOTE:
	- Ignore comment ('#' by defult; can be turned off) and blank lines	
	- Uses exact string matching. Can not do regex or partial matching
	- Assumes first column is 'key' and collowing column/s are 'value'
	- Assumes key is unique in -a/--add; if not unique will take the last value and print warning.
	- Will always add 'blank' values if target column not in key:value pairs.
'''
import sys
import os
import argparse
import gzip
import logging

VERSION=0.1

## Pass arguments.
def main():
	# Pass command line arguments. 
	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=DESCRIPTION)
	parser.add_argument('-i', '--input', metavar='data_file.txt', 
		required=False, default=sys.stdin, type=lambda x: __parse_file_check_compression(x, 'r'), 
		help='Input [gzip] file (default: stdin)'
	)
	parser.add_argument('-o', '--output', metavar='data_file_with_extra_column.txt', 
		required=False, default=sys.stdout, type=lambda x: __parse_file_check_compression(x, 'w'), 
		help='Output [gzip] file (default: stdout)'
	)
	parser.add_argument('-a', '--add', metavar='info_to_add.txt', 
		required=True, type=lambda x: __parse_file_check_compression(x, 'r'), 
		help='Input [gzip] key:value pairs'
	)
	parser.add_argument('-c', '--col', 
		required=False, default=1, type=int, 
		help='Column in --input of interest'
	)
	parser.add_argument('-d', '--default', 
		required=False, default='', type=str, 
		help='Value to add if not in -a/--add (default: %(default)s)'
	)
	parser.add_argument('--delim_input', 
		required=False, default='\t', type=str, 
		help='Delimiter for --input (default: \\t)'
	)
	parser.add_argument('--delim_add', 
		required=False, default='\t', type=str, 
		help='Delimiter for --add (default: \\t)'
	)
	parser.add_argument('--keep_comments', 
		required=False, action='store_true', 
		help='Keep comment lines from input file in output file (default: %(default)s)'
	)
	parser.add_argument('--debug', 
		required=False, action='store_true',  
		help='Print DEBUG info (default: %(default)s)'
	)
	args = parser.parse_args()
	
	# Set up basic debugger
	logFormat = "[%(levelname)s]: %(message)s"
	logging.basicConfig(format=logFormat, stream=sys.stderr, level=logging.INFO)
	if args.debug:
		logging.getLogger().setLevel(logging.DEBUG)
	
	logging.debug('%s', args) ## DEBUG
	
	info2add = load_key_value_from_file(args.add, args.delim_add)
	args.add.close()
	
	# For each line in input file
	for line in args.input:
		line = line.strip('\n')
		if not line:
			continue
		
		if line.startswith('#'):
			if args.keep_comments:
				args.output.write(line + '\n')
			continue
		
		line_sep = line.split(args.delim_input)
		
		try:
			key = line_sep[args.col-1]
			if key in info2add.keys():
				args.output.write(line + args.delim_input + info2add[key] + '\n')
				logging.debug('Value added: %s:%s', key, info2add[key]) ## DEBUG
			else:
				args.output.write(line + args.delim_input + args.default + '\n')
				logging.debug('Default added: %s', args.default) ## DEBUG
		except IndexError:
			logging.info("[ERROR]: %s", line)
			logging.info("[ERROR]: -c/--col %s out of range for --infile", args.col)
			sys.exit(1)
	
	args.input.close()
	args.output.close()



def load_key_value_from_file(keyvalue_file, delim):
	'''
	Loads a dict of key:value pairs to add to table.
	'''
	info2add = {}
	ids_seen = []
	for line in keyvalue_file:
		line = line.strip()
		if not line or line.startswith('#'):
			continue
		line_split = line.split(delim)
		
		key = line_split[0]
		if key in ids_seen:
			logging.info('[WARNING]: %s occurs multiple times - taking latest entry.', key) ## DEBUG
		ids_seen.append(key)
		
		info2add[key] = delim.join(line_split[1:])
	
	
	logging.debug('Pairs: %s', info2add) ## DEBUG
	logging.debug('Number of keys loaded: %s', len(info2add.keys())) ## DEBUG
	return info2add



def __parse_file_check_compression(fh, mode='r'):
	'''
	Open stdin/normal/gzip files - check file exists (if mode='r') and open using appropriate function.
	'''
	# Check file exists if mode='r'
	if not os.path.exists(fh) and mode == 'r':
		raise argparse.ArgumentTypeError("The file %s does not exist!" % fh)
	
	## open with gzip if it has the *.gz extension, else open normally (including stdin)
	try:
		if fh.endswith(".gz"):
			return gzip.open(fh, mode+'b')
		else:
			return open(fh, mode)
	except IOError as e:
		raise argparse.ArgumentTypeError('%s' % e)



if __name__ == '__main__':
	main()
