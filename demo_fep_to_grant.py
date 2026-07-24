from bleak_core.lough import LoughFieldOperator
from bleak_core.dataweaver import DataWeaver
from bleak_core.whorl import WhorlCoordinator

# 1. Initialize Runtime
field = LoughFieldOperator()
weaver = DataWeaver()
coordinator = WhorlCoordinator()

# 2. Simulate Signal (e.g., FEP detecting an opportunity)
field_state = field.propagate((50, 50), 0.8)
signal = weaver.weave(field_state, external_signal=10.5)

# 3. Coordinate Response
response = coordinator.coordinate(signal['woven_signal'])

print(f"FEP->Grant Pipeline Response: {response}")
