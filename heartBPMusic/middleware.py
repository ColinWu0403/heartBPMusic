from django.conf import settings


def SessionCookieSameSiteWorkaround(get_response):
    def middleware(request):
        # See:
        #   https://blog.chromium.org/2019/10/developers-get-ready-for-new.html
        #   https://github.com/django/django/pull/11894
        #   https://web.dev/samesite-cookie-recipes/#handling-incompatible-clients
        #   https://www.chromium.org/updates/same-site/incompatible-clients
        #
        # TLDR: Chrome (and soon Firefox and Safari) require that you set SameSite=None
        #       in order to have a cookie set cross-domain. The old behavior of SameSite
        #       being 'None' by default is no more. The new default is 'Lax'.
        #       The issue is that we can't just set SameSite=None and be done with it,
        #       because some older browsers will break with this. Therefore we devise
        #       a two-cookie approach: one that does the new behavior of setting
        #       SameSite=None, and the second is the "legacy" cookie which relies on
        #       the old-default's behavior. If we receive only the legacy cookie in
        #       a request, we know we're dealing with one of those older browsers,
        #       and we can repair the lost cookie before proceeding to process the
        #       request.
        cookie = settings.SESSION_COOKIE_NAME
        legacy = "{}_legacy".format(cookie)

        if legacy in request.COOKIES:
            if cookie not in request.COOKIES:
                request.COOKIES[cookie] = request.COOKIES[legacy]
            del request.COOKIES[legacy]

        response = get_response(request)

        if cookie in response.cookies:
            response.cookies[legacy] = response.cookies[cookie].value
            response.cookies[legacy].update(response.cookies[cookie])  # <-- set Expiry, Path, etc.
            response.cookies[cookie]['samesite'] = 'None'
            if settings.SESSION_COOKIE_SECURE and not response.cookies[cookie].get('secure', False):
                # Fix Django's silly `delete_cookie()` behavior which doesn't set `secure` correctly.
                response.cookies[cookie]['secure'] = True

        return response

    return middleware