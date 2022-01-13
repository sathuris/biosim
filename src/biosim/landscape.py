# -*- encoding: utf-8 -*-

"""
This file wll contain a main class Landscape(Superclass).
The Landscape class will have four subclasses, Highland, Lowland, Desert and Water.

We will use information from this file to build our map of Rossumøya
"""
__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

import random

from src.biosim.animals import Herbivore, Carnivore


class Landscape:
    parameters = {}
    migration_possible = True

    @classmethod
    def set_parameters(cls, added_parameters):
        """
        Classmethod for setting the parameter for fodder.
        """
        for parameter, value in added_parameters.items():
            if value < 0:
                raise ValueError("Inputted parameters for fodder can not be negative!")
            cls.parameters[parameter] = value
        cls.parameters.update(added_parameters)

    def __init__(self):
        """
        Empty list to count the population, and here will we append the new values every year.
        Food count starts at f_max which will be updated every year.
        """
        self.param = None
        self.herbivores = []
        self.carnivores = []
        self.fodder = self.parameters["f_max"]  # Kanskje ha en test her, om denne verdien er
        # mindre enn null.
        self.kill_probability = None
        self.migrate_probability = 0
        self.neighbors = []

    def population_update(self, population_list):
        """
        This function updates the population for a given list with animals.
        It will also separately put the species in their respective list.
        """
        for individual in population_list:
            if individual["species"] == "Herbivore":
                self.herbivores.append(Herbivore(age=individual["age"],
                                                 weight=individual["weight"]))

        for individual in population_list:
            if individual["species"] == "Carnivore":
                self.carnivores.append(Carnivore(age=individual["age"],
                                                 weight=individual["weight"]))

    def display_herbivores(self):
        """
        This function will display the number of herbivores in the self.herbivores list
        :return: the herbivore count
        """
        return len(self.herbivores)

    def display_carnivores(self):
        """
        This function will display the number of carnivores in the self.carnivores list
        :return: the carnivore count
        """
        return len(self.carnivores)

    def new_fodder(self):
        """
        Function to add the parameter "f_max" every year in Lowland and Highland
        """
        self.fodder = self.parameters["f_max"]

    def aging_population(self):
        """
        This function will age all the living population on Rossumøya
        every year since it common for both carnivores and herbivores
        """

        for individual in self.herbivores:  # egentlig bare individual!
            individual.aging()

        for individual in self.carnivores:
            individual.aging()

    def eat_fodder(self):
        """
        Function to reduce the fodder after the herbivore are pleased with themselves.
        Then remove the fodder amount that have been consumed by the herbivores
        Using random shuffle to let the herbivores eat in a random order, and break the loop
        if the fodder amount is on 0
        """
        # random.shuffle(self.herbivores)
        self.herbivores.sort(key=lambda x: "fitness") # Because herbivores eat from highest fitness
                                                    #to lowest fitness.
        for individual in self.herbivores:

            if self.fodder == 0:
                break

            elif self.fodder >= individual.param["F"]:
                individual.weight_increase(individual.param["F"])
                self.fodder -= individual.param["F"]

            elif self.fodder < individual.param["F"]:
                individual.weight_increase(self.fodder)
                self.fodder = 0

    def death_population(self):
        """
        Remove the animals that have died from the population list
        """
        self.herbivores = [individual for individual in self.herbivores
                           if not individual.death_animal()]
        self.carnivores = [individual for individual in self.carnivores
                           if not individual.death_animal()]

    def newborn_herbivore(self):
        """
        Adding the newborn herbivore to the population list
        Making a new list, then we can extend the population list
        If the amount of one species is lower than 2 the functions won't execute
        """
        herbivore_count = len(self.herbivores)

        if herbivore_count < 2:
            return False

        newborn_herbivore = []
        if herbivore_count >= 2:
            for individual in self.herbivores:
                newborn = individual.birth(herbivore_count)
                if newborn is not None:
                    newborn_herbivore.append(newborn)
        self.herbivores.extend(newborn_herbivore)

    def newborn_carnivore(self):
        """
        Adding the newborn carnivore to the population list
        Making a new list, then we can extend the population list
        If the amount of one species is lower than 2 the functions won't execute
        """
        individual_count = len(self.carnivores)

        if individual_count < 2:
            return False

        newborn_carnivore = []
        if individual_count >= 2:
            for individuals in self.carnivores:
                newborn = individuals.birth(individual_count)
                if newborn is not None:
                    newborn_carnivore.append(newborn)
        self.carnivores.extend(newborn_carnivore)

    def weight_loss(self):
        """
        The animals on the island will lose a specific amount of weight,
        and this will happen on this function
        """

        for individual in self.herbivores:
            return individual.weight_decrease()

        for individual in self.carnivores:
            return individual.weight_decrease()

    def prey(self):
        """
        Method for the prey of a herbivore by the carnivore.
        I have to add a way of calculating how much the carnivore has eaten.
        """
        # herbivores_newlist = sorted(herbivores_list, key=lambda x: "fitness", reverse=True)
        random.shuffle(self.carnivores)
        # carnivore = self.carni[0]

        # herbivores_newlist = sorted(herbivores_list, key=lambda x: "fitness", reverse=True)

        self.herbivores.sort(key=lambda x: "fitness", reverse=True)
        ate = 0

        for carnivore in self.carnivores:
            for herbivores in self.herbivores:

                kill_probability = 0

                if ate >= carnivore.param["F"] and carnivore.fitness <= herbivores.fitness:
                    pass
                elif 0 < carnivore.fitness - herbivores.fitness < carnivore.param["DeltaPhiMax"]:
                    kill_probability = (carnivore.fitness - herbivores.fitness) / \
                                       carnivore.param["DeltaPhiMax"]

                else:

                    kill_probability = 1
                if kill_probability < random.random():
                    w = herbivores.weight
                    if ate + herbivores.weight > carnivore.param["F"]:
                        w = carnivore.param["F"] - ate
                        ate = carnivore.param["F"]

                    ate += herbivores.weight
                    herbivores.death_animal()
                    carnivore.weight += carnivore.param["beta"] * w
                    carnivore.fitness_animal()

                carnivore.weight += carnivore.param["beta"] * herbivores.weight
                ate += herbivores.weight
                herbivores.death = True
                carnivore.fitness_animal()

            self.death_population()  # finne en ny måte å fjerne herb på

    def migrated_animals(self):

        """
        This is not how it should be done, but I have done it for now. Ask TA about a better way
        of doing this.
        """

        # migrated_herbivores = []
        # migrated_carnivores = []

        for herbivore in self.herbivores:
            if not herbivore.migrate and herbivore.migration_probability():
                arrival_cell = random.choice(self.neighbors)
                if arrival_cell.migration_possible:
                    herbivore.migrate = True
                    arrival_cell.herbivores.append(herbivore)
                    self.herbivores.remove(herbivore)
                else:
                    break

        for carnivore in self.carnivores:
            if not carnivore.migrate and carnivore.migration_probability():
                arrival_cell = random.choice(self.neighbors)
                if arrival_cell.migration_possible:
                    carnivore.migrate = True
                    arrival_cell.carnivores.append(carnivore)
                    self.carnivores.remove(carnivore)
                else:
                    break

    def annual_cycle(self):
        self.new_fodder()
        self.eat_fodder()
        # self.prey()
        self.newborn_herbivore()
        # self.newborn_carnivore()
        # self.migrated_animals()

        self.aging_population()
        self.weight_loss()
        self.death_population()


class Lowland(Landscape):
    """
    This class is a subclass of the Landscape class to portray the lowland
    """
    parameters = {"f_max": 800}


class Water(Landscape):
    """
    This class is a subclass of the Landscape class to portray the water
    """
    parameters = {"f_max": 0}
    migration_possible = False

    #    rc = len(self.map) #rows
    #    len(self.map[0]) #columns

    def annual_cycle(self):
        pass


class Highland(Landscape):
    """
    This class is a subclass of the Landscape class to portray the highland
    """
    parameters = {"f_max": 300}


class Desert(Landscape):
    """
    This class is a subclass of the Landscape class to portray the desert
    """
    parameters = {"f_max": 0}
