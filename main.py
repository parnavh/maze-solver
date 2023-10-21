import streamlit as st
from generate import MazeGenerator
from solve import MazeSolver
import cv2


# Setup App
st.set_page_config(
    page_title="Maze Solver",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
)

hide_streamlit_style = """
<style>
#MainMenu {display: none;}
footer {display: none;}
.stDeployButton {display: none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Initialize Session State
if "height" not in st.session_state:
    st.session_state["height"] = 50
if "width" not in st.session_state:
    st.session_state["width"] = 50


# Main App
st.title("Maze Solver")

tab_generate, tab_solve = st.tabs(["Generate Maze", "Solve Maze"])


# Generate Maze
with tab_generate:
    c1, c2 = st.columns(2)
    with c1:
        height = st.slider("Height", min_value=30, max_value=80, key="height")

    with c2:
        width = st.slider("Width", min_value=30, max_value=80, key="width")

    maze = MazeGenerator(height, width)

    st.subheader("Maze Generated:")
    st.image(maze.get_maze())

    c3, c4, c5 = st.columns(3)
    with c4:
        st.download_button(
            "Download Maze",
            data=cv2.imencode(".png", maze.get_maze())[1].tobytes(),
            file_name="maze.png",
            mime="image/png",
            use_container_width=True,
        )


# Solve Maze
with tab_solve:
    solution = MazeSolver(maze.get_maze())

    st.subheader("Path Generated:")
    st.image(solution.res)

    c7, c8, c9 = st.columns(3)
    with c8:
        st.download_button(
            "Download Solved Maze",
            data=cv2.imencode(".png", solution.res)[1].tobytes(),
            file_name="solved.png",
            mime="image/png",
            use_container_width=True,
        )

    st.divider()

    st.subheader("Steps Involved:")

    st.text("1. Draw Contours:")

    c10, c11 = st.columns(2)
    with c10:
        st.text("First pass")
        st.image(solution.contour1)
    with c11:
        st.text("Second pass")
        st.image(solution.contour2)

    st.text("2. Morphological Closing:")
    c12, c13 = st.columns(2)
    with c12:
        st.text("Dilate")
        st.image(solution.dilation)
    with c13:
        st.text("Erode")
        st.image(solution.erosion)

    st.text("3. Mask Generation:")
    c14, c15 = st.columns(2)
    with c14:
        st.text("Difference")
        st.image(solution.difference)
    with c15:
        st.text("Mask")
        st.image(solution.mask)

    st.text("4. Final Result:")
    st.image(solution.res)
