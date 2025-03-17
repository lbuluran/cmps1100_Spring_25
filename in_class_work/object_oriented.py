#Object oriented programming is a way to structure your code into re
#Here is a class for bicycles
class bike(object):
    def __init__(self, bike_type, location):
        self.bike_type = bike_type
        self.location = location
        self.flat = False
        self.owner = None
    def ride_to(self, destination):
        self.location = destination
    def become_flat(self):
        self.flat = True
        self.bike_type = "broken road bike"
    def fix_flat(self):
        self.flat = False
        self.bike_type = "road bike"
    def __repr__(self): #How to print out instance of bike
        return f"bike type: {self.bike_type} \nbike location: {self.location} \nflat? {self.flat}"

my_bike = bike('road_bike', 'uptown')
print(f'Our bike is a {my_bike.bike_type}')
my_bike.ride_to('by_water')
print(f'Our bike is at {my_bike.location}')
my_bike.become_flat()
print(f'Is our bike flat? {my_bike.flat}')
print(f"Current bike type {my_bike.bike_type}")


jons_bike = bike('mountain_bike', 'midcity')
print(jons_bike)