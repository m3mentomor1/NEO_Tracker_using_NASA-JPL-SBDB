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

    # Plot the data as a line graph
    plt.figure(figsize=(10, 6))
    plt.plot(approach_dates, approach_distances, marker='o', color='b', linestyle='-')
    plt.title('Near-Earth Objects (NEO) Approaching Earth')
    plt.xlabel('Close-Approach (CA) Date')
    plt.ylabel('CA Distance Nominal (AU)')
    plt.xticks(rotation=45)
    plt.grid(True)
    
    # Display AU values and object designations next to the data points
    for i in range(len(approach_dates)):
        plt.text(approach_dates[i], approach_distances[i], f'Object: {object_designations[i]}\n{approach_distances[i]:.5f} AU', fontsize=8, ha='right')

    plt.tight_layout()
    plt.show()

else:
    print("Failed to retrieve data from the API.")
