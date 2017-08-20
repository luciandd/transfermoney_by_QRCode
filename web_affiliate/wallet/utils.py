from wallet.models import Wallet
from django.core.exceptions import ObjectDoesNotExist

def get_token_wallet(user):
    try:
        wallet = Wallet.objects.get(user=user)
        token_wallet = wallet.token_wallet
        # token_wallet = 'ef2d69fe-49c7-4b30-9a1e-d9b5ab0a6b41'
        return token_wallet
    except ObjectDoesNotExist:
        return
