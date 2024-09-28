from .utils import VALID_STATS, VALID_CAPACITIES, ASTRALTECH_LORE
import xml.etree.ElementTree as ET
import xml.dom.minidom

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

    def generate_xml_element(self, tag, text=None, attrib=None):
        """Helper function to generate XML element"""
        element = ET.Element(tag, attrib if attrib else {})
        if text:
            element.text = text
        return element

    def generate_thingdef(self):
        root = self.generate_xml_element("ThingDef", attrib={"ParentName": "BodyPartBionicBase"})
        
        root.append(self.generate_xml_element("defName", self.addon_name))
        root.append(self.generate_xml_element("label", self.label))
        root.append(self.generate_xml_element("description", self.description))
        root.append(self.generate_xml_element("techLevel", "Spacer"))
        root.append(self.generate_xml_element("thingClass", self.thing_class))

        graphic_data = self.generate_xml_element("graphicData")
        graphic_data.append(self.generate_xml_element("texPath", self.tex_path))
        graphic_data.append(self.generate_xml_element("graphicClass", "Graphic_Single"))
        root.append(graphic_data)

        stat_bases = self.generate_xml_element("statBases")
        stat_bases.append(self.generate_xml_element("MarketValue", str(self.market_value)))
        root.append(stat_bases)

        tech_hediffs_tags = self.generate_xml_element("techHediffsTags")
        tech_hediffs_tags.append(self.generate_xml_element("li", "Advanced"))
        root.append(tech_hediffs_tags)

        thing_set_maker_tags = self.generate_xml_element("thingSetMakerTags")
        thing_set_maker_tags.append(self.generate_xml_element("li", "RewardStandardLowFreq"))
        root.append(thing_set_maker_tags)

        description_hyperlinks = self.generate_xml_element("descriptionHyperlinks")
        description_hyperlinks.append(self.generate_xml_element("RecipeDef", f"Install_{self.addon_name}"))
        root.append(description_hyperlinks)

        cost_list = self.generate_xml_element("costList")
        cost_list.append(self.generate_xml_element("Plasteel", "10"))
        cost_list.append(self.generate_xml_element("ComponentSpacer", "3"))
        root.append(cost_list)

        comps = self.generate_xml_element("comps")
        comps.append(self.generate_xml_element("li", attrib={"Class": "CompProperties_Forbiddable"}))
        root.append(comps)

        # Convert to string and prettify
        xml_string = ET.tostring(root, encoding="unicode")
        pretty_xml = xml.dom.minidom.parseString(xml_string).toprettyxml(indent="  ")

        return "\n".join(pretty_xml.split("\n")[1:])

    def generate_surgery_instruction(self, races=["Human"]):
        root = self.generate_xml_element("RecipeDef", attrib={"ParentName": "SurgeryFlesh"})
        
        root.append(self.generate_xml_element("defName", f"Install_{self.addon_name}"))
        root.append(self.generate_xml_element("label", f"install {self.label.lower()}"))
        root.append(self.generate_xml_element("description", f"Install an {self.label.lower()}."))
        root.append(self.generate_xml_element("jobString", f"Installing {self.label.lower()}."))
        root.append(self.generate_xml_element("workerClass", "Recipe_InstallImplant"))
        root.append(self.generate_xml_element("anesthetize", "true"))
        root.append(self.generate_xml_element("workAmount", "4500"))
        root.append(self.generate_xml_element("surgerySuccessChanceFactor", "1.2"))

        skill_requirements = self.generate_xml_element("skillRequirements")
        skill_requirements.append(self.generate_xml_element("Medicine", "8"))
        root.append(skill_requirements)

        recipe_users = self.generate_xml_element("recipeUsers")
        for race in races:
            recipe_users.append(self.generate_xml_element("li", race))
        root.append(recipe_users)

        ingredients = self.generate_xml_element("ingredients")
        ingredient_1 = self.generate_xml_element("li")
        filter_1 = self.generate_xml_element("filter")
        categories_1 = self.generate_xml_element("categories")
        categories_1.append(self.generate_xml_element("li", "Medicine"))
        filter_1.append(categories_1)
        ingredient_1.append(filter_1)
        ingredient_1.append(self.generate_xml_element("count", "2"))
        ingredients.append(ingredient_1)

        ingredient_2 = self.generate_xml_element("li")
        filter_2 = self.generate_xml_element("filter")
        thing_defs = self.generate_xml_element("thingDefs")
        thing_defs.append(self.generate_xml_element("li", self.addon_name))
        filter_2.append(thing_defs)
        ingredient_2.append(filter_2)
        ingredient_2.append(self.generate_xml_element("count", "1"))
        ingredients.append(ingredient_2)

        root.append(ingredients)

        fixed_ingredient_filter = self.generate_xml_element("fixedIngredientFilter")
        fixed_categories = self.generate_xml_element("categories")
        fixed_categories.append(self.generate_xml_element("li", "Medicine"))
        fixed_ingredient_filter.append(fixed_categories)
        fixed_thing_defs = self.generate_xml_element("thingDefs")
        fixed_thing_defs.append(self.generate_xml_element("li", self.addon_name))
        fixed_ingredient_filter.append(fixed_thing_defs)
        root.append(fixed_ingredient_filter)

        applied_on_fixed_body_parts = self.generate_xml_element("appliedOnFixedBodyParts")
        applied_on_fixed_body_parts.append(self.generate_xml_element("li", self.body_part))
        root.append(applied_on_fixed_body_parts)

        root.append(self.generate_xml_element("addsHediff", f"{self.addon_name}_hediff"))

        # Convert to string and prettify
        xml_string = ET.tostring(root, encoding="unicode")
        pretty_xml = xml.dom.minidom.parseString(xml_string).toprettyxml(indent="  ")

        return "\n".join(pretty_xml.split("\n")[1:])

    def generate_hediffdef(self):
        root = self.generate_xml_element("HediffDef", attrib={"ParentName": "AddedBodyPartBase"})
        
        root.append(self.generate_xml_element("defName", f"{self.addon_name}_hediff"))
        root.append(self.generate_xml_element("label", self.label))
        root.append(self.generate_xml_element("labelNoun", self.label))
        root.append(self.generate_xml_element("description", self.description))

        description_hyperlinks = self.generate_xml_element("descriptionHyperlinks")
        description_hyperlinks.append(self.generate_xml_element("ThingDef", self.addon_name))
        root.append(description_hyperlinks)

        root.append(self.generate_xml_element("spawnThingOnRemoved", self.addon_name))
        root.append(self.generate_xml_element("hediffClass", "Hediff_Implant"))

        root.append(self.generate_xml_element("isBad", "false"))

        added_part_props = self.generate_xml_element("addedPartProps")
        added_part_props.append(self.generate_xml_element("partEfficiency", str(self.part_efficiency)))
        root.append(added_part_props)

        stages = self.generate_xml_element("stages")
        stage = self.generate_xml_element("li")
        
        if self.capacity_factors or self.capacity_offsets:
            cap_mods = self.generate_xml_element("capMods")
            for stat in self.capacity_factors + self.capacity_offsets:
                cap_mod = self.generate_xml_element("li")
                cap_mod.append(self.generate_xml_element("capacity", stat.name))
                cap_mod.append(self.generate_xml_element("postFactor" if stat.mod_type == "factor" else "offset", str(stat.value)))
                cap_mods.append(cap_mod)
            stage.append(cap_mods)

        if self.stat_offsets:
            stat_offsets = self.generate_xml_element("statOffsets")
            for stat in self.stat_offsets:
                stat_offsets.append(self.generate_xml_element(stat.name, str(stat.value)))
            stage.append(stat_offsets)

        if self.stat_factors:
            stat_factors = self.generate_xml_element("statFactors")
            for stat in self.stat_factors:
                stat_factors.append(self.generate_xml_element(stat.name, str(stat.value)))
            stage.append(stat_factors)

        stages.append(stage)
        root.append(stages)

        # Convert to string and prettify
        xml_string = ET.tostring(root, encoding="unicode")
        pretty_xml = xml.dom.minidom.parseString(xml_string).toprettyxml(indent="  ")

        return "\n".join(pretty_xml.split("\n")[1:])
