from accounts.models import Account


def check_role(request):
    if request.user.is_authenticated:
        account = Account.objects.get(id=request.user.id)
        return {'methodist': account.methodist,
                'moderator': account.moderator}
    else:
        return {}