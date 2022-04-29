from random import randint


class VamRoll :

    def __init__(self, dice_pool, hunger, difficulty) :

        self.dice_pool = dice_pool
        self.hunger = hunger
        self.difficulty = difficulty

        if hunger > dice_pool :
            self.hunger_dice = dice_pool
        else :
            self.hunger_dice = hunger

        self.normal_dice = dice_pool - self.hunger_dice

        self.chance_bestial_fail = None
        self.chance_fail = None
        self.chance_normal_success = None
        self.chance_bestial_crit = None
        self.chance_normal_crit = None

        self.rolled = None

        def __roll_met(self, prerolled=None) :

        successes = 0
        fail = 0
        crit_normal = 0
        crit_hunger = 0
        rolled_dices_normal = []
        rolled_dices_hunger = []

        if prerolled is None :
            for d in range(self.normal_dice) :
                rolled = randint(1, 10)
                rolled_dices_normal += [rolled]
        else :
            rolled_dices_normal = prerolled            

        for rolled in rolled_dices_normal :
            if rolled == 10 :
                successes += 1
                crit_normal += 1
            elif rolled >= 6 :
                successes += 1

        for d in range(self.hunger_dice) :
            rolled = randint(1, 10)
            rolled_dices_hunger += [rolled]
            if rolled == 10 :
                successes += 1
                crit_hunger += 1
            elif rolled >= 6 :
                successes += 1
            elif rolled == 1 :
                fail = 1

        successes_crit = ((crit_hunger + crit_normal) // 2) * 2
        successes += successes_crit

        roll_info = {'successes' : successes,
                     'successes_crit' : successes_crit,
                     'fail' : fail,
                     'crit_normal' : crit_normal,
                     'crit_hunger' : crit_hunger,
                     'rolled_dices_normal' : rolled_dices_normal,
                     'rolled_dices_hunger' : rolled_dices_hunger,
                     'status' : 0}

        # failure
        if successes < self.difficulty :

            if fail != 0 :
                roll_info['status'] = 'bestial_fail_roll'
            else :
                roll_info['status'] = 'fail_roll'

        # success
        else :
            # critic
            if successes_crit > 0 :
                if crit_hunger != 0 :
                    roll_info['status'] = 'bestial_crit_roll'
                else :
                    roll_info['status'] = 'normal_crit_roll'

            # non-critic
            else :
                roll_info['status'] = 'success_roll'

        return roll_info

    def roll(self, prerolled=None) :
        self.rolled = VamRoll.__roll_met(self, prerolled)

    def probability(self, reps=10000) :
        rolls = {'normal_crit_roll' : 0,
                 'bestial_crit_roll' : 0,
                 'success_roll' : 0,
                 'bestial_fail_roll' : 0,
                 'fail_roll' : 0}

        for r in range(reps) :
            roll = VamRoll.__roll_met(self)
            roll_status = roll['status']
            rolls[roll_status] += 1

        self.chance_normal_crit = rolls['normal_crit_roll'] * 100 / reps
        self.chance_bestial_crit = rolls['bestial_crit_roll'] * 100 / reps
        self.chance_normal_success = rolls['success_roll'] * 100 / reps
        self.chance_fail = rolls['fail_roll'] * 100 / reps
        self.chance_bestial_fail = rolls['bestial_fail_roll'] * 100 / reps

    def willpower(self):

        if self.dice_pool >= 3 :
            how_many_can_reroll = 3
        else :
            how_many_can_reroll = self.normal_dice[:]

        print(self.rolled['rolled_dices_normal'])
        which_reroll = input('Type results to reroll.\n Separate by space. \n'
                             'You can choose %d dices or less\n' % how_many_can_reroll)

        which_reroll = which_reroll.split(' ')        
        new_dices_rolled = self.rolled['rolled_dices_normal'][:]
        for dice in which_reroll :            
            dice = int(dice)
            new_dices_rolled.remove(dice)
            new_dices_rolled.append(randint(1, 10))

        VamRoll.roll(self, new_dices_rolled)
        VamRoll.print_roll(self)

    def print_roll(self) :
        if self.rolled is None :
            VamRoll.roll(self)

        print("Dice pool:", self.dice_pool)
        print('Hunger:', self.hunger)
        print('Difficulty:', self.difficulty)
        print('Normal dice rolled:', self.rolled['rolled_dices_normal'])
        print('hunger dice rolled: ', self.rolled['rolled_dices_hunger'])
        print('Successes:', self.rolled['successes'])

        if self.rolled['status'] == 'normal_crit_roll' :
            print('CRITICAL SUCCESS')

        elif self.rolled['status'] == 'bestial_crit_roll' :
            print('BESTIAL SUCCESS')

        elif self.rolled['status'] == 'success_roll' :
            print('Success')

        elif self.rolled['status'] == 'bestial_fail_roll' :
            print('BESTIAL FAILURE')

        elif self.rolled['status'] == 'fail_roll' :
            print('Fail')

    def print_probability(self) :
        if self.chance_fail is None :
            VamRoll.probability(self)

        print('Crit chance: % 2.2f %%' % self.chance_normal_crit)
        print('Bestial crit chance: % 2.2f %%' % self.chance_bestial_crit)
        print('Normal success chance: % 2.2f %%' % self.chance_normal_success)
        print('Total chance for success: % 2.2f %%' % (self.chance_normal_crit +
                                                       self.chance_bestial_crit +
                                                       self.chance_normal_success))
        print('')
        print('Normal fail chance: % 2.2f %%' % self.chance_fail)
        print('Bestial failure chance: % 2.2f %%' % self.chance_bestial_fail)
        print('Total chance for failure: % 2.2f %%' % (self.chance_fail +
                                                       self.chance_bestial_fail))


if __name__ == '__main__' :
    control = 'r'
    while control == 'R' or control == 'r' :
        dices = int(input('Dice pool?\n'))
        hunger_level = int(input('Hunger?\n'))
        difficulty_level = int(input('Difficulty?\n'))

        if dices < 1 :
            print("Sorry, you just don't have a chance")
            control = input('To roll type "R\n'
                            'To end type "E"\n')
        else :

            test_vampire = VamRoll(dices, hunger_level, difficulty_level)
            test_vampire.print_roll()
            print('')
            test_vampire.print_probability()

            control = input('To use willpower to reroll type: "W"\n '
                            'To roll again type "R\n'
                            'To end type "E"\n')
    
            if control == 'W' or control == 'w' :
                test_vampire.willpower()
                control = input('To roll again type "R\n'
                                'To end type "E"\n')
