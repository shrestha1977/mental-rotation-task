import streamlit as st
import random
import time

# ---------------------------
# CONFIGURATION
# ---------------------------
# Provide your image sets here
# Each item = (target, correct, wrong)
image_sets = [
    ("images/target1.png", "images/correct1.png", "images/wrong1.png"),
    ("images/target2.png", "images/correct2.png", "images/wrong2.png"),
    ("images/target3.png", "images/correct3.png", "images/wrong3.png"),
    ("images/target4.png", "images/correct4.png", "images/wrong4.png"),
    ("images/target5.png", "images/correct5.png", "images/wrong5.png"),
    ("images/target6.png", "images/correct6.png", "images/wrong6.png"),
    ("images/target7.png", "images/correct7.png", "images/wrong7.png"),
    ("images/target8.png", "images/correct8.png", "images/wrong8.png"),
    ("images/target9.png", "images/correct9.png", "images/wrong9.png"),
    ("images/target10.png", "images/correct10.png", "images/wrong10.png"),
]

TOTAL_QUESTIONS = 10

# ---------------------------
# INITIALIZE SESSION STATE
# ---------------------------
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.current_question = 0
    st.session_state.results = []
    st.session_state.start_time = time.time()
    st.session_state.question_start_time = time.time()
    st.session_state.task_started = False
    # Randomize the order of questions
    st.session_state.randomized_indices = random.sample(range(len(image_sets)), TOTAL_QUESTIONS)
    st.session_state.current_trial_options = None

st.set_page_config(page_title="Mental Rotation Task")

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------
def record_answer(is_correct):
    """Record the answer and move to next question"""
    question_time = time.time() - st.session_state.question_start_time
    
    st.session_state.results.append({
        'question': st.session_state.current_question + 1,
        'correct': is_correct,
        'time': question_time
    })
    
    st.session_state.current_question += 1
    st.session_state.question_start_time = time.time()
    st.session_state.current_trial_options = None  # Reset for next trial

def show_results():
    """Display final results"""
    total_time = time.time() - st.session_state.start_time
    correct_count = sum(1 for r in st.session_state.results if r['correct'])
    accuracy = (correct_count / TOTAL_QUESTIONS) * 100
    avg_time = sum(r['time'] for r in st.session_state.results) / TOTAL_QUESTIONS

    
    st.markdown("## 🎉 Task Completed!")
    st.markdown("---")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Accuracy", f"{accuracy:.1f}%", f"{correct_count}/{TOTAL_QUESTIONS}")
    with col2:
        st.metric("⏱️ Total Time", f"{total_time:.1f}s")
    with col3:
        st.metric("⚡ Avg Time per Question", f"{avg_time:.2f}s")
    
    st.markdown("---")
    
    # Detailed results
    st.markdown("### 📊 Question-by-Question Results")
    for r in st.session_state.results:
        status = "✅" if r['correct'] else "❌"
        st.write(f"{status} Question {r['question']}: {r['time']:.2f}s")
    
    st.markdown("---")
    
    if st.button("🔄 Start New Task", type="primary", use_container_width=True):
        # Reset everything
        st.session_state.current_question = 0
        st.session_state.results = []
        st.session_state.start_time = time.time()
        st.session_state.question_start_time = time.time()
        st.session_state.task_started = False
        st.session_state.randomized_indices = random.sample(range(len(image_sets)), TOTAL_QUESTIONS)
        st.session_state.current_trial_options = None
        st.rerun()

# ---------------------------
# MAIN APP
# ---------------------------
# st.title("🧠 Mental Rotation Task")

# Start screen
if not st.session_state.task_started:
    st.markdown("""
    ### Welcome to the Mental Rotation Task!
    
    **Instructions:**
    - You will see a **target image** at the top
    - Below are **two choice images** - one is correctly rotated, one is wrong
    - **Click directly on the image** you think is the correct rotation
    - You will proceed to the next question automatically
    - Complete all 10 questions as quickly and accurately as possible
    
    **Ready? Click the button below to start!**
    """)
    
    if st.button("▶️ Start Task", type="primary", use_container_width=True):
        st.session_state.task_started = True
        st.session_state.start_time = time.time()
        st.session_state.question_start_time = time.time()
        st.rerun()
    
    st.stop()

# Task in progress
if st.session_state.current_question < TOTAL_QUESTIONS:
    # Progress bar
    # progress = st.session_state.current_question / TOTAL_QUESTIONS
    # st.progress(progress)
    st.markdown(f"**Question {st.session_state.current_question + 1} of {TOTAL_QUESTIONS}**")
    
    # Get current trial index
    trial_idx = st.session_state.randomized_indices[st.session_state.current_question]
    target_img, correct_img, wrong_img = image_sets[trial_idx]
    
    # Randomize left/right positions only once per trial
    if st.session_state.current_trial_options is None:
        options = [
            {"img": correct_img, "is_correct": True, "label": "Option A"},
            {"img": wrong_img, "is_correct": False, "label": "Option B"}
        ]
        random.shuffle(options)
        st.session_state.current_trial_options = options
    else:
        options = st.session_state.current_trial_options
    
    # Display target
    st.markdown("---")
    st.markdown(f"### 🎯 Target Image {st.session_state.current_question+1}")
    col_center = st.columns([1, 1, 1])
    with col_center[1]:
        st.image(target_img,width=175)
    
    st.markdown("---")
    st.markdown("### 👆 Click on the correct rotated version:")
    
    # Display choices with clickable images
    col1, col2 = st.columns([2,1.2])
    
    with col1:
        st.image(options[0]["img"], width=175)
        if st.button(   "Option A", key="choice_0", width=175, type="primary"):
            record_answer(options[0]["is_correct"])
            st.rerun()
    
    with col2:
        st.image(options[1]["img"], width=175)
        if st.button("Option B", key="choice_1", width=175, type="primary"):
            record_answer(options[1]["is_correct"])
            st.rerun()

# Task completed
else:
    show_results()