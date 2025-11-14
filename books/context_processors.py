"""
Context processors for adding global template variables
"""

def notifications_context(request):
    """
    Add unread notifications count to all templates
    """
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
        return {
            'unread_notifications_count': unread_count
        }
    return {
        'unread_notifications_count': 0
    }
