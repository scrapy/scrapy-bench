import random
import re

from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints

class Home(Resource):
    isLeaf = True

    def _delayedRender(self, request):

        path = "/var/www/html/books.toscrape.com/"
        filepath = '/'.join(request.postpath)
        fname = path + filepath

        with open(fname) as f:
            s = f.read()
            request.write(s)
            request.finish()

    def _responseFailed(self, err, call):
        call.cancel()

    def render_GET(self, request):

        domain_name = re.search(
            'domain(.*):8880',
            request.prePathURL()).group(1)

        random.seed(domain_name)
        mu = max(0.1, random.gauss(0.2, sigma=4))
        random.seed()
        delay = max(0, random.gauss(mu, sigma=mu / 2))

        call = reactor.callLater(delay, self._delayedRender, request)
        request.notifyFinish().addErrback(self._responseFailed, call)

        return NOT_DONE_YET


resource = Home()
factory = Site(resource)
endpoint = endpoints.TCP4ServerEndpoint(reactor, 8880, interface='0.0.0.0')
endpoint.listen(factory)
reactor.run()
