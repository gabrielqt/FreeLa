from home.models import CustomUser
def proposal_status(request):
    if request.user.is_authenticated:
        has_prop_wait = False
        proposal = CustomUser.objects.filter(proposals_receive__status='waiting')
        if proposal:
            has_prop_wait = True
    
    return {'has_prop_wait': has_prop_wait}