def get_coollist_map( n, *args ):
	return list(map(
		lambda i: "".join(
			map( lambda rule: rule[1] if i % rule[0] == rule[0] - 1 else "",
				args
			) ),
		range(n)
	))


def get_coollist_lc( n, *args ):
	return [
		"".join(
			[
				rule[1] if i % rule[0] == rule[0] - 1 else ""
				for rule in args
			]
		)
		for i in range(n)
	]

rules = [ ( 3, "fast" ), ( 5, "campus" ), ( 7, "school" ) ]

res0 = get_coollist_lc( 105, *rules )
res1 = get_coollist_map( 105, *rules )

print(res0)
print(res1)

# 설마 두번다 틀릴까.
print( res0 == res1 )
