import argparse
import datetime
import json
from typing import Optional, Union, List

import requests


def attempt_post(token: str, where: str, expected: Union[int, List[int]], params: Optional[dict] = None,
                 data: Optional[str] = None) -> Union[dict, bool]:
    if type(expected) is int:
        legal: List[int] = [expected]
    else:
        legal: List[int] = expected

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    print("POST =>", where, "params:", params, "json:", data)

    response = requests.post(where, params=params, data=data, headers=headers, verify=False)

    if response.status_code not in legal:
        print("Unexpected response", response.status_code, "received (vs ", ",".join([str(l) for l in legal]), ") for",
              where)
        print(response.content)
        raise RuntimeError("see log")

    if response.status_code == 204:
        print("=>", response.status_code)
    else:
        print("=>", response.status_code, response.json())

    if response.status_code == 204:
        return True
    else:
        return response.json()


def add_demo(token: str, host: str, no_approve: bool):
    """Add sample data to the database."""

    print("Registering user")
    user = attempt_post(token, host + "/users:register", [201, 409])

    # Sites
    virtualbox = {
        "name": "VirtualboxTestbed",
        "address": '127.0.0.1',
        "flavors": [
            {"name": "virtualbox-arch"}
        ]
    }
    cesga = {
        "name": 'CESGA',
        "address": 'unknown',
        "flavors": [
            {"name": "cor1mem2h10"},
            {"name": "cor2mem2hd20"},
            {"name": "cor4mem4hd40"}
        ]
    }
    cesnet = {
        "name": 'CESNET-MCC',
        "address": 'unknown',
        "flavors": [
            {"name": "standard.small"},
            {"name": "standard.medium"},
            {"name": "standard.large"},
            {"name": "hpc.8core-16ram"}
        ]
    }
    ifca = {
        "name": 'IFCA-LCG2',
        "address": 'unknown',
        "flavors": [
            {"name": "m1.small"},
            {"name": "cm4.large"},
            {"name": "m1.large"},
            {"name": "m1.xlarge"},
            {"name": "cm4.4xlarge"}
        ]
    }
    iisas = {
        "name": 'IISAS-FedCloud',
        "address": 'unknown',
        "flavors": [
            {"name": "m1.small"},
            {"name": "m1.medium"},
            {"name": "m1.large"},
            {"name": "m1.xlarge"}
        ]
    }
    ingrid = {
        "name": 'NCG-INGRID-PT',
        "address": 'unknown',
        "flavors": [
            {"name": "svc1.s"},
            {"name": "svc2.s"},
            {"name": "svc2.m"},
            {"name": "svc2.l"},
            {"name": "svc2.xl"},
            {"name": "svc2.xxl"}
        ]
    }

    site_metas = [
        virtualbox,
        cesga,
        cesnet,
        ifca,
        iisas,
        ingrid
    ]

    # Create sites
    for site_meta in site_metas:
        site = attempt_post(token, host + "/sites", expected=201, data=json.dumps({
            "name": site_meta["name"],
            "address": site_meta["address"]
        }))
        if not no_approve:
            attempt_post(token, host + "/sites/" + site["id"] + ":approve", expected=204)

        site_meta["id"] = site["id"]

        # Create flavors for each site
        for flavor_meta in site_meta["flavors"]:
            flavor = attempt_post(token, host + "/sites/" + site["id"] + "/flavors", expected=201, data=json.dumps({
                "name": flavor_meta["name"],
                "description": ""
            }))
            if not no_approve:
                attempt_post(token, host + "/flavors/" + flavor["id"] + ":approve",
                             expected=204)
            flavor_meta["id"] = flavor["id"]

    # Create benchmark
    with open('sample_data/template.json') as file:
        # the benchmark is real
        benchmark = attempt_post(token, host + "/benchmarks", expected=201, data=json.dumps({
            "docker_image": "thechristophe/openbench-c-ray",
            "docker_tag": "latest",
            "description": "Compare cpu perf with multithreaded raytracing",
            "json_schema": json.loads(file.read())
        }))
        if not no_approve:
            approval = attempt_post(token, host + "/benchmarks/" + benchmark["id"] + ":approve", expected=204)

    if no_approve:
        return
    # Create results
    results = [
        {'site': virtualbox, 'flavor': virtualbox["flavors"][0], 'file': 'result-1.json'},
        {'site': virtualbox, 'flavor': virtualbox["flavors"][0], 'file': 'result-2.json'},
        {'site': virtualbox, 'flavor': virtualbox["flavors"][0], 'file': 'result-4.json'},
        {'site': virtualbox, 'flavor': virtualbox["flavors"][0], 'file': 'result-8.json'},
        {'site': virtualbox, 'flavor': virtualbox["flavors"][0], 'file': 'result-12.json'},
        {'site': cesga, 'flavor': cesga["flavors"][0], 'file': 'c-ray/cesga-1.json'},
        {'site': cesnet, 'flavor': cesnet["flavors"][0], 'file': 'c-ray/cesnet-mcc-1.json'},
        {'site': cesnet, 'flavor': cesnet["flavors"][1], 'file': 'c-ray/cesnet-mcc-2.json'},
        {'site': cesnet, 'flavor': cesnet["flavors"][2], 'file': 'c-ray/cesnet-mcc-4.json'},
        {'site': cesnet, 'flavor': cesnet["flavors"][3], 'file': 'c-ray/cesnet-mcc-8.json'},
        {'site': ifca, 'flavor': ifca["flavors"][0], 'file': 'c-ray/ifca-lcg2-1.json'},
        {'site': ifca, 'flavor': ifca["flavors"][1], 'file': 'c-ray/ifca-lcg2-2.json'},
        {'site': ifca, 'flavor': ifca["flavors"][2], 'file': 'c-ray/ifca-lcg2-4.json'},
        {'site': ifca, 'flavor': ifca["flavors"][3], 'file': 'c-ray/ifca-lcg2-8.json'},
        {'site': ifca, 'flavor': ifca["flavors"][4], 'file': 'c-ray/ifca-lcg2-16.json'},
        {'site': iisas, 'flavor': iisas["flavors"][0], 'file': 'c-ray/iisas-fedcloud-1.json'},
        {'site': iisas, 'flavor': iisas["flavors"][1], 'file': 'c-ray/iisas-fedcloud-2.json'},
        {'site': iisas, 'flavor': iisas["flavors"][2], 'file': 'c-ray/iisas-fedcloud-4.json'},
        {'site': iisas, 'flavor': iisas["flavors"][3], 'file': 'c-ray/iisas-fedcloud-8.json'},
        {'site': ingrid, 'flavor': ingrid["flavors"][0], 'file': 'c-ray/ncg-ingrid-pt-1.json'},
        {'site': ingrid, 'flavor': ingrid["flavors"][1], 'file': 'c-ray/ncg-ingrid-pt-2.json'},
        {'site': ingrid, 'flavor': ingrid["flavors"][2], 'file': 'c-ray/ncg-ingrid-pt-4.json'},
        {'site': ingrid, 'flavor': ingrid["flavors"][3], 'file': 'c-ray/ncg-ingrid-pt-8.json'},
        {'site': ingrid, 'flavor': ingrid["flavors"][4], 'file': 'c-ray/ncg-ingrid-pt-16.json'},
        {'site': ingrid, 'flavor': ingrid["flavors"][5], 'file': 'c-ray/ncg-ingrid-pt-32.json'}
    ]
    for result_info in results:
        # Load JSON from file
        with open('sample_data/{}'.format(result_info['file'])) as file:
            data_raw = file.read()
            result_data = json.loads(data_raw)
        data = attempt_post(token, host + "/results", expected=201, params={
            "benchmark_id": benchmark["id"],
            # "site_id": result_info['site']["id"],
            "flavor_id": result_info['flavor']["id"],
            "execution_datetime": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "tags_ids": []
        }, data=data_raw)


def main():
    parser = argparse.ArgumentParser(description='Demo data helper')
    parser.add_argument('token', help='Bearer / access token to use')
    parser.add_argument('--host', nargs='?', default='https://localhost/api/v1', help='Host to POST data to')
    parser.add_argument("--no-approve", action="store_true",
                        help="Do not approve sites & benchmarks (and do not submit results)")

    args = parser.parse_args()

    add_demo(args.token, args.host, args.no_approve)


if __name__ == "__main__":
    main()
