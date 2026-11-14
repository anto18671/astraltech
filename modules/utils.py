import os

# Config
RESEARCH_TAB_DEF_NAME = "AST_Astraltech"
RESEARCH_DEF_NAME = "AST_AstraltechBionics"
RESEARCH_BASE_COST = 5000
CRAFTING_SKILL_REQUIRED = 10
BIONIC_WORK_TO_MAKE = 60000
ADDON_WORK_TO_MAKE = 40000
COMPONENT_COST_PERCENT = 70     # % of an item's target value paid in advanced components; plasteel covers the rest
COMPONENT_SPACER_VALUE = 200    # vanilla market value of one advanced component
PLASTEEL_VALUE = 9              # vanilla market value of one plasteel
COMPONENT_STEP = 5              # component counts are rounded to multiples of this
PLASTEEL_STEP = 10              # plasteel counts are rounded to multiples of this

# Define a preface that explains the Astraltech's superiority
ASTRALTECH_LORE = "Astraltech is a monumental leap in bionic technology, surpassing even the mysterious Archotech devices. Secretly developed by an advanced faction beyond known stars for the elite, these implants possess seemingly supernatural abilities that push physical limits. Their full capabilities are unknown, but their power is undeniable."

# Valid body parts for bionics and addons targeted
BODY_PARTS = [
    'Torso', 'Neck', 'Skull', 'Brain', 'Eye', 'Ear', 'Nose', 'Jaw',
    'Spine', 'Ribcage', 'Stomach', 'Heart', 'Lung', 'Kidney',
    'Liver', 'Shoulder', 'Pelvis', 'Leg'
]

# Valid stats for bionics and addons targeted
VALID_STATS = [
    'WorkSpeedGlobal', 'ShootingAccuracyPawn', 'MeleeHitChance', 'MoveSpeed', 'AimingDelayFactor',
    'PainShockThreshold', 'GlobalLearningFactor', 'MedicalTendSpeed',
    'MedicalTendQuality', 'MedicalSurgerySuccessChance', 'ResearchSpeed', 'SocialImpact',
    'NegotiationAbility', 'TradePriceImprovement', 'ConstructionSpeed', 'MiningYield',
    'PlantWorkSpeed', 'ButcheryFleshSpeed', 'ButcheryFleshEfficiency', 'ButcheryMechanoidSpeed',
    'ButcheryMechanoidEfficiency', 'CookSpeed', 'EatSpeed', 'ImmunityGainSpeed',
    'TameAnimalChance', 'TrainAnimalChance', 'PawnBeauty', 'RestRateMultiplier', 'HungerRate',
    'PsychicSensitivity', 'PsychicEntropyRecoveryRate', 'MeditationFocusGain', 'SocialImpact',
    'AnimalGatherYield', 'AnimalProductYield', 'ConstructionSpeed',
    'ConstructSuccessChance', 'SurgerySuccessChanceFactor', 'HealingSpeed', 'FoodPoisonChance',
    'CarryWeight', 'ShootingAccuracyPawn', 'CaravanRidingSpeed', 'BedRestEffectiveness',
    'Beauty', 'PainFactor', 'MentalBreakThreshold', 'EatingSpeed', 'Talking', 'NegotiationAbility',
    'TradePriceImprovement', 'MeleeDodgeChance', 'RestFallFactor',
    'FoodPoisonChance', 'MeleeDPS', 'MeleeDodgeChance', 'ArrestSuccessChance',
    'ArmorRating_Sharp', 'ArmorRating_Blunt', 'MedicalOperationSpeed', 'MaxNutrition'
]

# Valid capacities for bionics and addons targeted
VALID_CAPACITIES = [
    'Consciousness', 'Sight', 'Hearing', 'Moving', 'Manipulation', 'Talking', 'Eating', 'Breathing',
    'BloodPumping', 'BloodFiltration', 'Metabolism', 'Immunity'
]

def round_div(numerator, denominator):
    """Integer division rounded half up (10.5 -> 11), with no floats or banker's rounding involved."""
    return (2 * numerator + denominator) // (2 * denominator)

def round_to_step(numerator, denominator, step):
    """numerator / denominator rounded half up to the nearest multiple of step."""
    return round_div(numerator, denominator * step) * step

def crafting_cost(target_value):
    """Ingredients whose vanilla market value adds up to target_value.

    The ThingDefs set no MarketValue, so the game derives it from these ingredients
    (plus work); crafting an item and selling it can't turn a profit.
    All integer math, so a given target_value always maps to the same cost.
    Components are rounded first; plasteel then covers the remaining value.
    """
    if not isinstance(target_value, int):
        raise TypeError(f"target_value must be an int, got {target_value!r}")
    components = max(COMPONENT_STEP, round_to_step(target_value * COMPONENT_COST_PERCENT,
                                                   100 * COMPONENT_SPACER_VALUE, COMPONENT_STEP))
    remainder = target_value - components * COMPONENT_SPACER_VALUE
    if remainder < 0:
        raise ValueError(f"target_value {target_value} is below the value of {components} advanced components")
    plasteel = max(PLASTEEL_STEP, round_to_step(remainder, PLASTEEL_VALUE, PLASTEEL_STEP))
    return {"Plasteel": plasteel, "ComponentSpacer": components}

def write_xml_file(filename, content):
    relative_path = f"Astraltech/{filename}"
    os.makedirs(os.path.dirname(relative_path), exist_ok=True)
    with open(relative_path, "w", encoding='utf-8') as file:
        file.write(content)
    print(f"{relative_path} generated successfully.")

def write_published_file_id(published_file_id, mod_directory='Astraltech'):
    # Ensure the About folder exists
    about_folder = os.path.join(mod_directory, "About")
    if not os.path.exists(about_folder):
        os.makedirs(about_folder)

    # Define the path for PublishedFileId.txt
    file_path = os.path.join(about_folder, "PublishedFileId.txt")

    # Write the PublishedFileId.txt content
    with open(file_path, 'w') as file:
        file.write(f"{published_file_id}")

    print(f"PublishedFileId.txt created at: {file_path}")


def generate_about_xml():
    return (
        """<?xml version="1.0" encoding="utf-8"?>\n"""
        "<ModMetaData>\n"
        "\t<name>Astraltech Bionic Implants</name>\n"
        "\t<author>Anthony Therrien</author>\n"
        "\t<url></url>\n"
        "\t<description>Astraltech Bionic Implants introduces a new tier of advanced bionics to RimWorld...</description>\n"
        "\t<packageId>AnthonyTherrien.AstraltechBionics</packageId>\n"
        "\t<supportedVersions>\n"
        "\t\t<li>1.5</li>\n"
        "\t\t<li>1.6</li>\n"
        "\t\t<li>1.7</li>\n"
        "\t</supportedVersions>\n"
        "</ModMetaData>"
    )


def generate_research_xml():
    # Own tab: the Main tab next to Bionics is already filled by Royalty and Biotech projects
    return (
        """<?xml version="1.0" encoding="utf-8"?>\n"""
        "<Defs>\n"
        "  <ResearchTabDef>\n"
        f"    <defName>{RESEARCH_TAB_DEF_NAME}</defName>\n"
        "    <label>Astraltech</label>\n"
        "    <generalTitle>Astraltech research projects</generalTitle>\n"
        "    <generalDescription>Reverse-engineer the implants of a faction from beyond the known stars.</generalDescription>\n"
        "  </ResearchTabDef>\n"
        "  <ResearchProjectDef>\n"
        f"    <defName>{RESEARCH_DEF_NAME}</defName>\n"
        "    <label>astraltech bionics</label>\n"
        "    <description>Decode fragments of Astraltech design to fabricate implants and addons that surpass even archotech parts. Requires a skilled doctor to attach.</description>\n"
        f"    <baseCost>{RESEARCH_BASE_COST}</baseCost>\n"
        "    <techLevel>Spacer</techLevel>\n"
        "    <prerequisites>\n"
        "      <li>Bionics</li>\n"
        "      <li>AdvancedFabrication</li>\n"
        "    </prerequisites>\n"
        "    <requiredResearchBuilding>HiTechResearchBench</requiredResearchBuilding>\n"
        "    <requiredResearchFacilities>\n"
        "      <li>MultiAnalyzer</li>\n"
        "    </requiredResearchFacilities>\n"
        f"    <tab>{RESEARCH_TAB_DEF_NAME}</tab>\n"
        "    <researchViewX>0</researchViewX>\n"
        "    <researchViewY>0</researchViewY>\n"
        "  </ResearchProjectDef>\n"
        "</Defs>"
    )


def generate_language_keys():
    return (
        """<?xml version="1.0" encoding="utf-8" ?>\n"""
        "<LanguageData>\n"
        "\t<AstraltechDescription>Astraltech is the next leap in bionic technology, far beyond even the mysterious Archotech devices. Developed in secret by an advanced faction from beyond the known stars, these implants were created for only the most elite individuals. They are not only functional but also imbued with seemingly supernatural capabilities that push the very limits of physical performance. No one knows the full extent of their capabilities, but their power is unmistakable.</AstraltechDescription>\n"
        "</LanguageData>"
    )
