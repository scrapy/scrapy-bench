from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints

class Home(Resource):
    isLeaf = True

    def render_GET(self, request):
        path = "/var/www/html/books.toscrape.com/"
        filepath = '/'.join(request.postpath)
        fname = path + filepath
        
        with open(fname) as f: 
            s = f.read()
        return s

resource = Home()
factory = Site(resource)
endpoint = endpoints.TCP4ServerEndpoint(reactor, 8880, interface='0.0.0.0')
endpoint.listen(factory)
reactor.run()
