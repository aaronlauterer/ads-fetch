#!/usr/bin/env bash
set -e
set -x

continue=true
offset=0
rows=2000
file=data/output.csv
script="python bin/fetch.py"


while ${continue}; do
	python bin/fetch.py --output ${file} --sort "date desc" --fields title,pubdate,abstract,author,bibcode bibstem:"A&A" --start ${offset} --rows ${rows}
	if (($? == 0)); then
		offset=$((offset+rows))
	fi
	if (($? > 0)); then
		continue=false	
	fi
done
