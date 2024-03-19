# to fill json data
data = ["blood",
        "frost",
        "unholly",
        "balance",
        "feral_dps",
        "feral_tank",
        "restoration",
        "beast_mastery",
        "marksmanship",
        "survival",
        "arcane",
        "fire",
        "frost",
        "holy",
        "protection",
        "retribution",
        "discipline",
        "holy",
        "shadow",
        "assassination",
        "combat",
        "subtlety",
        "elemental",
        "enhancement",
        "restoration",
        "affliction",
        "demonology",
        "destruction",
        "arms",
        "fury",
        "protection"
        ]
processed = []

print("SPEC_CHOICES = [")
for i in data:
    if i not in processed:
        print(  # I'M SORRY FOR THIS
            "(" +
            '"'
            + i
            + '"'
            + ","
            + " "
            + '"'
            + i.capitalize().replace(
                '_',
                ' '
            ) +
            '"'
            + "),")
    processed.append(i)

print("]")
