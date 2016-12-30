#coding=utf-8

from scrapy.downloadermiddlewares.redirect import BaseRedirectMiddleware

class RedirectMiddleware(BaseRedirectMiddleware):
    """Handle redirection of requests based on response status and meta-refresh html tag"""

    def process_response(self, request, response, spider):
        if request.meta.get('dont_redirect', False):
            return response

        if request.method == 'HEAD':
            if response.status in [301, 302, 303, 307] and 'Location' in response.headers:
                redirected_url = urljoin(request.url, response.headers['location'])
                redirected = request.replace(url=redirected_url)
                return self._redirect(redirected, request, spider, response.status)
            else:
                return response

        if response.status in [302, 303] and 'Location' in response.headers:
            redirected_url = urljoin(request.url, response.headers['location'])
            redirected = self._redirect_request_using_get(request, redirected_url)

            print "find a %d status url %s"%(redirect.status ,request.url)

            return self._redirect(redirected, request, spider, response.status)

        if response.status in [301, 307] and 'Location' in response.headers:
            redirected_url = urljoin(request.url, response.headers['location'])
            redirected = request.replace(url=redirected_url)
            return self._redirect(redirected, request, spider, response.status)

        return response

