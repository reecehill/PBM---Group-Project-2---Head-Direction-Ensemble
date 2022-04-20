import numpy as np
import parameters as p
import weightHandler as wh
from classes.NeuronalPopulation import NeuronalPopulation

def generatePopulation():
    # Population collection format is inspired by Eloquent, Laravel: https://laravel.com/docs/9.x/eloquent
    population = NeuronalPopulation()
    
    np.savetxt(p.outputDirectory+'/noiseless-weights.csv',
               [neurone.weights for neurone in population.neurones], delimiter=',')
    return population


def getPopulationWeights(neuronalPopulation):
    return [neurone.weights for neurone in neuronalPopulation.neurones]
