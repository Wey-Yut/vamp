from random import randint


# noinspection PyStringFormat
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

        self.prerolled = False

        # Attributes of one random trow
        self.successes = None
        self.successes_crit = None
        self.fail = None
        self.crit_normal = None
        self.crit_hunger = None
        self.rolled_dices_normal = None
        self.rolled_dices_hunger = None
        self.status = None

        # Chances of this configuration overall
        self.chance_bestial_fail = None
        self.chance_fail = None
        self.chance_normal_success = None
        self.chance_bestial_crit = None
        self.chance_normal_crit = None

    # Used for rolls for one trow and probability
    def __roll_met(self) :

        successes = 0
        fail = 0
        crit_normal = 0
        crit_hunger = 0
        rolled_dices_normal = []
        rolled_dices_hunger = []

        # Only used in reroll (willpower use)
        if self.prerolled :
            rolled_dices_normal = self.rolled_dices_normal
            rolled_dices_hunger = self.rolled_dices_hunger

        # Used for everything else
        else :

            for d in range(self.normal_dice) :
                rolled = randint(1, 10)
                rolled_dices_normal += [rolled]

            for d in range(self.hunger_dice) :
                rolled = randint(1, 10)
                rolled_dices_hunger += [rolled]

        # For normal dice
        for rolled in rolled_dices_normal :
            if rolled == 10 :
                successes += 1
                crit_normal += 1
            elif rolled >= 6 :
                successes += 1

        # for hunger dice
        for rolled in rolled_dices_hunger :
            if rolled == 10 :
                successes += 1
                crit_hunger += 1
            elif rolled >= 6 :
                successes += 1
            elif rolled == 1 :
                fail = 1

        successes_crit = ((crit_hunger + crit_normal) // 2) * 2
        successes += successes_crit

        roll_info = {
                     'successes' : successes,
                     'successes_crit' : successes_crit,
                     'fail' : fail,
                     'crit_normal' : crit_normal,
                     'crit_hunger' : crit_hunger,
                     'rolled_dices_normal' : rolled_dices_normal,
                     'rolled_dices_hunger' : rolled_dices_hunger,
                     }

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

    def roll(self) :
        rolled = VamRoll.__roll_met(self)
        self.successes = rolled['successes']
        self.successes_crit = rolled['successes_crit']
        self.fail = rolled['fail']
        self.crit_normal = rolled['crit_normal']
        self.crit_hunger = rolled['crit_hunger']
        self.rolled_dices_normal = rolled['rolled_dices_normal']
        self.rolled_dices_hunger = rolled['rolled_dices_hunger']
        self.status = rolled['status']

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

    def willpower(self) :

        if self.dice_pool >= 3 :
            how_many_can_reroll = 3
        else :
            how_many_can_reroll = self.normal_dice

        print(self.rolled_dices_normal)
        which_reroll = input('Type results to reroll.\nSeparate by space. \n'
                             'You can choose %d dices or less\n' % how_many_can_reroll)

        which_reroll = which_reroll.split(' ')

        while len(which_reroll) > how_many_can_reroll:
            which_reroll = input('Type results to reroll.\nSeparate by space. \n'
                                 'YOU CAN CHOOSE %d DICES OR LESS\n' % how_many_can_reroll)
            which_reroll = which_reroll.split(' ')

        # Should work with aliasing, but I never know how it works, so I avoid it by all cost.
        new_dices_rolled = self.rolled_dices_normal[:]
        for dice in which_reroll :
            new_dices_rolled.remove(int(dice))
            new_dices_rolled.append(randint(1, 10))

        self.rolled_dices_normal = new_dices_rolled[:]

        self.prerolled = True

        VamRoll.roll(self)
        VamRoll.print_roll(self)

        self.prerolled = False

    def print_roll(self) :
        if self.status is None :
            VamRoll.roll(self)

        print("Dice pool:", self.dice_pool)
        print('Hunger:', self.hunger)
        print('Difficulty:', self.difficulty)
        print('Normal dice rolled:', self.rolled_dices_normal)
        print('hunger dice rolled: ', self.rolled_dices_hunger)
        print('Successes:', self.successes)

        if self.status == 'normal_crit_roll' :
            print('CRITICAL SUCCESS')

        elif self.status == 'bestial_crit_roll' :
            print('BESTIAL SUCCESS')

        elif self.status == 'success_roll' :
            print('SUCCESS')

        elif self.status == 'bestial_fail_roll' :
            print('BESTIAL FAILURE')

        elif self.status == 'fail_roll' :
            print('FAILED')

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

            control = input('To use willpower to reroll type: "W"\n'
                            'To roll again type "R\n'
                            'To end type "E"\n')

            if control == 'W' or control == 'w' :
                test_vampire.willpower()
                control = input('To roll again type "R\n'
                                'To end type "E"\n')
