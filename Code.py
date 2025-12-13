# =====================================
# City Network – Fixed Conditions Version
# =====================================

import math


# ---------- Location ----------
class Location:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y


# ---------- Street ----------
class Street:
    def __init__(
        self,
        street_name,
        to,
        avg_speed,
        distance,
        speed_limit,
        traffic_light_delay,
        accident,
        closed,
        weather
    ):
        self.street_name = street_name
        self.to = to
        self.avg_speed = avg_speed
        self.distance = distance
        self.speed_limit = speed_limit
        self.traffic_light_delay = traffic_light_delay
        self.accident = accident
        self.closed = closed
        self.weather = weather

    # g(n)
    def g_cost(self):
        if self.closed or self.weather == "Snow":
            return float("inf")

        speed = min(self.avg_speed, self.speed_limit)

        if self.weather == "Rain":
            speed *= 0.8
        elif self.weather == "Fog":
            speed *= 0.7

        if self.accident:
            speed *= 0.5

        speed = max(speed, 1)
        travel_time = (self.distance / speed) * 60
        return travel_time + self.traffic_light_delay


# ---------- h(n) ----------
def h_cost(curr, goal, max_speed=60):
    d = math.sqrt((curr.x - goal.x) ** 2 + (curr.y - goal.y) ** 2)
    return (d / max_speed) * 60


# ---------- 40 Virtual Locations ----------
locations = {
    "Central Hospital": Location("Central Hospital", 2, 8),
    "Children Hospital": Location("Children Hospital", 1, 8),
    "City Clinic": Location("City Clinic", 3, 7),
    "Main University": Location("Main University", 6, 8),
    "Engineering Faculty": Location("Engineering Faculty", 7, 8),
    "Medical School": Location("Medical School", 6, 7),
    "High School": Location("High School", 4, 6),
    "Primary School": Location("Primary School", 3, 6),
    "International School": Location("International School", 5, 6),
    "Central Park": Location("Central Park", 2, 5),
    "Community Park": Location("Community Park", 4, 5),
    "Sports Club": Location("Sports Club", 6, 5),
    "City Mall": Location("City Mall", 7, 5),
    "Local Market": Location("Local Market", 5, 4),
    "Wholesale Market": Location("Wholesale Market", 6, 4),
    "Police Station": Location("Police Station", 1, 4),
    "Fire Station": Location("Fire Station", 2, 4),
    "City Hall": Location("City Hall", 3, 4),
    "Bus Terminal": Location("Bus Terminal", 4, 4),
    "Train Station": Location("Train Station", 5, 3),
    "Metro Hub": Location("Metro Hub", 6, 3),
    "Residential A": Location("Residential A", 1, 3),
    "Residential B": Location("Residential B", 2, 3),
    "Residential C": Location("Residential C", 3, 3),
    "Residential D": Location("Residential D", 4, 3),
    "Residential E": Location("Residential E", 5, 2),
    "Industrial Zone A": Location("Industrial Zone A", 7, 3),
    "Industrial Zone B": Location("Industrial Zone B", 8, 3),
    "Power Station": Location("Power Station", 8, 2),
    "Water Facility": Location("Water Facility", 7, 2),
    "Tech Park": Location("Tech Park", 6, 2),
    "Research Center": Location("Research Center", 5, 1),
    "Hotel Plaza": Location("Hotel Plaza", 4, 1),
    "Business Tower": Location("Business Tower", 3, 1),
    "Convention Center": Location("Convention Center", 2, 1),
    "Old Town Square": Location("Old Town Square", 1, 1),
    "Museum": Location("Museum", 2, 0),
    "Library": Location("Library", 4, 0),
    "Cultural Center": Location("Cultural Center", 3, 0),
}


# ---------- City Graph (Fixed accidents & weather) ----------
city_graph = {
    "Central Hospital": [
        Street("Emergency Road", "Children Hospital", 40, 0.6, 50, 2, False, False, "Rain"),
        Street("Health Avenue", "City Clinic", 35, 0.8, 40, 1, True, False, "Clear"),
        Street("Park Lane", "Central Park", 30, 1.0, 40, 2, False, False, "Fog"),
    ],

    "Children Hospital": [
        Street("Care Street", "Central Hospital", 40, 0.6, 50, 1, False, False, "Rain"),
        Street("School Access Road", "Primary School", 30, 0.9, 40, 2, False, False, "Clear"),
        Street("Neighborhood Road", "Residential A", 35, 1.1, 40, 1, False, False, "Clear"),
    ],

    "City Clinic": [
        Street("Health Avenue", "Central Hospital", 35, 0.8, 40, 1, True, False, "Clear"),
        Street("Market Road", "Local Market", 30, 1.0, 35, 2, False, False, "Rain"),
        Street("Community Way", "High School", 30, 0.7, 35, 1, False, False, "Clear"),
    ],

    "Main University": [
        Street("University Avenue", "Engineering Faculty", 25, 0.4, 30, 1, False, False, "Clear"),
        Street("Campus Road", "Medical School", 25, 0.5, 30, 1, False, False, "Clear"),
        Street("City Connector", "Business Tower", 45, 1.8, 60, 3, False, False, "Rain"),
    ],

    "Engineering Faculty": [
        Street("University Avenue", "Main University", 25, 0.4, 30, 1, False, False, "Clear"),
        Street("Tech Road", "Tech Park", 35, 0.9, 40, 2, False, False, "Fog"),
    ],

    "Medical School": [
        Street("Campus Road", "Main University", 25, 0.5, 30, 1, False, False, "Clear"),
        Street("Health Link", "Central Hospital", 30, 1.2, 40, 2, False, False, "Rain"),
    ],
    "High School": [
        Street("Education Street", "Primary School", 30, 0.6, 35, 1, False, False, "Clear"),
        Street("Park Walk", "Community Park", 25, 0.8, 30, 2, False, False, "Rain"),
        Street("Neighborhood Link", "Residential C", 30, 0.7, 35, 1, False, False, "Clear"),
    ],

    "Primary School": [
        Street("Education Street", "High School", 30, 0.6, 35, 1, False, False, "Clear"),
        Street("Local Street", "Residential B", 25, 0.5, 30, 1, False, False, "Clear"),
        Street("School Access Road", "Children Hospital", 30, 0.9, 40, 2, False, False, "Clear"),
    ],

    "International School": [
        Street("Global Road", "High School", 35, 0.7, 40, 2, False, False, "Fog"),
        Street("Campus Access", "Community Park", 30, 0.9, 35, 1, False, False, "Clear"),
    ],

    "Central Park": [
        Street("Park Lane", "Central Hospital", 30, 1.0, 40, 2, False, False, "Fog"),
        Street("Green Way", "Community Park", 25, 0.6, 30, 1, False, False, "Clear"),
        Street("Museum Walk", "Museum", 20, 0.5, 25, 1, False, False, "Clear"),
    ],

    "Community Park": [
        Street("Green Way", "Central Park", 25, 0.6, 30, 1, False, False, "Clear"),
        Street("Park Walk", "High School", 25, 0.8, 30, 2, False, False, "Rain"),
        Street("Cultural Road", "Cultural Center", 30, 0.9, 35, 1, False, False, "Clear"),
    ],

    "Sports Club": [
        Street("Fitness Road", "Residential E", 30, 0.7, 35, 1, False, False, "Clear"),
        Street("Arena Way", "Convention Center", 40, 1.2, 50, 2, False, False, "Clear"),
    ],

    "City Mall": [
        Street("Commerce Avenue", "Business Tower", 35, 0.9, 40, 2, False, False, "Rain"),
        Street("Market Street", "Local Market", 30, 0.7, 35, 2, False, False, "Clear"),
        Street("Transit Road", "Metro Hub", 40, 1.1, 50, 3, False, False, "Clear"),
    ],

    "Local Market": [
        Street("Market Street", "City Mall", 30, 0.7, 35, 2, False, False, "Clear"),
        Street("Trade Road", "Wholesale Market", 35, 0.6, 40, 1, False, False, "Clear"),
        Street("Market Road", "City Clinic", 30, 1.0, 35, 2, False, False, "Rain"),
    ],

    "Wholesale Market": [
        Street("Trade Road", "Local Market", 35, 0.6, 40, 1, False, False, "Clear"),
        Street("Industrial Road", "Industrial Zone A", 45, 1.5, 60, 3, False, False, "Fog"),
    ],

    "Police Station": [
        Street("Security Road", "City Hall", 35, 0.8, 40, 1, False, False, "Clear"),
        Street("Response Route", "Fire Station", 40, 0.6, 45, 1, False, False, "Clear"),
    ],

    "Fire Station": [
        Street("Response Route", "Police Station", 40, 0.6, 45, 1, False, False, "Clear"),
        Street("Emergency Loop", "Industrial Zone B", 45, 1.4, 60, 3, False, False, "Rain"),
    ],

    "City Hall": [
        Street("Security Road", "Police Station", 35, 0.8, 40, 1, False, False, "Clear"),
        Street("Civic Avenue", "Old Town Square", 30, 0.5, 35, 1, False, False, "Clear"),
    ],

    "Bus Terminal": [
        Street("Transit Road", "Metro Hub", 40, 0.6, 50, 2, False, False, "Clear"),
        Street("Station Link", "Train Station", 35, 0.7, 40, 2, False, False, "Clear"),
    ],

    "Train Station": [
        Street("Station Link", "Bus Terminal", 35, 0.7, 40, 2, False, False, "Clear"),
        Street("Rail Avenue", "Old Town Square", 30, 0.8, 35, 1, False, False, "Clear"),
    ],

    "Metro Hub": [
        Street("Transit Road", "City Mall", 40, 1.1, 50, 3, False, False, "Clear"),
        Street("Transit Road", "Bus Terminal", 40, 0.6, 50, 2, False, False, "Clear"),
        Street("Industrial Link", "Industrial Zone A", 45, 1.3, 60, 3, False, False, "Fog"),
    ],

    "Residential A": [
        Street("Neighborhood Road", "Children Hospital", 35, 1.1, 40, 1, False, False, "Clear"),
        Street("Residential Street", "Residential B", 25, 0.4, 30, 1, False, False, "Clear"),
    ],

    "Residential B": [
        Street("Residential Street", "Residential A", 25, 0.4, 30, 1, False, False, "Clear"),
        Street("Local Street", "Primary School", 25, 0.5, 30, 1, False, False, "Clear"),
        Street("Community Link", "Residential C", 25, 0.5, 30, 1, False, False, "Clear"),
    ],

    "Residential C": [
        Street("Neighborhood Link", "High School", 30, 0.7, 35, 1, False, False, "Clear"),
        Street("Community Link", "Residential B", 25, 0.5, 30, 1, False, False, "Clear"),
        Street("Residential Road", "Residential D", 25, 0.5, 30, 1, False, False, "Clear"),
    ],

    "Residential D": [
        Street("Residential Road", "Residential C", 25, 0.5, 30, 1, False, False, "Clear"),
        Street("Sports Access", "Sports Club", 30, 0.8, 35, 1, False, False, "Clear"),
        Street("Mall Access", "City Mall", 35, 1.0, 40, 2, False, False, "Rain"),
    ],

    "Residential E": [
        Street("Fitness Road", "Sports Club", 30, 0.7, 35, 1, False, False, "Clear"),
        Street("Neighborhood Way", "Hotel Plaza", 35, 0.9, 40, 1, False, False, "Clear"),
    ],

    "Industrial Zone A": [
        Street("Industrial Road", "Wholesale Market", 45, 1.5, 60, 3, False, False, "Fog"),
        Street("Industrial Link", "Metro Hub", 45, 1.3, 60, 3, False, False, "Fog"),
        Street("Utility Road", "Power Station", 40, 1.1, 50, 2, False, False, "Clear"),
    ],

    "Industrial Zone B": [
        Street("Emergency Loop", "Fire Station", 45, 1.4, 60, 3, False, False, "Rain"),
        Street("Service Road", "Water Facility", 40, 1.0, 50, 2, False, False, "Clear"),
    ],

    "Power Station": [
        Street("Utility Road", "Industrial Zone A", 40, 1.1, 50, 2, False, False, "Clear"),
        Street("Grid Road", "Water Facility", 35, 0.8, 45, 1, False, False, "Clear"),
    ],

    "Water Facility": [
        Street("Service Road", "Industrial Zone B", 40, 1.0, 50, 2, False, False, "Clear"),
        Street("Grid Road", "Power Station", 35, 0.8, 45, 1, False, False, "Clear"),
    ],

    "Tech Park": [
        Street("Tech Road", "Engineering Faculty", 35, 0.9, 40, 2, False, False, "Fog"),
        Street("Innovation Way", "Research Center", 30, 0.8, 35, 1, False, False, "Clear"),
    ],

    "Research Center": [
        Street("Innovation Way", "Tech Park", 30, 0.8, 35, 1, False, False, "Clear"),
        Street("Science Road", "University", 35, 1.0, 40, 2, False, False, "Clear"),
    ],

    "Hotel Plaza": [
        Street("Neighborhood Way", "Residential E", 35, 0.9, 40, 1, False, False, "Clear"),
        Street("Business Route", "Business Tower", 40, 0.8, 50, 2, False, False, "Clear"),
    ],

    "Business Tower": [
        Street("Business Route", "Hotel Plaza", 40, 0.8, 50, 2, False, False, "Clear"),
        Street("Commerce Avenue", "City Mall", 35, 0.9, 40, 2, False, False, "Rain"),
        Street("City Connector", "Main University", 45, 1.8, 60, 3, False, False, "Rain"),
    ],

    "Convention Center": [
        Street("Arena Way", "Sports Club", 40, 1.2, 50, 2, False, False, "Clear"),
        Street("Event Road", "Old Town Square", 35, 1.0, 40, 2, False, False, "Clear"),
    ],

    "Old Town Square": [
        Street("Civic Avenue", "City Hall", 30, 0.5, 35, 1, False, False, "Clear"),
        Street("Rail Avenue", "Train Station", 30, 0.8, 35, 1, False, False, "Clear"),
        Street("Event Road", "Convention Center", 35, 1.0, 40, 2, False, False, "Clear"),
    ],

    "Museum": [
        Street("Museum Walk", "Central Park", 20, 0.5, 25, 1, False, False, "Clear"),
        Street("Culture Road", "Cultural Center", 25, 0.6, 30, 1, False, False, "Clear"),
    ],

    "Library": [
        Street("Knowledge Street", "Cultural Center", 25, 0.7, 30, 1, False, False, "Clear"),
        Street("Campus Access", "Main University", 30, 1.1, 40, 2, False, False, "Clear"),
    ],

    "Cultural Center": [
        Street("Culture Road", "Museum", 25, 0.6, 30, 1, False, False, "Clear"),
        Street("Cultural Road", "Community Park", 30, 0.9, 35, 1, False, False, "Clear"),
        Street("Knowledge Street", "Library", 25, 0.7, 30, 1, False, False, "Clear"),
    ],
    # Remaining locations follow the same fixed-condition pattern
}
