# csv2dita
Convert CSV files to DITA tables

`-t` accepts either `simple` for simple tables or `normal` for normal
tables. Use the `--header` option to convert the first line of the CSV into
the table header. Note, however, that no values may have internal commas.

After running, copy and paste the output into your favorite DITA editor.

## Setup

1. [Install Python 2.7](https://www.python.org/download/releases/2.7.8/)

2. [Install
BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup).

3. `git clone https://github.com/tintinno/csv2dita`

4. `cd csv2dita`


## Usage

```
C:\Users\tintinno\csv2dita>python csv2dita.py -h
usage: csv2dita.py [-h] [-i CSV] [-o DITA] [-t {normal,simple}] [--header]

Convert CSV files to DITA tables.

optional arguments:
  -h, --help          show this help message and exit
  -i CSV              input file
  -o DITA             output file
  -t {normal,simple}  DITA table type
  --header            use 1st row as table header
```

## Example

The example below converts a file named `start.csv` to DITA normal tables,
using the first line of the CSV as the table header, and saves it as 
`start.txt`. 

```
C:\Users\tintinno\csv2dita>python csv2dita.py -i start.csv -o start.txt -t normal --header
```
