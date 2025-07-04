def user_quota(request):
    if request.user.is_authenticated:
        try:
            status = request.user.userstatus
            used = status.used_quota or 0
            total = status.total_quota or 0
            sisa = total - used
        except:
            used = total = sisa = 0
    else:
        used = total = sisa = 0
    return {
        'used_quota': used,
        'total_quota': total,
        'sisa_quota': sisa
    }
