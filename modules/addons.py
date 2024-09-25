from const import VALID_STATS, VALID_CAPACITIES, ASTRALTECH_LORE

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