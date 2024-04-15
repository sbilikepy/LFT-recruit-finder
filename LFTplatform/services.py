CLASS_SPEC_VALID_COMBINATIONS = {
    "Death Knight": {"Blood", "Frost", "Unholy"},
    "Druid": {"Balance", "Feral dps", "Feral tank", "Restoration"},  # !
    "Hunter": {"Beast mastery", "Marksmanship", "Survival"},
    "Mage": {"Arcane", "Fire", "Frost"},  # !
    "Paladin": {"Holy", "Protection", "Retribution"},  # !
    "Priest": {"Discipline", "Holy", "Shadow"},  # !  # !
    "Rogue": {"Assassination", "Combat", "Subtlety"},
    "Shaman": {"Elemental", "Enhancement", "Restoration"},  # !
    "Warlock": {"Affliction", "Demonology", "Destruction"},
    "Warrior": {"Arms", "Fury", "Protection"},  # !
}

CLASS_CHOICES = [
    (class_name, class_name) for class_name in CLASS_SPEC_VALID_COMBINATIONS.keys()
]

SPEC_CHOICES = [
    (spec, spec)
    for class_name, specs in CLASS_SPEC_VALID_COMBINATIONS.items()
    for spec in sorted(specs)
]

print(CLASS_SPEC_VALID_COMBINATIONS, "\n\n\n", CLASS_CHOICES, "\n\n\n", SPEC_CHOICES)
