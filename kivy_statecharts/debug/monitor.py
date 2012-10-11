# ================================================================================
# Project:   Kivy.Statechart - A Statechart Framework for Kivy
# Copyright: (c) 2010, 2011 Michael Cohen, and contributors.
# Python Port: Jeff Pittman, ported from SproutCore, SC.Statechart
# ================================================================================

import collections
from kivy.event import EventDispatcher
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy_statecharts.debug.sequence_matcher import StatechartSequenceMatcher

class StatechartMonitor(EventDispatcher):
    statechart = ObjectProperty(None)
    length = NumericProperty(0)
    sequence = ListProperty([])

    def __init__(self, statechart, **kwargs):
        self.statechart = statechart
        self.bind(sequence=self._length)
        self.reset();
        super(StatechartMonitor, self).__init__(**kwargs)
  
    def reset(self):
        #self.propertyWillChange('length') #[PORT]
        self.sequence = []
        #self.propertyDidChange('length') #[PORT]
        self._length() # [PORT] length has changed
  
    def _length(self, *l):
        self.length = len(self.sequence)
  
    def append_entered_state(self, state):
        #self.propertyWillChange('length') #[PORT]
        self.sequence.append({ 'action': 'entered', 'state': state })
        #self.propertyDidChange('length') #[PORT]
        self._length() # [PORT] length has changed
  
    def append_exited_state(self, state):
        #self.propertyWillChange('length') #[PORT]
        self.sequence.append({ 'action': 'exited', 'state': state })
        #self.propertyDidChange('length') #[PORT]
        self._length() # [PORT] length has changed
  
    def match_sequence(self):
        return StatechartSequenceMatcher(self) # [PORT] call was ({ statechart_monitor: self }), but __init__ on SSM was changed to take monitor
  
    # [PORT] Check how arguments is used in the call. 
    # [PORT] arguments, in javascript. so *arguments was added here
    def match_entered_states(self, *expected):
        #if isinstance(arguments, collections.Sequence):
            #expected = arguments
        #else:
            #expected = [arguments]
        actual = self.statechart.entered_states()
        matched = 0
    
        if len(expected) != len(actual):
            return False
    
        for item in expected:
            if isinstance(item, basestring):
                item = self.statechart.get_state(item)
            if item is None:
                return False
            if self.statechart.state_is_entered(item) and item.is_entered_state():
                matched += 1
    
        return matched == len(actual)
  
    def toString(self):
        seq = ""
        i = 0
        item = null
    
        seq += "["

        for i in range(len(self.sequence)):
            item = self.sequence[i]
            seq += "{0} {1}".format(item.action, item.state.full_path)
            if i < len(self.sequence)-1:
                seq += ", "

        seq += "]"

        return seq;
