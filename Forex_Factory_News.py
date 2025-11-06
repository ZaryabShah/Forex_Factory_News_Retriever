# pip install curl_cffi==0.6.*
from curl_cffi import requests
from pathlib import Path
import json
from datetime import datetime, timedelta

# ========================
# DATE RANGE CONFIGURATION
# ========================
START_DATE = "2024-01-01"  # Format: YYYY-MM-DD
END_DATE = "2025-12-31"    # Format: YYYY-MM-DD

URL = "https://www.forexfactory.com/calendar/apply-settings/100000?navigation=0"

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://www.forexfactory.com",
    "referer": "https://www.forexfactory.com/",
    "sec-ch-ua": '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "x-csrf-token": "d5e17a615441887fe9db0d5b4ed497a7",
    # mirrors capture; curl_cffi auto-decompresses gzip/br/zstd
    "accept-encoding": "gzip, deflate, br, zstd",
    "cache-control": "no-cache",
    "pragma": "no-cache",
}

COOKIES = {
    # Use the exact cookies you captured (these may expire; replace as needed)
    "fflastvisit": "1761843724",
    "fflastactivity": "0",
    "ffsettingshash": "85759b2b39ba6b3d0209fa309ddf3e03",
    "fftab-history": "index",
    "auth_user": "78aab8cba954de9fd688ecd692a05893d2fe8ea542aaeb18533d024102ef7e90%3A2328b405faa9c461a0d364d8f1af3221087ebef5d7759f24ea363da80b306301",
    "__cf_bm": "K3K5mBkpCmvA__vPolsijB3vbhy94yNcPji1olstfFg-1762452179-1.0.1.1-pDYT01hR1Tnsb3RqcwgHwSFDMTX9Uq70YYzk9WZICcD4kULvUtG_KZQ_socdxQNuRmrBWf1M5cH72YRmaUhRpJiizDWZnVSixGY5rLj7W9Bh7t8KtSgEsBquQqWAUwKu",
    "__gads": "ID=b3f489cdf96c779c:T=1761843726:RT=1762452182:S=ALNI_MY_S-UpkZ2w8P38k24VpM-8VabOWg",
    "__gpi": "UID=00001286b4983e73:T=1761843726:RT=1762452182:S=ALNI_MaCdBxTCypLtD6fkmL-pantojNz9w",
    "__eoi": "ID=f20b59e94eb3a288:T=1761843726:RT=1762452182:S=AA-AfjbZdbzuz3ZzjtLJ3sPL4sZQ",
    "ffadon": "1",
    "_hjSessionUser_3279922": "eyJpZCI6IjViZjJlNDFkLTE3ODUtNTVjYS05ODRiLTRiNmQ4ZGNmOGZiMCIsImNyZWF0ZWQiOjE3NjE4NDM3Mjg5ODUsImV4aXN0aW5nIjp0cnVlfQ==",
    "_hjSession_3279922": "eyJpZCI6IjE2MzM1Y2I5LWE1NzgtNGYxNy1iNWIwLTI2OWFhYmNmOWU4ZCIsImMiOjE3NjI0NTIxODU3OTYsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=",
    "_hjHasCachedUserAttributes": "true",
    "_gid": "GA1.2.2020122813.1762452186",
    "cf_clearance": "24Tb6tO5t3X6b0ufcBkRvRVGNAF0xBoYsb4IWzgAjcs-1762452183-1.2.1.1-aab4nnmnb1QbqKjOMFxuCwALRDq7tHFoaj23MC4zFbCMCHnjCDxFcn7N2Sc35JbPXQ_HH76Fz3PWzzd3FdJq_LtcgaVmFjxjKyAp2PdW4aKkrQSVoSusMZwB9uBVfvHLnKaIhDMo174nmgOPqgIUwLGyPt.B1uZq4H7q6o68JUGJw4GstObdh9xWIk.gAXh8Lh5rTQ7W1.8pzMVD6tB9wyeURRcBIBX8iBuisrmogIo",
    "sessions_live": "1",
    "fftimezone": "Etc%2FUTC",
    "fftimezoneoffset": "0",
    "fftimeformat": "1",
    "_ga": "GA1.1.243506777.1761843729",
    "_gat_gtag_UA_3311429_1": "1",
    "_ga_QFGG4THJR2": "GS2.1.s1762452185$o2$g1$t1762452260$j60$l0$h0",
}

OUTFILE = Path("calendar_settings_response.json")

def split_date_range(start_date_str, end_date_str, max_days=90):
    """
    Split a date range into chunks of max_days (default 90 days ~ 3 months).
    
    Args:
        start_date_str: Start date in YYYY-MM-DD format
        end_date_str: End date in YYYY-MM-DD format
        max_days: Maximum days per chunk (default 90)
    
    Returns:
        List of tuples [(start1, end1), (start2, end2), ...]
    """
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    chunks = []
    current_start = start_date
    
    while current_start <= end_date:
        current_end = min(current_start + timedelta(days=max_days - 1), end_date)
        chunks.append((
            current_start.strftime("%Y-%m-%d"),
            current_end.strftime("%Y-%m-%d")
        ))
        current_start = current_end + timedelta(days=1)
    
    return chunks

def fetch_calendar_data(session, start_date, end_date):
    """
    Fetch calendar data for a specific date range.
    
    Args:
        session: curl_cffi requests session
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        JSON response data or None on error
    """
    payload = {
        "begin_date": start_date,
        "end_date": end_date,
        "default_view": "today",
        "impacts": [3, 2, 1, 0],
        "event_types": [1, 2, 3, 4, 5, 7, 8, 9, 10, 11],
        "currencies": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    }
    
    print(f"📅 Fetching data: {start_date} to {end_date}")
    
    try:
        resp = session.post(URL, json=payload, timeout=60)
        resp.raise_for_status()
        
        ctype = resp.headers.get("content-type", "")
        if "application/json" in ctype:
            return resp.json()
        else:
            print(f"⚠️  Non-JSON Content-Type: {ctype}")
            return None
    except requests.HTTPError as e:
        print(f"❌ HTTP error for {start_date} to {end_date}: {e}")
        return None
    except Exception as e:
        print(f"❌ Error for {start_date} to {end_date}: {e}")
        return None

def merge_calendar_data(all_data_list):
    """
    Merge multiple calendar data responses into one.
    
    Args:
        all_data_list: List of JSON responses
    
    Returns:
        Merged JSON data
    """
    if not all_data_list:
        return {}
    
    # Start with the first response as base
    merged = all_data_list[0].copy()
    
    # Merge days from subsequent responses
    for data in all_data_list[1:]:
        if "days" in data and "days" in merged:
            # Avoid duplicate days by checking dateline
            existing_datelines = {day["dateline"] for day in merged["days"]}
            for day in data["days"]:
                if day["dateline"] not in existing_datelines:
                    merged["days"].append(day)
                    existing_datelines.add(day["dateline"])
    
    # Sort days by dateline
    if "days" in merged:
        merged["days"].sort(key=lambda x: x["dateline"])
    
    # Update navigation to reflect the full range
    if all_data_list:
        merged["navigation"]["current"]["title"] = f"{START_DATE} - {END_DATE}"
    
    return merged

def apply_settings():
    """
    Main function to fetch calendar data for the configured date range.
    Automatically splits into multiple requests if needed.
    """
    print(f"🚀 Starting calendar data fetch")
    print(f"📆 Date range: {START_DATE} to {END_DATE}")
    
    # Split date range into chunks
    date_chunks = split_date_range(START_DATE, END_DATE, max_days=90)
    print(f"� Split into {len(date_chunks)} request(s)\n")
    
    all_responses = []
    
    with requests.Session(impersonate="chrome120") as s:
        s.headers.update(HEADERS)
        s.cookies.update(COOKIES)
        
        for i, (start, end) in enumerate(date_chunks, 1):
            print(f"Request {i}/{len(date_chunks)}")
            data = fetch_calendar_data(s, start, end)
            
            if data:
                all_responses.append(data)
                print(f"✅ Success! Retrieved {len(data.get('days', []))} days")
            else:
                print(f"⚠️  Failed to retrieve data for this chunk")
            print()
    
    # Merge all responses
    if all_responses:
        merged_data = merge_calendar_data(all_responses)
        
        # Save to file
        OUTFILE.write_text(
            json.dumps(merged_data, indent=2, ensure_ascii=False), 
            encoding="utf-8"
        )
        
        print(f"{'='*60}")
        print(f"✅ Successfully saved combined data to: {OUTFILE.resolve()}")
        print(f"📊 Total days retrieved: {len(merged_data.get('days', []))}")
        print(f"� Total requests made: {len(all_responses)}")
        if "days" in merged_data and merged_data["days"]:
            print(f"📅 Date range in data: {merged_data['days'][0]['date']} to {merged_data['days'][-1]['date']}")
        print(f"{'='*60}")
    else:
        print("❌ No data retrieved from any request")

if __name__ == "__main__":
    try:
        apply_settings()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
