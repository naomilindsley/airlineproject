import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit App Title
st.set_page_config(page_title="Happiest Countries Analysis App", layout="wide")

# Sidebar for Navigation
st.sidebar.title("Home")
page = st.sidebar.radio("Go to", ["Main Page", "Data Summary", "Exploratory Data Analysis"])

# File Upload in Sidebar (only uploaded once)
uploaded_file = st.sidebar.file_uploader("Upload your dataset (CSV file)", type=["csv"])
df = pd.read_csv(uploaded_file) if uploaded_file is not None else None

if page == "Main Page":
    st.title("😊 Welcome to the Happiest Countries Analysis App")
    st.write("Upload a dataset, explore happiness scores, and visualize key metrics.")
    st.write("Use the sidebar to navigate through different pages.")
    
    # Image Upload in Main Page
    image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if image_file:
        st.image(image_file, caption="Uploaded Image", use_column_width=True)
    
    if df is not None:
        st.dataframe(df.head())

elif df is not None:
    if page == "Data Summary":
        st.title("Happiness Data Summary")
        st.write("### Dataset Overview")
        st.write(df.describe())
        st.write("### Missing Values")
        st.write(df.isnull().sum())
        
    elif page == "Exploratory Data Analysis":
        st.title("Exploratory Data Analysis 📊")
        
        # Numeric and Categorical Columns
        num_cols = df.select_dtypes(include=["number"]).columns.tolist()
        obj_cols = df.select_dtypes(include=["object"]).columns.tolist()
        
        # Select Visualization Type
        st.subheader("Select a Visualization:")
        eda_type = st.multiselect("Choose visualization(s):", ["Histogram", "Box Plot", "Bar Plot", "Scatterplots"])
        
        # Histogram
        if "Histogram" in eda_type:
            st.subheader("Histogram")
            selected_col = st.selectbox("Select a numerical column:", num_cols)
            if selected_col:
                st.plotly_chart(px.histogram(df, x=selected_col, title=f"Histogram of {selected_col}", color_discrete_sequence=["blue"]))
        
        # Box Plot
        if "Box Plot" in eda_type:
            st.subheader("Box Plot")
            y_col = st.selectbox("Select a column for Box Plot (y-axis):", num_cols)
            x_col = st.selectbox("Select a column for Box Plot (x-axis):", obj_cols)
            if y_col and x_col:
                st.plotly_chart(px.box(df, x=x_col, y=y_col, title=f"Box Plot: {y_col} vs {x_col}", color=x_col))
        
        # Bar Plot
        if "Bar Plot" in eda_type:
            st.subheader("Bar Plot")
            x_col = st.selectbox("Select x-axis (categorical):", obj_cols, key="bar_x")
            y_col = st.selectbox("Select y-axis (numerical):", num_cols, key="bar_y")
            if x_col and y_col:
                st.plotly_chart(px.bar(df, x=x_col, y=y_col, title=f"Bar Plot: {y_col} by {x_col}", color=x_col))
        
        # Scatterplots
        if "Scatterplots" in eda_type:
            st.subheader("Scatterplots - Visualizing Relationships")
            selected_col_x = st.selectbox("Select x-axis variable:", num_cols)
            selected_col_y = st.selectbox("Select y-axis variable:", num_cols)
            if selected_col_x and selected_col_y:
                chart_title = f"{selected_col_x.title().replace('_', ' ')} vs. {selected_col_y.title().replace('_', ' ')}"
                st.plotly_chart(px.scatter(df, x=selected_col_x, y=selected_col_y, title=chart_title))
else:
    st.write("Upload a dataset to get started!")
