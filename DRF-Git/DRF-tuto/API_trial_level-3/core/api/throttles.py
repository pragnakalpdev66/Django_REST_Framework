from rest_framework.throttling import UserRateThrottle

class BookCreateThrottle(UserRateThrottle):
    rate = '5/day'