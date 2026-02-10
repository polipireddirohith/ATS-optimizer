"""
Quick diagnostic script to test ATS routes
"""
import requests

base_url = "http://localhost:5000"

print("=" * 60)
print("ATS Route Diagnostic Test")
print("=" * 60)

routes_to_test = [
    ('/', 'Main Page'),
    ('/bulk', 'Bulk Analysis Page'),
    ('/shortlist', 'Shortlist Page'),
]

for route, name in routes_to_test:
    url = base_url + route
    try:
        response = requests.get(url, timeout=5)
        status = "[OK]" if response.status_code == 200 else f"[ERROR {response.status_code}]"
        print(f"{name:25} {url:40} {status}")
    except Exception as e:
        print(f"{name:25} {url:40} [FAILED]: {str(e)}")

print("=" * 60)
print("\nIf all routes show ✅ OK, the server is working correctly.")
print("If you see ❌ errors, please share the error messages.")
print("\nNext steps:")
print("1. Open browser to http://localhost:5000")
print("2. Press F12 to open Developer Tools")
print("3. Click Console tab")
print("4. Try clicking navigation links")
print("5. Share any red error messages you see")
