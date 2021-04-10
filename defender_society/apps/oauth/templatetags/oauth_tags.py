from django import template

register = template.Library()


@register.inclusion_tag('oauth/tags/user_avatar.html')
def get_user_avatar_tag(user):
    '''Return the user's avatar, which is an img tag'''
    return {'user': user}


@register.simple_tag
def http_to_https(link):
    '''Replace the http link with https, the purpose is to change the avatar bed address of Weibo to HTTPS'''
    return link.replace('http://','https://')


@register.simple_tag
def get_user_link(user):
    '''
    Get the link of the authenticated user, and determine which authentication method the user is using (Github, Weibo, email)
    Refer to the usage of get_social_accounts(user)
    :param user: a USER object
    :return: Return the user's link and registration method and whether the email address has been verified. The priority of the link is user.link, followed by the github homepage.
            Considering that many people are unwilling to display the Weibo homepage, so do not display the Weibo homepage
    '''
    info = {
        'link': None,
        'provider': None,
        'is_verified': False
    }
    accounts = {}
    for account in user.socialaccount_set.all().iterator():
        providers = accounts.setdefault(account.provider, [])
        providers.append(account)
    if accounts:
        for key in ['github','weibo']:
            account_users = accounts.get(key)
            if account_users:
                account_user = account_users[0]
                the_link = account_user.get_profile_url()
                the_provider = account_user.get_provider().name
                if key =='github':
                    info['link'] = the_link
                if user.link:
                    info['link'] = user.link
                info['provider'] = the_provider
                info['is_verified'] = True
    else:
        the_link = user.link
        if the_link:
            info['link'] = the_link
        for emailaddress in user.emailaddress_set.all().iterator():
            if emailaddress.verified:
                info['is_verified'] = True
    return info