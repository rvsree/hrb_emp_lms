import urllib.request
import urllib.error
import json
import traceback

HOST = 'http://127.0.0.1:8091'
ENDPOINTS = ['/hrb_emp_lms/health/app', '/hrb_emp_lms/health/postgres']

print('Checking HTTP endpoints...')
for ep in ENDPOINTS:
    url = HOST + ep
    try:
        with urllib.request.urlopen(url, timeout=10) as u:
            body = u.read().decode('utf-8')
            print('\nEndpoint:', ep)
            print('HTTP', u.getcode())
            try:
                j = json.loads(body)
                print(json.dumps(j, indent=2))
            except Exception:
                print(body)
    except urllib.error.HTTPError as e:
        print('\nEndpoint:', ep)
        print('HTTPError', e.code)
        try:
            print(e.read().decode())
        except Exception:
            pass
    except Exception as e:
        print('\nEndpoint:', ep)
        print('ERROR', repr(e))
        traceback.print_exc()

print('\nCalling postgres_health_check() directly...')
try:
    from src.app.common.providers_client.db_client.postgres_db_client import postgres_health_check
    res = postgres_health_check()
    print(json.dumps(res, indent=2))
except Exception as e:
    print('Exception when calling postgres_health_check():', repr(e))
    traceback.print_exc()

