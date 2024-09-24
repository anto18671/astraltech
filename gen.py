from stats import Stat, VALID_STATS, VALID_CAPACITIES
import shutil
import os

# Define a preface that explains the Astraltech's superiority
ASTRALTECH_LORE = "Astraltech is a monumental leap in bionic technology, surpassing even the mysterious Archotech devices. Secretly developed by an advanced faction beyond known stars for the elite, these implants possess seemingly supernatural abilities that push physical limits. Their full capabilities are unknown, but their power is undeniable."

# Valid body parts for bionics and addons targeted
BODY_PARTS = [
    'Torso', 'Neck', 'Skull', 'Brain', 'Eye', 'Ear', 'Nose', 'Jaw',
    'Spine', 'Ribcage', 'Stomach', 'Heart', 'Lung', 'Kidney',
    'Liver', 'Shoulder', 'Pelvis', 'Leg'
]

# Check if the folder exists, then delete it
if os.path.exists("AstralTech/"):
    shutil.rmtree("AstralTech/")

class Addon:
    def __init__(self, addon_name, label, description, market_value, additional_stats=None, part_efficiency=1.0):
        self.addon_name = addon_name.replace(" ", "_")
        self.label = label
        self.description = ASTRALTECH_LORE.strip() + "\n\n" + description
        self.market_value = market_value
        self.tex_path = "Things/Item/Health/AstralAddons"
        self.body_part = None
        self.additional_stats = additional_stats or []
        self.thing_class = "ThingWithComps"
        self.part_efficiency = part_efficiency

        # Process stats
        self.stat_offsets = []
        self.stat_factors = []
        self.capacity_offsets = []
        self.capacity_factors = []

        for stat in self.additional_stats:
            if stat.name in VALID_STATS:
                if stat.mod_type == 'offset':
                    self.stat_offsets.append(stat)
                elif stat.mod_type == 'factor':
                    self.stat_factors.append(stat)
            elif stat.name in VALID_CAPACITIES:
                if stat.mod_type == 'offset':
                    self.capacity_offsets.append(stat)
                elif stat.mod_type == 'factor':
                    self.capacity_factors.append(stat)
            else:
                raise ValueError(f"Invalid stat or capacity: {stat.name}")

    def generate_thingdef(self):
        # Only MarketValue is included in statBases for ThingDef
        thingdef = (
            "<ThingDef ParentName=\"BodyPartBionicBase\">\n"
            f"\t<defName>{self.addon_name}</defName>\n"
            f"\t<label>{self.label}</label>\n"
            f"\t<description>{self.description}</description>\n"
            "\t<techLevel>Spacer</techLevel>\n"
            f"\t<thingClass>{self.thing_class}</thingClass>\n"
            "\t<graphicData>\n"
            f"\t\t<texPath>{self.tex_path}</texPath>\n"
            "\t\t<graphicClass>Graphic_Single</graphicClass>\n"
            "\t</graphicData>\n"
            "\t<statBases>\n"
            f"\t\t<MarketValue>{self.market_value}</MarketValue>\n"
            "\t</statBases>\n"
            f"\t<techHediffsTags><li>Advanced</li></techHediffsTags>\n"
            f"\t<thingSetMakerTags><li>RewardStandardLowFreq</li></thingSetMakerTags>\n"
            f"\t<descriptionHyperlinks>\n"
            f"\t\t<RecipeDef>Install_{self.addon_name}</RecipeDef>\n"
            f"\t</descriptionHyperlinks>\n"
            f"\t<costList>\n"
            f"\t\t<Plasteel>10</Plasteel>\n"
            f"\t\t<ComponentSpacer>3</ComponentSpacer>\n"
            f"\t</costList>\n"
            "\t<comps>\n"
            "\t\t<li Class=\"CompProperties_Forbiddable\" />\n"
            "\t</comps>\n"
            "</ThingDef>\n"
        )
        return thingdef

    def generate_surgery_instruction(self):
        surgery = (
            "<RecipeDef ParentName=\"SurgeryFlesh\">\n"
            f"\t<defName>Install_{self.addon_name}</defName>\n"
            f"\t<label>install {self.label.lower()}</label>\n"
            f"\t<description>Install an {self.label.lower()}.</description>\n"
            f"\t<jobString>Installing {self.label.lower()}.</jobString>\n"
            "\t<workAmount>4500</workAmount>\n"
            "\t<surgerySuccessChanceFactor>1.2</surgerySuccessChanceFactor>\n"
            "\t<skillRequirements>\n"
            "\t\t<Medicine>8</Medicine>\n"
            "\t</skillRequirements>\n"
            "\t<ingredients>\n"
            "\t\t<li>\n"
            "\t\t\t<filter>\n"
            "\t\t\t\t<categories>\n"
            "\t\t\t\t\t<li>Medicine</li>\n"
            "\t\t\t\t</categories>\n"
            "\t\t\t</filter>\n"
            "\t\t\t<count>2</count>\n"
            "\t\t</li>\n"
            "\t\t<li>\n"
            "\t\t\t<filter>\n"
            "\t\t\t\t<thingDefs>\n"
            f"\t\t\t\t\t<li>{self.addon_name}</li>\n"
            "\t\t\t\t</thingDefs>\n"
            "\t\t\t</filter>\n"
            "\t\t\t<count>1</count>\n"
            "\t\t</li>\n"
            "\t</ingredients>\n"
            "\t<fixedIngredientFilter>\n"
            "\t\t<categories>\n"
            "\t\t\t<li>Medicine</li>\n"
            "\t\t</categories>\n"
            "\t\t<thingDefs>\n"
            f"\t\t\t<li>{self.addon_name}</li>\n"
            "\t\t</thingDefs>\n"
            "\t</fixedIngredientFilter>\n"
            f"\t<appliedOnFixedBodyParts>\n"
            f"\t\t<li>{self.body_part}</li>\n"
            f"\t</appliedOnFixedBodyParts>\n"
            f"\t<addsHediff>{self.addon_name}_hediff</addsHediff>\n"
            "</RecipeDef>\n"
        )
        return surgery

    def generate_hediffdef(self):
        hediff = (
            "<HediffDef ParentName=\"AddedBodyPartBase\">\n"
            f"\t<defName>{self.addon_name}_hediff</defName>\n"
            f"\t<label>{self.label}</label>\n"
            f"\t<labelNoun>{self.label}</labelNoun>\n"
            f"\t<description>{self.description}</description>\n"
            "\t<descriptionHyperlinks>\n"
            f"\t\t<ThingDef>{self.addon_name}</ThingDef>\n"
            "\t</descriptionHyperlinks>\n"
            f"\t<spawnThingOnRemoved>{self.addon_name}</spawnThingOnRemoved>\n"
            "\t<hediffClass>Hediff_Implant</hediffClass>\n"
            "\t<isBad>false</isBad>\n"
            "\t<addedPartProps>\n"
            f"\t\t<partEfficiency>{self.part_efficiency}</partEfficiency>\n"
            "\t</addedPartProps>\n"
            "\t<stages>\n"
            "\t\t<li>\n"
        )

        if self.capacity_factors or self.capacity_offsets:
            hediff += "\t\t\t<capMods>\n"
            for stat in self.capacity_factors + self.capacity_offsets:
                hediff += (
                    "\t\t\t\t<li>\n"
                    f"\t\t\t\t\t<capacity>{stat.name}</capacity>\n"
                    f"\t\t\t\t\t<{'offset' if stat.mod_type == 'offset' else 'postFactor'}>{stat.value}</{'offset' if stat.mod_type == 'offset' else 'postFactor'}>\n"
                    "\t\t\t\t</li>\n"
                )
            hediff += "\t\t\t</capMods>\n"

        if self.stat_offsets:
            hediff += "\t\t\t<statOffsets>\n"
            for stat in self.stat_offsets:
                hediff += f"\t\t\t\t<{stat.name}>{stat.value}</{stat.name}>\n"
            hediff += "\t\t\t</statOffsets>\n"

        if self.stat_factors:
            hediff += "\t\t\t<statFactors>\n"
            for stat in self.stat_factors:
                hediff += f"\t\t\t\t<{stat.name}>{stat.value}</{stat.name}>\n"
            hediff += "\t\t\t</statFactors>\n"

        hediff += (
            "\t\t</li>\n"
            "\t</stages>\n"
            "</HediffDef>\n"
        )
        return hediff

class Bionic:
    def __init__(self, bionic_name, label, description, part_efficiency, market_value, mass,
                 body_part, damage_multiplier=1.0, additional_stats=None, replace_part=True, compatible_addons=None):
        if body_part not in BODY_PARTS:
            raise ValueError(f"Body part '{body_part}' not found in the list of valid parts.")

        self.bionic_name = bionic_name.replace(" ", "_")
        self.label = label
        self.description = ASTRALTECH_LORE.strip() + "\n\n" + description
        self.part_efficiency = part_efficiency
        self.market_value = market_value
        self.mass = mass
        self.tex_path = "Things/Item/Health/AstralBionics"
        self.body_part = body_part
        self.damage_multiplier = damage_multiplier
        self.additional_stats = additional_stats or []
        self.replace_part = replace_part
        self.compatible_addons = compatible_addons or []
        self.thing_class = "ThingWithComps"

        for addon in self.compatible_addons:
            addon.body_part = body_part

        # Process stats
        self.stat_offsets = []
        self.stat_factors = []
        self.capacity_offsets = []
        self.capacity_factors = []

        for stat in self.additional_stats:
            if stat.name in VALID_STATS:
                if stat.mod_type == 'offset':
                    self.stat_offsets.append(stat)
                elif stat.mod_type == 'factor':
                    self.stat_factors.append(stat)
            elif stat.name in VALID_CAPACITIES:
                if stat.mod_type == 'offset':
                    self.capacity_offsets.append(stat)
                elif stat.mod_type == 'factor':
                    self.capacity_factors.append(stat)
            else:
                raise ValueError(f"Invalid stat or capacity: {stat.name}")

    def generate_thingdef(self):
        # Only MarketValue and Mass are included in statBases for ThingDef
        thingdef = (
            "<ThingDef ParentName=\"BodyPartBionicBase\">\n"
            f"\t<defName>{self.bionic_name}</defName>\n"
            f"\t<label>{self.label}</label>\n"
            f"\t<description>{self.description}</description>\n"
            "\t<techLevel>Spacer</techLevel>\n"
            f"\t<thingClass>{self.thing_class}</thingClass>\n"
            "\t<graphicData>\n"
            f"\t\t<texPath>{self.tex_path}</texPath>\n"
            "\t\t<graphicClass>Graphic_Single</graphicClass>\n"
            "\t</graphicData>\n"
            "\t<statBases>\n"
            f"\t\t<MarketValue>{self.market_value}</MarketValue>\n"
            f"\t\t<Mass>{self.mass}</Mass>\n"
            "\t</statBases>\n"
            f"\t<techHediffsTags><li>Advanced</li></techHediffsTags>\n"
            f"\t<thingSetMakerTags><li>RewardStandardLowFreq</li></thingSetMakerTags>\n"
            f"\t<descriptionHyperlinks>\n"
            f"\t\t<RecipeDef>Install_{self.bionic_name}</RecipeDef>\n"
            f"\t</descriptionHyperlinks>\n"
            f"\t<costList>\n"
            f"\t\t<Plasteel>20</Plasteel>\n"
            f"\t\t<ComponentSpacer>5</ComponentSpacer>\n"
            f"\t</costList>\n"
            "\t<comps>\n"
            "\t\t<li Class=\"CompProperties_Forbiddable\" />\n"
            "\t</comps>\n"
            "</ThingDef>\n"
        )
        return thingdef

    def generate_surgery_instruction(self):
        surgery = (
            "<RecipeDef ParentName=\"SurgeryFlesh\">\n"
            f"\t<defName>Install_{self.bionic_name}</defName>\n"
            f"\t<label>install {self.label.lower()}</label>\n"
            f"\t<description>Install a {self.label.lower()}.</description>\n"
            f"\t<jobString>Installing {self.label.lower()}.</jobString>\n"
            "\t<workAmount>6000</workAmount>\n"
            "\t<surgerySuccessChanceFactor>1.2</surgerySuccessChanceFactor>\n"
            "\t<skillRequirements>\n"
            "\t\t<Medicine>8</Medicine>\n"
            "\t</skillRequirements>\n"
            "\t<ingredients>\n"
            "\t\t<li>\n"
            "\t\t\t<filter>\n"
            "\t\t\t\t<categories>\n"
            "\t\t\t\t\t<li>Medicine</li>\n"
            "\t\t\t\t</categories>\n"
            "\t\t\t</filter>\n"
            "\t\t\t<count>3</count>\n"
            "\t\t</li>\n"
            "\t\t<li>\n"
            "\t\t\t<filter>\n"
            "\t\t\t\t<thingDefs>\n"
            f"\t\t\t\t\t<li>{self.bionic_name}</li>\n"
            "\t\t\t\t</thingDefs>\n"
            "\t\t\t</filter>\n"
            "\t\t\t<count>1</count>\n"
            "\t\t</li>\n"
            "\t</ingredients>\n"
            "\t<fixedIngredientFilter>\n"
            "\t\t<categories>\n"
            "\t\t\t<li>Medicine</li>\n"
            "\t\t</categories>\n"
            "\t\t<thingDefs>\n"
            f"\t\t\t<li>{self.bionic_name}</li>\n"
            "\t\t</thingDefs>\n"
            "\t</fixedIngredientFilter>\n"
            f"\t<appliedOnFixedBodyParts>\n"
            f"\t\t<li>{self.body_part}</li>\n"
            f"\t</appliedOnFixedBodyParts>\n"
            f"\t<addsHediff>{self.bionic_name}_hediff</addsHediff>\n"
            "</RecipeDef>\n"
        )
        return surgery

    def generate_hediffdef(self):
        hediff_class = "Hediff_AddedPart" if self.replace_part else "Hediff_Implant"
        hediff = (
            "<HediffDef ParentName=\"AddedBodyPartBase\">\n"
            f"\t<defName>{self.bionic_name}_hediff</defName>\n"
            f"\t<label>{self.label}</label>\n"
            f"\t<labelNoun>{self.label}</labelNoun>\n"
            f"\t<description>{self.description}</description>\n"
            "\t<descriptionHyperlinks>\n"
            f"\t\t<ThingDef>{self.bionic_name}</ThingDef>\n"
            "\t</descriptionHyperlinks>\n"
            f"\t<spawnThingOnRemoved>{self.bionic_name}</spawnThingOnRemoved>\n"
            f"\t<hediffClass>{hediff_class}</hediffClass>\n"
            "\t<isBad>false</isBad>\n"
            "\t<addedPartProps>\n"
            f"\t\t<partEfficiency>{self.part_efficiency}</partEfficiency>\n"
            "\t</addedPartProps>\n"
        )

        # Special case for Astraltech Stomach
        if self.bionic_name == "Astraltech_Stomach":
            hediff += (
                "\t<stages>\n"
                "\t\t<li>\n"
                "\t\t\t<statOffsets>\n"
                "\t\t\t\t<RestRateMultiplier>0.2</RestRateMultiplier>\n"
                "\t\t\t\t<InjuryHealingFactor>0.2</InjuryHealingFactor>\n"
                "\t\t\t\t<ImmunityGainSpeed>0.2</ImmunityGainSpeed>\n"
                "\t\t\t\t<MaxNutrition>0.5</MaxNutrition>\n"
                "\t\t\t</statOffsets>\n"
                "\t\t\t<hungerRateFactor>0.25</hungerRateFactor>\n"
                "\t\t\t<capMods>\n"
                "\t\t\t\t<li>\n"
                "\t\t\t\t\t<capacity>Eating</capacity>\n"
                "\t\t\t\t\t<postFactor>6.0</postFactor>\n"
                "\t\t\t\t</li>\n"
                "\t\t\t\t<li>\n"
                "\t\t\t\t\t<capacity>Moving</capacity>\n"
                "\t\t\t\t\t<postFactor>1.75</postFactor>\n"
                "\t\t\t\t</li>\n"
                "\t\t\t</capMods>\n"
                "\t\t</li>\n"
                "\t</stages>\n"
            )
        else:
            hediff += "\t<stages>\n"
            hediff += "\t\t<li>\n"

            if self.stat_offsets:
                hediff += "\t\t\t<statOffsets>\n"
                for stat in self.stat_offsets:
                    hediff += f"\t\t\t\t<{stat.name}>{stat.value}</{stat.name}>\n"
                hediff += "\t\t\t</statOffsets>\n"

            if self.capacity_factors or self.capacity_offsets:
                hediff += "\t\t\t<capMods>\n"
                for stat in self.capacity_factors + self.capacity_offsets:
                    hediff += (
                        "\t\t\t\t<li>\n"
                        f"\t\t\t\t\t<capacity>{stat.name}</capacity>\n"
                        f"\t\t\t\t\t<{'offset' if stat.mod_type == 'offset' else 'postFactor'}>"
                        f"{stat.value}</{'offset' if stat.mod_type == 'offset' else 'postFactor'}>\n"
                        "\t\t\t\t</li>\n"
                    )
                hediff += "\t\t\t</capMods>\n"

            hediff += "\t\t</li>\n"
            hediff += "\t</stages>\n"

        hediff += "</HediffDef>\n"
        return hediff

def write_xml_file(filename, content):
    relative_path = f"AstralTech/{filename}"
    os.makedirs(os.path.dirname(relative_path), exist_ok=True)
    with open(relative_path, "w", encoding='utf-8') as file:
        file.write(content)
    print(f"{relative_path} generated successfully.")

def generate_mod_metadata():
    return (
        """<?xml version="1.0" encoding="utf-8" ?>\n"""
        "<ModMetaData>\n"
        "\t<name>AstralTech Bionic Implants</name>\n"
        "\t<author>Anthony Therrien</author>\n"
        "\t<description>Adds new advanced bionic implants to RimWorld, pushing the boundaries of human enhancement with the mysterious AstralTech technology.</description>\n"
        "\t<packageId>AnthonyTherrien.AstralTechBionics</packageId>\n"
        "\t<supportedVersions>\n"
        "\t\t<li>1.5</li>\n"
        "\t</supportedVersions>\n"
        "</ModMetaData>"
    )

def generate_about_xml():
    return (
        """<?xml version="1.0" encoding="utf-8"?>\n"""
        "<ModMetaData>\n"
        "\t<name>AstralTech Bionic Implants</name>\n"
        "\t<author>Anthony Therrien</author>\n"
        "\t<url></url>\n"
        "\t<description>AstralTech Bionic Implants introduces a new tier of advanced bionics to RimWorld. These implants, developed by a mysterious faction from beyond known space, offer unprecedented enhancements to human capabilities. Each AstralTech implant pushes the boundaries of what's possible, granting users abilities that border on the supernatural. Upgrade your colonists with these cutting-edge implants and experience a new level of power in the RimWorld universe.</description>\n"
        "\t<packageId>AnthonyTherrien.AstralTechBionics</packageId>\n"
        "\t<supportedVersions>\n"
        "\t\t<li>1.5</li>\n"
        "\t</supportedVersions>\n"
        "</ModMetaData>"
    )

def generate_language_keys():
    return (
        """<?xml version="1.0" encoding="utf-8" ?>\n"""
        "<LanguageData>\n"
        "\t<AstralTechDescription>AstralTech is the next leap in bionic technology, far beyond even the mysterious Archotech devices. Developed in secret by an advanced faction from beyond the known stars, these implants were created for only the most elite individuals. They are not only functional but also imbued with seemingly supernatural capabilities that push the very limits of physical performance. No one knows the full extent of their capabilities, but their power is unmistakable.</AstralTechDescription>\n"
        "</LanguageData>"
    )

# Creating multiple Bionic and Addon objects
if __name__ == "__main__":
    # Define a list of bionics with improved descriptions
    bionics_list = [
        Bionic(
            bionic_name="Astraltech Skull",
            label="Astraltech Skull",
            description=(
                "The Astraltech Skull is a highly advanced cranial implant designed to provide superior protection to the brain while significantly enhancing cognitive processing speed. "
                "In addition to its unmatched resilience against physical trauma, the Astraltech Skull provides an enhanced aesthetic appeal, dramatically improving the wearer's facial beauty. "
                "This implant not only increases mental clarity but also elevates social standing, making it an ideal upgrade for individuals in combat, diplomacy, or high-stress environments."
            ),
            part_efficiency=3.0,
            market_value=26000,
            mass=6,
            body_part="Skull",
            replace_part=False,
            additional_stats=[
                Stat("ArmorRating_Sharp", 1.2, stat_type='stat', mod_type='factor'),
                Stat("ArmorRating_Blunt", 1.2, stat_type='stat', mod_type='factor'),
                Stat("PawnBeauty", 3.0, stat_type='stat', mod_type='offset'),
                Stat("SocialImpact", 0.5, stat_type='stat', mod_type='offset'),
                Stat("NegotiationAbility", 0.5, stat_type='stat', mod_type='offset'),
                Stat("TradePriceImprovement", 0.25, stat_type='stat', mod_type='offset'),
            ]
        ),
        Bionic(
            bionic_name="Astraltech Brain",
            label="Astraltech Brain",
            description=(
                "The Astraltech Brain is a pinnacle of neurotechnology, vastly expanding cognitive capacities "
                "and mental acuity. It seamlessly integrates with neural pathways to provide heightened "
                "intelligence, rapid information processing, and enhanced decision-making capabilities."
            ),
            part_efficiency=3.0,
            market_value=78000,
            mass=2,
            replace_part=False,
            body_part="Brain",
            additional_stats=[
                Stat("PawnBeauty", 1.0, stat_type='stat', mod_type='offset'),
                Stat("SocialImpact", 0.75, stat_type='stat', mod_type='offset'),
                Stat("NegotiationAbility", 0.5, stat_type='stat', mod_type='offset'),
                Stat("TradePriceImprovement", 0.25, stat_type='stat', mod_type='offset'),
                Stat("Consciousness", 4.0, stat_type='capacity', mod_type='factor'),
                Stat("Sight", 1.5, stat_type='capacity', mod_type='factor'),
                Stat("Hearing", 1.5, stat_type='capacity', mod_type='factor'),
                Stat("Manipulation", 1.2, stat_type='capacity', mod_type='factor'),
                Stat("MeleeHitChance", 5.0, stat_type='stat', mod_type='offset'),
                Stat("ShootingAccuracyPawn", 5.0, stat_type='stat', mod_type='offset'),
                Stat("GlobalLearningFactor", 4.0, stat_type='stat', mod_type='offset'),
                Stat("MedicalOperationSpeed", 0.4, stat_type='stat', mod_type='offset'),
                Stat("MedicalTendSpeed", 0.4, stat_type='stat', mod_type='offset'),
                Stat("MedicalTendQuality", 0.4, stat_type='stat', mod_type='offset'),
                Stat("MedicalSurgerySuccessChance", 0.4, stat_type='stat', mod_type='offset'),
                Stat("MeditationFocusGain", 1.5, stat_type='stat', mod_type='offset'),
                Stat("ResearchSpeed", 3.0, stat_type='stat', mod_type='offset'),
            ],
            compatible_addons=[
                Addon(
                    addon_name="Astraltech Working Memory Augmentation",
                    label="Astraltech Working Memory Augmentation",
                    description=(
                        "The Astraltech Working Memory Augmentation drastically improves the brain's capacity to hold and manipulate information "
                        "in real-time. By enhancing short-term memory and cognitive agility, this addon is ideal for users engaged in complex, "
                        "high-pressure decision-making, allowing them to juggle multiple tasks and data points effortlessly."
                    ),
                    market_value=23400,
                    additional_stats=[
                        Stat("Consciousness", 1.25, stat_type='capacity', mod_type='factor'),
                        Stat("WorkSpeedGlobal", 1.1, stat_type='stat', mod_type='factor'),
                        Stat("GlobalLearningFactor", 1.0, stat_type='stat', mod_type='offset'),
                        Stat("ResearchSpeed", 2.0, stat_type='stat', mod_type='offset'),
                    ]
                ),
                Addon(
                    addon_name="Astraltech Emotional Regulator",
                    label="Astraltech Emotional Regulator",
                    description=(
                        "The Astraltech Emotional Regulator stabilizes emotional responses, ensuring that the user can stay "
                        "calm and composed under the most stressful conditions. This addon promotes clarity of thought and "
                        "enhances social dynamics by eliminating erratic emotional shifts."
                    ),
                    market_value=15600,
                    additional_stats=[
                        Stat("Consciousness", 1.1, stat_type='capacity', mod_type='factor'),
                        Stat("NegotiationAbility", 0.5, stat_type='stat', mod_type='offset'),
                        Stat("TradePriceImprovement", 0.25, stat_type='stat', mod_type='offset'),
                        Stat("MentalBreakThreshold", -0.4, stat_type='stat', mod_type='offset'),
                    ]
                ),
                Addon(
                    addon_name="Astraltech Cognitive Synchronizer",
                    label="Astraltech Cognitive Synchronizer",
                    description=(
                        "The Astraltech Cognitive Synchronizer tunes brainwave patterns to enhance focus and multi-tasking abilities. "
                        "With this addon, the user can seamlessly handle multiple tasks with minimal loss of efficiency, vastly "
                        "improving overall productivity."
                    ),
                    market_value=20800,
                    additional_stats=[
                        Stat("Consciousness", 1.1, stat_type='capacity', mod_type='factor'),
                        Stat("WorkSpeedGlobal", 1.1, stat_type='stat', mod_type='factor'),
                        Stat("Manipulation", 1.1, stat_type='capacity', mod_type='factor'),
                    ]
                ),
                Addon(
                    addon_name="AstraltechThoughtAccelerator",
                    label="Astraltech Rapid Thought Accelerator",
                    description=(
                        "The Astraltech Rapid Thought Accelerator boosts the brain’s processing speed, enabling quick decisions, "
                        "faster reactions, and split-second calculations. It’s perfect for users engaged in high-stakes operations "
                        "or intense mental tasks."
                    ),
                    market_value=26000,
                    additional_stats=[
                        Stat("Consciousness", 1.1, stat_type='capacity', mod_type='factor'),
                        Stat("GlobalLearningFactor", 1.5, stat_type='stat', mod_type='offset'),
                        Stat("WorkSpeedGlobal", 1.1, stat_type='stat', mod_type='factor'),
                        Stat("MeleeHitChance", 1.25, stat_type='stat', mod_type='offset'),
                        Stat("ShootingAccuracyPawn", 1.25, stat_type='stat', mod_type='offset'),
                    ]
                ),
            ]
        ),
        Bionic(
            bionic_name="Astraltech Eye",
            label="Astraltech Eye",
            description=(
                "The Astraltech Eye is a cutting-edge bionic implant designed to vastly improve visual acuity and perception. "
                "With advanced optical systems, it enhances sight beyond normal human limits, enabling the user to see in low-light conditions, "
                "improve reaction times, and increase accuracy in combat situations."
            ),
            part_efficiency=3.0,
            market_value=15000,
            mass=1,
            body_part="Eye",
            additional_stats=[
                Stat("Sight", 2.5, stat_type='capacity', mod_type='factor'),
                Stat("ShootingAccuracyPawn", 1.75, stat_type='stat', mod_type='offset'),
                Stat("MeleeHitChance", 1.5, stat_type='stat', mod_type='offset'),
                Stat("Manipulation", 1.1, stat_type='capacity', mod_type='factor'),
            ],
            compatible_addons=[
                Addon(
                    addon_name="AstraltechTargetingEnhancer",
                    label="Astraltech Targeting Enhancer",
                    description=(
                        "The Astraltech Targeting Enhancer improves the user’s ability to focus on targets and increases precision in combat. "
                        "With advanced tracking algorithms, this addon is ideal for sharpshooters and individuals in combat-heavy roles."
                    ),
                    market_value=11700,
                    additional_stats=[
                        Stat("Sight", 1.5, stat_type='capacity', mod_type='factor'),
                        Stat("ShootingAccuracyPawn", 1.6, stat_type='stat', mod_type='offset'),
                        Stat("MeleeHitChance", 1.4, stat_type='stat', mod_type='offset'),
                    ]
                ),
                Addon(
                    addon_name="AstraltechMotionDetectionModule",
                    label="Astraltech Motion Detection Module",
                    description=(
                        "The Astraltech Motion Detection Module enhances the user’s ability to detect movement, significantly increasing their reaction time "
                        "in fast-paced environments. It provides an edge in combat by allowing the user to anticipate and respond to threats more quickly."
                    ),
                    market_value=10400,
                    additional_stats=[
                        Stat("Sight", 1.5, stat_type='capacity', mod_type='factor'),
                        Stat("MeleeHitChance", 1.4, stat_type='stat', mod_type='offset'),
                        Stat("Manipulation", 1.1, stat_type='capacity', mod_type='factor'),
                        Stat("MoveSpeed", 1.1, stat_type='stat', mod_type='factor'),
                    ]
                ),
            ]
        ),
        Bionic(
            bionic_name="Astraltech Ear",
            label="Astraltech Ear",
            description=(
                "The Astraltech Ear is a marvel of auditory enhancement, granting its user unparalleled hearing abilities. "
                "It provides superhuman sound detection, heightened situational awareness, and flawless communication in any environment. "
                "With its otherworldly sound-processing capabilities, even the faintest whisper becomes clear as day."
            ),
            part_efficiency=2.5,
            market_value=19000,
            mass=0.5,
            body_part="Ear",
            additional_stats=[
                Stat("Hearing", 3.0, stat_type='capacity', mod_type='factor'),
                Stat("MeleeHitChance", 1.2, stat_type='stat', mod_type='offset'),
                Stat("ShootingAccuracyPawn", 1.2, stat_type='stat', mod_type='offset'),
                Stat("NegotiationAbility", 0.2, stat_type='stat', mod_type='offset'),
            ],
            compatible_addons=[
                Addon(
                    addon_name="AstraltechSoundAmplifier",
                    label="Astraltech Sound Amplifier",
                    description=(
                        "The Astraltech Sound Amplifier grants its user the ability to hear sounds from impossible distances. "
                        "This addon enhances long-range auditory detection and allows the user to hear through solid obstacles as if they weren't there."
                    ),
                    market_value=11700,
                    additional_stats=[
                        Stat("Hearing", 1.5, stat_type='capacity', mod_type='factor'),
                        Stat("ShootingAccuracyPawn", 1.1, stat_type='stat', mod_type='offset'),
                        Stat("MeleeHitChance", 1.1, stat_type='stat', mod_type='offset'),
                    ]
                ),
                Addon(
                    addon_name="AstraltechNoiseFilter",
                    label="Astraltech Noise Filter",
                    description=(
                        "The Astraltech Noise Filter eliminates all unwanted background noise, allowing the user to focus on crucial sounds with preternatural clarity. "
                        "In even the most chaotic environments, it filters out distractions, enhancing auditory perception to superhuman levels."
                    ),
                    market_value=8450,
                    additional_stats=[
                        Stat("Hearing", 1.25, stat_type='capacity', mod_type='factor'),
                        Stat("Sight", 1.1, stat_type='capacity', mod_type='factor'),
                    ]
                ),
                Addon(
                    addon_name="AstraltechEchoLocator",
                    label="Astraltech Echo Locator",
                    description=(
                        "The Astraltech Echo Locator utilizes impossible echolocation technology, granting the user an almost precognitive spatial awareness. "
                        "This addon provides unparalleled threat detection and environmental navigation, bordering on the supernatural."
                    ),
                    market_value=11700,
                    additional_stats=[
                        Stat("Hearing", 1.4, stat_type='capacity', mod_type='factor'),
                        Stat("MeleeHitChance", 1.3, stat_type='stat', mod_type='offset'),
                        Stat("ShootingAccuracyPawn", 1.2, stat_type='stat', mod_type='offset'),
                        Stat("MeleeDodgeChance", 1.2, stat_type='stat', mod_type='offset'),
                    ]
                ),
            ]
        ),
        Bionic(
            bionic_name="Astraltech Nose",
            label="Astraltech Nose",
            description=(
                "The Astraltech Nose is an olfactory marvel that transcends normal sensory limits. "
                "It offers supernatural detection of airborne particles, granting the ability to discern complex chemical compositions at a glance. "
                "Users can track scents across vast distances and even detect emotional states through pheromone analysis."
            ),
            part_efficiency=3.0,
            market_value=16000,
            mass=0.3,
            body_part="Nose",
            additional_stats=[
                Stat("PawnBeauty", 1.0, stat_type='stat', mod_type='offset'),
                Stat("SocialImpact", 0.5, stat_type='stat', mod_type='offset'),
                Stat("FoodPoisonChance", -0.5, stat_type='stat', mod_type='offset'),
                Stat("Breathing", 1.5, stat_type='capacity', mod_type='factor'),
            ]
        ),
        Bionic(
            bionic_name="Astraltech Jaw",
            label="Astraltech Jaw",
            description=(
                "The Astraltech Jaw is a pinnacle of oral enhancement, granting its user unparalleled speech capabilities. "
                "It provides flawless articulation in any language, enhanced persuasive abilities."
            ),
            part_efficiency=3.5,
            market_value=20800,
            mass=0.8,
            body_part="Jaw",
            additional_stats=[
                Stat("PawnBeauty", 1.0, stat_type='stat', mod_type='offset'),
                Stat("SocialImpact", 0.5, stat_type='stat', mod_type='offset'),
                Stat("NegotiationAbility", 0.5, stat_type='stat', mod_type='offset'),
                Stat("TradePriceImprovement", 0.1, stat_type='stat', mod_type='offset'),
                Stat("EatingSpeed", 1.5, stat_type='stat', mod_type='factor'),
            ]
        ),
        Bionic(
            bionic_name="Astraltech Neck",
            label="Astraltech Neck",
            description=(
                "The Astraltech Neck is a marvel of biomechanical engineering, offering superhuman structural integrity and flexibility. "
                "It grants the user near-invulnerability to neck injuries, perfect posture control, and enhanced sensory processing. "
                "This implant elevates the user's physical capabilities to mythical levels, making them a force to be reckoned with in any situation."
            ),
            part_efficiency=3.5,
            market_value=26000,
            mass=2,
            replace_part=False,
            body_part="Neck",
            additional_stats=[
                Stat("ArmorRating_Sharp", 1.2, stat_type='stat', mod_type='factor'),
                Stat("ArmorRating_Blunt", 1.2, stat_type='stat', mod_type='factor'),
                Stat("MeleeHitChance", 1.4, stat_type='stat', mod_type='offset'),
                Stat("ShootingAccuracyPawn", 1.3, stat_type='stat', mod_type='offset'),
                Stat("Manipulation", 1.1, stat_type='capacity', mod_type='factor'),
                Stat("MoveSpeed", 1.1, stat_type='stat', mod_type='factor'),
                Stat("MeleeDodgeChance", 1.2, stat_type='stat', mod_type='offset'),
                Stat("Breathing", 1.5, stat_type='capacity', mod_type='factor'),
            ]
        ),
        Bionic(
            bionic_name="Astraltech Arm",
            label="Astraltech Arm",
            description=(
                "The Astraltech Arm represents the pinnacle of prosthetic engineering, offering superhuman "
                "strength and dexterity. Its adaptive nanosystems allow for impossibly precise movements and effortless lifting of massive weights, "
                "while its indestructible construction ensures unmatched durability in even the most extreme situations."
            ),
            part_efficiency=3.0,
            market_value=32500,
            mass=4,
            body_part="Shoulder",
            damage_multiplier=3.0,
            additional_stats=[
                Stat("Manipulation", 2.0, stat_type='capacity', mod_type='factor'),
                Stat("WorkSpeedGlobal", 1.2, stat_type='stat', mod_type='factor'),
                Stat("ShootingAccuracyPawn", 1.5, stat_type='stat', mod_type='offset'),
                Stat("MedicalOperationSpeed", 0.4, stat_type='stat', mod_type='offset'),
                Stat("MedicalTendSpeed", 0.4, stat_type='stat', mod_type='offset'),
                Stat("MedicalTendQuality", 0.4, stat_type='stat', mod_type='offset'),
                Stat("MedicalSurgerySuccessChance", 0.4, stat_type='stat', mod_type='offset'),
                Stat("MeleeHitChance", 1.4, stat_type='stat', mod_type='offset'),
                Stat("MeleeDPS", 1.5, stat_type='stat', mod_type='factor'),
                Stat("ConstructionSpeed", 0.3, stat_type='stat', mod_type='offset'),
            ],
            compatible_addons=[
                Addon(
                    addon_name="Astraltech Shoulder Reinforcement",
                    label="Astraltech Shoulder Reinforcement",
                    description=(
                        "Engineered with otherworldly precision, the Astraltech Shoulder Reinforcement dramatically enhances the "
                        "structural integrity and power output of bionic arms, enabling strength beyond mortal comprehension and "
                        "unbreakable resilience in even the most extreme environments."
                    ),
                    market_value=19500,
                    additional_stats=[
                        Stat("Manipulation", 1.4, stat_type='capacity', mod_type='factor'),
                        Stat("MeleeDPS", 1.3, stat_type='stat', mod_type='factor'),
                        Stat("WorkSpeedGlobal", 1.2, stat_type='stat', mod_type='factor'),
                    ]
                ),
            ]
        ),
        Bionic(
            bionic_name="Astraltech Spine",
            label="Astraltech Spine",
            description=(
                "The Astraltech Spine is a revolutionary bionic implant that redefines human physicality. "
                "It grants the user inhuman core stability, mobility, and overall physical coordination. "
                "Wearers move with preternatural grace, maintain perfect balance in any situation, and possess flexibility that defies biological limitations."
            ),
            part_efficiency=3.0,
            market_value=39000,
            mass=6,
            replace_part=False,
            body_part="Spine",
            additional_stats=[
                Stat("Moving", 3.0, stat_type='capacity', mod_type='factor'),
                Stat("Manipulation", 1.4, stat_type='capacity', mod_type='factor'),
                Stat("MeleeHitChance", 1.5, stat_type='stat', mod_type='offset'),
                Stat("MeleeDodgeChance", 1.5, stat_type='stat', mod_type='offset'),
                Stat("MoveSpeed", 1.5, stat_type='stat', mod_type='factor'),
                Stat("Consciousness", 1.1, stat_type='capacity', mod_type='factor'),
            ],
            compatible_addons=[
                Addon(
                    addon_name="AstraltechPostureEnhancer",
                    label="Astraltech Posture Enhancer",
                    description=(
                        "The Astraltech Posture Enhancer perfects the user's body alignment, eliminating strain during any movement and granting limitless endurance. "
                        "This addon ensures flawless posture for any task, offering superhuman comfort and efficiency in all physical endeavors."
                    ),
                    market_value=23400,
                    additional_stats=[
                        Stat("Moving", 1.5, stat_type='capacity', mod_type='factor'),
                        Stat("Manipulation", 1.2, stat_type='capacity', mod_type='factor'),
                        Stat("WorkSpeedGlobal", 1.2, stat_type='stat', mod_type='factor'),
                        Stat("PawnBeauty", 1.0, stat_type='stat', mod_type='offset'),
                        Stat("SocialImpact", 0.5, stat_type='stat', mod_type='offset'),
                    ]
                ),
                Addon(
                    addon_name="AstraltechStabilityModule",
                    label="Astraltech Stability Module",
                    description=(
                        "The Astraltech Stability Module grants supernatural core stability, allowing the user to perform even the most delicate tasks with perfect accuracy and control. "
                        "It renders the user nearly immune to knockdowns and dramatically improves overall physical performance."
                    ),
                    market_value=26000,
                    additional_stats=[
                        Stat("Manipulation", 1.2, stat_type='capacity', mod_type='factor'),
                        Stat("MeleeHitChance", 1.3, stat_type='stat', mod_type='offset'),
                        Stat("ShootingAccuracyPawn", 1.3, stat_type='stat', mod_type='offset'),
                        Stat("MeleeDodgeChance", 1.3, stat_type='stat', mod_type='offset'),
                    ]
                ),
                Addon(
                    addon_name="AstraltechAgilityBooster",
                    label="Astraltech Agility Booster",
                    description=(
                        "The Astraltech Agility Booster elevates the user's agility to superhuman levels, enabling movements faster than the eye can track and instantaneous combat responses. "
                        "This addon dramatically enhances reflexes and coordination, making the user seem to bend the laws of physics in fast-paced environments."
                    ),
                    market_value=32500,
                    additional_stats=[
                        Stat("Moving", 1.8, stat_type='capacity', mod_type='factor'),
                        Stat("MeleeHitChance", 1.5, stat_type='stat', mod_type='offset'),
                        Stat("MeleeDodgeChance", 1.5, stat_type='stat', mod_type='offset'),
                        Stat("MoveSpeed", 1.4, stat_type='stat', mod_type='factor'),
                    ]
                ),
            ]
        ),
        Bionic(
            bionic_name="Astraltech Ribcage",
            label="Astraltech Ribcage",
            description=(
                "The Astraltech Ribcage is an impenetrable bionic implant that redefines the concept of physical protection. "
                "With its advanced energy-dispersing reinforcement, it renders the user nearly invulnerable to physical trauma, offering an unprecedented level of defense in combat situations."
            ),
            part_efficiency=3.0,
            market_value=28600,
            mass=5,
            body_part="Ribcage",
            additional_stats=[
                Stat("ArmorRating_Sharp", 1.2, stat_type='stat', mod_type='factor'),
                Stat("ArmorRating_Blunt", 1.2, stat_type='stat', mod_type='factor'),
                Stat("Breathing", 2.0, stat_type='capacity', mod_type='factor'),
                Stat("BloodPumping", 1.2, stat_type='capacity', mod_type='factor'),
            ]
        ),
        Bionic(
            bionic_name="Astraltech Torso",
            label="Astraltech Torso",
            description=(
                "The Astraltech Torso is a marvel of biotechnology that completely redefines human physical capabilities. "
                "Its hyper-advanced systems provide unparalleled internal support, allowing the user to endure forces that would shatter normal bodies. "
                "The implant's exotic technology ensures superhuman physical performance, seemingly limitless endurance, and rapid healing in any situation."
            ),
            part_efficiency=3.0,
            market_value=45500,
            mass=8,
            replace_part=False,
            body_part="Torso",
            additional_stats=[
                Stat("ArmorRating_Sharp", 1.2, stat_type='stat', mod_type='factor'),
                Stat("ArmorRating_Blunt", 1.2, stat_type='stat', mod_type='factor'),
                Stat("BloodPumping", 1.2, stat_type='capacity', mod_type='factor'),
                Stat("Moving", 1.5, stat_type='capacity', mod_type='factor'),
                Stat("MeleeHitChance", 1.5, stat_type='stat', mod_type='offset'),
                Stat("ShootingAccuracyPawn", 1.4, stat_type='stat', mod_type='offset'),
                Stat("Manipulation", 1.25, stat_type='capacity', mod_type='factor'),
                Stat("MoveSpeed", 1.3, stat_type='stat', mod_type='factor'),
            ],
            compatible_addons=[
                Addon(
                    addon_name="AstraltechResilienceEnhancer",
                    label="Astraltech Resilience Enhancer",
                    description=(
                        "The Astraltech Resilience Enhancer dramatically improves the user's overall toughness, allowing them to shrug off damage that would incapacitate or kill a normal human. "
                        "This addon grants near-superhuman physical endurance, making the user almost impervious to harsh conditions and physical trauma."
                    ),
                    market_value=19500,
                    additional_stats=[
                        Stat("Moving", 1.2, stat_type='capacity', mod_type='factor'),
                    ]
                ),
                Addon(
                    addon_name="AstraltechCoreStabilizer",
                    label="Astraltech Core Stabilizer",
                    description=(
                        "The Astraltech Core Stabilizer perfects the user's internal balance and core strength, dramatically improving movement efficiency and virtually eliminating energy expenditure during physical tasks. "
                        "This addon is essential for those who need to perform at peak levels indefinitely."
                    ),
                    market_value=23400,
                    additional_stats=[
                        Stat("Moving", 1.4, stat_type='capacity', mod_type='factor'),
                        Stat("Manipulation", 1.25, stat_type='capacity', mod_type='factor'),
                        Stat("WorkSpeedGlobal", 1.15, stat_type='stat', mod_type='factor'),
                    ]
                ),
                Addon(
                    addon_name="AstraltechDurabilityMatrix",
                    label="Astraltech Durability Matrix",
                    description=(
                        "The Astraltech Durability Matrix exponentially reinforces the torso's structural integrity, providing near-invulnerability to physical damage. "
                        "This addon ensures unparalleled survivability in combat situations, as the body becomes resistant to all but the most catastrophic injuries."
                    ),
                    market_value=26000,
                    additional_stats=[
                        Stat("ArmorRating_Sharp", 1.2, stat_type='stat', mod_type='factor'),
                        Stat("ArmorRating_Blunt", 1.2, stat_type='stat', mod_type='factor'),
                        Stat("Manipulation", 1.2, stat_type='capacity', mod_type='factor'),
                        Stat("MeleeHitChance", 1.4, stat_type='stat', mod_type='offset'),
                    ]
                ),
                Addon(
                    addon_name="AstraltechMetabolicRegulator",
                    label="Astraltech Metabolic Regulator",
                    description=(
                        "The Astraltech Metabolic Regulator perfects the user's metabolism, optimizing energy utilization to such a degree that fatigue becomes nearly non-existent. "
                        "This addon is crucial for individuals requiring perpetual physical exertion without any loss in stamina or endurance."
                    ),
                    market_value=32500,
                    additional_stats=[
                        Stat("Moving", 1.4, stat_type='capacity', mod_type='factor'),
                        Stat("WorkSpeedGlobal", 1.1, stat_type='stat', mod_type='factor'),
                        Stat("Consciousness", 1.05, stat_type='capacity', mod_type='factor'),
                    ]
                ),
                Addon(
                    addon_name="AstraltechInternalShielding",
                    label="Astraltech Internal Shielding",
                    description=(
                        "The Astraltech Internal Shielding creates an energy barrier that absorbs and dissipates impacts, dramatically reducing the severity of injuries. "
                        "This addon is invaluable in combat situations, where it can mean the difference between walking away unscathed and critical injury."
                    ),
                    market_value=39000,
                    additional_stats=[
                        Stat("ArmorRating_Sharp", 1.2, stat_type='stat', mod_type='factor'),
                        Stat("ArmorRating_Blunt", 1.2, stat_type='stat', mod_type='factor'),
                        Stat("Manipulation", 1.2, stat_type='capacity', mod_type='factor'),
                        Stat("ShootingAccuracyPawn", 1.2, stat_type='stat', mod_type='offset'),
                    ]
                ),
                Addon(
                    addon_name="Astraltech Shaper",
                    label="Astraltech Shaper",
                    description=(
                        "The Astraltech Shaper is an advanced implant that sculpts the user's physique to perfection. "
                        "It redefines the body's proportions, enhancing muscle tone and symmetry to create an ideal form. "
                        "This addon dramatically improves physical appearance, making the user exceptionally attractive."
                    ),
                    market_value=28600,
                    additional_stats=[
                        Stat("PawnBeauty", 3.0, stat_type='stat', mod_type='offset'),
                        Stat("SocialImpact", 0.5, stat_type='stat', mod_type='offset'),
                    ]
                ),
                Addon(
                    addon_name="Astraltech Skin Enhancer",
                    label="Astraltech Skin Enhancer",
                    description=(
                        "The Astraltech Skin Enhancer rejuvenates and perfects the user's skin at the cellular level. "
                        "It eliminates imperfections, scars, and signs of aging, granting flawless and radiant skin. "
                        "This addon significantly enhances the user's appearance and social presence."
                    ),
                    market_value=26600,
                    additional_stats=[
                        Stat("PawnBeauty", 2.0, stat_type='stat', mod_type='offset'),
                        Stat("SocialImpact", 0.5, stat_type='stat', mod_type='offset'),
                    ]
                ),
            ],
        ),
        Bionic(
            bionic_name="Astraltech Heart",
            label="Astraltech Heart",
            description=(
                "The Astraltech Heart is a revolutionary cardiovascular system that transcends the limitations of biology. "
                "It provides seemingly limitless stamina, complete immunity to fatigue, and superhuman physical performance, allowing the user to maintain peak activity levels indefinitely."
            ),
            part_efficiency=3.0,
            market_value=52000,
            mass=2,
            body_part="Heart",
            additional_stats=[
                Stat("BloodPumping", 2.75, stat_type='capacity', mod_type='factor'),
                Stat("Moving", 2.0, stat_type='capacity', mod_type='factor'),
                Stat("WorkSpeedGlobal", 1.2, stat_type='stat', mod_type='factor'),
                Stat("MoveSpeed", 1.5, stat_type='stat', mod_type='factor'),
                Stat("Consciousness", 1.1, stat_type='capacity', mod_type='factor'),
            ],
            compatible_addons=[
                Addon(
                    addon_name="AstraltechCardioBoost",
                    label="Astraltech Cardio Boost",
                    description=(
                        "The Astraltech Cardio Boost is an advanced addon that further enhances the heart's capabilities beyond comprehension. "
                        "This addon eliminates the concept of physical exhaustion, allowing the user to perform at peak levels continuously without any decline in performance."
                    ),
                    market_value=32500,
                    additional_stats=[
                        Stat("BloodPumping", 1.4, stat_type='capacity', mod_type='factor'),
                        Stat("Moving", 1.3, stat_type='capacity', mod_type='factor'),
                        Stat("WorkSpeedGlobal", 1.1, stat_type='stat', mod_type='factor'),
                        Stat("MoveSpeed", 1.3, stat_type='stat', mod_type='factor'),
                    ]
                ),
            ]
        ),
        Bionic(
            bionic_name="Astraltech Lung",
            label="Astraltech Lung",
            description=(
                "The Astraltech Lung is a revolutionary respiratory enhancement that defies the limits of biology. "
                "It allows for superhuman stamina and endurance, providing near-invulnerability to suffocation and unparalleled performance in any atmosphere."
            ),
            part_efficiency=3.0,
            market_value=39000,
            mass=2,
            body_part="Lung",
            additional_stats=[
                Stat("Breathing", 3.0, stat_type='capacity', mod_type='factor'),
                Stat("BloodPumping", 1.25, stat_type='capacity', mod_type='factor'),
                Stat("Moving", 1.75, stat_type='capacity', mod_type='factor'),
                Stat("MoveSpeed", 1.3, stat_type='stat', mod_type='factor'),
                Stat("Consciousness", 1.05, stat_type='capacity', mod_type='factor'),
            ]
        ),
        Bionic(
            bionic_name="Astraltech Kidney",
            label="Astraltech Kidney",
            description=(
                "The Astraltech Kidney is an unparalleled filtration system that revolutionizes the body's ability to purge toxins and regulate hydration. "
                "It grants near-immunity to poisons and illnesses, while dramatically enhancing overall vitality and resilience."
            ),
            part_efficiency=3.0,
            market_value=28000,
            mass=1.5,
            body_part="Kidney",
            additional_stats=[
                Stat("BloodFiltration", 6.0, stat_type='capacity', mod_type='factor'),
                Stat("Consciousness", 1.05, stat_type='capacity', mod_type='factor'),
                Stat("Breathing", 1.1, stat_type='capacity', mod_type='factor'),
            ]
        ),
        Bionic(
            bionic_name="Astraltech Liver",
            label="Astraltech Liver",
            description=(
                "The Astraltech Liver is a marvel of biotechnology, providing unimaginable detoxification and metabolic regulation. "
                "It grants the user virtual immunity to toxins and alcohol while dramatically accelerating healing and providing unmatched resilience to diseases."
            ),
            part_efficiency=3.0,
            market_value=31200,
            mass=3,
            body_part="Liver",
            additional_stats=[
                Stat("BloodFiltration", 6.0, stat_type='capacity', mod_type='factor'),
                Stat("Breathing", 1.2, stat_type='capacity', mod_type='factor'),
                Stat("Consciousness", 1.1, stat_type='capacity', mod_type='factor'),
            ]
        ),
        Bionic(
            bionic_name="Astraltech Stomach",
            label="Astraltech Stomach",
            description=(
                "The Astraltech Stomach is a revolutionary digestive system that redefines the limits of nutrient absorption and energy extraction. "
                "It allows for near-perfect metabolic efficiency, dramatically reducing food requirements while maximizing energy output and physical endurance."
            ),
            part_efficiency=3.0,
            market_value=28600,
            mass=3,
            body_part="Stomach",
            additional_stats=[
                Stat("Moving", 1.25, stat_type='capacity', mod_type='factor'),
                Stat("MaxNutrition", 1.5, stat_type='stat', mod_type='factor'),
                Stat("Consciousness", 1.05, stat_type='capacity', mod_type='factor'),
            ],
            compatible_addons=[
                Addon(
                    addon_name="AstraltechMetabolicOptimizer",
                    label="Astraltech Metabolic Optimizer",
                    description=(
                        "The Astraltech Metabolic Optimizer pushes the stomach's capabilities to near-magical levels. "
                        "This addon allows the user to extract maximum energy from minimal food, virtually eliminating fatigue and granting seemingly limitless endurance."
                    ),
                    market_value=20800,
                    additional_stats=[
                        Stat("Moving", 1.1, stat_type='capacity', mod_type='factor'),
                        Stat("WorkSpeedGlobal", 1.1, stat_type='stat', mod_type='factor'),
                        Stat("BloodFiltration", 2.0, stat_type='capacity', mod_type='factor'),
                        Stat("Consciousness", 1.05, stat_type='capacity', mod_type='factor'),
                    ]
                ),
            ]
        ),
        Bionic(
            bionic_name="Astraltech Pelvis",
            label="Astraltech Pelvis",
            description=(
                "The Astraltech Pelvis is a groundbreaking implant that redefines human biomechanics. "
                "It provides supernatural core stability and lower body strength, allowing for inhuman endurance, agility, and resilience in any physical endeavor."
            ),
            part_efficiency=3.0,
            market_value=36400,
            mass=7,
            replace_part=False,
            body_part="Pelvis",
            additional_stats=[
                Stat("Moving", 1.4, stat_type='capacity', mod_type='factor'),
                Stat("Manipulation", 1.25, stat_type='capacity', mod_type='factor'),
                Stat("MeleeHitChance", 1.25, stat_type='stat', mod_type='offset'),
                Stat("MeleeDodgeChance", 1.25, stat_type='stat', mod_type='offset'),
                Stat("MoveSpeed", 1.2, stat_type='stat', mod_type='factor'),
            ]
        ),
        Bionic(
            bionic_name="Astraltech Leg",
            label="Astraltech Leg",
            description=(
                "The Astraltech Leg is a marvel of bionic engineering that transcends human locomotion capabilities. "
                "Equipped with hyper-advanced kinetic systems, it enables movement faster than the eye can track, perfect balance in any terrain, "
                "and superhuman jumping abilities, redefining the limits of mobility and athletic performance."
            ),
            part_efficiency=3.0,
            market_value=32500,
            mass=5,
            body_part="Leg",
            additional_stats=[
                Stat("Moving", 1.75, stat_type='capacity', mod_type='factor'),
                Stat("MoveSpeed", 1.5, stat_type='stat', mod_type='factor'),
                Stat("MeleeHitChance", 1.3, stat_type='stat', mod_type='offset'),
                Stat("MeleeDodgeChance", 1.4, stat_type='stat', mod_type='offset'),
                Stat("WorkSpeedGlobal", 1.2, stat_type='stat', mod_type='factor'),
            ],
            compatible_addons=[
                Addon(
                    addon_name="Astraltech Knee Enhancement",
                    label="Astraltech Knee Enhancement",
                    description=(
                        "The Astraltech Knee Enhancement integrates otherworldly technology to push the capabilities of bionic legs beyond imagination. "
                        "It grants the user near-perfect agility, allowing for instantaneous direction changes and providing seemingly limitless endurance."
                    ),
                    market_value=19500,
                    additional_stats=[
                        Stat("Moving", 1.4, stat_type='capacity', mod_type='factor'),
                        Stat("MoveSpeed", 1.25, stat_type='stat', mod_type='factor'),
                        Stat("MeleeDodgeChance", 1.3, stat_type='stat', mod_type='offset'),
                        Stat("WorkSpeedGlobal", 1.15, stat_type='stat', mod_type='factor'),
                    ]
                ),
            ]
        ),
    ]

    # Generate mod structure and files
    write_xml_file("About/ModMetaData.xml", generate_mod_metadata())
    write_xml_file("About/About.xml", generate_about_xml())
    write_xml_file("Languages/English/Keyed/AstralTech_Keys.xml", generate_language_keys())

    # Initialize counters
    bionics_count = 0
    addons_count = 0

    # Generate ThingDefs for bionics and addons
    bionics_xml = '<?xml version="1.0" encoding="utf-8" ?>\n<Defs>\n'
    addons_xml = '<?xml version="1.0" encoding="utf-8" ?>\n<Defs>\n'
    bionics_surgery_xml = '<?xml version="1.0" encoding="utf-8" ?>\n<Defs>\n'
    addons_surgery_xml = '<?xml version="1.0" encoding="utf-8" ?>\n<Defs>\n'
    hediffs_xml = '<?xml version="1.0" encoding="utf-8" ?>\n<Defs>\n'

    for bionic in bionics_list:
        bionics_xml += bionic.generate_thingdef()
        bionics_surgery_xml += bionic.generate_surgery_instruction()
        hediffs_xml += bionic.generate_hediffdef()
        bionics_count += 1  # Increment bionic count
        for addon in bionic.compatible_addons:
            addons_xml += addon.generate_thingdef()
            addons_surgery_xml += addon.generate_surgery_instruction()
            hediffs_xml += addon.generate_hediffdef()
            addons_count += 1  # Increment addon count

    bionics_xml += "</Defs>"
    addons_xml += "</Defs>"
    bionics_surgery_xml += "</Defs>"
    addons_surgery_xml += "</Defs>"
    hediffs_xml += "</Defs>"

    write_xml_file("Defs/ThingDefs_AstralTechBionics.xml", bionics_xml)
    write_xml_file("Defs/ThingDefs_AstralTechAddons.xml", addons_xml)
    write_xml_file("Defs/SurgeryInstructions_AstralTechBionics.xml", bionics_surgery_xml)
    write_xml_file("Defs/SurgeryInstructions_AstralTechAddons.xml", addons_surgery_xml)
    write_xml_file("Defs/HediffDefs_AstralTech.xml", hediffs_xml)

    # Copy the texture files
    bionics_texture_source = "assets/astral_bionics.png"
    bionics_texture_destination = "AstralTech/Textures/Things/Item/Health/AstralBionics.png"
    addons_texture_source = "assets/astral_addons.png"
    addons_texture_destination = "AstralTech/Textures/Things/Item/Health/AstralAddons.png"

    # Ensure the destination directories exist
    os.makedirs(os.path.dirname(bionics_texture_destination), exist_ok=True)
    os.makedirs(os.path.dirname(addons_texture_destination), exist_ok=True)

    # Copy the texture files
    shutil.copy2(bionics_texture_source, bionics_texture_destination)
    shutil.copy2(addons_texture_source, addons_texture_destination)

    # Copy the Steam presentation file
    source_file = "assets/presentation.md"
    destination_file = "AstralTech/About/PublishedFileId.txt"
    shutil.copy2(source_file, destination_file)

    # Copy the Steam Workshop image
    steam_image_source = "assets/steam.png"
    steam_image_destination = "AstralTech/About/Preview.png"
    shutil.copy2(steam_image_source, steam_image_destination)

    print(f"AstralTech Bionic Implants mod generated successfully with {bionics_count} bionics and {addons_count} addons.")
    print("Texture files and Steam assets copied successfully.")
    