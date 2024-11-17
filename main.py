import json
import time

import requests


def test_user_agent():
    print("Testing user agent....")
    headers = {
        "user-agent": ""
    }
    resp = requests.get("http://127.0.0.1:5010/", headers=headers)
    print(f"HEADERS EMPTY: {resp.status_code}, {resp.status_code == 403}")
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) lol/130.0.0.0 kek/537.36"
    }
    resp = requests.get("http://127.0.0.1:5010/", headers=headers)
    print(f"HEADERS lol and kek: {resp.status_code}, {resp.status_code == 403}")

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }
    resp = requests.get("http://127.0.0.1:5010/", headers=headers)
    print(f"HEADERS Chrome/130: {resp.status_code}, {resp.status_code == 200}")

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/130.0.0.0 Safari/537.36"
    }
    resp = requests.get("http://127.0.0.1:5010/", headers=headers)
    print(f"HEADERS Firefox/130: {resp.status_code}, {resp.status_code == 200}")

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) lol/130.0.0.0 Safari/537.36"
    }
    resp = requests.get("http://127.0.0.1:5010/", headers=headers)
    print(f"HEADERS Safari/537.36: {resp.status_code}, {resp.status_code == 200}")
    print("-----------------------------")
    print()


def test_xss():
    print("Testing xss....")
    with open("xss/all-payload-list.txt", "r+") as f:
        all_list_xss = f.readlines()
    print("Testing xss payload list in args request...")
    # test_requests([{"params": {"test": line.strip()}} for line in all_list_xss])
    # test_requests([{"params": {line.strip(): "test"}} for line in all_list_xss])

    print("Testing xss payload list in cookies request...")
    # test_requests([{"cookies": {"test": line.strip()}} for line in all_list_xss])
    # test_requests([{"cookies": {line.strip(): "test"}} for line in all_list_xss])

    print("Testing xss payload list in headers request...")
    # test_requests([{"headers": {"test": line.strip()}} for line in all_list_xss])
    print("-----------------------------")
    print()


def test_sql():
    print("Testing sql....")
    with open("sql/all-payload-list.txt", "r+") as f:
        all_list_sql = f.readlines()
    print("Testing sql payload list in args request...")
    # test_requests([{"params": {"test": line.strip()}} for line in all_list_sql])
    # test_requests([{"params": {line.strip(): "test"}} for line in all_list_sql])

    print("Testing sql payload list in cookies request...")
    # test_requests([{"cookies": {"test": line.strip()}} for line in all_list_sql])
    # test_requests([{"cookies": {line.strip(): "test"}} for line in all_list_sql])

    print("Testing sql payload list in headers request...")
    # test_requests([{"headers": {"test": line.strip()}} for line in all_list_sql])
    print("-----------------------------")
    print()


def test_lfi():
    print("Testing lfi...")
    with open("lfi/all-payload-list.txt", "r+") as f:
        all_list_lfi = f.readlines()
    print("Testing lfi payloads list in args request...")
    test_requests([{"params": {"test": line.strip()}} for line in all_list_lfi])
    # test_requests([{"params": {line.strip(): "test"}} for line in all_list_lfi])

    print("Testing lfi payload list in cookies request...")
    # test_requests([{"cookies": {"test": line.strip()}} for line in all_list_lfi])
    # test_requests([{"cookies": {line.strip(): "test"}} for line in all_list_lfi])

    print("Testing lfi payload list in headers request...")
    # test_requests([{"headers": {"test": line.strip()}} for line in all_list_lfi])
    print("-----------------------------")
    print()


def test_requests(lines):
    drops = []
    errors = []
    for data in lines:
        for _ in range(5):
            try:
                headers = {
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
                    **data.get("headers", {})
                }
                resp = requests.get("http://127.0.0.1:5010/", params=data.get("params"), cookies=data.get("cookies"), headers=headers)
                if resp.status_code == 200:
                    drops.append(json.dumps(data))
                if resp.status_code != 403 and resp.status_code != 200:
                    errors.append({
                        "data": data,
                        "url": resp.url,
                        "status_code": resp.status_code
                    })
                break
            except Exception as e:
                print(str(e))
                time.sleep(5)
                continue
    print(f"Drop count = {len(drops)}:")
    # for drop in drops:
        # print(drop)
    with open("lfi/drop_requests_lfi.txt", "w+") as f:
        f.write("\n".join(drops))
    print(f"Errors count = {len(errors)}:")
    for error in errors:
        print(f"{json.dumps(error)}")


def test_base_requests():
    print("Testing base requests....")
    all_list = []
    with open("requests.txt", "rb") as f:
        for line in f.readlines():
            if line.strip():
                all_list.append(line.strip().decode('latin-1', errors='ignore'))

    drops = []
    errors = []
    for line in all_list:
        data = json.loads(line)
        headers = {
            "user-agent": data.get("user_agent"),
            "referer": data.get("referer")
        }
        resp = requests.get("http://127.0.0.1:5010" + data.get("url"), headers=headers)
        if resp.status_code == 200:
            drops.append(line.strip())
        if resp.status_code != 403 and resp.status_code != 200:
            errors.append({
                "line": line.strip(),
                "url": resp.url,
                "status_code": resp.status_code
            })
    print(f"Drop count = {len(drops)}:")
    for drop in drops:
        print(drop)
    print(f"Errors count = {len(errors)}:")
    for error in errors:
        print(f"{json.dumps(error)}")
    print("-----------------------------")
    print()


if __name__ == "__main__":
    # test_base_requests()
    test_user_agent()
    # test_xss()
    # test_lfi()
    # test_sql()