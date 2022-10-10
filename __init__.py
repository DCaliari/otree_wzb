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
	@staticmethod
	def after_all_players_arrive(group: Group):
		players = group.get_players()  # store the list of players in a local variables
		contributions = [p.contribution for p in players]  # list of contributions per player
		group.total = sum(contributions)
		payout = group.total * C.MULTIPLIER
		for p in players:
			p.payoff = C.BUDGET - p.contribution + payout  # the payoff variable is pre-defined
		

class Feedback(Page):
	@staticmethod
	def vars_for_template(player: Player):
		others = player.get_others_in_group()
		others_contributions = [o.contribution for o in others]
		others_payoffs = [o.payoff for o in others]
		return dict(
			others=others,
			others_contributions=others_contributions,
			others_payoffs=others_payoffs
		)
		
		
class FinalFeedback(Page):
	@staticmethod
	def is_displayed(player: Player):
		return player.round_number == C.NUM_ROUNDS


page_sequence = [Choice, ChoiceWaitPage, Feedback, FinalFeedback]


# FUNCTIONS

def creating_session(subsession: Subsession):
	subsession.group_randomly()
