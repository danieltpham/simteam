# components/streamlit_register.py
import os
import streamlit.components.v1 as components

_build_path = os.path.join(
    os.path.dirname(__file__),
    "org_chart_component", "build"
)
_org_chart = components.declare_component("org_chart", path=_build_path)

def render_org_chart(data=None, key=None, height=500):
    """height=600 sets the iframe height statically."""
    return _org_chart(data=data, key=key, height=height)
