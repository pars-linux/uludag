liaisons = {
	'alpha' : ['armin76',		'klausman',	],
	'amd64' : ['keytoaster',	'chainsaw',	],
	'hppa'  : ['jer',				],
	'ppc'   : ['josejx',		'ranger',	],
	'ppc64' : ['josejx',		'ranger',	],
	'sparc' : ['armin76',		'tcunha',       ],
	'x86'   : ['fauli', 		'maekke',	],
	'release': ['pva', ]
}

def get (arch):
	if arch in liaisons:
		return liaisons[arch]
	else:
		return None
