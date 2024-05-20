import streamlit as st
import pandas as pd


# Function to load dataset
@st.cache_resource
def load_data(file):
    data = pd.read_csv(file)
    return data


# Function to plot data using Streamlit's native methods
def plot_data(df, chart_type, x_axis, y_axis):
    if chart_type == 'Scatter Plot':
        st.write("### Scatter Plot")
        st.vega_lite_chart(df, {
            'mark': {'type': 'point', 'tooltip': True},
            'encoding': {
                'x': {'field': x_axis, 'type': 'quantitative'},
                'y': {'field': y_axis, 'type': 'quantitative'},
                'tooltip': [{'field': x_axis}, {'field': y_axis}]
            }
        })
    elif chart_type == 'Line Chart':
        st.write("### Line Chart")
        st.line_chart(df.set_index(x_axis)[y_axis])
    elif chart_type == 'Bar Chart':
        st.write("### Bar Chart")
        st.bar_chart(df.set_index(x_axis)[y_axis])
    elif chart_type == 'Histogram':
        st.write("### Histogram")
        st.vega_lite_chart(df, {
            'mark': {'type': 'bar', 'tooltip': True},
            'encoding': {
                'x': {'field': x_axis, 'type': 'quantitative', 'bin': True},
                'y': {'aggregate': 'count', 'type': 'quantitative'},
                'tooltip': [{'field': x_axis, 'type': 'quantitative'}, {'aggregate': 'count', 'type': 'quantitative'}]
            }
        })
    elif chart_type == 'Box Plot':
        st.write("### Box Plot")
        st.vega_lite_chart(df, {
            'mark': {'type': 'boxplot', 'tooltip': True},
            'encoding': {
                'x': {'field': x_axis, 'type': 'nominal'},
                'y': {'field': y_axis, 'type': 'quantitative'},
                'tooltip': [{'field': x_axis}, {'field': y_axis}]
            }
        })
    else:
        st.write("Please select a chart type.")


# Streamlit app
def main():
    st.title("Interactive Data Dashboard")
    st.write("Upload the dataset and see the relations between the attributes in different ways!")

    st.sidebar.title("Options")
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = load_data(uploaded_file)
        st.write("## Dataset")
        st.write(df)

        st.sidebar.subheader("Visualization Settings")
        chart_type = st.sidebar.selectbox("Select Chart Type",
                                          ["Scatter Plot", "Line Chart", "Bar Chart", "Histogram", "Box Plot"])
        x_axis = st.sidebar.selectbox("Select X-axis", df.columns)
        y_axis = st.sidebar.selectbox("Select Y-axis", df.columns)

        st.write("## Visualization")
        plot_data(df, chart_type, x_axis, y_axis)


if __name__ == "__main__":
    main()
