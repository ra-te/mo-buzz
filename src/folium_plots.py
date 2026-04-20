
import folium

def plot_sequences_map(sequence_dfs, save_name):
    # Find the center of the map using the first sequences average coordinates
    first_seq = sequence_dfs[0]
    center_lat = first_seq["stop_lat"].mean()
    center_lon = first_seq["stop_lon"].mean()
    
    # Create the base map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles='cartodb positron')
    
    # Define a few distinct colors for different sequences
    colors = ["purple", "blue", "green", "orange", "red", "darkred", "black"]
    
    for i, seq_df in enumerate(sequence_dfs):
        color = colors[i % len(colors)]
        
        # Folium expects coordinates as a list of [lat, lon] pairs
        coordinates = list(zip(seq_df["stop_lat"], seq_df["stop_lon"]))
        
        # Draw the path line connecting the stops
        folium.PolyLine(
            locations=coordinates,
            color=color,
            weight=4,
            opacity=0.7,
            tooltip=f"Sequence {i+1}"
        ).add_to(m)
        
        # Add dots for the actual stops
        for _, row in seq_df.iterrows():
            folium.CircleMarker(
                location=[row["stop_lat"], row["stop_lon"]],
                radius=4,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.9,
                tooltip=f"Seq {i+1}: {row["stop_name"]}"
            ).add_to(m)

    # Save the map to an interactive HTML file
    m.save(f"../maps/{save_name}.html")
    print(f"Map saved as {save_name}.html. Open this file in your web browser!")


def plot_stops_map(stop_df, save_name, heat=False):
    # Find the center of the map using the first sequences average coordinates
    center_lat = stop_df["stop_lat"].mean()
    center_lon = stop_df["stop_lon"].mean()
    
    # Create the base map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles='cartodb positron')
        
    # Add dots for the actual stops
    for _, row in stop_df.iterrows():
        if heat:
            color = row["color"]
            tooltip = f"{row["stop_name"]}, {row["count"]}"
        else:
            color = "black"
            tooltip = f"{row["stop_name"]}"

        folium.CircleMarker(
            location=[row["stop_lat"], row["stop_lon"]],
            radius=4,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            tooltip=tooltip
        ).add_to(m)

    # Save the map to an interactive HTML file
    m.save(f"../maps/{save_name}.html")
    print(f"Map saved as {save_name}.html. Open this file in your web browser!")