from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

COLOR_MAP_SENTIMENT: dict[str, str] = {
    "Positivo": "#2DD4BF",
    "Neutro": "#64748B",
    "Negativo": "#F87171",
}

COLOR_MAP_SLA: dict[str, str] = {
    "Baixo": "#34D399",
    "Medio": "#FBBF24",
    "Alto": "#F87171",
}

COLOR_MAP_PRIORITY: dict[str, str] = {
    "Baixa": "#34D399",
    "Media": "#FBBF24",
    "Alta": "#FB923C",
    "Critica": "#F87171",
}

COLOR_MAP_CATEGORY = "#4F8EF7"

PLOTLY_LAYOUT_DEFAULTS: dict = {
    "paper_bgcolor": "#1A2233",
    "plot_bgcolor": "#1A2233",
    "font": {"color": "#E8EDF4"},
    "margin": {"l": 10, "r": 50, "t": 40, "b": 10},
    "yaxis": {"automargin": True},
    "xaxis": {"automargin": True},
}

_REPO_URL = "https://github.com/anotther/support-ticket-insight-lab"

_CSS = """
<style>
[data-testid="stMetric"] {
    background-color: #1A2233;
    border: 1px solid #2D3F5E;
    border-radius: 8px;
    padding: 12px 16px;
}
.stButton > button {
    border-radius: 6px;
    transition: box-shadow 0.2s ease;
}
.stButton > button:hover {
    box-shadow: 0 4px 14px rgba(79, 142, 247, 0.35);
}
[data-testid="stAlert"] {
    border-radius: 6px;
}
section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

/* Hide Share, Favorite and Rename toolbar buttons */
[data-testid="stToolbarActionButtonShare"],
[data-testid="stToolbarActionButtonFavorite"],
[data-testid="stToolbarActionButtonStar"],
[data-testid="stToolbarActionButtonRename"],
[data-testid="stToolbarActionButtonEdit"] {
    display: none !important;
}
</style>
"""

_FIX_GITHUB_JS = f"""
<script>
(function fixGithubLink() {{
    try {{
        var doc = window.parent.document;
        var links = doc.querySelectorAll('a[href*="github.com"]');
        links.forEach(function(link) {{
            if (link.href.includes('github.com/anotther/support-ticket-insight-lab')) {{
                link.href = '{_REPO_URL}';
                link.target = '_blank';
                link.rel = 'noopener noreferrer';
            }}
        }});
    }} catch (e) {{}}
}})();
setTimeout(function() {{
    try {{
        var doc = window.parent.document;
        var links = doc.querySelectorAll('a[href*="github.com"]');
        links.forEach(function(link) {{
            if (link.href.includes('github.com/anotther/support-ticket-insight-lab')) {{
                link.href = '{_REPO_URL}';
            }}
        }});
    }} catch (e) {{}}
}}, 2000);
</script>
"""


def apply_global_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)
    components.html(_FIX_GITHUB_JS, height=0, scrolling=False)
