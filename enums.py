TURNOUT_THROWN = 'TURNOUT_THROWN'
TURNOUT_CLOSED = 'TURNOUT_CLOSED'
TURNOUT_UNKNOWN = 'TURNOUT_UNKNOWN'

SENSOR_ACTIVE = 'SENSOR_ACTIVE'
SENSOR_INACTIVE = 'SENSOR_INACTIVE'
SENSOR_UNKNOWN = 'SENSOR_UNKNOWN'

SIGNAL_CLEAR = 'SIGNAL_CLEAR'
SIGNAL_ADVANCE_APPROACH = 'SIGNAL_ADVANCE_APPROACH'
SIGNAL_APPROACH = 'SIGNAL_APPROACH'
SIGNAL_APPROACH_CLEAR_SIXTY = 'SIGNAL_APPROACH_CLEAR_SIXTY'
SIGNAL_APPROACH_CLEAR_FIFTY = 'SIGNAL_APPROACH_CLEAR_FIFTY'
SIGNAL_APPROACH_DIVERGING = 'SIGNAL_APPROACH_DIVERGING'
SIGNAL_APPROACH_RESTRICTING = 'SIGNAL_APPROACH_RESTRICTING'
SIGNAL_RESTRICTING = 'SIGNAL_RESTRICTING'

SIGNAL_DIVERGING_CLEAR = 'SIGNAL_DIVERGING_CLEAR'
SIGNAL_DIVERGING_CLEAR_LIMITED = 'SIGNAL_DIVERGING_CLEAR_LIMITED'
SIGNAL_DIVERGING_ADVANCE_APPROACH = 'SIGNAL_DIVERGING_ADVANCE_APPROACH'
SIGNAL_DIVERGING_APPROACH = 'SIGNAL_DIVERGING_APPROACH'
SIGNAL_DIVERGING_RESTRICTING = 'SIGNAL_DIVERGING_RESTRICTING'

SIGNAL_STOP = 'SIGNAL_STOP'
SIGNAL_DARK = 'SIGNAL_DARK'

HEAD_GREEN = 'HEAD_GREEN'
HEAD_FLASHING_GREEN = 'HEAD_FLASHING_GREEN'
HEAD_YELLOW = 'HEAD_YELLOW'
HEAD_FLASHING_YELLOW = 'HEAD_FLASHING_YELLOW'
HEAD_RED = 'HEAD_RED'
HEAD_FLASHING_RED = 'HEAD_FLASHING_RED'
HEAD_DARK = 'HEAD_DARK'

SVL_DISPATCH_SIGNAL_CONTROL_MEMORY_VAR_NAME = 'IMSVL_DISPATCH_SIGNALING'

def ConvertAspectToDivergingAspect(aspect):
	if aspect.startswith('SIGNAL_APPROACH_CLEAR_'):
		return SIGNAL_DIVERGING_CLEAR_LIMITED
	elif aspect.startswith('SIGNAL_APPROACH_'):
		return SIGNAL_DIVERGING_APPROACH

	return {
		SIGNAL_CLEAR: SIGNAL_DIVERGING_CLEAR,
		SIGNAL_ADVANCE_APPROACH: SIGNAL_DIVERGING_ADVANCE_APPROACH,
		SIGNAL_APPROACH: SIGNAL_DIVERGING_APPROACH,
		SIGNAL_RESTRICTING: SIGNAL_DIVERGING_RESTRICTING,
	}.get(aspect, SIGNAL_STOP)