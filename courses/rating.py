from courses.models import *

def calculate_weighted_rating(course):
    votes = course.review_count
    avg_rating = course.rating
    all_courses = Course.objects.all()
    total_rating = 0.0
    for each_course in courses:
        total_rating += each_course.rating
    default_votes = 20
    cummulative_rating = total_rating/len(all_courses)
    weighted_rating = ((avg_rating*votes)+(cummulative_rating*default_votes))/(votes + default_votes)
    return weighted_rating