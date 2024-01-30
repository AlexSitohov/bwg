from app.db.enums import CoursePair


async def get_course_pair(course_rate_pare: CoursePair | None = None):
    if isinstance(course_rate_pare, CoursePair):
        return course_rate_pare.value
    else:
        return None
