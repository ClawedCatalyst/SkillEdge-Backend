from courses.models import *


def calculate_weighted_rating(course):
    specific_votes = course.review_count
    specific_avg_rating = course.rating
    all_courses = Course.objects.all()
    total_rating = 0.0
    for each_course in all_courses:
        total_rating += each_course.rating
    default_votes = 50
    cummulative_rating = total_rating / len(all_courses)
    for hosted_course in all_courses:
        votes = hosted_course.review_count
        avg_rating = hosted_course.rating
        live_weighted_rating = (
            (avg_rating * votes) + (cummulative_rating * default_votes)
        ) / (votes + default_votes)
        hosted_course.weighted_rating = live_weighted_rating
        hosted_course.save()
    specific_weighted_rating = (
        (specific_avg_rating * specific_votes) + (cummulative_rating * default_votes)
    ) / (specific_votes + default_votes)
    return specific_weighted_rating
