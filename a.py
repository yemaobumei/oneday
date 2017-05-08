def foo(n):
	s=[0]
	def bar(i):

		s[0]=s[0]+i
		return s[0]
	return bar

 def foo(n):
 	def bar(i):
 		n=n+i
 		return n+i
 	return bar
 function foo(){
 	return function(i){
 		n=n+i;
 		return n;
 	}
 }	
def inc(n):
	return lambda i:i+n

def make_adder(addend):
    def adder(augend):
        return augend + addend
    return adder

print r"""
\\\\\
'''''
"""
