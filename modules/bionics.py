from const import BODY_PARTS, VALID_STATS, VALID_CAPACITIES, ASTRALTECH_LORE

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
                "\t\t\t\t\t<postFactor>1.2</postFactor>\n"
                "\t\t\t\t</li>\n"
                "\t\t\t\t<li>\n"
                "\t\t\t\t\t<capacity>Moving</capacity>\n"
                "\t\t\t\t\t<postFactor>1.1</postFactor>\n"
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