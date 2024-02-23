import streamlit as st
import pandas as pd
import plotly
import plotly.graph_objects as go


# Step 1: Load the Excel file
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, engine='openpyxl')  # Adjust "YourSheetName" as necessary

    # Step 2: Pre-process the DataFrame
    # Assuming the DataFrame columns are properly named
    df.dropna(subset=['Longitude', 'Latitude'], inplace=True)

    # Step 3: Filter by Year
    year = st.slider("Select a year", int(df['Year'].min()), int(df['Year'].max()))
    df_filtered = df[df['Year'] <= year]

    # Create a dictionary to map ID Number to coordinates
    id_to_coords = {row['ID Number']: (row['Longitude'], row['Latitude']) for index, row in df_filtered.iterrows()}

    fig = go.Figure()

    # Step 4: Plot Points
    for _, row in df_filtered.iterrows():
        fig.add_trace(go.Scattergeo(
            locationmode='country names',
            lon=[row['Longitude']],
            lat=[row['Latitude']],
            mode='markers',
            marker=dict(size=5),
            text=row['Name'],  # Display the name as hover text
        ))

    # Step 5: Plot Connections
    for _, row in df_filtered.iterrows():
        if row['Other Connection ID'] in id_to_coords:
            start_lon, start_lat = row['Longitude'], row['Latitude']
            end_lon, end_lat = id_to_coords[row['Other Connection ID']]
            fig.add_trace(go.Scattergeo(
                locationmode='country names',
                lon=[start_lon, end_lon],
                lat=[start_lat, end_lat],
                mode='lines',
                line=dict(width=1, color='red'),
            ))

    # Update layout for better visualization
    fig.update_layout(
        title_text='World Map of Connections for Selected Year',
        geo=dict(
            projection_type='equirectangular',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
        )
    )

    st.plotly_chart(fig)

