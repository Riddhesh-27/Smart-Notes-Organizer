import os
import html
import streamlit as st
from utils.gemini_handler import organize_notes, get_api_key

# Page Configuration
st.set_page_config(
    page_title="Smart Notes Organizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Color palettes for category sticky notes
STICKY_PALETTES = [
    {
        "name": "Sunny Yellow",
        "bg": "#fef9c3",
        "accent": "#eab308",
        "title_color": "#854d0e",
        "pin": "📌",
    },
    {
        "name": "Sky Blue",
        "bg": "#e0f2fe",
        "accent": "#0284c7",
        "title_color": "#0369a1",
        "pin": "📌",
    },
    {
        "name": "Mint Green",
        "bg": "#dcfce7",
        "accent": "#22c55e",
        "title_color": "#15803d",
        "pin": "📌",
    },
    {
        "name": "Soft Lavender",
        "bg": "#f3e8ff",
        "accent": "#a855f7",
        "title_color": "#7e22ce",
        "pin": "📌",
    },
    {
        "name": "Blossom Pink",
        "bg": "#ffe4e6",
        "accent": "#f43f5e",
        "title_color": "#be123c",
        "pin": "📌",
    },
    {
        "name": "Warm Peach",
        "bg": "#ffedd5",
        "accent": "#f97316",
        "title_color": "#c2410c",
        "pin": "📌",
    },
    {
        "name": "Aqua Teal",
        "bg": "#ccfbf1",
        "accent": "#14b8a6",
        "title_color": "#0f766e",
        "pin": "📌",
    },
]

# Custom Styling for modern, clean aesthetic and sticky notes
st.markdown(
    """
    <style>
    /* Main container styling */
    .main {
        background-color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Header typography */
    .app-header {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .app-header h1 {
        font-size: 2.3rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        color: #ffffff;
    }
    .app-header p {
        font-size: 1.05rem;
        color: #cbd5e1;
        margin: 0;
    }

    /* Sticky Note Card */
    .sticky-note-card {
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -1px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .sticky-note-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    .sticky-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px dashed rgba(0, 0, 0, 0.15);
        padding-bottom: 0.5rem;
        margin-bottom: 0.75rem;
    }
    .sticky-title {
        font-weight: 700;
        font-size: 1.15rem;
        margin: 0;
    }
    .sticky-items {
        margin: 0;
        padding-left: 1.2rem;
        font-size: 0.95rem;
        line-height: 1.6;
        color: #1e293b;
    }
    .sticky-items li {
        margin-bottom: 0.35rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Session State
if "notes_input" not in st.session_state:
    st.session_state.notes_input = ""
if "organized_markdown" not in st.session_state:
    st.session_state.organized_markdown = ""
if "error_message" not in st.session_state:
    st.session_state.error_message = ""


def parse_markdown_to_clusters(markdown_text: str):
    """Parse Markdown headings and bullets into structured clusters for sticky notes."""
    lines = markdown_text.strip().split("\n")
    clusters = []
    current_title = None
    current_items = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            if current_title or current_items:
                clusters.append({
                    "title": current_title or "General Notes",
                    "items": current_items,
                })
            current_title = stripped.lstrip("#").strip()
            current_items = []
        elif stripped.startswith(("*", "-", "+")):
            item = stripped.lstrip("*-+ ").strip()
            if item:
                current_items.append(item)
        elif stripped:
            current_items.append(stripped)

    if current_title or current_items:
        clusters.append({
            "title": current_title or "General Notes",
            "items": current_items,
        })
    return clusters


def load_sample_notes():
    """Load sample unorganized notes from the sample dataset file."""
    sample_file_path = os.path.join(
        os.path.dirname(__file__), "sample_data", "sample_notes.txt"
    )
    if os.path.exists(sample_file_path):
        with open(sample_file_path, "r", encoding="utf-8") as f:
            st.session_state.notes_input = f.read()
            st.session_state.error_message = ""
    else:
        st.session_state.notes_input = (
            "Python is a high-level programming language.\n"
            "Supervised learning uses labelled datasets.\n"
            "SQL is used to manage relational databases.\n"
            "Complete the project documentation.\n\n"
            "Python supports object-oriented programming.\n"
            "Regression predicts continuous values.\n"
            "Primary keys uniquely identify records.\n"
            "Prepare the final presentation."
        )


def clear_all():
    """Reset the application state."""
    st.session_state.notes_input = ""
    st.session_state.organized_markdown = ""
    st.session_state.error_message = ""


# App Header
st.markdown(
    """
    <div class="app-header">
        <h1>📝 Smart Notes Organizer</h1>
        <p>Turn scattered notes into structured knowledge with Colorful Sticky Notes</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Check API Key Status
api_key = get_api_key()
if not api_key or api_key == "your_gemini_api_key_here":
    st.warning(
        "⚠️ **Gemini API Key Missing**: Please set your `GEMINI_API_KEY` in the `.env` file to enable note organization.",
        icon="⚠️",
    )

# Two-column layout
col_input, col_output = st.columns([1, 1], gap="large")

# ----------------- STEP 1: INPUT SECTION -----------------
with col_input:
    st.subheader("📥 Paste Your Notes")
    st.caption("Paste scattered notes across various topics below (use blank lines to separate notes).")

    notes_text = st.text_area(
        label="Notes Input",
        value=st.session_state.notes_input,
        placeholder="Paste your unorganized notes here...\n\nExample:\n- Meeting notes about project timeline\n- Concept definitions for AI exam\n- Database schema requirements\n- To-do items for submission",
        height=340,
        label_visibility="collapsed",
        key="text_area_input",
    )
    st.session_state.notes_input = notes_text

    # Action Buttons for Input
    btn_col1, btn_col2, btn_col3 = st.columns([1.5, 1, 1.5])

    with btn_col1:
        if st.button("📂 Load Sample Notes", use_container_width=True):
            load_sample_notes()
            st.rerun()

    with btn_col2:
        if st.button("🗑️ Clear", use_container_width=True):
            clear_all()
            st.rerun()

    with btn_col3:
        organize_clicked = st.button("✨ Organize My Notes", type="primary", use_container_width=True)

    if organize_clicked:
        if not st.session_state.notes_input.strip():
            st.error("Please enter or paste some notes before organizing.")
        else:
            with st.spinner("🤖 Gemini is clustering topics into sticky notes..."):
                try:
                    result = organize_notes(st.session_state.notes_input)
                    st.session_state.organized_markdown = result
                    st.session_state.error_message = ""
                    st.success("Notes organized successfully into color-coded categories!")
                except Exception as err:
                    st.session_state.error_message = str(err)
                    st.error(f"Error: {err}")

# ----------------- STEP 2 & 3: OUTPUT SECTION -----------------
with col_output:
    st.subheader("📑 Your Organized Notes")
    st.caption("Each category is displayed in its own distinct colorful sticky note.")

    if st.session_state.error_message:
        st.error(st.session_state.error_message)

    if st.session_state.organized_markdown:
        clusters = parse_markdown_to_clusters(st.session_state.organized_markdown)

        # Tabs for Sticky Notes View vs Classic Markdown View
        tab_sticky, tab_doc = st.tabs(["📌 Sticky Notes Board", "📄 Document Preview"])

        with tab_sticky:
            # Display colored sticky note boxes
            for idx, cluster in enumerate(clusters):
                palette = STICKY_PALETTES[idx % len(STICKY_PALETTES)]
                escaped_title = html.escape(cluster["title"])
                items_html = "".join([f"<li>{html.escape(item)}</li>" for item in cluster["items"]])

                st.markdown(
                    f"""
                    <div class="sticky-note-card" style="background-color: {palette['bg']}; border-top: 6px solid {palette['accent']}; border-left: 1px solid {palette['accent']}40; border-right: 1px solid {palette['accent']}40; border-bottom: 1px solid {palette['accent']}40;">
                        <div class="sticky-header">
                            <span class="sticky-title" style="color: {palette['title_color']};">{escaped_title}</span>
                            <span style="font-size: 1.15rem;">📌</span>
                        </div>
                        <ul class="sticky-items">
                            {items_html}
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with tab_doc:
            st.markdown(st.session_state.organized_markdown)

        st.divider()

        # Output Action Options: Download, Reorganize, Reset
        act_col1, act_col2, act_col3 = st.columns([1.2, 1.2, 1])

        with act_col1:
            st.download_button(
                label="📥 Download .md",
                data=st.session_state.organized_markdown,
                file_name="organized_notes.md",
                mime="text/markdown",
                use_container_width=True,
            )

        with act_col2:
            if st.button("🔄 Reorganize", use_container_width=True):
                with st.spinner("🤖 Re-processing notes with Gemini..."):
                    try:
                        result = organize_notes(st.session_state.notes_input)
                        st.session_state.organized_markdown = result
                        st.session_state.error_message = ""
                        st.rerun()
                    except Exception as err:
                        st.session_state.error_message = str(err)
                        st.error(f"Error: {err}")

        with act_col3:
            if st.button("❌ Reset", use_container_width=True):
                clear_all()
                st.rerun()

        # Raw Markdown view for easy manual copy
        with st.expander("📋 View Raw Markdown (for easy copy)"):
            st.code(st.session_state.organized_markdown, language="markdown")

    else:
        st.info("👈 Enter notes on the left and click **Organize My Notes** to see your colorful category cards here.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.85rem;'>"
    "Smart Notes Organizer • Powered by Google Gemini Flash • Final Year Generative AI Project"
    "</div>",
    unsafe_allow_html=True,
)
