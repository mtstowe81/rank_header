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
python ./rankheader/main.py --data_path "./data/top-1m.csv"
2021-02-15 19:55:57,518 INFO getting site headers...
2021-02-15 19:56:57,806 INFO --- gather duration: 60.28849720954895
2021-02-15 19:56:57,821 INFO --- site analysis duration: 0.015004158020019531 seconds ---
2021-02-15 19:56:57,821 INFO --- site analysis report: ---
                            result  total
1                     TimeoutError    566
2                          Success    403
3  ClientConnectorCertificateError     14
4             ClientConnectorError     11
5          ClientConnectorSSLError      3
6          ServerDisconnectedError      2
7              ClientResponseError      1
2021-02-15 19:56:57,848 INFO --- header analysis duration: 0.026995182037353516 seconds ---
2021-02-15 19:56:57,849 INFO --- header analysis report: ---
              header  total_site_occurrences  total_occurrences  percent_sites
1               Date                     378                378           37.8
2       Content-Type                     362                362           36.2
3             Server                     330                330           33.0
4         Connection                     304                304           30.4
5      Cache-Control                     266                275           26.6
6     Content-Length                     226                226           22.6
7         Set-Cookie                     205                587           20.5
8               Vary                     198                216           19.8
9   Content-Encoding                     196                196           19.6
10           Expires                     149                150           14.9
2021-02-15 19:56:57,849 INFO --- program duration: 60.3314995765686 seconds ---

```

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