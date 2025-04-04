from unittest import TestCase
from homework2 import *
import unittest
from gradescope_utils.autograder_utils.decorators import weight, number, visibility

TIMESTEP_CONSTANT = 5.0 #Each timestep represents this many seconds.
class velocipede(object):
    def __init__(self, gear_ratios, weight, wheel_circumference = 5.0, efficiency=0.9): #gear_ratios is a list of tuples [(p,w)], 
                                                #where p is the number of times the pedal turns and w is the number of times the wheel turns. This is assumed to be in order.
                                             #weight is a floating point number, representing the weight in pounds.
        self.gear_ratios = gear_ratios #an ordered list of tuples. A tuple (p,w) means that the gear ratio is w/p. w is the number of times the wheel turns, p is the number of times the pedals turn.
        self.weight = weight # A float.
        self.current_gear_ratio_index = 0 #start in the lowest gear.
        self.current_gear_ratio = self.gear_ratios[0]
        self.current_speed = 0.0 #A float, the current speed.
        self.location = 0.0 #A float. Represents how far along the track the velocipede has moved.
        self.efficiency = efficiency #a float that represents how much the bike will slow if the rider doesn't pedal.
        self.wheel_circumference = wheel_circumference #a float.

    def __repr__(self):
        return(f"Gear is {self.current_gear_ratio} and weight is {round(self.weight,2)}. \n Located at {round(self.location,2)}.")
    
    def change_gears(self, increase): #expects increase to be an integer. How many gears to shift up if positive, how many down if negative. 0 if no shift.
            #Returns none, has the side effect of changing self.current_gear_ratio.
        self.current_gear_ratio_index = max( min( self.current_gear_ratio_index +increase, len(self.gear_ratios)-1),0)
        self.current_gear_ratio=self.gear_ratios[self.current_gear_ratio_index]
    def update_location(self):
        #Expects none and returns none. Has the side effect of updating the location using the speed.
        self.location = self.location + TIMESTEP_CONSTANT*self.current_speed

class bicycle(velocipede): 
    '''This class inherits from velocipede, 
    so any functions defined for the velocipede 
    are automatically defined for the bicycle.

    The benefits are that the code is more organized,
    and we avoid duplicating the code to (for example) switch gears.
    This means that if we need to change our function to switch gears,
    then we only need to make that change in one place.
    '''
    def wheelie(self): #Expects none, returns none.
        '''
        This is an example of how we can define functions 
        that are unique to bicycles and are not contained 
        in the velocipede class.
        '''
        print("sick wheelie")

class rider(object):
    '''
    This class contains information about the bicycle riders.
    '''
    def __init__(self, name, velocipede_to_ride, weight, max_stamina, regeneration, pedal_energy_cost,silent = False):
        self.name = name #Expected to be a string, the name of the rider.
        self.velocipede = velocipede_to_ride #Expected to be an instance of the velocipede class.
        self.weight = weight #Expected to be a float.
        self.stamina = max_stamina #The rider initially has full stamina.
        self.max_stamina = max_stamina #Expected to be a float that represents jouls.
        self.regeneration = regeneration
        self.pedal_energy_cost = pedal_energy_cost #A float. The amount of stamina required to make the pedals turn once, ignoring resistance.
            #The point of pedal_energy_cost is to prevent you from staying in the lowest gear and pedaling really fast.
        self.silent = silent #used to suppress printing.
    def gear_switch_policy(self,track):
        #Returns an integer. How many gears to go up or down.
        return 1 #the rider always switches gears up.
    def pedal_policy(self,track):
        #Returns a float. How many times to pedal in the timestep.
        return 5 #the rider always pedals 5 times.
    
    def pedal_energy_and_speed(self, num_rotations):
        #Returns a tuple: (speed, energy). Energy: A tuple (kinetic_energy_cost, low_gear_cost, high_gear_cost) The sum of these is the amount of stamina it will cost.
        #                                   Speed: The speed that the bike will be going if that happens.
        #Side-Effects: None
        old_speed = self.velocipede.current_speed*self.velocipede.efficiency #The speed if pedaling stops.
        ratio = self.velocipede.current_gear_ratio[1]/self.velocipede.current_gear_ratio[0] #each revolution of the pedals moves the bike this far.
        total_weight = self.weight+self.velocipede.weight
        new_speed = max(old_speed, TIMESTEP_CONSTANT * num_rotations * ratio * self.velocipede.wheel_circumference)
  
        #Calculate the energy difference caused by pedaling.
        old_energy = 0.00005*(total_weight)*old_speed**2
        new_energy = 0.00005*(total_weight)*new_speed**2
        kinetic_energy_cost = new_energy-old_energy
        #We also add an energy cost for doing each rotation, regardless of how much resistance there is. This rules out pedaling very fast in a low gear.
        low_gear_cost = self.pedal_energy_cost * num_rotations *TIMESTEP_CONSTANT

        high_gear_cost = 0.1*total_weight*(max(new_speed - old_speed,0))/(TIMESTEP_CONSTANT)*ratio
        return (new_speed, (kinetic_energy_cost, low_gear_cost, high_gear_cost))
    def pedal(self, num_rotations):
        #Input: num_rotations is expected to be a float.
        #Output: None.
        #Side-effects: Updates the speed and stamina after pedaling this number of times. Does nothing if the rider lacks the energy.
        new_speed, energy_breakdown = self.pedal_energy_and_speed(num_rotations)
        #print(f"energy breakdown: {energy_breakdown}")
        change_in_energy = energy_breakdown[0]+ energy_breakdown[1]+ energy_breakdown[2]
        new_stamina = self.stamina - change_in_energy
        if new_stamina < 0 or energy_breakdown[0]<0.01: #If the rider doesn't have the energy to do the pedaling...
            if not self.silent:
                print(f"{self.name} is out of energy.\n energy: {self.stamina}")
            self.velocipede.current_speed = self.velocipede.current_speed *self.velocipede.efficiency
            return #do nothing
        else:
            self.stamina = new_stamina #Return the energy to him.
            self.velocipede.current_speed = new_speed #set the speed to be the speed from coasting.
    
    def regenerate(self):
        #Input: None, Output: None
        #Side Effects: increase stamina by the regeneration amount.
        self.stamina = min(self.max_stamina, self.stamina + self.regeneration*TIMESTEP_CONSTANT)

    def handle_timestep(self, track):
        #Returns False if the rider has not crossed the finish line.
        #Returns True if the rider has crossed the finish line.
        num_rotations = self.pedal_policy(track)
        self.velocipede.change_gears(self.gear_switch_policy(track))
        
        self.pedal(num_rotations) #sets the speed.
        self.regenerate() #Recover some stamina.
        self.velocipede.update_location()
        return self.velocipede.location > track.distance
    def __repr__(self):
        return f"Name: {self.name}, Location: {round(self.velocipede.location,2)}, speed: {round(self.velocipede.current_speed,2)}, \n gear: {self.velocipede.current_gear_ratio}, stamina: {round(self.stamina,2)}"

class track(object):
    def __init__(self,distance=10000):
        #distance is the length of the track. 
        self.distance = distance

class race(object):
    def __init__(self, racers, course):
        self.racers = racers
        self.track = course
    def __repr__(self):
        #We'll print out the race by dividing the track into 25 pieces.
        #We'll figure out which piece each racer is in.
        #We need as many lines as the piece of track with the most racers.
        #We print the first letter of their name to indicate their location.
        distance = self.track.distance
        piece_length = distance /25
        simplified_locations = [ (int(racer.velocipede.location / piece_length), racer.name)for racer in self.racers] #For example, could be [(2,M)] to indicate Mario is on the second piece of track.
        placed_racers = [] #The racers that have been printed.
        return_strings = []
        current_string = []
        while len(placed_racers)<len([racer for racer in self.racers if racer.velocipede.location < self.track.distance]): #keep looping until all of the racers that haven't finished have been printed.
            for index in range(25): #loop through the entire track.
                relevant_markers = [marker for marker in simplified_locations if marker[0]==index and not marker[1] in placed_racers] #Represents the riders that will be placed now.
                if len(relevant_markers) == 0:
                    if len(return_strings)==0:
                        current_string.append('-') #The first line uses dashes to represent the road.
                    else:
                        current_string.append(' ') #later lines use spaces.
                else:
                    current_string.append(relevant_markers[0][1][0]) #Place the zeroth of the relevant riders.
                    placed_racers.append(relevant_markers[0][1]) #Add the marker to the placed riders to indicate that this rider has already been printed.
            return_strings.append("".join(current_string)+'\n')
            current_string = []
        return "".join(return_strings)

    def start_race(self, silent = False): #Does the race. Returns the winner(s). Side-effects: Updates the racers and their velocipedes' locations and speeds.
        while True:
            wins= [racer.handle_timestep(self.track) for racer in self.racers]
            if any(wins):
                return [racer for racer in self.racers if racer.velocipede.location >= self.track.distance] #Return the list of riders that win.
            elif not silent: #Only print the race if it's not set to silent mode.
                print(self)

'''
Instructions:
Implement a class called user_rider that asks the user for input to determine the number of times to pedal and how to shift gears.
Play around to find a strategy that causes Mario and Wario to win when the other riders stick to the default strategy.
Then, implement a class called optimized_rider that overwrites the rider class and implements your strategy programmatically.
You may not change the parameters of the riders or their velocipedes. You can only chang the pedal policy or gear shift policy.
You may use a different strategy for Mario than for Wario, though I didn't find this necessary.
You may add more attributes to your optimized_rider class to help plan their strategy. I found it useful to store the previous pedal amount and previous energy breakdown.
You may add more print statements to get more information about what strategies work.
I found it helpful to use the super() keyword, which refers to the parent class.
'''

# Add these inside your homework2.py at the bottom, replacing the TODO stubs:

class user_rider(rider):
    def gear_switch_policy(self, track):
        try:
            shift = int(input(f"{self.name}: Enter how many gears to shift (positive = up, negative = down, 0 = stay): "))
        except ValueError:
            print("Invalid input, staying in current gear.")
            shift = 0
        return shift

    def pedal_policy(self, track):
        try:
            pedals = float(input(f"{self.name}: Enter how many times to pedal this round: "))
        except ValueError:
            print("Invalid input, pedaling 0 times.")
            pedals = 0.0
        return pedals

class optimized_rider(rider):
    def __init__(self, name, velocipede_to_ride, weight, max_stamina, regeneration, pedal_energy_cost, silent=False):
        super().__init__(name, velocipede_to_ride, weight, max_stamina, regeneration, pedal_energy_cost, silent)
        self.previous_energy = (0, 0, 0)
        self.pedals_last = 5

    def gear_switch_policy(self, track):
        current_index = self.velocipede.current_gear_ratio_index
        max_index = len(self.velocipede.gear_ratios) - 1
        speed = self.velocipede.current_speed

        # Shift up if stamina is decent and not already at high gear
        if self.stamina > self.max_stamina * 0.5 and current_index < max_index:
            return 1
        # Shift down if stamina is low or speed has dropped significantly
        elif self.stamina < self.max_stamina * 0.2 and current_index > 0:
            return -1
        return 0

    def pedal_policy(self, track):
        max_safe_energy = self.stamina * 0.8
        max_pedal = 8

        best_pedal = 1
        best_speed = self.velocipede.current_speed
        for pedals in range(1, max_pedal + 1):
            speed, energy = self.pedal_energy_and_speed(pedals)
            cost = sum(energy)
            if cost <= max_safe_energy and speed > best_speed:
                best_pedal = pedals
                best_speed = speed

        self.previous_energy = self.pedal_energy_and_speed(best_pedal)[1]
        return best_pedal
    pass
if __name__=="__main__":
    #The code here also appears in test_unoptimized_race in the test file.
    #Using the default pedal policy, Yoshi should win the race.
    marios_velocipede = velocipede([(1,1), (2,3), (1,2),(1,5),(1,7)], 30,efficiency = 0.8)
    warios_velocipede = velocipede([(1,1), (2,3), (1,2),(1,3),(1,5)], 30,efficiency = 0.7)
    yoshis_velocipede = velocipede([(3,1),(2,1),(1,1), (2,3), (1,2),(1,3),(1,5),(1,7)], 30, efficiency = 0.9)

    mario = rider("Mario",marios_velocipede, 50, 6000, 30,10) #The parameters are name, velocipede, weight, max_stamina, regeneration, cost per pedal
    wario = rider("Wario", warios_velocipede, 100, 11000, 20, 20)
    yoshi = rider("Yoshi", yoshis_velocipede, 75, 7000, 25, 15)
    rainbow_road = track()
    grand_prix1 = race([mario,wario, yoshi],rainbow_road)
    print(f"And the winner is: {grand_prix1.start_race()}")