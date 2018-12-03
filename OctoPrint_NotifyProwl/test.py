import prowlpy

apikey = 'a8f9ee86009aeb552fc916e373d402ba4b983dd8'
p = prowlpy.Prowl(apikey)
try:
    p.add('TestApp','Server Down',"The Web Box isn't responding to a ping", 1, None, "http://www.prowlapp.com/")
    print 'Success'
except Exception,msg:
    print msg


