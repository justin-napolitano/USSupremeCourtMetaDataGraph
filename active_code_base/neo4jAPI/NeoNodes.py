from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, BooleanProperty, EmailProperty, Relationship)

class City(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    state = Relationship('State', 'OF')
    country = Relationship('Country', 'OF')
    
    
class Country(StructuredNode):
    uid = UniqueIdProperty()
    code = StringProperty(unique_index=True, required=True)
    name = StringProperty(unique_index=True, required=True)
    state = Relationship('State', 'OF')

class State(StructuredNode):
    uid = UniqueIdProperty()
    code = StringProperty(unique_index=True, required=True)
    name = StringProperty(unique_index=True, required=True)
    


class URL(StructuredNode):
    uid = UniqueIdProperty()
    url = StringProperty(unique_index=True, required=True)
    searched = BooleanProperty(unique_index = True, required = True)
    state = Relationship('State', 'OF')
    city = Relationship('City', 'OF')

class Person(StructuredNode):
    uid = UniqueIdProperty()
    full_name = StringProperty(required = True)
    email = EmailProperty()