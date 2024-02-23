import streamlit as st
import pandas as pd
import pydeck as pdk

# Streamlit interface for file upload
uploaded_file = st.file_uploader("Choose a file", type=['xlsx'])

if uploaded_file is not None:
    # Read data from the uploaded file
    df = pd.read_excel(uploaded_file, engine='openpyxl')

    # Define color mapping for categories
    color_map = {
        'Business': [0, 128, 0],  # Green
        'Research and Design': [64, 224, 208],  # Turquoise
        'Technology': [0, 0, 255]  # Blue
    }

    # Prepare data for map
    data_for_map = df.copy()
    data_for_map['color'] = data_for_map['Category'].map(color_map)

    # Streamlit dashboard title
    st.title("Connections Map")

    # Define the initial view state of the map
    view_state = pdk.ViewState(latitude=0, longitude=-60, zoom=1)

    # Prepare the scatter plot layer
    scatterplot_layer = pdk.Layer(
        "ScatterplotLayer",
        data_for_map,
        get_position=["Longitude", "Latitude"],
        get_color="color",
        get_radius=200000,
    )

    # Prepare lines for connections
    lines_data = []
    for index, row in df.iterrows():
        if pd.notna(row['Other Connection ID']):
            other = df[df['ID Number'] == row['Other Connection ID']].iloc[0]
            lines_data.append({
                'source': [row['Longitude'], row['Latitude']],
                'target': [other['Longitude'], other['Latitude']],
                'color': [255, 165, 0]  # Orange
            })

    line_layer = pdk.Layer(
        type="LineLayer",
        data=lines_data,
        get_source_position="source",
        get_target_position="target",
        get_color="color",
        get_width=5,
    )

    # Render the map
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        layers=[scatterplot_layer, line_layer],
    ))
else:
    st.text("Please upload an Excel file to get started.")
