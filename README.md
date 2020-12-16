# Top site header analyzer

## Introduction

This tool is designed to obtain a set of sites from a specified site file and determine which headers appear the most.

## Building and Running

Building, running tests, and executing this tool may be performed from the provided make file.

```
make virtualenv                 # create virtualenv
source env/Scripts/activate     # optionally set virtualenv in your shell
make init                       # install requirements.txt into virtualenv
make test                       # run `pytest tests`
make run                        # finds and runs `main.py` in the `src` directory 
```

## Inputs

Download the following CSV file: http://s3.amazonaws.com/alexa-static/top-1m.csv.zip

This file can be placed in the /data folder and input into the script.

## Advanced command line usage

```
usage: main.py [-h] [--data_path DATA_PATH] [--num_headers NUM_HEADERS]
               [--num_sites NUM_SITES] [--display_graph {True,False}]
               [--http_concurrency HTTP_CONCURRENCY]
               [--http_timeout HTTP_TIMEOUT]

Calculate top 10 header stats

optional arguments:
  -h, --help            show this help message and exit
  --data_path DATA_PATH
                        Path to data file (top-1m.csv) (default:
                        ../data/top-1m.csv)
  --num_headers NUM_HEADERS     Number of headers to take as top rank (default: 10)
  --num_sites NUM_SITES
                        Number of sites to analyze (default: 1000)
  --display_graph {True,False}
                        Display the graph (default: True)
  --http_concurrency HTTP_CONCURRENCY
                        Number of concurrent requests (default: 20)
  --http_timeout HTTP_TIMEOUT
                        Request timeout (sec) (default: 30)

```

## Output

The tool logs all details to the standard output.

```
$ python main.py
2020-09-27 18:49:27,115 INFO getting site headers...
...
2020-09-27 18:56:06,227 INFO received 1000 results from sites
2020-09-27 18:56:06,227 INFO getting site headers stats...
2020-09-27 18:56:06,242 INFO calculating top headers stats...
2020-09-27 18:56:06,243 INFO rank: 1 | header=Content-Type | total_occurrences=965 | total_site_occurrences=963 | percent_site_occurrences=96.3
2020-09-27 18:56:06,243 INFO rank: 2 | header=Date | total_occurrences=922 | total_site_occurrences=922 | percent_site_occurrences=92.2
2020-09-27 18:56:06,243 INFO rank: 3 | header=Content-Encoding | total_occurrences=815 | total_site_occurrences=815 | percent_site_occurrences=81.5
2020-09-27 18:56:06,243 INFO rank: 4 | header=Server | total_occurrences=803 | total_site_occurrences=802 | percent_site_occurrences=80.2
2020-09-27 18:56:06,243 INFO rank: 5 | header=Connection | total_occurrences=809 | total_site_occurrences=764 | percent_site_occurrences=76.4
2020-09-27 18:56:06,243 INFO rank: 6 | header=Cache-Control | total_occurrences=742 | total_site_occurrences=729 | percent_site_occurrences=72.89999999999999
2020-09-27 18:56:06,243 INFO rank: 7 | header=Vary | total_occurrences=703 | total_site_occurrences=663 | percent_site_occurrences=66.3
2020-09-27 18:56:06,243 INFO rank: 8 | header=Transfer-Encoding | total_occurrences=524 | total_site_occurrences=524 | percent_site_occurrences=52.400000000000006
2020-09-27 18:56:06,243 INFO rank: 9 | header=Set-Cookie | total_occurrences=1480 | total_site_occurrences=483 | percent_site_occurrences=48.3
2020-09-27 18:56:06,243 INFO rank: 10 | header=Content-Length | total_occurrences=437 | total_site_occurrences=437 | percent_site_occurrences=43.7
2020-09-27 18:56:06,244 INFO --- analysis duration: 399.1310975551605 seconds ---
2020-09-27 18:56:27,248 INFO --- program duration: 420.1345977783203 seconds ---
```

## Graphs

At the conclusion of the analysis the tool will present a visualization of the results.

![Report](/images/Figure_1.png)

## Tests

Unit and integration tests may be executed by running:
```
/rankheader/pytest ./tests/
```

Sample output:
```
$ pytest ./test/
============================= test session starts =============================
platform win32 -- Python 3.7.8, pytest-6.1.0, py-1.9.0, pluggy-0.13.1
rootdir: \rankheader
plugins: asyncio-0.14.0
collected 4 items

test\test_integration.py .                                               [ 25%]
test\test_siteinfoanalyzer.py .                                          [ 50%]
test\test_siteinfocollector.py ..                                        [100%]

============================== 4 passed in 2.74s ==============================
```