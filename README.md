# ads-fetch

A small python script that will fetch data from the [ADS](https://ui.adsabs.harvard.edu/ "astrophysics data system") and save it into a CSV file.

It allows to specify the search term and the fields that should be fetched.

Since it is using https://github.com/andycasey/ads/ I am shamelessly stealing some of his readme that also applies here:

> **Getting Started**
> 
> 1. You'll need an API key from NASA ADS labs. Sign up for the newest version of ADS search at https://ui.adsabs.harvard.edu, visit account settings and generate a new API token. The official documentation is available at https://github.com/adsabs/adsabs-dev-api
> 
> 2. When you get your API key, save it to a file called ``~/.ads/dev_key`` or save it as an environment variable named ``ADS_DEV_KEY``
> 
> 3. From a terminal type ``pip install ads`` (or [if you must](https://stackoverflow.com/questions/3220404/why-use-pip-over-easy-install), use ``easy_install ads``)

## How to use it
```bash
$ python fetch.py --help
usage: fetch.py [-h] [--fields comma separated list] [--sort string]
                [--rows int] [--start int] [--output Path]
                query

Fetches data from ADS for a given search query and stores the supplied fields
in a CSV file

positional arguments:
  query                 the query string

optional arguments:
  -h, --help            show this help message and exit
  --fields comma separated list
                        dict containing the fields to fetch (default: title,
                        author, bibcode)
  --sort string         sort string (e.g. date desc)
  --rows int            number of rows to fetch (default: 200, max: 2000)
  --start int           offset from which to start, pagination, (default: 0)
  --output Path         path to output file, will append if already existing
                        (default: out<datetime>)
```
A list of searchable fields can be found in the [ADS documentation](https://github.com/adsabs/adsabs-dev-api/blob/master/search.md#fields).

So for example if we want the last twenty papers published by A&A we will run something like this:
```bash
$ python fetch.py --output aanda.csv --sort "date desc" --fields title,pubdate,abstract,author,bibcode --rows 20 bibstem:"A&A"
```
This will fetch the fields 
* title
* pubdate
* abstract
* author
* bibcode
and save them in the file `aanda.csv`.

I did not get around to implement the ADS pagination but took the quick and dirty approach which can be seen in the [sample bash script](ads-fetch/get_script.sh).
 

