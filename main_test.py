import streamlit as st
import pandas as pd
import random
import os
import time
from datetime import datetime

# --- QUESTIONS DATASET (30 selected from pool of 50) ---
QUESTIONS_POOL = [
    {"q": "Which measurement involves bringing the target quantity into contact with the system?", "o": ["", "Indirect", "Direct", "Virtual", "Standard"], "a": "Direct"},
    {"q": "What is the measurement accuracy of a Vernier Caliper?", "o": ["", "0.01 mm", "1.0 mm", "0.1 mm", "0.001 mm"], "a": "0.1 mm"},
    {"q": "Which instrument measures the flatness of a flat area?", "o": ["", "Micrometer", "Vernier Caliper", "Dial Indicator", "Manometer"], "a": "Dial Indicator"},
    {"q": "A densitometer measures the amount of ________ absorbed by an object.", "o": ["", "Wind", "Heat", "Light", "Sound"], "a": "Light"},
    {"q": "Errors resulting from human mistakes like taking the wrong reading are:", "o": ["", "Systematic", "Random", "Gross", "Environmental"], "a": "Gross"},
    {"q": "The loading effect is a common type of which error?", "o": ["", "Instrumental", "Environmental", "Observational", "Random"], "a": "Instrumental"},
    {"q": "Closeness of a measurement to the expected value is defined as:", "o": ["", "Precision", "Resolution", "Calibration", "Accuracy"], "a": "Accuracy"},
    {"q": "Parallax error in analog meters is minimized by using:", "o": ["", "Stronger springs", "Mirrored scales", "Digital displays", "Thicker needles"], "a": "Mirrored scales"},
    {"q": "Which instrument predicts weather by measuring wind speed?", "o": ["", "Barometer", "Anemometer", "Manometer", "Hygrometer"], "a": "Anemometer"},
    {"q": "The difference between true value and measured value is:", "o": ["", "Accuracy", "Precision", "Measurement Error", "Tolerance"], "a": "Measurement Error"},
    {"q": "A transducer changes a physical quantity into an equivalent ________ form.", "o": ["", "Mechanical", "Thermal", "Electrical", "Chemical"], "a": "Electrical"},
    {"q": "In a digital system, what converts analog data to digital form?", "o": ["", "Signal Modifier", "Multiplexer", "ADC", "Display Unit"], "a": "ADC"},
    {"q": "PMMC instruments are primarily used for:", "o": ["", "AC only", "AC and DC", "DC only", "Radio signals"], "a": "DC only"},
    {"q": "In PMMC instruments, controlling torque is typically provided by:", "o": ["", "Gravity", "Eddy currents", "Phosphorous bronze springs", "Magnets"], "a": "Phosphorous bronze springs"},
    {"q": "What reduces temperature effects on a PMMC moving coil?", "o": ["", "Shunt resistance", "Swamping resistance", "Transformer", "Capacitor"], "a": "Swamping resistance"},
    {"q": "To convert a galvanometer to an ammeter, connect a:", "o": ["", "High series resistor", "Low series resistor", "High parallel resistor", "Low shunt resistor"], "a": "Low shunt resistor"},
    {"q": "Which instrument is simple and used for both AC and DC?", "o": ["", "PMMC", "Moving Iron (MI)", "Digital Multimeter", "Galvanometer"], "a": "Moving Iron (MI)"},
    {"q": "The scale of a Moving Iron instrument is usually:", "o": ["", "Linear", "Uniform", "Non-uniform", "Logarithmic"], "a": "Non-uniform"},
    {"q": "Voltage sensitivity is defined as deflection per unit ________.", "o": ["", "Current", "Voltage", "Resistance", "Torque"], "a": "Voltage"},
    {"q": "Which material is used for permanent magnets in PMMC?", "o": ["", "Soft iron", "Copper", "Alnico", "Phosphor-bronze"], "a": "Alnico"},
    {"q": "An analog multimeter is fundamentally based on a:", "o": ["", "Voltmeter", "Microammeter", "Ohmmeter", "Frequency meter"], "a": "Microammeter"},
    {"q": "A voltmeter must be connected to a circuit in:", "o": ["", "Series", "Parallel", "Series-Parallel", "Bridge"], "a": "Parallel"},
    {"q": "An oscilloscope displays which quantity on its vertical scale?", "o": ["", "Frequency", "Time", "Instantaneous voltage", "Current"], "a": "Instantaneous voltage"},
    {"q": "Horizontal sweep in an oscilloscope is measured in:", "o": ["", "Volts/div", "Amps/div", "Seconds/div", "Ohms/div"], "a": "Seconds/div"},
    {"q": "The 'common' port on a multimeter typically takes the ________ lead.", "o": ["", "Red", "Yellow", "Black", "Green"], "a": "Black"},
    {"q": "Continuity testing verifies:", "o": ["", "High resistance", "A complete circuit path", "Voltage levels", "AC frequency"], "a": "A complete circuit path"},
    {"q": "Modern oscilloscopes often use this display type:", "o": ["", "LED", "Plasma", "LCD", "Analog needle"], "a": "LCD"},
    {"q": "An ammeter should ideally have ________ resistance.", "o": ["", "High", "Infinite", "Low", "Medium"], "a": "Low"},
    {"q": "Which bridge measures unknown resistance?", "o": ["", "Maxwell", "Hay’s", "Wheatstone", "Schering"], "a": "Wheatstone"},
    {"q": "A balanced Wheatstone bridge shows ________ deflection.", "o": ["", "Full-scale", "Half-scale", "Null", "Oscillating"], "a": "Null"},
    {"q": "A Function Generator can produce which wave?", "o": ["", "Sine", "Square", "Triangular", "All of the above"], "a": "All of the above"},
    {"q": "Typical Frequency Synthesizer range is:", "o": ["", "1-100 Hz", "1-160 MHz", "1-10 GHz", "10-50 kHz"], "a": "1-160 MHz"},
    {"q": "RF generators provide test signals for:", "o": ["", "Resistance", "Radio/TV equipment", "AC to DC", "Gas pressure"], "a": "Radio/TV equipment"},
    {"q": "The SI unit of pressure is:", "o": ["", "Newton", "Joule", "Pascal", "Watt"], "a": "Pascal"},
    {"q": "The vacuum above mercury in a barometer is the:", "o": ["", "Atmospheric", "Torricellian", "Aneroid", "Mercury gap"], "a": "Torricellian"},
    {"q": "An Aneroid Barometer uses a ________ to measure pressure.", "o": ["", "Water column", "Mercury column", "Flexible metal box", "Electronic sensor"], "a": "Flexible metal box"},
    {"q": "Standard atmospheric pressure is approximately:", "o": ["", "100 mm Hg", "760 mm Hg", "500 mm Hg", "1000 mm Hg"], "a": "760 mm Hg"},
    {"q": "Which recorder plots one variable against another?", "o": ["", "Strip chart", "Magnetic tape", "X-Y recorder", "Circular chart"], "a": "X-Y recorder"},
    {"q": "In an X-Y recorder, the writing head is controlled by a:", "o": ["", "Manual crank", "Servo system", "Spring", "Magnet"], "a": "Servo system"},
    {"q": "A UPS provides backup power for:", "o": ["", "Voltage increase", "Orderly shutdown", "DC to AC", "Frequency"], "a": "Orderly shutdown"},
    {"q": "A UPS consists of sensing circuitry and ________.", "o": ["", "Mercury tubes", "Rechargeable batteries", "Moving coils", "Transducers"], "a": "Rechargeable batteries"},
    {"q": "Troubleshooting determines the cause of a problem and:", "o": ["", "Builds a new circuit", "Takes corrective action", "Measures facts", "Designs manuals"], "a": "Takes corrective action"},
    {"q": "Which method divides a circuit in half to find a fault?", "o": ["", "Functional area", "Signal injection", "Split-half", "Substitution"], "a": "Split-half"},
    {"q": "The first step in troubleshooting is to:", "o": ["", "Replace parts", "Define the problem", "Implement solutions", "Test equipment"], "a": "Define the problem"},
    {"q": "Which is a material tool for troubleshooting?", "o": ["", "Oscilloscope", "Multimeter", "Soldering iron", "All of the above"], "a": "All of the above"},
    {"q": "The Functional Area Approach traces faults to a specific ________.", "o": ["", "Component", "Unit (e.g. Amplifier)", "Wire", "Screw"], "a": "Unit (e.g. Amplifier)"},
    {"q": "Unexpected circuit behavior can be caused by:", "o": ["", "Aging", "Overheating", "Bad soldering", "All of the above"], "a": "All of the above"},
    {"q": "Signal Tracing follows a signal to see where it:", "o": ["", "Starts", "Disappears/Distorts", "Heats up", "Changes color"], "a": "Disappears/Distorts"},
    {"q": "When proposing solutions, you should start with the:", "o": ["", "Expensive", "Complex", "Simplest", "Theoretical"], "a": "Simplest"},
    {"q": "After implementing a solution, you must:", "o": ["", "Stop", "Test it again", "Discard notes", "Increase voltage"], "a": "Test it again"}
]

CSV_FILE = "glt302_results.csv"

# --- CORE FUNCTIONS ---
def save_data(name, app_num, dept, score):
    data = {
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Full Name": [name],
        "App Number": [app_num],
        "Department": [dept],
        "Score": [f"{score}/30"]
    }
    df = pd.DataFrame(data)
    df.to_csv(CSV_FILE, mode='a', index=False, header=not os.path.exists(CSV_FILE))

def has_submitted(name, app_num):
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        return not df[(df["Full Name"] == name) & (df["App Number"] == int(app_num))].empty
    return False

# --- UI CONFIG ---
st.set_page_config(page_title="GLT 302 TEST Portal", layout="centered")

st.markdown("""
    <style>
    .timer-header {
        position: fixed; top: 0; left: 0; width: 100%; background-color: #ffffff;
        text-align: center; padding: 10px; border-bottom: 2px solid #2e7d32; z-index: 1000;
    }
    .main { background-color: #f8f9fa; }
    div[data-baseweb="select"] > div { border: 2px solid #2e7d32; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- APP STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'responses' not in st.session_state:
    st.session_state.responses = {}

# --- LOGIN VIEW ---
if st.session_state.page == 'login':
    st.title("🎓 GLT 302 TEST (Microbiology and Physics)")
    with st.container(border=True):
        st.subheader("Student DETAILS")
        name = st.text_input("Full Name")
        app_num = st.text_input("Application Number (Last 4-Digits)", max_chars=4)
        dept = st.selectbox("Department", ["", "Microbiology Morning", "Microbiology Evening", "Physics"])
        
        #if st.button("Start TEST"):
            #if not name or len(app_num) != 4 or not app_num.isdigit() or not dept:
                        st.error("Please provide your name, Last 4-digit ID, and select your department.")
           # elif has_submitted(name, app_num):
                st.warning(f"Submission found for {name} ({app_num}). Access denied.")
            #else:
                st.session_state.student_name = name
                st.session_state.student_id = app_num
                st.session_state.dept = dept
                st.session_state.questions = random.sample(QUESTIONS_POOL, 30)
                st.session_state.start_time = time.time()
                st.session_state.page = 'exam'
                st.rerun()

# --- EXAM VIEW ---
elif st.session_state.page == 'exam':
    # Timer logic
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 480 - int(elapsed)) # 8 minutes
    
    # Auto-submit if time up
    if remaining <= 0:
        st.session_state.page = 'submit'
        st.rerun()

    # Sticky Top Timer
    mins, secs = divmod(remaining, 60)
    st.markdown(f'<div class="timer-header"><h2 style="color: #d32f2f; margin:0;">⏳ Remaining Time: {mins:02d}:{secs:02d}</h2></div>', unsafe_allow_html=True)
    st.write("---")
    st.header(f"TEST for {st.session_state.student_name}")
    st.caption(f"Dept: {st.session_state.dept} | ID: {st.session_state.student_id}")

    # Question UI
    for i, item in enumerate(st.session_state.questions):
        st.markdown(f"### Question {i+1}")
        st.write(item['q'])
        st.session_state.responses[i] = st.selectbox(
            "Select Answer", 
            item['o'], 
            key=f"q_{i}", 
            label_visibility="collapsed"
        )
        st.divider()

    if st.button("Submit Final Answers", type="primary"):
        st.session_state.page = 'submit'
        st.rerun()

    # Refresh timer
    time.sleep(1)
    st.rerun()

# --- SUBMISSION LOGIC ---
elif st.session_state.page == 'submit':
    score = 0
    for i, item in enumerate(st.session_state.questions):
        if st.session_state.responses.get(i) == item['a']:
            score += 1
            
    save_data(st.session_state.student_name, st.session_state.student_id, st.session_state.dept, score)
    
    st.success("TEST Submitted Successfully.")
    st.balloons()
    st.title("Final Result")
    st.metric("Score", f"{score} / 30")
    st.info("Your details and score have been logged. You may now close this tab.")
    st.stop()
