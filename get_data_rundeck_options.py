#!/bin/python

import argparse
import requests
import json
from pprint import pprint

URL_API = "https://api.digitalocean.com/v2/"

parser = argparse.ArgumentParser()
parser.add_argument("-t","--token", required=True, help="Token for Digital Ocean API")
parser.add_argument("-d","--data", required=True, help="Data type for get")
parser.add_argument("-o","--output", required=True, help="Path for create file")
args = parser.parse_args()

headers = {'content-type': 'application/json', 'Authorization': 'Bearer {0}'.format(args.token)}
req = requests.get(URL_API+"/"+args.data + "?per_page=1000", headers=headers)
response = req.json()

output_json = {}
ord = 1
for data in response.get(args.data):
    match args.data:
        case 'regions':
            key = data.get('name')
            value = data.get('slug')
        case 'sizes':
            key = "{:02}".format(ord) + " - {description} | Mem: {memory} Mb | CPUs: {vcpus} | Disk: {vcpus} Gb | Trans: {transfer} Tb/mo | Price: {price_monthly} €/mo".format(**data)
            value = data.get('slug')
            ord += 1
        case 'images':
            key = "{:03}".format(ord) + " - {distribution} | {name}".format(**data)
            value = data.get('slug')
            ord += 1
    output_json[key] = value

f = open(args.output, 'w')
f.write(json.dumps(output_json, indent=2))
