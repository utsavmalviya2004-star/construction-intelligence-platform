"""
Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1
Production-Ready Streamlit Application with Gemini Multimodal Integration
"""

import os
import json
import io
import urllib.parse
from PIL import Image
import streamlit as st

# ---------------------------------------------------------
# Page Configuration & Custom CSS Injection
# ---------------------------------------------------------
st.set_page_config(
    page_title="Multimodal Construction Intelligence",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    /* Metric & Card styling */
    .metric-container {
        background-color: #1a1e24;
        border: 1px solid #2d3748;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .badge-critical {
        background-color: #ef4444;
        color: white;
        padding: 3px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-high {
        background-color: #f97316;
        color: white;
        padding: 3px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-medium {
        background-color: #eab308;
        color: black;
        padding: 3px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-low {
        background-color: #22c55e;
        color: white;
        padding: 3px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .weather-alert-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-left: 5px solid #f59e0b;
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .status-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .status-pass { background-color: #064e3b; color: #6ee7b7; border: 1px solid #059669; }
    .status-warn { background-color: #78350f; color: #fde68a; border: 1px solid #d97706; }
    .status-fail { background-color: #7f1d1d; color: #fca5a5; border: 1px solid #dc2626; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar Configuration & Setup
# ---------------------------------------------------------
with st.sidebar:
    st.title("🏗️ BuildIntel AI")
    st.caption("Capstone Project 1 | Multimodal Platform")
    
    st.markdown("---")
    st.subheader("🔑 Authentication")
    api_key_input = st.text_input(
        "Google Gemini API Key",
        type="password",
        help="Leave blank to run in Demonstration/Offline Sandbox mode with synthetic inference."
    )
    
    # Check key availability
    has_api_key = bool(api_key_input.strip() or os.getenv("GEMINI_API_KEY"))
    active_api_key = api_key_input.strip() if api_key_input.strip() else os.getenv("GEMINI_API_KEY")

    if has_api_key:
        st.success("API Key Detected: Live Multimodal Mode", icon="🟢")
    else:
        st.info("No Key Found: Running in Simulation Mode", icon="ℹ️")

    st.markdown("---")
    st.subheader("🏛️ Architecture Overview")
    st.markdown(
        """
        - **Model Engine**: Gemini 2.5 Flash Multimodal
        - **Compliance**: OSHA 1926 & IS 456:2000
        - **Generative 3D**: Pollinations Engine
        - **Data Pipeline**: Zero-DB Client-Side State
        """
    )
    st.caption("v1.0.0-production | Streamlit Community Ready")

# ---------------------------------------------------------
# LLM / Gemini Multimodal Utility Functions
# ---------------------------------------------------------
def call_gemini_multimodal(image: Image.Image, prompt: str, is_json: bool = True):
    """
    Invokes Google GenAI SDK if an API key is available;
    otherwise returns realistic domain fallback responses.
    """
    if has_api_key:
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=active_api_key)
            
            # Convert PIL image to bytes
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_bytes = buffered.getvalue()

            config_args = {}
            if is_json:
                config_args["response_mime_type"] = "application/json"

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
                    prompt
                ],
                config=types.GenerateContentConfig(**config_args) if config_args else None
            )
            
            if is_json:
                # Strip markdown code fence if wrapped
                clean_text = response.text.strip()
                if clean_text.startswith("```json"):
                    clean_text = clean_text[7:]
                if clean_text.startswith("```"):
                    clean_text = clean_text[3:]
                if clean_text.endswith("```"):
                    clean_text = clean_text[:-3]
                return json.loads(clean_text)
            return response.text
        except Exception as e:
            st.warning(f"Live API call encountered an error: {e}. Switching to synthetic validation response.")
    
    # High-fidelity Fallback Simulation
    if is_json and "ppe_detection" in prompt:
        return {
            "safety_score": 68,
            "overall_status": "Conditional Compliance (Remediation Required)",
            "standards_referenced": ["OSHA 29 CFR 1926.100", "IS 456:2000 Section 3.2"],
            "ppe_detection": {
                "helmets_hard_hats": {"detected": True, "compliant_count": 3, "non_compliant_count": 1},
                "high_visibility_vests": {"detected": True, "compliant_count": 2, "non_compliant_count": 2},
                "steel_toe_boots": {"detected": True, "compliant_count": 4, "non_compliant_count": 0},
                "safety_harnesses_fall_arrest": {"detected": False, "compliant_count": 0, "non_compliant_count": 1}
            },
            "identified_hazards": [
                {
                    "hazard": "Worker observed working near open edge without anchored safety harness.",
                    "severity": "Critical",
                    "standard_violation": "OSHA 1926.501(b)(1) Fall Protection",
                    "corrective_remedy": "Suspend elevated work immediately; enforce twin-lanyard 100% tie-off lifelines."
                },
                {
                    "hazard": "Subcontractor technician operating grinding equipment without reflective vest.",
                    "severity": "Medium",
                    "standard_violation": "IS 456 safety protocol & OSHA 1926.201",
                    "corrective_remedy": "Issue Class 2 high-visibility apparel prior to site re-entry."
                }
            ]
        }
    elif is_json and "crack_type" in prompt:
        return {
            "crack_type": "Structural Shear Defect",
            "confidence_score": 0.93,
            "estimated_width_mm": 3.8,
            "severity_level": "High",
            "urgency": "Immediate intervention within 48-72 hours",
            "root_causes": [
                "Differential settlement of primary pile cap foundation",
                "Shear stress exceeding tensile capacity per IS 456 shear reinforcement limits",
                "Thermal cyclic contraction across unreinforced construction joints"
            ],
            "engineering_repairs": [
                "Low-pressure structural epoxy injection (viscosity <200 cps)",
                "Installation of carbon fiber reinforced polymer (CFRP) shear wraps",
                "Sub-surface foundation pressure re-grouting and geotechnical settlement monitoring"
            ],
            "is_load_bearing_risk": True
        }
    
    return "Demo response generated. Connect your Gemini API key in the sidebar for live multimodal reasoning."

def call_gemini_chat(chat_history, user_message, context=""):
    """Multi-turn construction engineering assistant"""
    if has_api_key:
        try:
            from google import genai

            client = genai.Client(api_key=active_api_key)
            system_prompt = (
                "You are an expert Structural Engineer, Project Manager, and OSHA/IS 456 Inspector. "
                "Provide authoritative, accurate, and concise field guidance with formulas and standards where relevant.\n"
                f"Current Site Context:\n{context}"
            )
            # Format history for prompt
            conversation_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
            full_prompt = f"{system_prompt}\n\nConversation:\n{conversation_str}\nUser: {user_message}\nAssistant:"

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt
            )
            return response.text
        except Exception as e:
            return f"⚠️ API Error: {str(e)}. Fallback: Check local site guidelines per IS 456 clause 5.4."
    
    # Fallback simulation response
    return (
        f"[Demonstration Mode] Based on standard construction protocols: Ensure all curing follows IS 456 "
        f"(minimum 7 to 14 days under standard conditions). For weather risk '{context}', suspend high-elevation "
        f"lifts and double-check formwork lateral bracings."
    )

# ---------------------------------------------------------
# Main Application Tabs
# ---------------------------------------------------------
st.title("🏗️ Multimodal Construction Intelligence Platform")
st.markdown(
    "Automated site safety monitoring, AI crack diagnostic telemetry, project valuation analytics, "
    "and weather-informed engineering decision support."
)

tab1, tab2, tab3, tab4 = st.tabs([
    "🦺 Site Safety & PPE Audit",
    "🔍 Crack Diagnostics & Structural Integrity",
    "📊 Planning & Real Estate Valuation",
    "⛅ Daily Site Assistant & Weather Advisory"
])

# =========================================================
# TAB 1: SITE SAFETY & PPE AUDIT (EPIC 2)
# =========================================================
with tab1:
    st.header("Site Safety & OSHA / IS 456 PPE Compliance Audit")
    st.write(
        "Upload site surveillance feeds or high-resolution photos to conduct an automated multimodal "
        "compliance check for PPE gear (helmets, vests, boots, harnesses) and real-time hazard classification."
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_safety_img = st.file_uploader(
            "Upload Construction Site Image (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            key="safety_uploader"
        )
        if uploaded_safety_img:
            image_safety = Image.open(uploaded_safety_img)
            st.image(image_safety, caption="Uploaded Inspection View", use_container_width=True)

    with col2:
        if uploaded_safety_img:
            if st.button("Run Comprehensive Safety Audit", type="primary", use_container_width=True):
                with st.spinner("Executing multimodal vision inference against OSHA 1926 & IS 456 standards..."):
                    ppe_prompt = """
                    You are a certified senior OSHA Construction Safety Inspector and IS 456 Quality Auditor.
                    Analyze this construction site image with high precision.
                    
                    Return a STRICT JSON response with this exact schema:
                    {
                        "safety_score": <integer between 0 and 100>,
                        "overall_status": "<Compliant Compliance Conditional Non-Compliant |>",
                        "standards_referenced": ["OSHA 1926.xxx", "IS 456:2000 Section ..."],
                        "ppe_detection": {
                            "helmets_hard_hats": {"detected": true/false, "compliant_count": int, "non_compliant_count": int},
                            "high_visibility_vests": {"detected": true/false, "compliant_count": int, "non_compliant_count": int},
                            "steel_toe_boots": {"detected": true/false, "compliant_count": int, "non_compliant_count": int},
                            "safety_harnesses_fall_arrest": {"detected": true/false, "compliant_count": int, "non_compliant_count": int}
                        },
                        "identified_hazards": [
                            {
                                "hazard": "Description of hazard",
                                "severity": "Low" | "Medium" | "High" | "Critical",
                                "standard_violation": "Specific code/standard citation",
                                "corrective_remedy": "Clear engineering or operational corrective action"
                            }
                        ]
                    }
                    """
                    result = call_gemini_multimodal(image_safety, ppe_prompt, is_json=True)
                    st.session_state["ppe_audit_result"] = result

        if "ppe_audit_result" in st.session_state:
            res = st.session_state["ppe_audit_result"]
            
            # Top-level KPI score display
            score = res.get("safety_score", 0)
            status_text = res.get("overall_status", "Audited")
            
            status_class = "status-pass" if score >= 80 else ("status-warn" if score >= 50 else "status-fail")
            
            st.markdown(f"### Safety Audit Result: <span class='status-pill {status_class}'>{status_text}</span>", unsafe_allow_html=True)
            
            m_col1, m_col2 = st.columns(2)
            with m_col1:
                st.metric(label="Safety Index Score", value=f"{score}/100", delta=f"{score - 75}% vs Benchmark")
            with m_col2:
                st.metric(label="Critical Hazards", value=len([h for h in res.get("identified_hazards", []) if h.get("severity") in ["High", "Critical"]]))

            # PPE Checklist Table
            st.subheader("PPE Compliance Checklist")
            ppe_data = res.get("ppe_detection", {})
            for item, details in ppe_data.items():
                col_name, col_status = st.columns([2, 1])
                with col_name:
                    st.write(f"**{item.replace('_', ' ').title()}**")
                with col_status:
                    comp = details.get("compliant_count", 0)
                    non_comp = details.get("non_compliant_count", 0)
                    if non_comp == 0 and comp > 0:
                        st.markdown("<span class='badge-low'>100% Compliant</span>", unsafe_allow_html=True)
                    elif non_comp > 0:
                        st.markdown(f"<span class='badge-critical'>{non_comp} Violation(s)</span>", unsafe_allow_html=True)
                    else:
                        st.caption("Not Observed")

            # Hazards Breakdown
            st.subheader("Identified Site Hazards & Remediation")
            for h in res.get("identified_hazards", []):
                sev = h.get("severity", "Medium")
                badge_class = f"badge-{sev.lower()}"
                st.markdown(
                    f"""
                    <div style="border-left: 4px solid #4a5568; padding: 10px 14px; margin-bottom: 8px; background: rgba(255,255,255,0.03); border-radius: 4px;">
                        <div><span class='{badge_class}'>{sev.upper()}</span> <strong>{h.get('hazard')}</strong></div>
                        <div style="font-size:0.85rem; color:#94a3b8; margin-top:4px;">Violation: {h.get('standard_violation')}</div>
                        <div style="font-size:0.85rem; color:#38bdf8; margin-top:2px;">Remedy: {h.get('corrective_remedy')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # JSON Export
            st.download_button(
                label="📥 Download OSHA/IS 456 JSON Audit Report",
                data=json.dumps(res, indent=2),
                file_name="site_safety_audit_report.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.info("Upload an image on the left and run the audit to preview inspection metrics.")

# =========================================================
# TAB 2: CRACK DIAGNOSTICS & STRUCTURAL INTEGRITY (EPIC 2)
# =========================================================
with tab2:
    st.header("Automated Crack Diagnostics & Concrete Structural Telemetry")
    st.write(
        "Upload surface photography of beams, columns, masonry walls, or bridge abutments. "
        "The model classifies structural crack regimes per IS 456/ACI 224R guidelines."
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_crack_img = st.file_uploader(
            "Upload Concrete / Masonry Image",
            type=["jpg", "jpeg", "png"],
            key="crack_uploader"
        )
        if uploaded_crack_img:
            image_crack = Image.open(uploaded_crack_img)
            st.image(image_crack, caption="Defect Region of Interest", use_container_width=True)

    with col2:
        if uploaded_crack_img:
            if st.button("Perform Defect Structural Analysis", type="primary", use_container_width=True):
                with st.spinner("Analyzing micro-fractures, load trajectories, and spalling risk..."):
                    crack_prompt = """
                    You are a Principal Forensic Structural Engineer specializing in concrete degradation and crack classification.
                    Analyze this concrete or masonry structural defect.
                    
                    Return a STRICT JSON response with this schema:
                    {
                        "crack_type": "Hairline | Settlement | Structural Shear | Thermal Expansion | Spalling",
                        "confidence_score": <float between 0.0 and 1.0>,
                        "estimated_width_mm": <float estimated crack width in mm>,
                        "severity_level": "Low" | "Medium" | "High" | "Critical",
                        "urgency": "Immediate intervention timeframe guidance",
                        "root_causes": ["Cause 1", "Cause 2", "Cause 3"],
                        "engineering_repairs": [
                            "Specific repair technique (e.g. epoxy injection, structural re-grouting, stitching, carbon fiber jacketing)"
                        ],
                        "is_load_bearing_risk": true/false
                    }
                    """
                    crack_result = call_gemini_multimodal(image_crack, crack_prompt, is_json=True)
                    st.session_state["crack_diag_result"] = crack_result

        if "crack_diag_result" in st.session_state:
            c_res = st.session_state["crack_diag_result"]
            
            c_type = c_res.get("crack_type", "Structural Defect")
            width = c_res.get("estimated_width_mm", 0.0)
            sev = c_res.get("severity_level", "Medium")
            urgency = c_res.get("urgency", "Review within standard lifecycle")
            load_bearing = c_res.get("is_load_bearing_risk", False)

            # Metrics row
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("Defect Classification", c_type)
            with col_m2:
                st.metric("Est. Crack Width", f"{width} mm", delta="Tolerance Exceeded" if width > 0.3 else "Within Limits")
            with col_m3:
                badge_class = f"badge-{sev.lower()}"
                st.markdown(f"**Severity**: <span class='{badge_class}'>{sev.upper()}</span>", unsafe_allow_html=True)
                st.caption(f"Load Bearing Risk: {'🚨 YES' if load_bearing else '🟢 NO'}")

            st.markdown(f"**Intervention Timeline**: `{urgency}`")

            # Root Causes & Remedies
            st.subheader("Root Cause Analysis")
            for rc in c_res.get("root_causes", []):
                st.markdown(f"- ⚠️ {rc}")

            st.subheader("Recommended Engineering Remediation")
            for rep in c_res.get("engineering_repairs", []):
                st.markdown(f"- 🔧 **{rep}**")

            st.download_button(
                label="📥 Download Forensic Structural Report",
                data=json.dumps(c_res, indent=2),
                file_name="structural_crack_diagnostic.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.info("Upload an image of the concrete wall or slab to initiate diagnostic scan.")

# =========================================================
# TAB 3: PLANNING & REAL ESTATE VALUATION (EPIC 3)
# =========================================================
with tab3:
    st.header("Project Budgeting, Material Requirements & Asset Valuation")
    st.write(
        "Estimate Indian market construction cost per built-up area (IS benchmarks), forecast steel & cement "
        "consumption, calculate capital expenditure incurred, and generate conceptual architectural previews."
    )

    col_in1, col_in2 = st.columns([1, 1])

    with col_in1:
        st.subheader("📐 Project Specifications")
        structure_type = st.selectbox(
            "Structure Classification",
            ["Residential High-Rise (RCC)", "Commercial Grade-A Office", "Industrial PEB Warehouse", "Luxury Villa Development"]
        )
        built_up_sqft = st.number_input("Total Built-Up Area (sq. ft.)", min_value=1000, max_value=2000000, value=25000, step=1000)
        location_tier = st.selectbox("Location Tier", ["Tier 1 (Metro: Mumbai, Bengaluru, Delhi NCR)", "Tier 2 (Pune, Hyderabad, Ahmedabad, Jaipur)", "Tier 3 (Emerging Urban Centers)"])
        completion_pct = st.slider("Project Completion Progress (%)", min_value=0, max_value=100, value=45)

    # Cost Matrix & Estimation Engine (INR)
    base_costs = {
        "Residential High-Rise (RCC)": {"Tier 1": 2400, "Tier 2": 1950, "Tier 3": 1600},
        "Commercial Grade-A Office": {"Tier 1": 3100, "Tier 2": 2500, "Tier 3": 2100},
        "Industrial PEB Warehouse": {"Tier 1": 1750, "Tier 2": 1450, "Tier 3": 1200},
        "Luxury Villa Development": {"Tier 1": 4200, "Tier 2": 3400, "Tier 3": 2800}
    }
    
    tier_key = "Tier 1" if "Tier 1" in location_tier else ("Tier 2" if "Tier 2" in location_tier else "Tier 3")
    rate_per_sqft = base_costs[structure_type][tier_key]
    
    # Financial calculations
    total_project_cost_inr = built_up_sqft * rate_per_sqft
    capex_incurred_inr = total_project_cost_inr * (completion_pct / 100.0)
    
    # Valuation appreciation factor based on progress & market tier
    valuation_multiplier = 1.30 if tier_key == "Tier 1" else (1.22 if tier_key == "Tier 2" else 1.15)
    current_asset_valuation_inr = capex_incurred_inr * valuation_multiplier

    # Material calculations (Rules of thumb per sq ft in Indian construction)
    # Cement: ~0.4 bags/sqft, Steel: ~3.5 kg/sqft
    cement_bags_needed = int(built_up_sqft * 0.40)
    steel_metric_tonnes = round((built_up_sqft * 3.75) / 1000, 1)

    def format_inr(val):
        if val >= 10000000:
            return f"₹{val / 10000000:.2f} Cr"
        elif val >= 100000:
            return f"₹{val / 100000:.2f} Lakhs"
        return f"₹{val:,.0f}"

    with col_in2:
        st.subheader("💰 Capital Analytics & Valuation")
        st.progress(completion_pct / 100, text=f"Milestone Progress: {completion_pct}% Work Complete")

        fin_col1, fin_col2 = st.columns(2)
        with fin_col1:
            st.metric("Total Project Budget", format_inr(total_project_cost_inr), help=f"Estimated at ₹{rate_per_sqft}/sq.ft.")
            st.metric("CapEx Incurred to Date", format_inr(capex_incurred_inr))
        with fin_col2:
            st.metric("Current Asset Valuation", format_inr(current_asset_valuation_inr), delta=f"+{int((valuation_multiplier-1)*100)}% Unrealized Margin")
            st.metric("Cement / Steel Demand", f"{cement_bags_needed:,} bags | {steel_metric_tonnes} MT")

    st.markdown("---")
    st.subheader("🎨 Conceptual 3D Architectural Visualization (Pollinations Engine)")
    st.write("Generate an AI architectural render of this planned facility for investor pitch decks.")

    arch_style = st.selectbox("Design Language", ["Parametric Biophilic Modernism", "Brutalist Exposed Concrete & Glass", "Contemporary Indian Vernacular", "Sleek Ultra-Minimalist Curtain Wall"])
    render_button = st.button("Generate Architectural Visualisation", type="secondary")

    if render_button:
        with st.spinner("Synthesizing 3D architectural rendering via Pollinations AI..."):
            render_prompt = (
                f"Photorealistic 3D architectural render of a {structure_type}, {arch_style}, "
                f"located in {location_tier}, dynamic sunset golden hour lighting, 8k resolution, octane render, architectural photography"
            )
            encoded_prompt = urllib.parse.quote(render_prompt)
            pollinations_url = f"[https://image.pollinations.ai/prompt/](https://image.pollinations.ai/prompt/){encoded_prompt}?width=1200&height=675&nologo=true&seed=42"
            
            st.image(pollinations_url, caption=f"AI Generated Concept: {structure_type} ({arch_style})", use_container_width=True)
            st.caption(f"Prompt Seed: `{render_prompt}`")

# =========================================================
# TAB 4: DAILY SITE ASSISTANT & WEATHER ADVISORY (EPIC 5)
# =========================================================
with tab4:
    st.header("Daily Field Assistant & Weather-Aware Advisory")
    st.write(
        "Dynamic protocol dispatch calibrated to micrometeorological hazards, backed by an interactive "
        "multi-turn structural engineering assistant chatbot."
    )

    # Weather Selector Section
    col_w1, col_w2 = st.columns([1, 2])
    with col_w1:
        weather_condition = st.selectbox(
            "Current Field Weather Condition",
            ["Normal (Sunny / Clear)", "High Wind (>45 km/h)", "Heavy Rain / Monsoon Inundation", "Extreme Heat (>40°C)"]
        )

    # Weather dynamic alerts logic
    weather_protocols = {
        "Normal (Sunny / Clear)": {
            "title": "🟢 Normal Operational Status",
            "alert": "Standard daily operations permitted. Maintain regular water misting for concrete curing and verify dust suppression protocols.",
            "checkpoints": ["Standard PPE enforcement", "Routine equipment inspection", "Regular curing cycles"]
        },
        "High Wind (>45 km/h)": {
            "title": "⚠️ Severe Wind Hazard: Crane & Lift Suspension",
            "alert": "MANDATORY HALT: Suspend tower crane lifts, external cradle access, and loose sheet roofing installation immediately per OSHA 1926.1431.",
            "checkpoints": ["Lock and weathervane tower cranes", "Secure scaffolding ties and perimeter debris nettings", "Evacuate external cantilevered platforms"]
        },
        "Heavy Rain / Monsoon Inundation": {
            "title": "🌧️ Flood & Electrical Shock Protocol",
            "alert": "Dewatertrenching and deep excavations immediately. De-energize temporary ground electrical distribution boxes per IS 456 / NFPA 70E.",
            "checkpoints": ["Verify shoring integrity on open trenches", "Halt un-shielded concrete pours to prevent water-cement ratio corruption", "Isolate electrical junction boxes"]
        },
        "Extreme Heat (>40°C)": {
            "title": "☀️ Concrete Flash-Set & Heat Stress Protocol",
            "alert": "Implement hot-weather concreting procedures per ACI 305R: Use chilled mix water or liquid nitrogen dosing to keep fresh concrete under 32°C. Provide shaded worker hydration stations.",
            "checkpoints": ["Shift heavy pours to night/early morning hours", "Enforce 20-min hydration rotations for steel-tying teams", "Apply immediate curing compound to prevent plastic shrinkage cracking"]
        }
    }

    selected_weather = weather_protocols[weather_condition]

    with col_w2:
        st.markdown(
            f"""
            <div class="weather-alert-card">
                <h4 style="margin:0 0 8px 0; color:#f59e0b;">{selected_weather['title']}</h4>
                <p style="margin:0 0 10px 0; color:#e2e8f0; font-size:0.95rem;">{selected_weather['alert']}</p>
                <strong>Mandatory Site Actions:</strong>
                <ul style="margin:5px 0 0 0; padding-left:20px; color:#cbd5e1;">
                    {"".join([f"<li>{cp}</li>" for cp in selected_weather['checkpoints']])}
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.subheader("💬 Interactive Field Engineering Assistant")
    st.caption("Ask questions about mix designs, formwork stripping intervals, load calculations, or OSHA regulations.")

    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = [
            {"role": "assistant", "content": "Hello Engineer. I am your site compliance copilot. How can I assist with your site operations or code interpretations today?"}
        ]

    # Display chat messages
    for msg in st.session_state["chat_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat user input
    if user_query := st.chat_input("E.g., What is the minimum formwork stripping time for beam soffits under IS 456?"):
        # Append user message
        st.session_state["chat_messages"].append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Consulting engineering specs..."):
                response_text = call_gemini_chat(
                    chat_history=st.session_state["chat_messages"][:-1],
                    user_message=user_query,
                    context=f"Active Site Weather: {weather_condition}"
                )
                st.markdown(response_text)
                st.session_state["chat_messages"].append({"role": "assistant", "content": response_text})

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.85rem;'>"
    "Multimodal Construction Intelligence Platform • Capstone Project 1 • Built for Streamlit Community Cloud"
    "</div>",
    unsafe_allow_html=True
)