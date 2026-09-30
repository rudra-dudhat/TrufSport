import urllib.request
import json

base_url = "http://localhost:5000"
endpoints = [
    {"url": "/", "method": "GET", "expected": 200},
    {"url": "/login", "method": "GET", "expected": 200},
    {"url": "/venue?id=box-cricket", "method": "GET", "expected": 200},
    {"url": "/my-bookings", "method": "GET", "expected": 200},
    {"url": "/api/slots?venue_name=Greenfield%20Box%20Cricket&date=2026-08-01", "method": "GET", "expected": 200},
    {"url": "/api/my-bookings?username=testuser", "method": "GET", "expected": 200}
]

errors = 0

for ep in endpoints:
    url = base_url + ep['url']
    try:
        req = urllib.request.Request(url, method=ep['method'])
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            if status != ep['expected']:
                print(f"FAIL: {url} returned {status} (expected {ep['expected']})")
                errors += 1
            else:
                print(f"PASS: {url} returned {status}")
    except urllib.error.HTTPError as e:
        if e.code == ep['expected']:
            print(f"PASS: {url} returned {e.code}")
        else:
            print(f"FAIL: {url} returned {e.code} (expected {ep['expected']})")
            errors += 1
    except Exception as e:
        print(f"FAIL: {url} threw exception {e}")
        errors += 1

if errors == 0:
    print("\nALL TESTS PASSED! 0 uncaught exceptions.")
else:
    print(f"\n{errors} TESTS FAILED.")
