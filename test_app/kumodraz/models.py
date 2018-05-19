class Weather:

    def __init__(self, db):
        self.db = db

    def get_all(self):
        try:
            weathers = self.db.weather.find({})
            return weathers
        except:
            print('Error getting all weathers')

        return None

    def get_last_10(self):
        try:
            last_ten = self.db.weather.find().sort({"date": -1}).limit(10)

            if last_ten:
                return last_ten
        except:
            return None

        return None
