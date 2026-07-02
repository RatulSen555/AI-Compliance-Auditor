import os, json, re, random, logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

_use_gemini = False
_model = None

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

if API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        _model = genai.GenerativeModel("gemini-2.0-flash")
        test = _model.generate_content("Say OK")
        if test and test.text:
            _use_gemini = True
            logger.info("Gemini API connected - real AI mode active")
        else:
            logger.warning("Gemini test returned empty - mock mode")
    except Exception as e:
        logger.warning(f"Gemini unavailable ({type(e).__name__}: {e}) - mock mode")
else:
    logger.info("No GEMINI_API_KEY - mock mode active")


def clean_response(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
    return text.strip()


# ================ MOCK ANALYSES ================

MOCK_ANALYSES = {
    "ISO 45001": {
        "score": 62,
        "summary": "The room shows moderate compliance with ISO 45001 occupational health and safety standards. Several critical gaps were identified in emergency exit accessibility, fire safety equipment placement, and workspace ergonomics that require immediate attention to achieve full compliance.",
        "gaps": [
            {"area": "Emergency Exits", "description": "Emergency exit path appears partially blocked by stored materials, violating ISO 45001 clause 6.1.3 regarding emergency preparedness and response arrangements.", "severity": "high"},
            {"area": "Fire Safety Equipment", "description": "Fire extinguisher is not visibly mounted at the required height and lacks a visible inspection tag, failing to meet ISO 45001 documentation and maintenance requirements.", "severity": "high"},
            {"area": "Ergonomic Setup", "description": "Workstation chairs lack adjustable lumbar support and monitors are positioned below eye level, creating musculoskeletal disorder risks per ISO 45001 risk assessment requirements.", "severity": "medium"},
            {"area": "Floor Safety", "description": "Electrical cables running across walkway without cable covers, creating a trip hazard that contravenes ISO 45001 hazard identification protocols.", "severity": "medium"},
            {"area": "Lighting", "description": "Lighting levels appear below the recommended 300-500 lux for office environments, potentially causing eye strain and reducing task accuracy.", "severity": "low"}
        ],
        "actionPlan": [
            {"action": "Clear all materials from emergency exit pathways and mark floor with high-visibility tape. Conduct weekly walkthroughs.", "priority": "high", "timeline": "Immediate (today)"},
            {"action": "Install fire extinguishers at regulation height (1.2m from floor) with current inspection tags. Schedule quarterly inspections.", "priority": "high", "timeline": "Within 3 days"},
            {"action": "Procure ergonomic chairs with adjustable lumbar support and monitor arms. Adjust all monitors to eye level.", "priority": "medium", "timeline": "Within 2 weeks"},
            {"action": "Install cable management covers on all floor-running cables. Route cables along walls where possible.", "priority": "medium", "timeline": "Within 1 week"},
            {"action": "Upgrade lighting to meet 300-500 lux standard. Add task lighting at individual workstations.", "priority": "low", "timeline": "Within 1 month"}
        ]
    },
    "OSHA": {
        "score": 55,
        "summary": "The room has significant OSHA compliance gaps, particularly around walkway clearance, electrical safety, and PPE availability. Several violations could result in citations during an OSHA inspection.",
        "gaps": [
            {"area": "Walkway Clearance", "description": "Aisles do not maintain the required 28-inch minimum clear width per OSHA 1910.22(a)(2), with boxes obstructing passage.", "severity": "high"},
            {"area": "Electrical Safety", "description": "Power strips are daisy-chained together, violating OSHA 1910.305(g)(2)(iii) prohibition on daisy-chain connections.", "severity": "high"},
            {"area": "First Aid Kit", "description": "No visible first aid kit or emergency contact information posted, violating OSHA 1910.151(b) medical services requirements.", "severity": "high"},
            {"area": "Hazard Communication", "description": "Chemical containers lack required GHS-compliant labels and no Safety Data Sheets are readily accessible.", "severity": "medium"},
            {"area": "Housekeeping", "description": "General housekeeping per OSHA 1910.22(a)(1) not met, with debris, spills, and disorganized materials present.", "severity": "medium"}
        ],
        "actionPlan": [
            {"action": "Clear all walkways to 28-inch minimum width. Mark aisles with yellow floor tape and install permanent signage.", "priority": "high", "timeline": "Immediate (today)"},
            {"action": "Replace daisy-chained power strips with properly rated individual circuits. Have qualified electrician assess needs.", "priority": "high", "timeline": "Within 2 days"},
            {"action": "Install OSHA-compliant first aid kit in visible location with posted emergency contacts.", "priority": "high", "timeline": "Within 1 day"},
            {"action": "Ensure all chemical containers have GHS labels. Compile Safety Data Sheets in accessible binder.", "priority": "medium", "timeline": "Within 1 week"},
            {"action": "Implement daily housekeeping checklist. Assign area ownership and conduct weekly inspections.", "priority": "medium", "timeline": "Within 1 week"}
        ]
    },
    "NEBOSH": {
        "score": 58,
        "summary": "The room demonstrates partial alignment with NEBOSH health and safety management principles. Key deficiencies in risk control measures, safety signage, and ventilation indicate need for systematic risk assessment and improvement plan.",
        "gaps": [
            {"area": "Risk Assessment Display", "description": "No visible risk assessment or hazard register posted, a fundamental NEBOSH requirement for maintaining safety awareness.", "severity": "high"},
            {"area": "Safety Signage", "description": "Required safety signage including fire exit signs, first aid location, and emergency assembly point information is missing.", "severity": "high"},
            {"area": "Ventilation", "description": "Space lacks adequate natural or mechanical ventilation, potentially failing NEBOSH occupational health air quality standards.", "severity": "medium"},
            {"area": "Storage", "description": "Items stored above 1.8m without proper securing, creating falling object hazards per NEBOSH risk control hierarchy.", "severity": "medium"},
            {"area": "PPE Availability", "description": "No PPE station or signage indicating required personal protective equipment for tasks in this area.", "severity": "low"}
        ],
        "actionPlan": [
            {"action": "Conduct and display comprehensive risk assessment with hazard register. Review and update quarterly.", "priority": "high", "timeline": "Within 3 days"},
            {"action": "Install photoluminescent fire exit signs, first aid location signs, and emergency assembly notices.", "priority": "high", "timeline": "Within 5 days"},
            {"action": "Assess ventilation and install mechanical ventilation if natural is insufficient. Monitor CO2 levels.", "priority": "medium", "timeline": "Within 2 weeks"},
            {"action": "Secure all items stored above 1.8m with proper racking. Implement stacking height limits.", "priority": "medium", "timeline": "Within 1 week"},
            {"action": "Install PPE station with appropriate equipment and clear usage signage.", "priority": "low", "timeline": "Within 2 weeks"}
        ]
    },
    "NFPA 101": {
        "score": 48,
        "summary": "The room has critical fire safety deficiencies under NFPA 101 Life Safety Code. Emergency egress, fire protection systems, and compartmentalization require immediate remediation to meet minimum life safety requirements.",
        "gaps": [
            {"area": "Emergency Egress", "description": "Secondary means of egress is obstructed, violating NFPA 101 Chapter 7 requirements for accessible exit access.", "severity": "high"},
            {"area": "Fire Alarm", "description": "No visible fire alarm pull station or smoke detector, failing NFPA 101 fire alarm and detection requirements.", "severity": "high"},
            {"area": "Fire Sprinklers", "description": "No fire sprinkler coverage visible. Depending on occupancy, NFPA 101 may require automatic sprinkler protection.", "severity": "high"},
            {"area": "Compartmentation", "description": "Openings in walls/ceilings may compromise fire-rated compartmentation, allowing fire and smoke spread.", "severity": "medium"},
            {"area": "Exit Signage", "description": "Exit signs missing or not illuminated per NFPA 101 Section 7.10 requirements for visibility and placement.", "severity": "medium"}
        ],
        "actionPlan": [
            {"action": "Immediately clear all exit pathways. Ensure secondary egress is unobstructed and clearly marked.", "priority": "high", "timeline": "Immediate (today)"},
            {"action": "Install fire alarm pull station and smoke detectors. Connect to building fire alarm system.", "priority": "high", "timeline": "Within 1 week"},
            {"action": "Engage fire protection engineer to assess sprinkler requirements based on occupancy classification.", "priority": "high", "timeline": "Within 2 weeks"},
            {"action": "Inspect and restore fire-rated barriers. Seal penetrations with fire-rated materials.", "priority": "medium", "timeline": "Within 1 month"},
            {"action": "Install NFPA 101 compliant exit signs with electrical and photoluminescent backup.", "priority": "medium", "timeline": "Within 2 weeks"}
        ]
    },
    "Fire Safety": {
        "score": 51,
        "summary": "Multiple fire safety deficiencies identified. The space lacks adequate fire prevention measures, detection systems, and emergency response provisions essential for occupant safety.",
        "gaps": [
            {"area": "Fire Extinguishers", "description": "Insufficient coverage. Room requires at least one accessible extinguisher within 75 feet travel distance.", "severity": "high"},
            {"area": "Smoke Detection", "description": "No smoke detectors visible, a critical gap in early fire detection capability.", "severity": "high"},
            {"area": "Evacuation Plan", "description": "No posted evacuation route map or emergency procedures, leaving occupants unaware of protocols.", "severity": "high"},
            {"area": "Flammable Materials", "description": "Flammable materials stored without proper separation, increasing fire load beyond acceptable limits.", "severity": "medium"},
            {"area": "Emergency Lighting", "description": "No emergency lighting or illuminated exit markers for safe evacuation during power failure.", "severity": "medium"}
        ],
        "actionPlan": [
            {"action": "Install ABC-type fire extinguishers within 75 feet of all areas. Schedule annual inspections.", "priority": "high", "timeline": "Within 3 days"},
            {"action": "Install photoelectric smoke detectors at maximum 30-foot spacing on ceiling.", "priority": "high", "timeline": "Within 1 week"},
            {"action": "Create and post evacuation maps at all entrances. Conduct evacuation drill within 30 days.", "priority": "high", "timeline": "Within 5 days"},
            {"action": "Audit flammable material storage. Use approved cabinets with minimum separation distances.", "priority": "medium", "timeline": "Within 2 weeks"},
            {"action": "Install battery-backed emergency lighting along exit paths. Test monthly.", "priority": "medium", "timeline": "Within 2 weeks"}
        ]
    }
}

DEFAULT_MOCK_ANALYSIS = {
    "score": 60,
    "summary": "The room shows moderate compliance with the specified standard. Several areas require attention including safety equipment, signage, and general housekeeping. A structured improvement plan is recommended.",
    "gaps": [
        {"area": "Safety Equipment", "description": "Essential safety equipment is missing, expired, or improperly positioned per the selected compliance standard.", "severity": "high"},
        {"area": "Signage", "description": "Required safety and informational signage is absent or not clearly visible across most standards.", "severity": "medium"},
        {"area": "Housekeeping", "description": "General housekeeping does not meet standard requirements, with items creating potential hazards.", "severity": "medium"},
        {"area": "Documentation", "description": "No visible compliance documentation, checklists, or inspection records posted as required.", "severity": "low"}
    ],
    "actionPlan": [
        {"action": "Audit and install all required safety equipment per standard. Establish inspection schedule.", "priority": "high", "timeline": "Within 1 week"},
        {"action": "Install all required safety signage at designated locations.", "priority": "high", "timeline": "Within 5 days"},
        {"action": "Implement daily housekeeping checklist with assigned responsibilities.", "priority": "medium", "timeline": "Within 1 week"},
        {"action": "Create compliance documentation including inspection logs and training records.", "priority": "low", "timeline": "Within 2 weeks"}
    ]
}


# ================ MOCK QUESTIONS ================

MOCK_QUESTIONS = {
    "ISO 45001": [
        {"id": 1, "question": "What is a risk assessment according to ISO 45001, and what are the key steps when conducting one for a workplace?", "expectedTopics": ["hazard identification", "risk evaluation", "risk control measures", "hierarchy of controls", "documentation"], "difficulty": "medium"},
        {"id": 2, "question": "Can you explain the Plan-Do-Check-Act cycle in the context of ISO 45001 and how it drives continuous improvement?", "expectedTopics": ["PDCA cycle", "continual improvement", "management review", "performance evaluation", "corrective actions"], "difficulty": "medium"},
        {"id": 3, "question": "What legal and regulatory requirements must an organization consider when implementing ISO 45001?", "expectedTopics": ["legal register", "regulatory compliance", "legislation monitoring", "compliance evaluation", "due diligence"], "difficulty": "hard"},
        {"id": 4, "question": "Describe the role of worker participation and consultation in ISO 45001. Why is it critical?", "expectedTopics": ["worker consultation", "participation mechanisms", "safety committees", "reporting systems", "empowerment"], "difficulty": "easy"},
        {"id": 5, "question": "What types of emergencies should an ISO 45001 compliant organization prepare for?", "expectedTopics": ["emergency preparedness", "evacuation procedures", "drill frequency", "first aid provisions", "incident reporting"], "difficulty": "easy"}
    ],
    "OSHA": [
        {"id": 1, "question": "What is the OSHA General Duty Clause, and how does it apply to workplace hazards not covered by specific standards?", "expectedTopics": ["Section 5(a)(1)", "recognized hazards", "employer responsibility", "reasonable care", "enforcement"], "difficulty": "medium"},
        {"id": 2, "question": "Explain the OSHA hazard communication standard. What must employers do for chemical safety compliance?", "expectedTopics": ["GHS labels", "safety data sheets", "written program", "employee training", "chemical inventory"], "difficulty": "medium"},
        {"id": 3, "question": "What are the key requirements for OSHA-compliant walking-working surfaces?", "expectedTopics": ["1910.22", "housekeeping", "floor maintenance", "guardrails", "fall protection"], "difficulty": "easy"},
        {"id": 4, "question": "Describe OSHA recordkeeping requirements. What must be recorded on the OSHA 300 log?", "expectedTopics": ["OSHA 300 log", "recordable injuries", "fatality reporting", "privacy cases", "retention"], "difficulty": "hard"},
        {"id": 5, "question": "What rights do employees have under OSHA regarding safety complaints and inspections?", "expectedTopics": ["employee rights", "whistleblower protection", "complaint process", "inspection procedures", "citation appeals"], "difficulty": "medium"}
    ],
    "NEBOSH": [
        {"id": 1, "question": "Explain the NEBOSH hierarchy of risk controls with practical examples of each level.", "expectedTopics": ["elimination", "substitution", "engineering controls", "administrative controls", "PPE"], "difficulty": "easy"},
        {"id": 2, "question": "What is the ALARP principle and how does it relate to risk tolerability?", "expectedTopics": ["ALARP", "risk tolerance", "reasonably practicable", "cost-benefit analysis", "residual risk"], "difficulty": "hard"},
        {"id": 3, "question": "Describe the key elements of a health and safety management system as defined by NEBOSH.", "expectedTopics": ["policy", "organizing", "planning", "measuring performance", "auditing"], "difficulty": "medium"},
        {"id": 4, "question": "What are the main types of workplace inspections and how do you conduct an effective safety tour?", "expectedTopics": ["safety tours", "safety sampling", "safety surveys", "checklists", "reporting"], "difficulty": "medium"},
        {"id": 5, "question": "Explain the difference between immediate and underlying causes of accidents.", "expectedTopics": ["immediate causes", "root causes", "incident investigation", "causation models", "corrective actions"], "difficulty": "hard"}
    ],
    "NFPA 101": [
        {"id": 1, "question": "What are the fundamental occupancy classifications under NFPA 101 and how do requirements change?", "expectedTopics": ["occupancy types", "hazard of contents", "occupant load", "egress requirements", "fire protection"], "difficulty": "medium"},
        {"id": 2, "question": "Explain NFPA 101 requirements for means of egress. What are the three components?", "expectedTopics": ["exit access", "exit", "exit discharge", "travel distance", "capacity"], "difficulty": "medium"},
        {"id": 3, "question": "What are NFPA requirements for fire alarm systems and when are they mandatory?", "expectedTopics": ["fire alarm initiation", "notification appliances", "monitoring", "occupancy thresholds", "pull stations"], "difficulty": "hard"},
        {"id": 4, "question": "Describe NFPA 101 emergency lighting requirements. Where must it be installed?", "expectedTopics": ["emergency lighting", "illumination levels", "battery backup", "exit signs", "testing"], "difficulty": "easy"},
        {"id": 5, "question": "What are NFPA 101 fire extinguisher requirements for various occupancy types?", "expectedTopics": ["extinguisher types", "placement distance", "travel distance", "inspection frequency", "maintenance"], "difficulty": "easy"}
    ],
    "Fire Safety": [
        {"id": 1, "question": "What are the main classes of fire and which extinguisher type is appropriate for each?", "expectedTopics": ["Class A", "Class B", "Class C", "Class D", "Class K", "extinguisher types"], "difficulty": "easy"},
        {"id": 2, "question": "Describe the key components of a fire safety evacuation plan and practice frequency.", "expectedTopics": ["evacuation routes", "assembly points", "fire wardens", "drill frequency", "special needs"], "difficulty": "medium"},
        {"id": 3, "question": "What is the fire triangle and fire tetrahedron? How does this help in fire prevention?", "expectedTopics": ["heat", "fuel", "oxygen", "chemical chain reaction", "prevention methods"], "difficulty": "easy"},
        {"id": 4, "question": "Explain the importance of fire compartmentation in building design.", "expectedTopics": ["fire-rated walls", "fire doors", "fire dampers", "penetration sealing", "compartment sizes"], "difficulty": "hard"},
        {"id": 5, "question": "What are common causes of workplace fires and what preventive measures should be implemented?", "expectedTopics": ["electrical hazards", "flammable storage", "hot work", "housekeeping", "fire safety training"], "difficulty": "medium"}
    ]
}

DEFAULT_MOCK_QUESTIONS = [
    {"id": 1, "question": "What is the primary purpose of a compliance audit and what key areas should be covered?", "expectedTopics": ["audit objectives", "hazard identification", "risk assessment", "regulatory requirements", "documentation"], "difficulty": "easy"},
    {"id": 2, "question": "Describe the key elements of an effective safety management system.", "expectedTopics": ["management commitment", "risk management", "competence and training", "monitoring", "continuous improvement"], "difficulty": "medium"},
    {"id": 3, "question": "How would you prioritize identified compliance gaps?", "expectedTopics": ["risk prioritization", "severity assessment", "resource allocation", "timeline planning", "stakeholder communication"], "difficulty": "medium"},
    {"id": 4, "question": "What documentation is required to demonstrate compliance?", "expectedTopics": ["policies", "inspection records", "training logs", "risk assessments", "corrective action records"], "difficulty": "hard"},
    {"id": 5, "question": "Explain the role of employee training in maintaining compliance.", "expectedTopics": ["induction training", "refresher training", "emergency procedures", "hazard awareness", "training records"], "difficulty": "easy"}
]


# ================ MOCK SCORER ================

def _mock_score(question: str, answer: str, expected_topics: list) -> dict:
    answer_lower = answer.lower()
    topics_covered = []
    for topic in expected_topics:
        topic_words = topic.lower().split()
        if any(w in answer_lower for w in topic_words if len(w) > 3):
            topics_covered.append(topic)

    coverage = len(topics_covered) / max(len(expected_topics), 1)
    word_count = len(answer.split())
    length_score = min(1.0, word_count / 40)
    base = int((coverage * 0.6 + length_score * 0.4) * 18 + 2)
    score = max(2, min(20, base))
    missed = [t for t in expected_topics if t not in topics_covered]

    if score >= 15:
        feedback = f"Strong answer demonstrating good understanding. Covered {len(topics_covered)}/{len(expected_topics)} expected topics. Well-structured with practical knowledge."
    elif score >= 10:
        feedback = f"Decent attempt but key areas missed. Covered {len(topics_covered)}/{len(expected_topics)} topics. Be more comprehensive and reference specific standards."
    else:
        feedback = f"Answer needs significant improvement. Only {len(topics_covered)}/{len(expected_topics)} topics addressed. Study the relevant standard sections more thoroughly."

    strengths = []
    if len(topics_covered) >= 3:
        strengths.append("Good coverage of multiple key topics")
    if word_count > 30:
        strengths.append("Provided adequate detail")
    if topics_covered:
        strengths.append(f"Demonstrated knowledge of: {', '.join(topics_covered[:3])}")
    if not strengths:
        strengths.append("Attempted to answer the question")

    return {"score": score, "feedback": feedback, "missedPoints": missed, "strengths": strengths}


# ================ PUBLIC FUNCTIONS ================

def analyze_image(image_bytes: bytes, mime_type: str, standard: str) -> dict:
    if _use_gemini and _model:
        try:
            prompt = f"""You are a compliance auditor AI. Analyze this room photo against "{standard}" standards.
Return ONLY valid JSON (no markdown, no explanation):
{{
  "score": <number 0-100>,
  "summary": "<brief 2-3 sentence summary>",
  "gaps": [
    {{"area": "<gap area>", "description": "<what's wrong>", "severity": "<high/medium/low>"}}
  ],
  "actionPlan": [
    {{"action": "<what to do>", "priority": "<high/medium/low>", "timeline": "<estimated time>"}}
  ]
}}"""
            response = _model.generate_content([
                {"mime_type": mime_type, "data": image_bytes},
                prompt
            ])
            return json.loads(clean_response(response.text))
        except Exception as e:
            logger.warning(f"Gemini analyze failed ({type(e).__name__}), using mock")
    # Fallback to mock
    base = MOCK_ANALYSES.get(standard, DEFAULT_MOCK_ANALYSIS)
    score = max(0, min(100, base["score"] + random.randint(-5, 5)))
    return {"score": score, "summary": base["summary"], "gaps": base["gaps"], "actionPlan": base["actionPlan"]}


def generate_questions(standard: str) -> dict:
    if _use_gemini and _model:
        try:
            prompt = f"""You are a compliance interviewer. Generate 5 interview questions about "{standard}" compliance for a room audit.
Return ONLY valid JSON:
{{
  "questions": [
    {{"id": 1, "question": "<question text>", "expectedTopics": ["<topic1>", "<topic2>"], "difficulty": "<easy/medium/hard>"}}
  ]
}}"""
            response = _model.generate_content(prompt)
            return json.loads(clean_response(response.text))
        except Exception as e:
            logger.warning(f"Gemini questions failed ({type(e).__name__}), using mock")
    # Fallback to mock
    qs = MOCK_QUESTIONS.get(standard, DEFAULT_MOCK_QUESTIONS)
    return {"questions": qs}


def score_answer(question: str, answer: str, expected_topics: list) -> dict:
    if _use_gemini and _model:
        try:
            prompt = f"""You are scoring a compliance interview answer.
Question: {question}
Answer: {answer}
Expected topics to cover: {json.dumps(expected_topics)}
Return ONLY valid JSON:
{{
  "score": <number 0-20>,
  "feedback": "<detailed feedback>",
  "missedPoints": ["<missed topic>"],
  "strengths": ["<strength>"]
}}"""
            response = _model.generate_content(prompt)
            return json.loads(clean_response(response.text))
        except Exception as e:
            logger.warning(f"Gemini score failed ({type(e).__name__}), using mock")
    # Fallback to mock
    return _mock_score(question, answer, expected_topics)