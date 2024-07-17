from home.models import CustomUser
def proposal_status(request):
    has_prop_wait = False
    if request.user.is_authenticated:
        user = request.user
        proposal = CustomUser.objects.filter(proposals_receive__status='waiting', id=user.id)
        if proposal:
            has_prop_wait = True
    
    return {'has_prop_wait': has_prop_wait}