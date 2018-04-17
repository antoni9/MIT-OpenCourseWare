# 6.00 Problem Set 12
#
# Name:
# Collaborators:
# Time:

import numpy as np
import random
import pylab


class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """


#
# PROBLEM 1
#

class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """

    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)

        clearProb: Maximum clearance probability (a float between 0-1).
        """
        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def doesClear(self):
        """
        Stochastically determines whether this virus is cleared from the
        patient's body at a time step.

        returns: Using a random number generator (random.random()), this method
        returns True with probability self.clearProb and otherwise returns
        False.
        """
        # TODO
        if random.random() <= self.clearProb:
            return True
        else: return False

    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        # TODO
        if self.maxBirthProb * (1 - popDensity) >= random.random():
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException


class SimplePatient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """
        # TODO
        self.viruses = viruses
        self.maxPop = maxPop

    def getTotalPop(self):
        """
        Gets the current total virus population.

        returns: The total virus population (an integer)
        """
        # TODO
        return len(self.viruses)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
          of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update()

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.

        returns: the total virus population at the end of the update (an
        integer)
        """
        # TODO
        for virus in self.viruses:
            if virus.doesClear():
                self.viruses.pop(self.viruses.index(virus))
        self.newViruses = []
        for virus in self.viruses:
            self.popDensity = (len(self.viruses) + len(self.newViruses)) / self.maxPop
            if self.popDensity >= 1:
                break   # Population not sustainable
            try:
                self.newViruses.append(virus.reproduce(self.popDensity))
            except NoChildException:
                None
        self.viruses = self.viruses + self.newViruses
        return len(self.viruses)

#
# PROBLEM 2
#

def problem2(virusCount, maxBirthProb, clearProb, maxPop):
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).

    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.
    """
    # TODO
    viruses = []
    virAtTimeStep = []
    for i in range(0, virusCount):
        viruses.append(SimpleVirus(maxBirthProb, clearProb))
    patient = SimplePatient(viruses, maxPop)
    for timeStep in range(0, 300):
        v = patient.update()
        virAtTimeStep.append(v)
    return virAtTimeStep

def runProblem2(numTimes):
    """ Gets averages for each time step of problem2 and plots smooth/averaged curves
    :param numTimes: int
    :return: plot
    """
    virAtTimeStep = []
    for trial in range(0, numTimes):
        virAt = problem2(100, 0.1, 0.05, 1000)
        if virAtTimeStep == []:
            virAtTimeStep = virAt
        else:
            virAtTimeStep = list(np.average([virAtTimeStep, virAt], axis=0))

    pylab.plot(virAtTimeStep)
    pylab.xlabel('time')
    pylab.ylabel('virus count')
    pylab.title('untreated patient, t=300')

# The difference in the smoothness of the curve running 10 trials and 100 trials is negligible
# runProblem2(1)


#
# PROBLEM 3
#

class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb

    def getResistance(self, drugs):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.

        drug: the drug (a string).

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        # TODO
        for drug in drugs.keys():
            if self.resistances[drug] == False:
                return False
        else: return True

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:

        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        # TODO
        if self.maxBirthProb * (1 - popDensity) >= random.random():
            self.mutatedResistances = {}
            for resistance in self.resistances:
                if self.mutProb >= random.random():
                    self.mutatedResistances[resistance] = not self.resistances[resistance]
                else:
                    self.mutatedResistances[resistance] = self.resistances[resistance]
            new = ResistantVirus(self.maxBirthProb, self.clearProb, self.mutatedResistances, self.mutProb)
            return new
        else:
            raise NoChildException

class Patient(SimplePatient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """
        # TODO
        self.viruses = viruses
        self.maxPop = maxPop
        self.drugs = {}

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        # TODO
        if newDrug not in self.drugs:
            self.drugs[newDrug] = True

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        # TODO
        return list(self.drugs.keys())

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        # TODO
        self.resistantViruses = []
        for virus in self.viruses:
            if virus.getResistance(drugResist):
                self.resistantViruses.append(virus)
        return len(self.resistantViruses)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: the total virus population at the end of the update (an
        integer)
        """
        # TODO
        for virus in self.viruses:
            if virus.doesClear():
                self.viruses.pop(self.viruses.index(virus))
            if len(self.drugs) > 0:
                if not virus.getResistance(self.drugs):
                    try:
                        self.viruses.pop(self.viruses.index(virus))
                    except ValueError:
                        None
        self.newViruses = []
        for virus in self.viruses:
            self.popDensity = (len(self.viruses) + len(self.newViruses)) / self.maxPop
            if self.popDensity >= 1:
                break   # Population not sustainable
            try:
                self.newViruses.append(virus.reproduce(self.popDensity, self.drugs))
            except NoChildException:
                None
        self.viruses = self.viruses + self.newViruses

        self.virusGuttagonol, self.virusGrimpex = 0, 0
        for virus in self.viruses:
            if virus.getResistance({'guttagonol': True}):
                self.virusGuttagonol += 1
            if virus.getResistance({'grimpex': True}):
                self.virusGrimpex += 1

        return len(self.viruses), self.virusGuttagonol, self.virusGrimpex

#
# PROBLEM 4
#

def problem4(virusCount, maxBirthProb, clearProb, maxPop, mutProb, delay):
    """
    Runs simulations and plots graphs for problem 4.

    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.

    total virus population vs. time  and guttagonol-resistant virus population
    vs. time are plotted
    """
    # TODO
    viruses = []
    virAtTimeStep = []
    resVirAtTimeStep = []
    resistances = {'guttagonol': False}
    for i in range(0, virusCount):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
    patient = Patient(viruses, maxPop)
    for timeStep in range(0, delay):
        v = patient.update()
        virAtTimeStep.append(v)
        resVirAtTimeStep.append(patient.getResistPop(resistances))
    patient.addPrescription('guttagonol')
    for timeStep in range(0, 150):
        v = patient.update()
        virAtTimeStep.append(v)
        resVirAtTimeStep.append(patient.getResistPop(resistances))

    return virAtTimeStep, resVirAtTimeStep

def runProblem4(numTimes, delay):
    """ Gets averages for each time step of problem4 and plots smooth/averaged curves
    :param numTimes: int
    :return: plot
    """

    virAtTimeStep, resVirAtTimeStep = [], []
    for trial in range(0, numTimes):
        virAt, resVirAt = problem4(100, 0.1, 0.05, 1000, 0.005, delay)
        if virAtTimeStep == []:
            virAtTimeStep = virAt
            resVirAtTimeStep = resVirAt
        else:
            virAtTimeStep = list(np.average([virAtTimeStep, virAt], axis=0))
            resVirAtTimeStep = list(np.average([resVirAtTimeStep, resVirAt], axis=0))

    pylab.figure()
    pylab.plot(virAtTimeStep, label='non-resistant')
    pylab.plot(resVirAtTimeStep, label='resistant')
    pylab.legend()
    pylab.xlabel('time')
    pylab.ylabel('virus count')
    pylab.title('treated patient, t=%d+drug+150'%(delay))
    # pylab.show()

# The difference in the smoothness of the curve running 10 trials and 100 trials is negligible
# runProblem4(10, 150)


#
# PROBLEM 5
#

def problem5():
    """
    Runs simulations and make histograms for problem 5.

    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).
    """
    # TODO
    for delay in [300, 150, 75, 0]:
        runProblem4(10, delay)
    pylab.show()

# problem5()

#
# PROBLEM 6
#

def problem6(virusCount, maxBirthProb, clearProb, maxPop, mutProb, delayDrug2):
    """
    Runs simulations and make histograms for problem 6.

    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    # TODO
    viruses = []
    virAtLastTimeStep = []
    resVirAtLastTimeStepAll, resVirAtLastTimeStepGuttagonol, resVirAtLastTimeStepGrimpex = [], [], []
    resistances = {'guttagonol': False, 'grimpex': False}
    for i in range(0, virusCount):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
    patient = Patient(viruses, maxPop)
    for timeStep in range(0, 150):
        v = patient.update()
        virAtLastTimeStep.append(v)
        resVirAtLastTimeStepGuttagonol.append(patient.getResistPop({'guttagonol': False}))
        resVirAtLastTimeStepGrimpex.append(patient.getResistPop({'grimpex': False}))
    patient.addPrescription('guttagonol')
    for timeStep in range(0, delayDrug2):
        v = patient.update()
        virAtLastTimeStep.append(v)
        resVirAtLastTimeStepGuttagonol.append(patient.getResistPop({'guttagonol': False}))
        resVirAtLastTimeStepGrimpex.append(patient.getResistPop({'grimpex': False}))
    patient.addPrescription('grimpex')
    for timeStep in range(0, 149):
        v = patient.update()
        virAtLastTimeStep.append(v)
        resVirAtLastTimeStepGuttagonol.append(patient.getResistPop({'guttagonol': False}))
        resVirAtLastTimeStepGrimpex.append(patient.getResistPop({'grimpex': False}))
    for timeStep in range(0, 1):
        v = patient.update()
        virAtLastTimeStep.append(v)
        resVirAtLastTimeStepGuttagonol.append(patient.getResistPop({'guttagonol': False}))
        resVirAtLastTimeStepGrimpex.append(patient.getResistPop({'grimpex': False}))

    return virAtLastTimeStep, resVirAtLastTimeStepAll, resVirAtLastTimeStepGuttagonol, resVirAtLastTimeStepGrimpex



def runProblem6(delays):
    for delay in delays:
        virAtTimeStep, resVirAtTimeStep = [], []
        for trial in range(0, 30):
            virAt, resVirAt = problem6(100, 0.1, 0.05, 1000, 0.005, delay)
            if virAtTimeStep == []:
                virAtTimeStep = virAt
                resVirAtTimeStep = resVirAt
            else:
                virAtTimeStep = list(np.average([virAtTimeStep, virAt], axis=0))
                resVirAtTimeStep = list(np.average([resVirAtTimeStep, resVirAt], axis=0))

        pylab.figure()
        pylab.plot(virAtTimeStep, label='non-resistant')
        pylab.plot(resVirAtTimeStep, label='resistant')
        pylab.legend()
        pylab.xlabel('time')
        pylab.ylabel('virus count')
        pylab.title('treated patient, t=150+drug1+%d+drug2+150' % (delay))

    pylab.show()

# Only delay of 0 between drugs results in final population < 50viruses
# runProblem6([300, 150, 75, 50, 25, 0])

#
# PROBLEM 7
#

def runProblem7(delays):
    """
    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.

    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.
    """
    # TODO
    for delay in delays:
        virAtTimeStep, resVirAtAll, resVirAtTimeStepGuttagonol, resVirAtTimeStepGrimpex = [], [], [], []
        for trial in range(0, 30):
            virAt, resVirAtAll, resVirAtGu, resVirAtGr = problem6(100, 0.1, 0.05, 1000, 0.005, delay)
            if virAtTimeStep == []:
                virAtTimeStep = virAt
                # resVirAtAll = np.add(resVirAtGu, resVirAtGr)
                resVirAtTimeStepGuttagonol = resVirAtGu
                resVirAtTimeStepGrimpex = resVirAtGr
            else:
                virAtTimeStep = list(np.average([virAtTimeStep, virAt], axis=0))
                # resVirAtAll = list(np.average([resVirAtAll, (np.add(resVirAtGu, resVirAtGr))], axis=0))
                resVirAtTimeStepGuttagonol = list(np.average([resVirAtTimeStepGuttagonol, resVirAtGu], axis=0))
                resVirAtTimeStepGrimpex = list(np.average([resVirAtTimeStepGrimpex, resVirAtGr], axis=0))
        pylab.figure()
        pylab.plot(virAtTimeStep, label='non-resistant')
        pylab.plot(resVirAtAll, label='resistantAll')
        pylab.plot(resVirAtTimeStepGuttagonol, label='resistantGu')
        pylab.plot(resVirAtTimeStepGrimpex, label='resistantGr')
        pylab.legend()
        pylab.xlabel('time')
        pylab.ylabel('virus count')
        pylab.title('treated patient, t=150+drug1+%d+drug2+150' % (delay))

    pylab.show()


runProblem7([300, 0])