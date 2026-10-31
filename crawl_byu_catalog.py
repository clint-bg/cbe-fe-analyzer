import urllib.request
import ssl
import json
import csv
import re
import html
import time
import urllib.parse

def clean_text(text):
    if not text:
        return ""
    # Unescape HTML entities
    text = html.unescape(text)
    # Replace non-breaking spaces
    text = text.replace('\xa0', ' ')
    # Strip HTML tags if present
    text = re.sub(r'<[^>]+>', ' ', text)
    # Normalize multiple whitespace within lines, but preserve newlines if needed, or collapse
    # For CSV cells, collapsing consecutive spaces:
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in text.splitlines()]
    text = '\n'.join([l for l in lines if l])
    return text.strip()

def main():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    target_courses = [
        "CBE 170", "CBE 263", "CBE 273", "CBE 374", "CBE 311", "CBE 191", 
        "CBE 285", "CBE 345", "CBE 445", "CBE 385", "CBE 291", "CBE 391", 
        "CBE 373", "CBE 376", "CBE 378", "CBE 386", "CBE 461", "CBE 476", 
        "CBE 479", "CBE 436", "CBE 451", "MATH 112", "MATH 113", "PHSCS 121", 
        "CHEM 111", "CHEM 112", "MATH 302", "MATH 303", "BIO 130", "CHEM 357", 
        "CHEM 467", "ECON 110", "WRTG 316", "STAT 121"
    ]

    catalog_id = "SDA0rZZwClSdh47nMnGv"
    base_search_url = "https://app.coursedog.com/api/v1/cm/byu/courses/search/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Requested-With": "catalog",
        "Origin": "https://catalog.byu.edu",
        "Referer": "https://catalog.byu.edu/"
    }

    courses_data = []

    print(f"Starting crawl for {len(target_courses)} courses from BYU Undergraduate Catalog...")

    for code in target_courses:
        parts = code.split()
        subj, num = parts[0], parts[1]
        encoded_query = urllib.parse.quote(code)
        url = f"{base_search_url}{encoded_query}?catalogId={catalog_id}"
        
        req = urllib.request.Request(url, headers=headers)
        matched_course = None
        try:
            with urllib.request.urlopen(req, context=ctx) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                course_list = res.get("data", [])
                for item in course_list:
                    if item.get("subjectCode") == subj and str(item.get("courseNumber")) == num:
                        matched_course = item
                        break
        except Exception as e:
            print(f"Error fetching {code}: {e}")

        if not matched_course:
            print(f"Warning: Exact match not found for {code}!")
            courses_data.append({
                "code": code,
                "title": "",
                "description": "",
                "courseGroupId": "",
                "catalogUrl": "",
                "outcomes": []
            })
            continue

        title = clean_text(matched_course.get("name", ""))
        desc = clean_text(matched_course.get("description", ""))
        cg_id = matched_course.get("courseGroupId", "")
        catalog_url = f"https://catalog.byu.edu/courses/{cg_id}" if cg_id else ""
        raw_outcomes = matched_course.get("learningOutcomes", []) or []

        cleaned_outcomes = []
        for o in raw_outcomes:
            o_name = clean_text(o.get("name", ""))
            o_obj = clean_text(o.get("objective", ""))
            if o_name or o_obj:
                cleaned_outcomes.append({
                    "name": o_name,
                    "objective": o_obj
                })

        courses_data.append({
            "code": code,
            "title": title,
            "description": desc,
            "courseGroupId": cg_id,
            "catalogUrl": catalog_url,
            "outcomes": cleaned_outcomes
        })

        print(f"Retrieved {code}: '{title}' ({len(cleaned_outcomes)} outcomes)")
        time.sleep(0.05)

    # 1. Write courses summary CSV (one row per course)
    summary_csv_path = "byu_courses.csv"
    with open(summary_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Course Code", "Course Title", "Course Description", "Learning Outcomes", "Outcome Count", "Catalog URL"])
        for c in courses_data:
            # Format outcomes as: Name: Objective; Name: Objective
            formatted_outcomes = []
            for o in c["outcomes"]:
                name = o["name"]
                obj = o["objective"]
                if name and obj:
                    formatted_outcomes.append(f"{name}: {obj}")
                elif name:
                    formatted_outcomes.append(name)
                elif obj:
                    formatted_outcomes.append(obj)
            outcomes_str = "; ".join(formatted_outcomes)

            writer.writerow([
                c["code"],
                c["title"],
                c["description"],
                outcomes_str,
                len(c["outcomes"]),
                c["catalogUrl"]
            ])

    print(f"\nWrote summary CSV to {summary_csv_path}")

    # 2. Write itemized learning outcomes CSV (one row per learning outcome)
    itemized_csv_path = "byu_course_learning_outcomes_itemized.csv"
    with open(itemized_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Course Code",
            "Course Title",
            "Course Description",
            "Outcome Index",
            "Outcome Name",
            "Outcome Objective",
            "Full Outcome Text",
            "Catalog URL"
        ])
        for c in courses_data:
            if not c["outcomes"]:
                # Course has no outcomes listed
                writer.writerow([
                    c["code"],
                    c["title"],
                    c["description"],
                    "",
                    "",
                    "",
                    "No learning outcomes listed in catalog",
                    c["catalogUrl"]
                ])
            else:
                for idx, o in enumerate(c["outcomes"], start=1):
                    name = o["name"]
                    obj = o["objective"]
                    if name and obj:
                        full_text = f"{name}: {obj}"
                    elif name:
                        full_text = name
                    else:
                        full_text = obj
                    writer.writerow([
                        c["code"],
                        c["title"],
                        c["description"],
                        idx,
                        name,
                        obj,
                        full_text,
                        c["catalogUrl"]
                    ])

    print(f"Wrote itemized CSV to {itemized_csv_path}")

if __name__ == "__main__":
    main()
