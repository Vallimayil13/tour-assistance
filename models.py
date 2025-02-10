from pymongo import MongoClient
from math import radians, sin, cos, sqrt, atan2

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client['heritage_sites_db']
collection = db['heritage_sites']

class HeritageSite:
    def __init__(self, name, built_by, location, contact_number, god, unique_features, latitude, longitude, audio_tour):
        self.name = name
        self.built_by = built_by
        self.location = location
        self.contact_number = contact_number
        self.god = god
        self.unique_features = unique_features
        self.latitude = latitude
        self.longitude = longitude
        self.audio_tour = audio_tour
    
    # Method to add a heritage site to the database
    @staticmethod
    def add_site(site_data):
        collection.insert_one(site_data)
    
    # Method to retrieve all heritage sites
    @staticmethod
    def get_all_sites():
        sites = list(collection.find())
        for site in sites:
            # Remove the MongoDB ObjectId before returning
            site['_id'] = str(site['_id'])
        return sites
    
    # Method to retrieve a specific heritage site by name
    @staticmethod
    def get_site_by_name(name):
        site = collection.find_one({"name": name})
        if site:
            # Convert ObjectId to string for serialization
            site['_id'] = str(site['_id'])
            return site
        return None
    
    # Method to calculate distance using the Haversine formula
    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Radius of the Earth in kilometers
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) * sin(dlon / 2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c  # Returns the distance in kilometers
    
    # Method to fetch nearby sites based on latitude and longitude
    @staticmethod
    def get_nearby_sites(user_lat, user_lon, max_distance=50):
        # Set a max distance in kilometers (default: 50 km)
        nearby_sites = list(collection.find())
        result_sites = []

        for site in nearby_sites:
            site['_id'] = str(site['_id'])  # Convert MongoDB ObjectId to string
            distance = HeritageSite.haversine(user_lat, user_lon, site['latitude'], site['longitude'])

            # If the site is within the specified max distance, add it to the result list
            if distance <= max_distance:
                site['distance'] = distance
                result_sites.append(site)

        return result_sites

# Example Data Entry for Brihadeeswarar Temple
brihadeeswarar_data = {
    "name": "Brihadeeswarar Temple",
    "built_by": "Rajaraja Chola I",
    "location": "Thanjavur",
    "contact_number": "0436-2274476",
    "god": "Shiva",
    "unique_features": "The temple houses one of the largest monolithic Nandi statues, and its sanctum contains a massive Shiva lingam",
    "latitude": 10.7844,
    "longitude": 79.1324,
    "audio_tour": """
    Welcome to the beautiful Brihadeeswarar Temple, a famous piece of Chola architecture and a UNESCO World Heritage site.
    One of the special things about this temple is the huge dome made of a single piece of stone, weighing over 80 tons, 
    brought here from more than 50 kilometers away. The tall entrance tower, or gopuram, stands 66 meters high and is covered 
    in detailed carvings, showing the power of Lord Shiva. Inside, you’ll see one of the largest Nandi statues in India, 
    all made from a single stone. As you explore, enjoy the amazing paintings and sculptures that show the great art and 
    skills of the Chola dynasty.
    """
}
# Example Data Entry for Airavatesvara Temple
airavatesvara_data = {
    "name": "Airavatesvara Temple",
    "built_by": "Rajaraja Chola II",
    "location": "Darasuram (near Kumbakonam)",
    "contact_number": "0435-2417157",
    "god": "Shiva",
    "unique_features": "The Airavatesvara Temple is known for its intricate Dravidian architecture, detailed sculptures depicting stories from Hindu mythology, and the unique portrayal of Airavata, the celestial elephant, in its carvings.",
    "latitude": 10.9662,
    "longitude": 79.1194,
    "audio_tour": """
    Welcome to the Airavatesvara Temple, dedicated to Lord Shiva and known for its beautiful Dravidian design.
    The temple has detailed carvings that tell stories from Hindu mythology, including the elephant Airavata worshiping Lord Shiva.
    Inside, the central sanctum holds a large Shiva lingam, a symbol of Lord Shiva’s power. The artwork and tall pillars show 
    the skill of the Chola dynasty. This temple is a wonderful example of South Indian temple architecture and its rich history.
    """
}
# Example Data Entry for Mahabalipuram
mahabalipuram_data = {
    "name": "Mahabalipuram",
    "built_by": "Pallava dynasty",
    "location": "Mahabalipuram (near Chennai)",
    "contact_number": "0452-2344360",  
    "god": "Shiva",
    "unique_features": "Mahabalipuram is known for its rock-cut architecture and monolithic temples, especially the Shore Temple, which is a UNESCO World Heritage Site. The Pancha Rathas are also a remarkable example of Dravidian architecture, each representing a different style and form.",
    "latitude": 12.6202,
    "longitude": 80.1792,
    "audio_tour": """
    Welcome to Mahabalipuram, a town known for its ancient rock-cut temples and rich history. The Shore Temple, which stands 
    as a testament to the brilliance of Pallava architecture, overlooks the Bay of Bengal. The Pancha Rathas, a group of 
    five monolithic temples carved from a single rock, are a spectacular sight, each representing a unique architectural style. 
    Mahabalipuram is a UNESCO World Heritage site, and its intricate carvings and beautiful sculptures make it a must-visit for 
    anyone interested in history and architecture.
    """
}
# Example Data Entry for Gangaikonda Cholapuram
gangaikonda_cholapuram_data = {
    "name": "Gangaikonda Cholapuram",
    "built_by": "Rajendra Chola I",
    "location": "Gangaikonda Cholapuram (near Ariyalur)",
    "contact_number": "9751341108",
    "god": "Shiva",
    "unique_features": "Gangaikonda Cholapuram is known for its grandeur and historical significance, serving as the capital of the Chola dynasty after Rajendra Chola I's successful campaign to the Ganges. The temple is designed similarly to the Brihadeeswarar Temple in Thanjavur, with a massive central dome and intricate carvings. The temple is also home to a large Shiva lingam.",
    "latitude": 11.1241,  # Latitude for Gangaikonda Cholapuram
    "longitude": 79.1478,  # Longitude for Gangaikonda Cholapuram
    "audio_tour": """
    Welcome to Gangaikonda Cholapuram, a magnificent temple built by Rajendra Chola I to commemorate his victory over the 
    Ganges. The temple is a marvel of Chola architecture, modeled after the Brihadeeswarar Temple in Thanjavur. The towering 
    gopuram and majestic Shiva lingam stand as symbols of the power and grandeur of the Chola dynasty. Take in the beautiful 
    sculptures that narrate ancient myths, and explore the serene surroundings of this architectural wonder.
    """
}

# Adding Sites to MongoDB
HeritageSite.add_site(brihadeeswarar_data)
HeritageSite.add_site(airavatesvara_data)
HeritageSite.add_site(mahabalipuram_data)
HeritageSite.add_site(gangaikonda_cholapuram_data)
