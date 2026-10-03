import random

possibleEvents = ['Power Failure', 'Water Contamination', 'Communication Loss', 'Transportation Emergency', 'Resource Overconsumption']

affectedResources = {
    'Power Failure': {
        'Energy': 0,
        'Water': 0,
        'Food': 0,
        'Communication': 0,

        'Text': {
            0: 'The city power grid is failing.',
            1: 'Several districts have lost electricity.',
            2: 'The emergency generators are under heavy load.',
            3: 'A major power station has gone offline.',
            4: 'Energy supply is dropping across the city.'
        }
    },

    'Water Contamination': {
        'Energy': 0,
        'Water': 0,
        'Food': 0,
        'Communication': 0,

        'Text': {
            0: 'The city water supply may be contaminated.',
            1: 'Dangerous substances have been detected in the water.',
            2: 'The main water network is no longer safe.',
            3: 'Contamination is spreading through the water system.',
            4: 'Several districts are reporting unsafe water.'
        }
    },
    
    'Communication Loss': {
        'Energy': 0,
        'Water': 0,
        'Food': 0,
        'Communication': 0,

        'Text': {
            0: 'The city communication network is going offline.',
            1: 'Several communication towers have stopped working.',
            2: 'Emergency channels are becoming unstable.',
            3: 'Contact with multiple districts has been lost.',
            4: 'The main communication system is failing.'
        }
    },

    'Transportation Emergency': {
        'Energy': 0,
        'Water': 0,
        'Food': 0,
        'Communication': 0,

        'Text': {
            0: 'Major transportation routes are becoming inaccessible.',
            1: 'Several emergency vehicles are unable to move.',
            2: 'A critical transport route has been blocked.',
            3: 'The city transport network is experiencing major disruptions.',
            4: 'Supply vehicles are being delayed across the city.'
        }
    },

    'Resource Overconsumption': {
        'Energy': 0,
        'Water': 0,
        'Food': 0,
        'Communication': 0,

        'Text': {
            0: 'The city is consuming resources too quickly.',
            1: 'Critical supplies are being depleted at an alarming rate.',
            2: 'Resource demand has exceeded safe levels.',
            3: 'The current consumption rate cannot be maintained.',
            4: 'Essential resources are running out faster than expected.'
        }
    }
}

possibleActions = {
    'Power Failure': {
        0: {
            'Text': 'Activate backup generators',

            'Energy': 8,
            'Water': -6,
            'Food': -2,
            'Communication': 0,

            'Score': 80
        },

        1: {
            'Text': 'Reduce non-essential energy consumption',

            'Energy': 6,
            'Water': 2,
            'Food': 0,
            'Communication': -5,

            'Score': 70
        },

        2: {
            'Text': 'Redirect power to critical areas',

            'Energy': 4,
            'Water': -1,
            'Food': 0,
            'Communication': -2,

            'Score': 50
        },
        3: {
            'Text': 'Shut down overloaded sectors',

            'Energy': 3,
            'Water': 0,
            'Food': 0,
            'Communication': 0,

            'Score': 50
        },
        4: {
            'Text': 'Request external energy support',

            'Energy': 8,
            'Water': -2,
            'Food': -2,
            'Communication': -3,

            'Score': 30
        }
    },

    'Water Contamination': {
        0: {
            'Text': 'Shut down the contaminated supply',

            'Energy': 2,
            'Water': 6,
            'Food': -2,
            'Communication': 0,

            'Score': 80
        },

        1: {
            'Text': 'Activate emergency purification systems',

            'Energy': -3,
            'Water': 10,
            'Food': 5,
            'Communication': 0,

            'Score': 100
        },

        2: {
            'Text': 'Distribute stored clean water',

            'Energy': -5,
            'Water': 7,
            'Food': 0,
            'Communication': 0,

            'Score': 50
        },

        3: {
            'Text': 'Isolate affected districts',

            'Energy': 0,
            'Water': 8,
            'Food': -2,
            'Communication': -4,

            'Score': 60
        },

        4: {
            'Text': 'Request external water supplies',

            'Energy': -1,
            'Water': 6,
            'Food': 0,
            'Communication': -2,

            'Score': 40
        }
    },
    
    'Communication Loss': {
        0: {
            'Text': 'Switch to backup communication channels',

            'Energy': -3,
            'Water': 0,
            'Food': 0,
            'Communication': 10,

            'Score': 100
        },

        1: {
            'Text': 'Restart the central communication system',

            'Energy': -4,
            'Water': -1,
            'Food': -1,
            'Communication': 15,

            'Score': 70
        },

        2: {
            'Text': 'Deploy emergency radio units',

            'Energy': -5,
            'Water': 0,
            'Food': 0,
            'Communication': 12,

            'Score': 100
        },

        3: {
            'Text': 'Prioritize critical communication traffic',

            'Energy': 0,
            'Water': 0,
            'Food': -4,
            'Communication': 6,

            'Score': 70
        },

        4: {
            'Text': 'Repair damaged communication towers',

            'Energy': -5,
            'Water': -3,
            'Food': -2,
            'Communication': 18,

            'Score': 100
        }
    },

    'Transportation Emergency': {
        0: {
            'Text': 'Redirect traffic through alternate outes',

            'Energy': -2,
            'Water': 0,
            'Food': 0,
            'Communication': -2,

            'Score': 10
        },

        1: {
            'Text': 'Deploy emergency transport units',

            'Energy': -2,
            'Water': 0,
            'Food': 0,
            'Communication': -2,

            'Score': 10
        },

        2: {
            'Text': 'Close unsafe roads',

            'Energy': -2,
            'Water': 0,
            'Food': 0,
            'Communication': -8,

            'Score': 20
        },
        3: {
            'Text': 'Prioritize supply and rescue vehicles',

            'Energy': -1,
            'Water': -2,
            'Food': -3,
            'Communication': 12,

            'Score': 100
        },
        4: {
            'Text': 'Request additional transport support',

            'Energy': 0,
            'Water': -4,
            'Food': -6,
            'Communication': -8,

            'Score': 50
        }
    },

    'Resource Overconsumption': {
        0: {
            'Text': 'Apply emergency rationing',

            'Energy': -7,
            'Water': 6,
            'Food': 6,
            'Communication': 0,

            'Score': 50
        },

        1: {
            'Text': 'Reduce non-essential consumption',

            'Energy': 3,
            'Water': 2,
            'Food': 2,
            'Communication': -4,

            'Score': 10
        },

        2: {
            'Text': 'Redistribute available resources',

            'Energy': -3,
            'Water': 4,
            'Food': 4,
            'Communication': 0,

            'Score': 50
        },

        3: {
            'Text': 'Limit access to critical supplies',

            'Energy': 2,
            'Water': 7,
            'Food': 9,
            'Communication': -10,

            'Score': 90
        },

        4: {
            'Text': 'Request additional resource deliveries',

            'Energy': -2,
            'Water': 7,
            'Food': 9,
            'Communication': -3,

            'Score': 100
        }
    }
}

def newEvent():
    global event
    global eventText
    
    event = random.randint(0, 4)
    eventText = random.randint(0, 4)

    x = affectedResources[possibleEvents[event]]

    if event == 0:
        x['Energy'] = random.randint(4, 18)
        x['Water'] = random.randint(1, 8)
        x['Food'] = random.randint(1, 3)
        x['Communication'] = random.randint(1, 13)

    elif event == 1:
        x['Energy'] = random.randint(1, 9)
        x['Water'] = random.randint(1, 3)
        x['Food'] = random.randint(3, 10)
        x['Communication'] = random.randint(3, 19)

    elif event == 2:
        x['Energy'] = random.randint(1, 3)
        x['Water'] = random.randint(2, 15)
        x['Food'] = random.randint(2, 21)
        x['Communication'] = random.randint(1, 10)

    elif event == 3:
        x['Energy'] = random.randint(1, 3)
        x['Water'] = random.randint(2, 15)
        x['Food'] = random.randint(2, 21)
        x['Communication'] = random.randint(1, 10)

    elif event == 4:
        x['Energy'] = random.randint(1, 18)
        x['Water'] = random.randint(4, 20)
        x['Food'] = random.randint(5, 21)
        x['Communication'] = random.randint(1, 4)