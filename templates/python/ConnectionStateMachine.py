from statemachine.statemachine import StateMachine
from statemachine.state import State

class ConnectionStateMachine:

	state_closed = State("Closed")
	state_handleRecvData = State("HandleRecvData")
	state_idle = State("Idle")
	state_init = State("Init")

	# Conditions/Guards
	def is_error(self):
		raise NotImplementedError("is_error not implemented yet")

	def is_recv_data(self):
		raise NotImplementedError("is_recv_data not implemented yet")

	def is_true(self):
		raise NotImplementedError("is_true not implemented yet")

	def is_no_error_and_no_send_data(self):
		raise NotImplementedError("is_no_error_and_no_send_data not implemented yet")

	def is_send_data(self):
		raise NotImplementedError("is_send_data not implemented yet")

	def is_timeout(self):
		raise NotImplementedError("is_timeout not implemented yet")

	# Transitions
	def close(self):
		raise NotImplementedError("close not implemented yet")

	def handle_callback(self):
		raise NotImplementedError("handle_callback not implemented yet")

	def initialize(self):
		raise NotImplementedError("initialize not implemented yet")

	def recv(self):
		raise NotImplementedError("recv not implemented yet")

	def send(self):
		raise NotImplementedError("send not implemented yet")

	def timeout(self):
		raise NotImplementedError("timeout not implemented yet")

	def run(self):

		sm = StateMachine(self.state_init, [
				self.state_closed,
			] , {
			self.state_idle	: [
				(self.is_error,self.close,self.state_closed),
				(self.is_no_error_and_no_send_data,self.recv,self.state_handleRecvData),
				(self.is_send_data,self.send,self.state_idle),
			],
			self.state_handleRecvData	: [
				(self.is_recv_data,self.handle_callback,self.state_idle),
				(self.is_timeout,self.timeout,self.state_idle),
			],
			self.state_init	: [
				(self.is_true,self.initialize,self.state_idle),
			],
		})

		while sm.nextState():
			pass
