#This file contains the tests for the bike racing Homework2.
from unittest import TestCase
from homework2 import *
import unittest
from gradescope_utils.autograder_utils.decorators import weight, number, visibility

class CreateTests(TestCase):

    def test_unoptimized_race(self):
        '''
        This test checks that yoshi wins the race if none of the racers are optimized.
        '''
        marios_velocipede = velocipede([(1,1), (2,3), (1,2),(1,5),(1,7)], 30,efficiency = 0.8)
        warios_velocipede = velocipede([(1,1), (2,3), (1,2),(1,3),(1,5)], 30,efficiency = 0.7)
        yoshis_velocipede = velocipede([(3,1),(2,1),(1,1), (2,3), (1,2),(1,3),(1,5),(1,7)], 30, efficiency = 0.9)

        mario = rider("Mario",marios_velocipede, 50, 6000, 30,10,silent=True) #The parameters are name, velocipede, weight, max_stamina, regeneration, cost per pedal
        wario = rider("Wario", warios_velocipede, 100, 11000, 20, 20,silent=True)
        yoshi = rider("Yoshi", yoshis_velocipede, 75, 7000, 25, 15,silent=True)
        rainbow_road = track()
        grand_prix1 = race([mario,wario, yoshi],rainbow_road)
        winners = grand_prix1.start_race(silent=True)
        winners = [rider.name for rider in winners]
        assert yoshi.name in winners
        assert not mario.name in winners
        assert not wario.name in winners
    def test_small_changes(self):
        '''
        This test checks that improving one of the riders makes that rider the winner.
        The students do not need to make this test pass. It should already pass.
        The point of having this test is to provide some basic assurance that the code works reasonably,
        and to set a good example. Code should always have at least some tests.
        '''
        marios_velocipede = velocipede([(1,1), (2,3), (1,2),(1,5),(1,7)], 30,efficiency = 0.8)
        warios_velocipede = velocipede([(1,1), (2,3), (1,2),(1,3),(1,5)], 30,efficiency = 0.7)
        yoshis_velocipede = velocipede([(3,1),(2,1),(1,1), (2,3), (1,2),(1,3),(1,5),(1,7)], 30, efficiency = 0.9)
    
        rainbow_road = track()

        #create identical copies of each vehicle.
        marios_velocipede_copy = velocipede([(1,1), (2,3), (1,2),(1,5),(1,7)], 30,efficiency = 0.8)
        warios_velocipede_copy = velocipede([(1,1), (2,3), (1,2),(1,3),(1,5)], 30,efficiency = 0.7)
        yoshis_velocipede_copy = velocipede([(3,1),(2,1),(1,1), (2,3), (1,2),(1,3),(1,5),(1,7)], 30, efficiency = 0.9)
        
        #create two copies of yoshi.
        yoshi = rider("Yoshi", yoshis_velocipede, 75, 7000, 25, 15,silent=True)
        yoshi_improved = rider("ImprovedYoshi", yoshis_velocipede_copy, 25,7000,25,15,silent=True) #The improved yoshi is lighter and should be faster.
        rainbow_road= track()
        grand_prix1 = race([yoshi,yoshi_improved],rainbow_road)

        winners = grand_prix1.start_race(silent=True)
        winners = [rider.name for rider in winners]
        assert yoshi_improved.velocipede.location > yoshi.velocipede.location 

        #next, we check that increasing Mario's stamina makes him finish faster.        
        mario = rider("Mario", marios_velocipede,  50, 5000, 30,10,silent=True) #Mario actually does not finish the race with these parameters.
        mario_improved = rider("ImprovedMario", marios_velocipede_copy,50, 8000, 30, 10,silent=True)

        grand_prix2 = race([mario,mario_improved],rainbow_road)
        winners = grand_prix2.start_race(silent=True)
        winners = [rider.name for rider in winners]
        assert mario_improved.velocipede.location >= mario.velocipede.location

        #The last check is that decreasing the pedal energy cost will make Warrio faster.
        wario = rider("Wario", warios_velocipede,  100,11000, 20, 20,silent=True) #Mario actually does not finish the race with these parameters.
        wario_improved = rider("ImprovedWario", warios_velocipede_copy,100,11000, 20, 5,silent=True)

        grand_prix3 = race([wario,wario_improved],rainbow_road)
        winners = grand_prix3.start_race(silent=True)
        winners = [rider.name for rider in winners]
        assert wario_improved.velocipede.location > wario.velocipede.location


    @weight(20)
    @number('1')
    @visibility('visible')
    def test_mario_wins(self):

        '''
        Tests that mario wins when he is optimized and the others aren't.
        '''
        #reset velocipedes.
        marios_velocipede = velocipede([(1,1), (2,3), (1,2),(1,5),(1,7)], 30,efficiency = 0.8)
        warios_velocipede = velocipede([(1,1), (2,3), (1,2),(1,3),(1,5)], 30,efficiency = 0.7)
        yoshis_velocipede = velocipede([(3,1),(2,1),(1,1), (2,3), (1,2),(1,3),(1,5),(1,7)], 30, efficiency = 0.9)
        
        #reset riders. Optimize mario.
        mario = optimized_rider("Mario", marios_velocipede, 50, 6000, 30,10,silent=True) #The parameters are name, velocipede, weight, max_stamina, regeneration, cost per pedal
        wario = rider("Wario", warios_velocipede, 100, 11000, 20, 20,silent=True)
        yoshi = rider("Yoshi", yoshis_velocipede, 75, 7000, 25, 15,silent=True)
        rainbow_road=track()
        grand_prix1 = race([mario,wario, yoshi],rainbow_road)
        winners = grand_prix1.start_race(silent=True)
        winners = [racer.name for racer in winners]

        assert mario.name in winners
        assert not yoshi.name in winners
        assert not wario.name in winners
    
    @weight(10)
    @number('2')
    @visibility('visible')
    def test_wario_wins(self):

        '''
        tests that Wario wins when he is optimized and the others aren't.
        '''
        marios_velocipede = velocipede([(1,1), (2,3), (1,2),(1,5),(1,7)], 30,efficiency = 0.8)
        warios_velocipede = velocipede([(1,1), (2,3), (1,2),(1,3),(1,5)], 30,efficiency = 0.7)
        yoshis_velocipede = velocipede([(3,1),(2,1),(1,1), (2,3), (1,2),(1,3),(1,5),(1,7)], 30, efficiency = 0.9)
        
        #reset riders. Optimize mario.
        mario = rider("Mario", marios_velocipede, 50, 6000, 30,10,silent=True) #The parameters are name, velocipede, weight, max_stamina, regeneration, cost per pedal
        wario = optimized_rider("Wario", warios_velocipede, 100, 11000, 20, 20,silent=True)
        yoshi = rider("Yoshi", yoshis_velocipede, 75, 7000, 25, 15,silent=True)
        
        rainbow_road=track()
        grand_prix1 = race([mario,wario, yoshi],rainbow_road)
        winners = grand_prix1.start_race(silent=True)
        winners = [racer.name for racer in winners]

        assert wario.name in winners
        assert not yoshi.name in winners
        assert not mario.name in winners
    
if __name__=="__main__":
    unittest.main()