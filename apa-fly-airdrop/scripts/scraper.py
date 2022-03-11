import json, math
from brownie import interface

# IAPA = interface.IAPA("0x880fe52c6bc4ffffb92d6c03858c97807a900691")

# # Get TokenID -> ImageID
# lot = []
# for i in range(int(10_000 / 1000)):
#     lot.extend(IAPA.getImageIDs(i*1000, 1000))

# with open("imageids.json", "w") as f:
#     f.write(json.dumps(lot))
# assert(len(set(lot)) == 10_000)


def handle(metadata: dict):
    data = {}
    categories = {}
    for element in metadata:
        category = ""
        for j in element["attributes"]:
            if j["trait_type"] == "rarity":
                category = j["value"]

                if category not in categories:
                    categories[category] = 1
                else:
                    categories[category] += 1

        assert len(category) > 0
        data[element["token_id"]] = category

    print(f"Categories: {categories}")
    return data


def getNumberedCategory(category: str) -> int:
    if category == "Common":
        return 0
    elif category == "Rare":
        return 1
    elif category == "Exceptional":
        return 2
    elif category == "Epic":
        return 3
    elif category == "Legendary":
        return 4
    else:
        assert False


def getAllocationFromCategory(category: int) -> int:
    if category == 0:  # common
        return 50
    elif category == 1:  # rare
        return 84
    elif category == 2:  # exceptional
        return 166
    elif category == 3:  # epic
        return 416
    elif category == 4:  # legendary
        return 2500
    else:
        return 0


def main():
    tokens = []
    with open("scripts/data/imageids.json", "r") as f:
        tokens = json.load(f)

    metadata = {}
    with open("scripts/data/metadata.json", "r") as f:
        metadata = json.load(f)

    print(f"ImageIDS: {len(tokens)}")
    print(f"metadata: {len(metadata)}")

    assert len(tokens) < len(metadata)
    assert len(tokens) == 10_000

    categoryData = handle(metadata)
    assert len(categoryData) == len(metadata)

    bitArray = [0] * math.ceil(10_000 / 85)
    totalAmount = 0
    for index, token in enumerate(tokens):

        arrIndex = math.floor(index / 85)
        bitIndex = index % 85

        category = getNumberedCategory(categoryData[token])
        totalAmount += getAllocationFromCategory(category)

        bitArray[arrIndex] |= category << (bitIndex * 3)

    # First happens to be rare
    assert bitArray[0] & 0b111 == 1

    # Verify expected amount
    total = 20 * 2500 + 480 * 416 + 1500 * 166 + 3000 * 84 + 5000 * 50
    assert total == totalAmount

    # Verify integrity of the bits
    totalAmount = 0
    for tokenId in range(6500 + 1000 * 3 + 400):
        arrIndex = math.floor(tokenId / 85)
        bitIndex = tokenId % 85

        totalAmount += getAllocationFromCategory(
            (bitArray[arrIndex] >> bitIndex * 3) & 0b111
        )

    # assert(total == totalAmount)
    print(totalAmount)
    # print(bitArray)
