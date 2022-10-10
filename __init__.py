from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
	NAME_IN_URL = 'pgg'
	PLAYERS_PER_GROUP = 3
	NUM_ROUNDS = 2
	BUDGET = cu(10)  # short for currency, otree-function
	MULTIPLIER = 0.4


class Subsession(BaseSubsession):
	pass


class Group(BaseGroup):
	total = models.CurrencyField()


class Player(BasePlayer):
	contribution = models.CurrencyField(
		label='How much to you want to put into the group account?',
		min=0,
		max=C.BUDGET,
	)


# PAGES
class Choice(Page):
	form_model = 'player'
	form_fields = ['contribution']


class ChoiceWaitPage(WaitPage):  # wait pages html is automatically generated
	pass


class Feedback(Page):
	pass


class FinalFeedback(Page):
	pass


page_sequence = [Choice, ChoiceWaitPage, Feedback, FinalFeedback]
