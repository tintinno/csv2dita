#!/usr/bin/python

# convert CSV files to DITA tables

import argparse

try:
	from bs4 import BeautifulSoup
except ImportError:
	print "Install BeautifulSoup:\n  sudo pip install beautifulsoup4"
	raise SystemExit(1)

p = argparse.ArgumentParser(description="Convert CSV files to DITA tables.")
p.add_argument('-i', action="store", dest="csv", help='input file')
p.add_argument('-o', action="store", dest="dita", help='output file')
p.add_argument('-t', action="store", dest="table", nargs=1, 
              help='DITA table type', choices=['normal','simple'])
p.add_argument('--header', action="store_true", 
              help='use 1st row as table header')

args = p.parse_args()

if not args.table:
	raise SystemExit("Missing -t option. See -h for help.")
elif args.table[0] == 'simple':
	table = "<simpletable><strow></strow></simpletable>"
elif args.table[0] == 'normal':
	table = "<table><tgroup><tbody></tbody></tgroup></table>"
else:
	raise SystemExit("Some weird, impossible error.")

soup = BeautifulSoup(table,"html.parser")

# open input file
with open(args.csv,'r') as f:
	csv = f.readlines()

# beautifulsoup functions 
def build_entry(tag,value,number):
	entry = soup.new_tag(tag)
	if args.table[0] == 'normal':
		entry['colname'] = number
	entry.string = value
	return entry

def build_row(row_tag,entry_tag,entries):
	row = soup.new_tag(row_tag)
	for number,item in enumerate(entries.split(',')):
		item = item.strip()
		entry = build_entry(entry_tag,item,number + 1)
		row.insert(number, entry)
	return row

def build_colspec(number):
	colspec = soup.new_tag('colspec')
	colspec['colnum'] = number
	colspec['colname'] = 'col' + str(number)
	colspec['colwidth'] = "*"
	return colspec

def build_header(header_tag,row_tag,entry_tag,entries):
	header = soup.new_tag(header_tag)
	header_row = build_row(row_tag,entry_tag,entries)
	header.insert(0,header_row)
	return header


# get the number of columns this table will have
COLUMNS = csv[0].count(',') + 1

# Normal tables
if args.table[0] == 'normal':

	# tgroup and colspec elements 
	soup.tgroup['cols'] = COLUMNS
	count = 1
	while count <= COLUMNS:
		colspec = build_colspec(count)
		soup.tgroup.insert(count - 1, colspec)
		count += 1

	# test whether we need to make a <thead> element
	if args.header:
		header = build_header('thead','row','entry',csv[0])
		soup.tbody.insert_before(header)
		csv.pop(0)

	# make the tbody element
	for number,line in enumerate(csv):
		row = build_row('row','entry',line)
		soup.tbody.insert(number,row)

# Simple tables
elif args.table[0] == 'simple':

	# make the body elements
	for number,line in enumerate(csv):
		row = build_row('strow','stentry',line)
		soup.simpletable.insert(number,row)

	# if simpletables, we'll just change the fist strow to sthead
	if args.header:
		soup.simpletable.strow.name = 'sthead'

else:
	raise SystemExit('Crap.')

# save to output file
with open(args.dita,'w') as out:
	out.write(str(soup) + '\n')
