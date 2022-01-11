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
    parameters = {"f_max": 800}

    def __init__(self):
        """
        Empty list to count the population, and here will we append the new values every year.
        Food count starts at f_max which will be updated every year.
        """
        self.param = None
        self.herbivores = []
        self.carnivores = []
        self.fodder = self.parameters["f_max"]
        self.kill_probability = None

    def population_update(self, population_list):
        """
        This function updates the population for a given list with animals.
        It will also separately put the species in their respective list.
        """
        for individuals in population_list:
            if individuals["species"] == "Herbivore":
                self.herbivores.append(Herbivore(age=individuals["age"],
                                                 weight=individuals["weight"]))

        for individuals in population_list:
            if individuals["species"] == "Carnivore":
                self.carnivores.append(Carnivore(age=individuals["age"],
                                                 weight=individuals["weight"]))

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

        for individuals in self.herbivores:
            individuals.aging()

        for individuals in self.carnivores:
            individuals.aging()

    def eat_fodder(self):
        """
        Function to reduce the fodder after the herbivore are pleased with themselves.
        Then remove the fodder amount that have been consumed by the herbivores
        Using random shuffle to let the herbivores eat in a random order, and break the loop
        if the fodder amount is on 0
        """
        random.shuffle(self.herbivores)
        for individuals in self.herbivores:

            if self.fodder == 0:
                break

            elif self.fodder >= individuals.param["F"]:
                individuals.weight_increase(individuals.param["F"])
                self.fodder -= individuals.param["F"]

            elif self.fodder < individuals.param["F"]:
                individuals.weight_increase(self.fodder)
                self.fodder = 0

    def death_population(self):
        """
        Remove the animals that have died from the population list
        """
        self.herbivores = [individuals for individuals in self.herbivores
                           if not individuals.death_animal()]
        self.carnivores = [individuals for individuals in self.carnivores
                           if not individuals.death_animal()]

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
            for individuals in self.herbivores:
                newborn = individuals.birth(herbivore_count)
                if newborn is not None:
                    newborn_herbivore.append(newborn)
        self.herbivores.extend(newborn_herbivore)

    def newborn_carnivore(self):
        """
        Adding the newborn carnivore to the population list
        Making a new list, then we can extend the population list
        If the amount of one species is lower than 2 the functions won't execute
        """
        individuals_count = len(self.carnivores)

        if individuals_count < 2:
            return False

        newborn_carnivore = []
        if individuals_count >= 2:
            for individuals in self.carnivores:
                newborn = individuals.birth(individuals_count)
                if newborn is not None:
                    newborn_carnivore.append(newborn)
        self.carnivores.extend(newborn_carnivore)

    def weight_loss(self):
        """
        The animals on the island will lose a specific amount of weight,
        and this will happen on this function
        """

        for individuals in self.herbivores:
            return individuals.weight_decrease()

        for individuals in self.carnivores:
            return individuals.weight_decrease()

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
                    kill_probability = (carnivore.fitness - herbivores.fitness) /\
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

            self.death_population()

    def simulate(self):
        self.new_fodder()
        self.eat_fodder()
        self.prey()
        self.newborn_herbivore()
        self.newborn_carnivore()

        self.aging_population()
        self.weight_loss()
        self.death_population()



class Lowland(Landscape):
    """
    This class is a subclass of the Landscape class to portray the lowland
    """
    parameters = {"f_max": 800}

    def __init__(self):
        super().__init__()


class Water(Landscape):
    """
    This class is a subclass of the Landscape class to portray the water
    """
    parameters = {"f_max": 0}

    def __init__(self):
        super().__init__()
