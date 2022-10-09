from unicodedata import name

# TODO: add status field to Order

class Order:
    def __init__(self,id, name, temp, shelfLife, decayRate):
        self.id = id
        self.name = name
        self.temp = temp
        self.shelfLife = shelfLife
        self.decayRate = decayRate

    def __repr__(self):
        str = """Order: {id}
        name: {name}
        temp: {temp}
        shelfLife: {shelfLife}
        decayRate: {decayRate}""".format(
            id = self.id,
            name = self.name,
            temp = self.temp,
            shelfLife = self.shelfLife,
            decayRate = self.decayRate
            )

        return str

    @staticmethod
    def decodeFromJSON(json):
        # TODO: validate each fields and return appropriate error
        # TODO: refactor as custom validator method
        
        if not 'id' in json:
            raise InvalidOrderError("id should not be empty")
        id = json["id"]

        order = Order(
        id,
        json["name"],
        json["temp"],
        json["shelfLife"],
        json["decayRate"],
        )
        return order

class InvalidOrderError(Exception):
    pass
    