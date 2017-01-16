import argparse
import ads
import time
import unicodecsv as csv
import numbers
import os.path
import sys


def fetch():
    parser = argparse.ArgumentParser(description='Fetches data from ADS for a given search query and stores the supplied fields in a CSV file')
    parser.add_argument('query', help='the query string')
    parser.add_argument('--fields', metavar='comma separated list', default=['title', 'author', 'bibcode'], help='dict containing the fields to fetch (default: title, author, bibcode)')
    parser.add_argument('--sort', metavar='string', help='sort string (e.g. date desc)')
    parser.add_argument('--rows', metavar='int', type=int, default=200, help='number of rows to fetch (default: 200, max: 2000)')
    parser.add_argument('--start', metavar='int', type=int, default=0, help='offset from which to start, pagination, (default: 0)')
    parser.add_argument('--output', metavar='Path', dest='outfile', default='out' + time.strftime('%Y%m%d-%H%M'), help='path to output file, will append if already existing (default: out<datetime>)')

    args = parser.parse_args()

    # if args.fields is not a list we don't have the default value, therefore split the string to get a list
    if type(args.fields) is not list:
        args.fields = args.fields.split(',')

    # create the ADS query object
    q = ads.SearchQuery(q=args.query, fl=args.fields, rows=args.rows, start=args.start)

    # we will add this later ourselves to the paper object
    args.fields.append('timestamp')

    if os.path.isfile(args.outfile):
        # append
        writemode = 'ab'
    else:
        # new file
        writemode = 'wb'

    try:
        writer = csv.DictWriter(open(args.outfile, writemode), delimiter='|', fieldnames=args.fields)
        if writemode == 'wb':
            writer.writeheader()
    except OSError as err:
        print("OS error: {0}".format(err))

    current_time = time.time()

    try:
        for paper in q:
            paper.timestamp = current_time
            current_paper = {}

            for field in args.fields:
                attr = getattr(paper, field)
                if isinstance(attr, (str, numbers.Number, type(None))):
                    current_paper[field] = str(attr)
                else:
                    # if attr is none of the above we assume it a list like object -> we join it together
                    current_paper[field] = ';'.join(attr)

            writer.writerow(current_paper)
    except IndexError:
        sys.exit("Empty search result!")

    print(
"""---- Done ----
Meta info:
----------""")
    print("Limit: " + q.response.get_ratelimits()['limit'])
    print("Remaining: " + q.response.get_ratelimits()['remaining'])
    print("Reset at: " + time.ctime(int(q.response.get_ratelimits()['reset'])))
    print("----------")

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    import sys
    fetch()
