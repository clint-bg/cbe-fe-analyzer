import json
import csv
from fe_matcher import get_refined_matcher

fe_topics = [
    {
        "id": "1",
        "name": "Mathematics",
        "questions": "6–9",
        "items": [
            {"subId": "A", "title": "Analytic geometry, logarithms, and trigonometry"},
            {"subId": "B", "title": "Calculus (e.g., single-variable, integral, differential)"},
            {"subId": "C", "title": "Differential equations (e.g., ordinary, partial, Laplace)"},
            {"subId": "D", "title": "Numerical methods (e.g., error propagation, Taylor's series, curve fitting, Newton-Raphson, Fourier series)"},
            {"subId": "E", "title": "Algebra (e.g., fundamentals, matrix algebra, systems of equations)"},
            {"subId": "F", "title": "Accuracy, precision, and significant figures"}
        ]
    },
    {
        "id": "2",
        "name": "Probability and Statistics",
        "questions": "4–6",
        "items": [
            {"subId": "A", "title": "Probability distributions (e.g., discrete, continuous, normal, binomial)"},
            {"subId": "B", "title": "Expected value (weighted average) in decision making"},
            {"subId": "C", "title": "Hypothesis testing and design of experiments (e.g., t-test, outlier testing, analysis of the variance)"},
            {"subId": "D", "title": "Measures of central tendencies and dispersions (e.g., mean, mode, standard deviation, confidence intervals)"},
            {"subId": "E", "title": "Regression and curve fitting"},
            {"subId": "F", "title": "Statistical control (e.g., control limits)"}
        ]
    },
    {
        "id": "3",
        "name": "Engineering Sciences",
        "questions": "4–6",
        "items": [
            {"subId": "A", "title": "Basic dynamics (e.g., friction, force, mass, acceleration, momentum)"},
            {"subId": "B", "title": "Work, energy, and power (as applied to particles or rigid bodies)"},
            {"subId": "C", "title": "Electricity, current, and voltage laws (e.g., charge, energy, current, voltage, power, Kirchhoff's law, Ohm's law)"}
        ]
    },
    {
        "id": "4",
        "name": "Materials Science",
        "questions": "4–6",
        "items": [
            {"subId": "A", "title": "Chemical, electrical, mechanical, and physical properties (e.g., effect of temperature, pressure, stress, strain, failure)"},
            {"subId": "B", "title": "Material types and compatibilities (e.g., engineered materials, ferrous and nonferrous metals)"},
            {"subId": "C", "title": "Corrosion mechanisms and control"},
            {"subId": "D", "title": "Polymers, ceramics, and composites"}
        ]
    },
    {
        "id": "5",
        "name": "Chemistry and Biology",
        "questions": "7–11",
        "items": [
            {"subId": "A", "title": "Inorganic chemistry (e.g., molarity, normality, molality, acids, bases, redox reactions, valence, solubility product, pH, pK, electrochemistry, periodic table)"},
            {"subId": "B", "title": "Organic chemistry (e.g., nomenclature, structure, balanced equations, reactions, synthesis)"},
            {"subId": "C", "title": "Analytical chemistry (e.g., wet chemistry and instrumental chemistry)"},
            {"subId": "D", "title": "Biochemistry, microbiology, and molecular biology (e.g., organization and function of the cell; Krebs, glycolysis, Calvin cycles; enzymes and protein chemistry; genetics; protein synthesis, translation, transcription)"},
            {"subId": "E", "title": "Bioprocessing (e.g., fermentation, biological treatment systems, aerobic, anaerobic process, nutrient removal)"}
        ]
    },
    {
        "id": "6",
        "name": "Fluid Mechanics/Dynamics",
        "questions": "8–12",
        "items": [
            {"subId": "A", "title": "Fluid properties"},
            {"subId": "B", "title": "Dimensionless numbers (e.g., Reynolds number)"},
            {"subId": "C", "title": "Mechanical energy balance (e.g., pipes, valves, fittings, pressure losses across packed beds, pipe networks)"},
            {"subId": "D", "title": "Bernoulli equation (hydrostatic pressure, velocity head)"},
            {"subId": "E", "title": "Laminar and turbulent flow"},
            {"subId": "F", "title": "Flow measurement (e.g., orifices, Venturi meters)"},
            {"subId": "G", "title": "Pumps, turbines, compressors, and vacuum systems"},
            {"subId": "H", "title": "Compressible flow and non-Newtonian fluids"}
        ]
    },
    {
        "id": "7",
        "name": "Thermodynamics",
        "questions": "8–12",
        "items": [
            {"subId": "A", "title": "Thermodynamic properties of pure components and mixtures (e.g., specific volume, internal energy, enthalpy, entropy, free energy, ideal gas law)"},
            {"subId": "B", "title": "Properties data and phase diagrams of pure components and mixtures (e.g., steam tables, psychrometric charts, T-s, P-h, x-y, T-x-y)"},
            {"subId": "C", "title": "Thermodynamic laws (e.g., first law, second law)"},
            {"subId": "D", "title": "Thermodynamic processes (e.g., isothermal, adiabatic, isentropic, phase changes)"},
            {"subId": "E", "title": "Cyclic processes and efficiencies (e.g., power, refrigeration, heat pump)"},
            {"subId": "F", "title": "Phase equilibrium (e.g., fugacity, activity coefficient, Raoult's law)"},
            {"subId": "G", "title": "Chemical equilibrium"},
            {"subId": "H", "title": "Heats of reaction and mixing"}
        ]
    },
    {
        "id": "8",
        "name": "Material/Energy Balances",
        "questions": "10–15",
        "items": [
            {"subId": "A", "title": "Steady-state mass balance"},
            {"subId": "B", "title": "Unsteady-state mass balance"},
            {"subId": "C", "title": "Steady-state energy balance"},
            {"subId": "D", "title": "Unsteady-state energy balance"},
            {"subId": "E", "title": "Recycle/bypass processes"},
            {"subId": "F", "title": "Reactive systems (e.g., combustion)"}
        ]
    },
    {
        "id": "9",
        "name": "Heat Transfer",
        "questions": "8–12",
        "items": [
            {"subId": "A", "title": "Conductive heat transfer"},
            {"subId": "B", "title": "Convective heat transfer (natural and forced)"},
            {"subId": "C", "title": "Radiation heat transfer"},
            {"subId": "D", "title": "Heat-transfer coefficients (e.g., overall, local, fouling)"},
            {"subId": "E", "title": "Heat-transfer equipment, operation, and design (e.g., double pipe, shell and tube, fouling, number of transfer units, log-mean temperature difference, flow configuration)"}
        ]
    },
    {
        "id": "10",
        "name": "Mass Transfer and Separation",
        "questions": "8–12",
        "items": [
            {"subId": "A", "title": "Molecular diffusion (e.g., steady and unsteady state, physical property estimation)"},
            {"subId": "B", "title": "Convective mass transfer (e.g., mass-transfer coefficient, eddy diffusion)"},
            {"subId": "C", "title": "Separation systems (e.g., distillation, absorption, extraction, membrane processes, adsorption)"},
            {"subId": "D", "title": "Equilibrium stage methods (e.g., graphical methods, McCabe-Thiele, efficiency)"},
            {"subId": "E", "title": "Continuous contact methods (e.g., number of transfer units, height equivalent to a theoretical plate, height of transfer unit, number of theoretical plates)"},
            {"subId": "F", "title": "Humidification, drying, and evaporation"}
        ]
    },
    {
        "id": "11",
        "name": "Solids Handling",
        "questions": "3–5",
        "items": [
            {"subId": "A", "title": "Particle properties (e.g., surface and bulk forces, particle size distribution)"},
            {"subId": "B", "title": "Processing (e.g., crushing, grinding, crystallization)"},
            {"subId": "C", "title": "Transportation and storage (e.g., belts, pneumatic, slurries, tanks, hoppers)"}
        ]
    },
    {
        "id": "12",
        "name": "Chemical Reaction Engineering",
        "questions": "7–11",
        "items": [
            {"subId": "A", "title": "Reaction rates and order"},
            {"subId": "B", "title": "Rate constant (e.g., Arrhenius function)"},
            {"subId": "C", "title": "Conversion, yield, and selectivity"},
            {"subId": "D", "title": "Type of reactions (e.g., series, parallel, forward, reverse, homogeneous, heterogeneous, biological)"},
            {"subId": "E", "title": "Reactor types (e.g., batch, semibatch, continuous stirred tank, plug flow, gas phase, liquid phase)"},
            {"subId": "F", "title": "Catalysis (e.g., mechanisms, biocatalysis, physical properties)"}
        ]
    },
    {
        "id": "13",
        "name": "Economics",
        "questions": "4–6",
        "items": [
            {"subId": "A", "title": "Time value of money (e.g., present worth, annual worth, future worth, rate of return)"},
            {"subId": "B", "title": "Economic analyses (e.g., break-even, benefit-cost, optimal economic life)"},
            {"subId": "C", "title": "Uncertainty (e.g., expected value and risk)"},
            {"subId": "D", "title": "Project selection (e.g., comparison of projects with unequal lives, lease/buy/make, depreciation, discounted cash flow)"}
        ]
    },
    {
        "id": "14",
        "name": "Process Design",
        "questions": "7–11",
        "items": [
            {"subId": "A", "title": "Process flow diagrams and piping and instrumentation diagrams"},
            {"subId": "B", "title": "Equipment selection (e.g., sizing and scale-up)"},
            {"subId": "C", "title": "Equipment and facilities cost estimation (e.g., cost indices, equipment costing)"},
            {"subId": "D", "title": "Process design and optimization (e.g., sustainability, efficiency, green engineering, inherently safer design, evaluation of specifications, product design)"},
            {"subId": "E", "title": "Design standards (e.g., regulatory, ASTM, ISO, OSHA)"}
        ]
    },
    {
        "id": "15",
        "name": "Process Control",
        "questions": "4–6",
        "items": [
            {"subId": "A", "title": "Dynamics (e.g., first- and second-order processes, gains and time constants, stability, damping, and transfer functions)"},
            {"subId": "B", "title": "Control strategies (e.g., feedback, feedforward, cascade, ratio, PID controller tuning, alarms, other safety equipment)"},
            {"subId": "C", "title": "Control loop design and hardware (e.g., matching measured and manipulated variables, sensors, control valves, conceptual process control, distributed control system [DCS] programming, programmable logic controller [PLC] programming, interlocks)"}
        ]
    },
    {
        "id": "16",
        "name": "Safety, Health, and Environment",
        "questions": "5–8",
        "items": [
            {"subId": "A", "title": "Hazardous properties of materials, including SDS (e.g., corrosivity, flammability, toxicity, reactivity, handling, storage, transportation)"},
            {"subId": "B", "title": "Industrial hygiene (e.g., toxicity, noise, PPE, ergonomics)"},
            {"subId": "C", "title": "Process safety, risk assessment, and hazard analysis (e.g., layer of protection analysis, hazard and operability [HAZOP] studies, fault and event tree analysis, dispersion modeling)"},
            {"subId": "D", "title": "Overpressure and underpressure protection (e.g., relief, redundant control, inherently safe)"},
            {"subId": "E", "title": "Waste minimization, waste treatment, and regulation (e.g., air, water, solids, RCRA, CWA, other EPA, OSHA)"},
            {"subId": "F", "title": "Reactivity hazards (e.g., inerting, runaway reactions, compatibility)"}
        ]
    },
    {
        "id": "17",
        "name": "Ethics and Professional Practice",
        "questions": "3–5",
        "items": [
            {"subId": "A", "title": "Codes of ethics (professional and technical societies)"},
            {"subId": "B", "title": "Agreements, contracts, and contract law (e.g., noncompete, nondisclosure, memorandum of understanding)"},
            {"subId": "C", "title": "Public health, safety, and welfare (e.g., public protection issues, licensing, professional liability, regulatory issues)"},
            {"subId": "D", "title": "Intellectual property (e.g., copyright, trade secrets, patents, trademarks)"}
        ]
    }
]

# 1. Load data
with open("byu_courses.csv", encoding="utf-8") as f:
    courses = list(csv.DictReader(f))

with open("byu_course_learning_outcomes_itemized.csv", encoding="utf-8") as f:
    itemized = list(csv.DictReader(f))

catalog_items = []
for c in courses:
    desc = c["Course Description"].strip()
    if desc:
        catalog_items.append({
            "courseCode": c["Course Code"],
            "courseTitle": c["Course Title"],
            "catalogUrl": c["Catalog URL"],
            "itemType": "course_description",
            "outcomeIndex": None,
            "outcomeName": "Course Description",
            "text": desc,
            "fullLabel": f"{c['Course Code']} - Course Description"
        })

for row in itemized:
    outcome_text = row["Outcome Objective"].strip()
    outcome_name = row["Outcome Name"].strip()
    idx = row["Outcome Index"].strip()
    if not idx or not (outcome_text or outcome_name):
        continue
    combined_text = f"{outcome_name}: {outcome_text}" if outcome_name and outcome_text else (outcome_name or outcome_text)
    catalog_items.append({
        "courseCode": row["Course Code"],
        "courseTitle": row["Course Title"],
        "catalogUrl": row["Catalog URL"],
        "itemType": "learning_outcome",
        "outcomeIndex": int(idx),
        "outcomeName": outcome_name,
        "text": combined_text,
        "fullLabel": f"{row['Course Code']} - LO #{idx}: {outcome_name}"
    })

matcher = get_refined_matcher()

# Build comprehensive FE coverage data
full_topics_data = []
csv_rows = []

for topic in fe_topics:
    t_id = topic["id"]
    t_name = topic["name"]
    t_questions = topic["questions"]
    
    topic_obj = {
        "id": t_id,
        "name": t_name,
        "questions": t_questions,
        "items": [],
        "totalLoCount": 0,
        "totalDescCount": 0,
        "totalMatchesCount": 0
    }
    
    for item in topic["items"]:
        sub_id = f"{t_id}.{item['subId']}"
        check_fn = matcher.get(sub_id)
        
        matches = []
        if check_fn:
            for c_item in catalog_items:
                c = c_item["courseCode"]
                t = c_item["text"].lower()
                o = (c_item["outcomeName"] or "").lower()
                it = c_item["itemType"]
                if check_fn(c, t, o, it):
                    matches.append(c_item)
                    
        lo_matches = [m for m in matches if m["itemType"] == "learning_outcome"]
        desc_matches = [m for m in matches if m["itemType"] == "course_description"]
        distinct_courses = sorted(list(set(m["courseCode"] for m in matches)))
        
        item_obj = {
            "subId": item["subId"],
            "fullId": sub_id,
            "title": item["title"],
            "loCount": len(lo_matches),
            "descCount": len(desc_matches),
            "totalCount": len(matches),
            "courses": distinct_courses,
            "matches": matches
        }
        
        topic_obj["items"].append(item_obj)
        topic_obj["totalLoCount"] += len(lo_matches)
        topic_obj["totalDescCount"] += len(desc_matches)
        topic_obj["totalMatchesCount"] += len(matches)
        
        courses_str = ", ".join(distinct_courses)
        matches_summary = "; ".join([f"{m['fullLabel']}: {m['text'][:80]}..." for m in matches])
        csv_rows.append({
            "Topic ID": sub_id,
            "Knowledge Area": t_name,
            "Sub-Item Letter": item["subId"],
            "Sub-Item Title": item["title"],
            "FE Questions": t_questions,
            "Learning Outcomes Count": len(lo_matches),
            "Course Descriptions Count": len(desc_matches),
            "Total Coverage Count": len(matches),
            "Covering Courses": courses_str,
            "Details Summary": matches_summary
        })
        
    full_topics_data.append(topic_obj)

# Save JSON
with open("fe_coverage_data.json", "w", encoding="utf-8") as f:
    json.dump(full_topics_data, f, indent=2)

print("Saved fe_coverage_data.json")

# Save CSV
with open("fe_exam_byu_coverage.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Topic ID", "Knowledge Area", "Sub-Item Letter", "Sub-Item Title",
        "FE Questions", "Learning Outcomes Count", "Course Descriptions Count",
        "Total Coverage Count", "Covering Courses", "Details Summary"
    ])
    writer.writeheader()
    writer.writerows(csv_rows)

print("Saved fe_exam_byu_coverage.csv")

# Identify Learning Outcomes not matched to any FE topic
matched_lo_keys = set()
for topic in full_topics_data:
    for item in topic["items"]:
        for m in item["matches"]:
            if m["itemType"] == "learning_outcome":
                matched_lo_keys.add((m["courseCode"], m["outcomeIndex"]))

unmatched_los = []
for row in itemized:
    idx_str = row["Outcome Index"].strip()
    if not idx_str:
        continue
    code = row["Course Code"]
    idx = int(idx_str)
    if (code, idx) not in matched_lo_keys:
        unmatched_los.append({
            "Course Code": code,
            "Course Title": row["Course Title"],
            "Outcome Index": idx,
            "Outcome Name": row["Outcome Name"],
            "Outcome Objective": row["Outcome Objective"],
            "Catalog URL": row["Catalog URL"]
        })

with open("byu_course_learning_outcomes_non_fe.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Course Code", "Course Title", "Outcome Index", "Outcome Name", "Outcome Objective", "Catalog URL"
    ])
    writer.writeheader()
    writer.writerows(unmatched_los)

print(f"Saved byu_course_learning_outcomes_non_fe.csv ({len(unmatched_los)} outcomes)")
