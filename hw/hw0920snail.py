def print_snail( snail ):
	for row in snail:
		print( row )

def get_next_direction( d ):
	if d['x'] == 1:
		new_d = { 'x':0, 'y':1 }
	elif d['x'] == -1:
		new_d = { 'x':0, 'y':-1 }
	elif d['y'] == 1:
		new_d = { 'x':-1, 'y':0 }
	else:
		new_d = { 'x':1, 'y':0 }

	return new_d

def get_snail(n):

	snail = []
	for i in range(n):
		snail.append( [] )
		for j in range(n):
			snail[i].append( 0 )

	print_snail( snail )

	curpos = { 'x':0, 'y':0 }
	direction = { 'x':1, 'y':0 }
	nextpos = {}

	for i in range(n*n):
		snail[curpos['y']][curpos['x']] = i + 1
		
		nextpos['x'] = curpos['x'] + direction['x']
		nextpos['y'] = curpos['y'] + direction['y']

		if ( nextpos['x'] < 0 or nextpos['x'] >= n or
			nextpos['y'] < 0 or nextpos['y'] >= n or
			snail[nextpos['y']][nextpos['x']] != 0 ):
			direction = get_next_direction( direction )

		curpos['x'] += direction['x']
		curpos['y'] += direction['y']

	return snail

print_snail( get_snail(4) )

