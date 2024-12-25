import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Define the API endpoint
url = "https://ssd-api.jpl.nasa.gov/cad.api"

# Define parameters for the API request (modify as needed)
parameters = {
    'date-min': 'now',
    'dist-max': '0.05',
    'neo': 'true',
    'sort': 'date',
    'limit': '10'  # Limiting to 10 results for demonstration purposes
}

# Make the API request
response = requests.get(url, params=parameters)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse JSON response
    data = response.json()

    # Extract relevant information
    approach_dates = []
    approach_distances = []
    object_designations = []  # To store object primary designations

    for record in data.get('data', []):
        # Convert time to 12-hour format
        time_24h = record[3].split()[1]  # Extract time portion
        time_12h = datetime.strptime(time_24h, "%H:%M").strftime("%I:%M %p")  # Convert to 12-hour format
        approach_dates.append(f"{record[3].split()[0]} {time_12h}")  # Formatted date and time
        approach_distances.append(float(record[4]))  # Nominal approach distance (au)
        object_designations.append(record[0])  # Object primary designation

    # Plot the data as a scatter plot
    plt.figure(figsize=(12, 6))
    scatter = plt.scatter(
        approach_dates,
        approach_distances,
        c=approach_distances,
        cmap='viridis',
        s=100,
        edgecolor='k',
        alpha=0.8
    )
    
    # Add a colorbar to indicate distances
    cbar = plt.colorbar(scatter)
    cbar.set_label('CA Distance Nominal (AU)')

    # Annotate data points with object designations and distances
    for i in range(len(approach_dates)):
        plt.text(
            approach_dates[i],
            approach_distances[i],
            f"{object_designations[i]}\n{approach_distances[i]:.5f} AU",
            fontsize=8,
            ha='right'
        )

    # Customize the plot
    plt.title('Near-Earth Objects (NEO) Approaching Earth')
    plt.xlabel('Close-Approach (CA) Date')
    plt.ylabel('CA Distance Nominal (AU)')
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Show the plot
    plt.show()

else:
    print("Failed to retrieve data from the API.")
