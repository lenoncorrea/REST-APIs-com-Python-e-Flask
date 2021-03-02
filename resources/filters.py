
class FiltersResource:
    def normalize_path_params(city=None, min_stars=0, 
                                max_stars=5, min_daily=0, 
                                max_daily=10000, limit=50,
                                ofsset=0, **kwargs):
        if city:
            return {'min_stars': min_stars,
                'max_stars': max_stars,
                'min_daily': min_daily,
                'max_daily': max_daily,
                'city': city,
                'limit': limit,
                'ofsset': ofsset }
        return {'min_stars': min_stars,
                'max_stars': max_stars,
                'min_daily': min_daily,
                'max_daily': max_daily,
                'limit': limit,
                'ofsset': ofsset}
    def consult_no_city():
        return "SELECT * FROM hotels WHERE (stars >= ? and stars <= ?) and (daily >= ? and daily <= ?) LIMIT ? OFFSET ?"
        # return "SELECT * FROM hotels WHERE (stars >= %s and stars <= %s) and (daily >= %s and daily <= %s) LIMIT %s OFFSET %s"

    def consult_with_city():
        return "SELECT * FROM hotels WHERE (stars >= ? and stars <= ?) and (daily >= ? and daily <= ?) and (city LIKE ?) LIMIT ? OFFSET ?"
        # return "SELECT * FROM hotels WHERE (stars >= %s and stars <= %s) and (daily >= %s and daily <= %s) and (city LIKE %s) LIMIT %s OFFSET %s"