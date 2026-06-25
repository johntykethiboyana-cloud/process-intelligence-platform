from comparison.normalizer import Normalizer

normalizer = Normalizer()

samples = [

    "Fill in the account details and submit by clicking on OK button.",

    "Once you receive the approved email kindly accept and complete the TRAX whitelisting SI task in FINDUR.",

    "Click on Treasury Lists under Reference Data.",

    "Validate the request before approval."

]

for sentence in samples:

    print("\nOriginal :")
    print(sentence)

    print("\nNormalized :")
    print(normalizer.normalize(sentence))

    print("-" * 70)