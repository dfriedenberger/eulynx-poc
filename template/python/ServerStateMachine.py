from statemachine.statemachine import StateMachine
from statemachine.state import State

class ServerStateMachine:

	state_accepted = State("Accepted")
	state_idle = State("Idle")
	state_init = State("Init")

	# Conditions/Guards
	def is_true(self):
		raise NotImplementedError("is_true not implemented yet")

	def is_new_connection(self):
		raise NotImplementedError("is_new_connection not implemented yet")

	def is_timeout(self):
		raise NotImplementedError("is_timeout not implemented yet")

	# Transitions
	def accept(self):
		raise NotImplementedError("accept not implemented yet")

	def handle_connection(self):
		raise NotImplementedError("handle_connection not implemented yet")

	def initialize(self):
		raise NotImplementedError("initialize not implemented yet")

	def timeout(self):
		raise NotImplementedError("timeout not implemented yet")

	def run(self):

		sm = StateMachine(self.state_init, [
			] , {
			self.state_idle	: [
				(self.is_true,self.accept,self.state_accepted),
			],
			self.state_accepted	: [
				(self.is_new_connection,self.handle_connection,self.state_idle),
				(self.is_timeout,self.timeout,self.state_idle),
			],
			self.state_init	: [
				(self.is_true,self.initialize,self.state_idle),
			],
		})

		while sm.nextState():
			pass
