
def deco_start( func ):
	print( "deco_start" )
	def wrapper( *args, **kwargs ):
		print( "==== start ====" )
		result = func( *args, **kwargs )
		return result
	
	return wrapper

def deco_end( func ):
	print( "deco_end" )
	def wrapper( *args, **kwargs ):
		result = func( *args, **kwargs )
		print( "====  end  ====" )
		return result
	
	return wrapper

@deco_start
@deco_end
def hello():
	print "Hello World!!!"

	hello()
