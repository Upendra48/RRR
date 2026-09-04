"""
populate_bids_via_api.py

Posts ~30 random bids to your running Django app at:
    http://127.0.0.1:8000/bids/

USAGE:
    1. Make sure your Django dev server is running:
           python manage.py runserver
    2. pip install requests   (if not already installed)
    3. Fill in the numeric ID for each developer name below in
       DEVELOPER_NAME_TO_ID (see note below).
    4. python populate_bids_via_api.py

IMPORTANT — developer IDs:
    Your API expects "developer" as an integer primary key, not a
    name. Below are the 5 real developer names from your database —
    you just need to fill in the matching numeric ID for each one.
    Quickest way to get them, from your project root:

        python manage.py shell
        >>> from bids.models import Developer
        >>> list(Developer.objects.values_list("id", "name"))

    That prints pairs like (3, 'Upendra Raj Joshi') — match each
    name below to its ID from that output. The script will refuse
    to run if any are left as None, so you can't accidentally post
    bad data.

CSRF NOTE:
    Since the endpoint isn't under /api/, this script assumes it's a
    normal Django view protected by CsrfViewMiddleware (session-based
    CSRF), so it does a GET first to pick up the csrftoken cookie,
    then sends it back as the X-CSRFToken header on each POST — this
    is the standard pattern for scripting against Django's CSRF
    protection. If your endpoint is actually a DRF view using
    TokenAuthentication (no CSRF enforcement), you can safely delete
    the CSRF-related lines and it'll still work.
"""

import random
import sys
import requests

BASE_URL = "http://127.0.0.1:8000"
BIDS_ENDPOINT = f"{BASE_URL}/bids/"

# ---- REQUIRED: fill in the real numeric ID for each developer ----
DEVELOPER_NAME_TO_ID = {
    "Upendra Raj Joshi": 1,
    "Test User": 2,
    "Test User2": 3,
    "Test User3": 4,
    "Test User4": 5,
}

COUNT = 30

AGENCIES = [
    ("State of Arkansas - Purchasing Dept.", "AR"),
    ("City of Springfield - Purchasing Dept.", "IL"),
    ("Lake County Forest Preserves - Purchasing Dept.", "IL"),
    ("Village of Mahomet - Purchasing Dept.", "IL"),
    ("City of Atlantic Beach - Purchasing Dept.", "FL"),
    ("Career Source South Florida - Purchasing Dept.", "FL"),
    ("NJ Dept. of Corrections - Purchasing Dept.", "NJ"),
    ("Cameron County - Purchasing Dept.", "TX"),
    ("NYS Deferred Compensation Board - Purchasing Dept.", "NY"),
    ("Town of Union - Purchasing Dept.", "NY"),
    ("Anderson School District #2 - Purchasing Dept.", "SC"),
    ("Town of West Boylston - Purchasing Dept.", "MA"),
    ("City of Clewiston - Purchasing Dept.", "FL"),
    ("City of Cottonwood Heights - Purchasing Dept.", "UT"),
    ("Algonac Community Schools - Purchasing Dept.", "MI"),
    ("Ionia County Road Commission - Purchasing Dept.", "MI"),
    ("Baldwin County School District - Purchasing Dept.", "AL"),
    ("City of Doraville - Purchasing Dept.", "GA"),
    ("Georgia State Road & Tollway Authority - Purchasing Dept.", "GA"),
    ("College of Western Idaho - Purchasing Dept.", "ID"),
    ("New York State Gaming Commission - Purchasing Dept.", "NY"),
    ("Rockdale County School District - Purchasing Dept.", "GA"),
    ("Champaign County Highway Department - Purchasing Dept.", "IL"),
    ("City of Upland - Purchasing Dept.", "CA"),
    ("Emmet County Road Commission - Purchasing Dept.", "MI"),
    ("City of Wilmington - Purchasing Dept.", "NC"),
    ("Rancho Santiago Community College District - Purchasing Dept.", "CA"),
    ("Town of Springfield - Finance Dept.", "MA"),
]

BID_TYPES = ["New", "Update/Repair"]
PRIORITIES = ["High", "Normal"]
PRIORITY_WEIGHTS = [25, 75]  # mostly Normal, some High
PROCUREMENT_TYPES = [
    "Procurement Spider",
    "Bonfire Spider",
    "Bidnet AMR",
    "Demandstar AMR",
]

COMMENT_SNIPPETS = [
    "Original bid link was changed to a search query. Needs to go back to the original link.",
    "Has been broken for the past 14 days; needs correction ASAP.",
    "Please verify the fix works correctly before marking complete.",
    "Spider was returning stale results — this repairs the pagination handling.",
    "New request. No existing spider for this agency yet.",
    "",
]

used_ecgains = set()


def random_ecgains():
    while True:
        code = "-".join(
            [
                f"{random.randint(0, 99):02d}",
                f"{random.randint(0, 99):02d}",
                f"{random.randint(0, 999):03d}",
                f"{random.randint(0, 9999):04d}",
                f"{random.randint(0, 999999):06d}",
            ]
        )
        if code not in used_ecgains:
            used_ecgains.add(code)
            return code


def build_random_bid():
    agency_name, state = random.choice(AGENCIES)
    developer_id = random.choice(list(DEVELOPER_NAME_TO_ID.values()))

    return {
        "agency_name": agency_name,
        "ecgains": random_ecgains(),
        "contact_email": f"contact{random.randint(100, 999)}@example.com",
        "state": state,
        "initials": "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=2)),
        "bid_url": f"https://example-{random.randint(1000, 9999)}.gov/procurement/bids/",
        "comments": random.choice(COMMENT_SNIPPETS),
        "module_name": f"{state}_module_{random.randint(1, 999)}.ini"
        if random.random() < 0.6
        else "",
        "developer": developer_id,
        "bid_type": random.choice(BID_TYPES),
        "priority": random.choices(PRIORITIES, weights=PRIORITY_WEIGHTS)[0],
        "has_bids": random.random() < 0.35,
        "procurement_type": random.choice(PROCUREMENT_TYPES),
    }


def main():
    missing = [name for name, dev_id in DEVELOPER_NAME_TO_ID.items() if dev_id is None]
    if missing:
        print("ERROR: The following developers are missing a numeric ID in")
        print("DEVELOPER_NAME_TO_ID — fill these in before running:")
        for name in missing:
            print(f"  - {name}")
        print(
            "\nRun this to look up the real IDs:\n"
            "  python manage.py shell\n"
            "  >>> from bids.models import Developer\n"
            "  >>> list(Developer.objects.values_list('id', 'name'))"
        )
        sys.exit(1)

    session = requests.Session()

    # Prime the session with a CSRF cookie (standard Django session-auth flow)
    session.get(BIDS_ENDPOINT)
    csrf_token = session.cookies.get("csrftoken")

    headers = {}
    if csrf_token:
        headers["X-CSRFToken"] = csrf_token
        headers["Referer"] = BIDS_ENDPOINT

    created = 0
    failed = 0

    for i in range(COUNT):
        payload = build_random_bid()
        response = session.post(BIDS_ENDPOINT, json=payload, headers=headers)

        if response.status_code in (200, 201):
            created += 1
            print(f"[{i + 1}/{COUNT}] Created: {payload['ecgains']} — {payload['agency_name']}")
        else:
            failed += 1
            print(
                f"[{i + 1}/{COUNT}] FAILED ({response.status_code}): "
                f"{payload['ecgains']} — {response.text[:300]}"
            )

    print(f"\nDone. Created {created}, failed {failed}.")


if __name__ == "__main__":
    main()