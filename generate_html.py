import json

# Read fe_coverage_data.json
with open("fe_coverage_data.json", encoding="utf-8") as f:
    coverage_data = json.load(f)

# Compute stats
total_subitems = sum(len(t["items"]) for t in coverage_data)
covered_subitems = sum(sum(1 for it in t["items"] if it["totalCount"] > 0) for t in coverage_data)
total_lo_matches = sum(t["totalLoCount"] for t in coverage_data)
total_desc_matches = sum(t["totalDescCount"] for t in coverage_data)
all_courses = sorted(list(set(c for t in coverage_data for it in t["items"] for c in it["courses"])))

# Read CSV contents for self-contained downloads
with open("fe_exam_byu_coverage.csv", encoding="utf-8") as f:
    csv_coverage = f.read()

with open("byu_courses.csv", encoding="utf-8") as f:
    csv_courses = f.read()

with open("byu_course_learning_outcomes_itemized.csv", encoding="utf-8") as f:
    csv_itemized = f.read()

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BYU CBE Curriculum vs FE Chemical CBT Exam Specifications</title>
  <style>
    :root {{
      --primary: #002e5d; /* BYU Navy */
      --primary-light: #0062bb;
      --primary-hover: #001a35;
      --accent: #d97706;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #1e293b;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --border-dark: #cbd5e1;
      --highlight: #eff6ff;
      --badge-bg: #e0f2fe;
      --badge-text: #0369a1;
      --lo-badge-bg: #f0fdf4;
      --lo-badge-text: #166534;
      --desc-badge-bg: #fef3c7;
      --desc-badge-text: #92400e;
      --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
      --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
      --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      --font-serif: "Times New Roman", Times, Georgia, serif;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-family);
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding: 24px;
    }}

    .container {{
      max-width: 1200px;
      margin: 0 auto;
      background: var(--card-bg);
      box-shadow: var(--shadow);
      border-radius: 8px;
      border: 1px solid var(--border);
      overflow: hidden;
    }}

    /* Top Controls Bar */
    .toolbar {{
      background: #0f172a;
      color: #fff;
      padding: 12px 24px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      font-size: 0.875rem;
    }}

    .toolbar-title {{
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .toolbar-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #1e293b;
      color: #f8fafc;
      padding: 6px 12px;
      border-radius: 6px;
      border: 1px solid #334155;
      font-size: 0.8rem;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.15s ease;
    }}

    .btn:hover {{
      background: #334155;
      color: #fff;
    }}

    .btn-primary {{
      background: var(--primary-light);
      border-color: var(--primary-light);
    }}

    .btn-primary:hover {{
      background: #004b91;
    }}

    /* Document Header - Matches NCEES PDF */
    .document-header {{
      padding: 36px 40px 24px;
      border-bottom: 2px solid #000;
      background: #fff;
    }}

    .ncees-brand {{
      display: flex;
      align-items: flex-start;
      gap: 16px;
      margin-bottom: 24px;
    }}

    .ncees-logo-box {{
      border: 3px solid #000;
      padding: 6px 12px;
      font-family: var(--font-family);
      font-weight: 900;
      font-size: 28px;
      letter-spacing: -1px;
      line-height: 1;
      display: inline-block;
    }}

    .ncees-tagline {{
      font-size: 13px;
      font-style: italic;
      color: #334155;
      margin-top: 6px;
    }}

    .doc-titles {{
      text-align: center;
      margin-bottom: 20px;
    }}

    .doc-title-main {{
      font-family: var(--font-serif);
      font-size: 20px;
      font-weight: bold;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .doc-title-sub {{
      font-family: var(--font-serif);
      font-size: 18px;
      font-weight: bold;
      letter-spacing: 0.5px;
      margin-top: 2px;
    }}

    .doc-effective {{
      font-size: 14px;
      font-weight: 600;
      margin-top: 6px;
      color: #334155;
    }}

    .doc-bullets {{
      margin: 16px 0 20px 24px;
      font-size: 13.5px;
      color: #1e293b;
    }}

    .doc-bullets li {{
      margin-bottom: 6px;
    }}

    /* Stats Ribbon */
    .stats-ribbon {{
      background: #f1f5f9;
      padding: 14px 40px;
      border-bottom: 1px solid var(--border);
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
    }}

    .stat-pill {{
      display: flex;
      align-items: baseline;
      gap: 6px;
      font-size: 0.85rem;
    }}

    .stat-num {{
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--primary);
    }}

    .filter-group {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.85rem;
    }}

    select, input[type="text"] {{
      padding: 6px 10px;
      border-radius: 6px;
      border: 1px solid var(--border-dark);
      font-size: 0.85rem;
      background: #fff;
      color: var(--text);
    }}

    /* Specifications Table */
    .table-container {{
      overflow-x: auto;
    }}

    table.spec-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13.5px;
    }}

    th {{
      background: #f8fafc;
      padding: 12px 16px;
      text-align: left;
      font-weight: 700;
      color: #0f172a;
      border-bottom: 2px solid #000;
      font-family: var(--font-family);
      position: sticky;
      top: 0;
      z-index: 5;
    }}

    th.col-knowledge {{
      width: 58%;
    }}

    th.col-questions {{
      width: 14%;
      text-align: center;
      white-space: nowrap;
    }}

    th.col-lo {{
      width: 14%;
      text-align: center;
    }}

    th.col-desc {{
      width: 14%;
      text-align: center;
    }}

    /* Topic Header Row */
    tr.topic-header-row {{
      background-color: #f8fafc;
      border-top: 1.5px solid #cbd5e1;
      border-bottom: 1px solid #cbd5e1;
    }}

    tr.topic-header-row td {{
      padding: 10px 16px;
      font-weight: 700;
      font-size: 14.5px;
      color: #000;
    }}

    tr.topic-header-row .topic-number-title {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    tr.topic-header-row .topic-questions {{
      text-align: center;
      font-weight: 700;
    }}

    tr.topic-header-row .topic-summary-badge {{
      text-align: center;
    }}

    /* Sub-item Row */
    tr.subitem-row {{
      border-bottom: 1px solid #f1f5f9;
      transition: background-color 0.15s ease;
    }}

    tr.subitem-row:hover {{
      background-color: #f8fafc;
    }}

    tr.subitem-row.highlighted {{
      background-color: #e0f2fe;
    }}

    td.subitem-desc {{
      padding: 8px 16px 8px 36px;
      vertical-align: top;
      color: #1e293b;
    }}

    .subitem-letter {{
      font-weight: 600;
      display: inline-block;
      width: 22px;
    }}

    td.cell-center {{
      text-align: center;
      vertical-align: middle;
      padding: 6px 12px;
    }}

    /* Badges & Triggers */
    .coverage-pill {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 4px 10px;
      border-radius: 9999px;
      font-weight: 700;
      font-size: 12.5px;
      cursor: pointer;
      transition: all 0.15s ease;
      user-select: none;
      border: 1px solid transparent;
      min-width: 32px;
    }}

    .coverage-pill.has-matches {{
      background: var(--badge-bg);
      color: var(--badge-text);
      border-color: #bae6fd;
    }}

    .coverage-pill.has-matches:hover {{
      background: #0284c7;
      color: #ffffff;
      transform: scale(1.06);
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}

    .coverage-pill.zero-matches {{
      background: #f1f5f9;
      color: #94a3b8;
      border-color: #e2e8f0;
      cursor: default;
    }}

    .lo-pill {{
      background: var(--lo-badge-bg);
      color: var(--lo-badge-text);
      border-color: #bbf7d0;
    }}

    .lo-pill:hover {{
      background: #15803d;
      color: #fff;
    }}

    .desc-pill {{
      background: var(--desc-badge-bg);
      color: var(--desc-badge-text);
      border-color: #fde68a;
    }}

    .desc-pill:hover {{
      background: #b45309;
      color: #fff;
    }}

    /* Floating Popover / Tooltip */
    #popover {{
      position: fixed;
      display: none;
      background: #ffffff;
      border: 1px solid var(--border-dark);
      border-radius: 8px;
      box-shadow: var(--shadow-lg);
      padding: 16px;
      width: 420px;
      max-width: 90vw;
      max-height: 480px;
      overflow-y: auto;
      z-index: 1000;
      font-size: 13px;
      line-height: 1.45;
      pointer-events: auto;
    }}

    #popover.visible {{
      display: block;
      animation: popoverFade 0.15s ease-out;
    }}

    @keyframes popoverFade {{
      from {{ opacity: 0; transform: translateY(4px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .popover-header {{
      border-bottom: 1px solid var(--border);
      padding-bottom: 8px;
      margin-bottom: 12px;
    }}

    .popover-title {{
      font-weight: 700;
      font-size: 14px;
      color: var(--primary);
    }}

    .popover-subtitle {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    .popover-item {{
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 10px;
      margin-bottom: 8px;
    }}

    .popover-item-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 4px;
      font-size: 12px;
    }}

    .popover-badge {{
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 11px;
    }}

    .popover-badge.lo {{
      background: var(--lo-badge-bg);
      color: var(--lo-badge-text);
    }}

    .popover-badge.desc {{
      background: var(--desc-badge-bg);
      color: var(--desc-badge-text);
    }}

    .catalog-link {{
      color: var(--primary-light);
      text-decoration: none;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 3px;
    }}

    .catalog-link:hover {{
      text-decoration: underline;
      color: var(--primary);
    }}

    .popover-text {{
      color: #334155;
      font-size: 12.5px;
    }}

    /* Modal for Full View */
    .modal-backdrop {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.5);
      z-index: 2000;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}

    .modal-backdrop.open {{
      display: flex;
    }}

    .modal-content {{
      background: #fff;
      border-radius: 10px;
      width: 750px;
      max-width: 95vw;
      max-height: 85vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.25);
      overflow: hidden;
    }}

    .modal-header {{
      padding: 16px 20px;
      background: #002e5d;
      color: #fff;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .modal-header h3 {{
      font-size: 16px;
      font-weight: 700;
    }}

    .modal-close {{
      background: transparent;
      border: none;
      color: #fff;
      font-size: 24px;
      cursor: pointer;
      line-height: 1;
    }}

    .modal-body {{
      padding: 20px;
      overflow-y: auto;
      flex: 1;
    }}

    .footer {{
      padding: 24px 40px;
      border-top: 1px solid var(--border);
      background: #f8fafc;
      font-size: 12px;
      color: var(--text-muted);
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 12px;
    }}

    @media print {{
      body {{
        padding: 0;
        background: #fff;
      }}
      .toolbar, .stats-ribbon, .btn, #popover {{
        display: none !important;
      }}
      .container {{
        box-shadow: none;
        border: none;
      }}
    }}
  </style>
</head>
<body>

<div class="container">
  <!-- Top Application Control Bar -->
  <div class="toolbar">
    <div class="toolbar-title">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
      BYU Chemical Engineering Catalog Analyzer &amp; FE Exam Specification Matrix
    </div>
    <div class="toolbar-actions">
      <button onclick="downloadCsv('coverage')" class="btn btn-primary" title="Download FE Exam Coverage CSV">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        Download Coverage CSV
      </button>
      <button onclick="downloadCsv('courses')" class="btn" title="Download All 34 BYU Courses CSV">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        Courses CSV
      </button>
      <button onclick="downloadCsv('itemized')" class="btn" title="Download Itemized Learning Outcomes CSV">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        Itemized LOs CSV
      </button>
      <button onclick="window.print()" class="btn">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
        Print
      </button>
    </div>
  </div>

  <!-- Document Header matching NCEES Exam Specification PDF -->
  <header class="document-header">
    <div class="ncees-brand">
      <div>
        <div class="ncees-logo-box">NCEES</div>
        <div class="ncees-tagline">advancing licensure for engineers and surveyors</div>
      </div>
    </div>

    <div class="doc-titles">
      <div class="doc-title-main">Fundamentals of Engineering (FE)</div>
      <div class="doc-title-sub">CHEMICAL CBT Exam Specifications</div>
      <div class="doc-effective">Effective Beginning with the July 2020 Examinations</div>
    </div>

    <ul class="doc-bullets">
      <li>The FE exam is a computer-based test (CBT). It is closed book with an electronic reference.</li>
      <li>Examinees have 6 hours to complete the exam, which contains 110 questions. The 6-hour time also includes a tutorial and an optional scheduled break.</li>
      <li>The FE exam uses both the International System of Units (SI) and the U.S. Customary System (USCS).</li>
    </ul>
  </header>

  <!-- Interactive Controls & Summary Stats -->
  <div class="stats-ribbon">
    <div style="display:flex; gap: 20px; flex-wrap: wrap;">
      <div class="stat-pill">
        <span class="stat-num">{covered_subitems}/{total_subitems}</span>
        <span>FE Topics Covered ({covered_subitems/total_subitems*100:.0f}%)</span>
      </div>
      <div class="stat-pill">
        <span class="stat-num">{total_lo_matches}</span>
        <span>Learning Outcomes Mapped</span>
      </div>
      <div class="stat-pill">
        <span class="stat-num">{total_desc_matches}</span>
        <span>Descriptions Mapped</span>
      </div>
    </div>

    <div class="filter-group">
      <label for="courseFilter"><strong>Filter Course:</strong></label>
      <select id="courseFilter" onchange="filterByCourse(this.value)">
        <option value="">All 34 BYU Courses</option>
        {''.join(f'<option value="{c}">{c}</option>' for c in all_courses)}
      </select>

      <input type="text" id="searchInput" placeholder="Search topics or keywords..." oninput="searchTopics(this.value)">
    </div>
  </div>

  <!-- Main Specifications Table -->
  <div class="table-container">
    <table class="spec-table">
      <thead>
        <tr>
          <th class="col-knowledge">Knowledge</th>
          <th class="col-questions">Number of Questions</th>
          <th class="col-lo" title="Number of BYU Course Learning Outcomes covering this item">Learning Outcomes</th>
          <th class="col-desc" title="Number of BYU Course Descriptions covering this item">Course Descriptions</th>
          <th class="col-questions" title="Total BYU Coverage Items">Total Coverage</th>
        </tr>
      </thead>
      <tbody id="specTableBody">
"""

for topic in coverage_data:
    t_id = topic["id"]
    t_name = topic["name"]
    t_q = topic["questions"]
    t_lo = topic["totalLoCount"]
    t_desc = topic["totalDescCount"]
    t_tot = topic["totalMatchesCount"]

    html_content += f"""
        <!-- Topic Header Row: {t_id}. {t_name} -->
        <tr class="topic-header-row" data-topic-id="{t_id}">
          <td>
            <div class="topic-number-title">
              <span>{t_id}.</span>
              <span>{t_name}</span>
            </div>
          </td>
          <td class="topic-questions">{t_q}</td>
          <td class="cell-center">
            <span class="coverage-pill lo-pill {'has-matches' if t_lo > 0 else 'zero-matches'}" 
                  onclick="openTopicModal('{t_id}', 'lo')">{t_lo}</span>
          </td>
          <td class="cell-center">
            <span class="coverage-pill desc-pill {'has-matches' if t_desc > 0 else 'zero-matches'}" 
                  onclick="openTopicModal('{t_id}', 'desc')">{t_desc}</span>
          </td>
          <td class="cell-center">
            <span class="coverage-pill {'has-matches' if t_tot > 0 else 'zero-matches'}" 
                  onclick="openTopicModal('{t_id}', 'all')">{t_tot}</span>
          </td>
        </tr>
    """

    for item in topic["items"]:
        sub_id = item["subId"]
        full_id = item["fullId"]
        title = item["title"]
        lo_cnt = item["loCount"]
        desc_cnt = item["descCount"]
        tot_cnt = item["totalCount"]
        courses_attr = ",".join(item["courses"])

        html_content += f"""
        <!-- Subitem Row: {full_id} -->
        <tr class="subitem-row" data-sub-id="{full_id}" data-courses="{courses_attr}">
          <td class="subitem-desc">
            <span class="subitem-letter">{sub_id}.</span>
            <span class="subitem-title-text">{title}</span>
          </td>
          <td class="cell-center text-muted">—</td>
          <td class="cell-center">
            <span class="coverage-pill lo-pill {'has-matches' if lo_cnt > 0 else 'zero-matches'}"
                  data-full-id="{full_id}" data-type="lo"
                  onmouseenter="showPopover(event, '{full_id}', 'lo')"
                  onmouseleave="hidePopover()"
                  onclick="openSubitemModal('{full_id}', 'lo')">
              {lo_cnt}
            </span>
          </td>
          <td class="cell-center">
            <span class="coverage-pill desc-pill {'has-matches' if desc_cnt > 0 else 'zero-matches'}"
                  data-full-id="{full_id}" data-type="desc"
                  onmouseenter="showPopover(event, '{full_id}', 'desc')"
                  onmouseleave="hidePopover()"
                  onclick="openSubitemModal('{full_id}', 'desc')">
              {desc_cnt}
            </span>
          </td>
          <td class="cell-center">
            <span class="coverage-pill {'has-matches' if tot_cnt > 0 else 'zero-matches'}"
                  data-full-id="{full_id}" data-type="all"
                  onmouseenter="showPopover(event, '{full_id}', 'all')"
                  onmouseleave="hidePopover()"
                  onclick="openSubitemModal('{full_id}', 'all')">
              {tot_cnt}
            </span>
          </td>
        </tr>
        """

html_content += f"""
      </tbody>
    </table>
  </div>

  <footer class="footer">
    <div>
      <strong>Source Data:</strong> Brigham Young University Undergraduate Course Catalog (<a href="https://catalog.byu.edu/courses" target="_blank">catalog.byu.edu</a>)
      &bull; NCEES FE Chemical CBT Specifications
    </div>
    <div>
      Hover over or click any number badge to view covering courses and direct catalog links.
    </div>
  </footer>
</div>

<!-- Floating Hover Popover -->
<div id="popover"></div>

<!-- Modal Dialog for Detailed Inspection -->
<div id="modalBackdrop" class="modal-backdrop" onclick="closeModal(event)">
  <div class="modal-content" onclick="event.stopPropagation()">
    <div class="modal-header">
      <h3 id="modalTitle">Coverage Details</h3>
      <button class="modal-close" onclick="closeModal()">&times;</button>
    </div>
    <div class="modal-body" id="modalBody"></div>
  </div>
</div>

<script>
  // Complete coverage data embedded
  const coverageData = {json.dumps(coverage_data)};

  // Map for fast lookup by fullId
  const subitemMap = {{}};
  coverageData.forEach(topic => {{
    topic.items.forEach(item => {{
      subitemMap[item.fullId] = {{
        topicId: topic.id,
        topicName: topic.name,
        ...item
      }};
    }});
  }});

  const popover = document.getElementById('popover');
  let popoverTimeout = null;

  function showPopover(e, fullId, filterType) {{
    clearTimeout(popoverTimeout);
    const item = subitemMap[fullId];
    if (!item || item.totalCount === 0) return;

    let matches = item.matches;
    if (filterType === 'lo') {{
      matches = matches.filter(m => m.itemType === 'learning_outcome');
    }} else if (filterType === 'desc') {{
      matches = matches.filter(m => m.itemType === 'course_description');
    }}

    if (matches.length === 0) return;

    // Group by course
    const byCourse = {{}};
    matches.forEach(m => {{
      if (!byCourse[m.courseCode]) byCourse[m.courseCode] = [];
      byCourse[m.courseCode].push(m);
    }});

    let html = `
      <div class="popover-header">
        <div class="popover-title">${{item.fullId}}. ${{item.title}}</div>
        <div class="popover-subtitle">
          Covered by ${{matches.length}} item${{matches.length > 1 ? 's' : ''}} across ${{Object.keys(byCourse).length}} course${{Object.keys(byCourse).length > 1 ? 's' : ''}}
          <span style="float:right; font-weight:600; color:#0284c7;">Click badge for full modal</span>
        </div>
      </div>
    `;

    for (const [courseCode, cMatches] of Object.entries(byCourse)) {{
      cMatches.forEach(m => {{
        const isLo = m.itemType === 'learning_outcome';
        const badgeClass = isLo ? 'lo' : 'desc';
        const badgeLabel = isLo ? `LO #${{m.outcomeIndex}}` : 'Course Description';
        const link = m.catalogUrl ? `<a href="${{m.catalogUrl}}" target="_blank" class="catalog-link">View in BYU Catalog &nearr;</a>` : '';

        html += `
          <div class="popover-item">
            <div class="popover-item-header">
              <div>
                <strong style="color:var(--primary); font-size:13px;">${{courseCode}}</strong>
                <span style="color:#64748b; font-size:11.5px;">&bull; ${{m.courseTitle}}</span>
              </div>
              <span class="popover-badge ${{badgeClass}}">${{badgeLabel}}</span>
            </div>
            <div class="popover-text" style="margin-bottom:6px;">
              ${{m.text.length > 180 ? m.text.substring(0, 180) + '...' : m.text}}
            </div>
            ${{link}}
          </div>
        `;
      }});
    }}

    popover.innerHTML = html;
    popover.classList.add('visible');

    // Position popover
    const rect = e.target.getBoundingClientRect();
    let top = rect.bottom + 8;
    let left = rect.left - 160;

    // Adjust boundaries
    if (left + 420 > window.innerWidth) {{
      left = window.innerWidth - 440;
    }}
    if (left < 10) left = 10;

    if (top + 350 > window.innerHeight) {{
      top = rect.top - popover.offsetHeight - 8;
      if (top < 10) top = 10;
    }}

    popover.style.top = top + 'px';
    popover.style.left = left + 'px';
  }}

  function hidePopover() {{
    popoverTimeout = setTimeout(() => {{
      popover.classList.remove('visible');
    }}, 150);
  }}

  popover.addEventListener('mouseenter', () => {{
    clearTimeout(popoverTimeout);
  }});

  popover.addEventListener('mouseleave', () => {{
    hidePopover();
  }});

  // Modal Handlers
  function openSubitemModal(fullId, filterType) {{
    hidePopover();
    const item = subitemMap[fullId];
    if (!item) return;

    let matches = item.matches;
    let typeLabel = "All Coverage";
    if (filterType === 'lo') {{
      matches = matches.filter(m => m.itemType === 'learning_outcome');
      typeLabel = "Learning Outcomes";
    }} else if (filterType === 'desc') {{
      matches = matches.filter(m => m.itemType === 'course_description');
      typeLabel = "Course Descriptions";
    }}

    document.getElementById('modalTitle').textContent = `${{item.fullId}}. ${{item.title}} (${{typeLabel}})`;

    let bodyHtml = `
      <div style="margin-bottom:16px; padding:12px; background:#f1f5f9; border-radius:6px; font-size:13.5px;">
        <strong>FE Specification Topic:</strong> ${{item.topicName}} &bull; Item ${{item.subId}}<br>
        <strong>Covering Courses (${{item.courses.length}}):</strong> ${{item.courses.join(', ') || 'None'}}
      </div>
    `;

    if (matches.length === 0) {{
      bodyHtml += `<p style="color:#64748b; font-style:italic;">No ${{typeLabel.toLowerCase()}} currently mapped for this topic.</p>`;
    }} else {{
      matches.forEach(m => {{
        const isLo = m.itemType === 'learning_outcome';
        const badgeClass = isLo ? 'lo' : 'desc';
        const badgeLabel = isLo ? `Learning Outcome #${{m.outcomeIndex}}` : 'Course Description';
        const link = m.catalogUrl ? `<a href="${{m.catalogUrl}}" target="_blank" class="catalog-link">Open BYU Catalog Page &nearr;</a>` : '';

        bodyHtml += `
          <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:14px; margin-bottom:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
              <div>
                <strong style="color:var(--primary); font-size:15px;">${{m.courseCode}}</strong>: ${{m.courseTitle}}
              </div>
              <span class="popover-badge ${{badgeClass}}" style="font-size:12px; padding:3px 8px;">${{badgeLabel}}</span>
            </div>
            <div style="font-size:13.5px; color:#334155; line-height:1.5; margin-bottom:10px; background:#f8fafc; padding:10px; border-radius:6px;">
              ${{m.text}}
            </div>
            <div>${{link}}</div>
          </div>
        `;
      }});
    }}

    document.getElementById('modalBody').innerHTML = bodyHtml;
    document.getElementById('modalBackdrop').classList.add('open');
  }}

  function openTopicModal(topicId, filterType) {{
    hidePopover();
    const topic = coverageData.find(t => t.id === topicId);
    if (!topic) return;

    let allMatches = [];
    topic.items.forEach(it => {{
      let m = it.matches;
      if (filterType === 'lo') m = m.filter(x => x.itemType === 'learning_outcome');
      if (filterType === 'desc') m = m.filter(x => x.itemType === 'course_description');
      m.forEach(match => {{
        allMatches.push({{
          ...match,
          subItemTitle: `${{it.subId}}. ${{it.title}}`
        }});
      }});
    }});

    document.getElementById('modalTitle').textContent = `${{topic.id}}. ${{topic.name}} - Full Topic Overview`;

    let bodyHtml = `
      <div style="margin-bottom:16px; padding:12px; background:#f1f5f9; border-radius:6px; font-size:13.5px;">
        <strong>Total Questions on FE Exam:</strong> ${{topic.questions}}<br>
        <strong>Total Matches:</strong> ${{allMatches.length}} (${{topic.totalLoCount}} Outcomes, ${{topic.totalDescCount}} Descriptions)
      </div>
    `;

    allMatches.forEach(m => {{
      const isLo = m.itemType === 'learning_outcome';
      const badgeClass = isLo ? 'lo' : 'desc';
      const badgeLabel = isLo ? `LO #${{m.outcomeIndex}}` : 'Course Description';
      const link = m.catalogUrl ? `<a href="${{m.catalogUrl}}" target="_blank" class="catalog-link">Open BYU Catalog Page &nearr;</a>` : '';

      bodyHtml += `
        <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:12px; margin-bottom:10px;">
          <div style="font-size:12px; color:#64748b; margin-bottom:4px;">Covers: <strong>${{m.subItemTitle}}</strong></div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:var(--primary);">${{m.courseCode}}: ${{m.courseTitle}}</strong>
            <span class="popover-badge ${{badgeClass}}">${{badgeLabel}}</span>
          </div>
          <div style="font-size:13px; color:#334155; margin-bottom:8px;">${{m.text}}</div>
          <div>${{link}}</div>
        </div>
      `;
    }});

    document.getElementById('modalBody').innerHTML = bodyHtml;
    document.getElementById('modalBackdrop').classList.add('open');
  }}

  function closeModal(e) {{
    document.getElementById('modalBackdrop').classList.remove('open');
  }}

  // Filter Functions
  function filterByCourse(courseCode) {{
    const rows = document.querySelectorAll('tr.subitem-row');
    rows.forEach(r => {{
      const courses = r.getAttribute('data-courses').split(',');
      if (!courseCode || courses.includes(courseCode)) {{
        r.style.display = '';
        if (courseCode) r.classList.add('highlighted');
        else r.classList.remove('highlighted');
      }} else {{
        r.style.display = 'none';
        r.classList.remove('highlighted');
      }}
    }});
  }}

  function searchTopics(query) {{
    const q = query.toLowerCase().trim();
    const rows = document.querySelectorAll('tr.subitem-row');
    rows.forEach(r => {{
      const title = r.querySelector('.subitem-title-text').textContent.toLowerCase();
      const subId = r.getAttribute('data-sub-id').toLowerCase();
      const courses = r.getAttribute('data-courses').toLowerCase();
      if (!q || title.includes(q) || subId.includes(q) || courses.includes(q)) {{
        r.style.display = '';
      }} else {{
        r.style.display = 'none';
      }}
    }});
  }}

  // Embedded CSV Data for 100% self-contained downloads
  const CSV_FILES = {{
    coverage: {{
      name: 'fe_exam_byu_coverage.csv',
      data: {json.dumps(csv_coverage)}
    }},
    courses: {{
      name: 'byu_courses.csv',
      data: {json.dumps(csv_courses)}
    }},
    itemized: {{
      name: 'byu_course_learning_outcomes_itemized.csv',
      data: {json.dumps(csv_itemized)}
    }}
  }};

  function downloadCsv(type) {{
    const file = CSV_FILES[type];
    if (!file) return;
    const blob = new Blob([file.data], {{ type: 'text/csv;charset=utf-8;' }});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = file.name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }}
</script>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated index.html ({len(html_content)} bytes)")
