import xml.etree.ElementTree as ET
import xml.dom.minidom

class Backstory:
    def __init__(self, slot, title, def_name, title_short, base_desc, spawn_categories, skill_gains, work_disables=None):
        self.slot = slot
        self.title = title
        self.def_name = def_name
        self.title_short = title_short
        self.base_desc = base_desc
        self.spawn_categories = spawn_categories
        self.skill_gains = skill_gains
        self.work_disables = work_disables or []

    def generate_xml(self) -> str:
        root = ET.Element("BackstoryDef")
        
        ET.SubElement(root, "slot").text = self.slot
        ET.SubElement(root, "title").text = self.title
        ET.SubElement(root, "defName").text = self.def_name
        ET.SubElement(root, "titleShort").text = self.title_short
        ET.SubElement(root, "baseDesc").text = self.base_desc
        
        spawn_categories = ET.SubElement(root, "spawnCategories")
        for category in self.spawn_categories:
            ET.SubElement(spawn_categories, "li").text = category
        
        skill_gains = ET.SubElement(root, "skillGains")
        for skill, gain in self.skill_gains.items():
            ET.SubElement(skill_gains, skill).text = str(gain)
        
        if self.work_disables:
            work_disables = ET.SubElement(root, "workDisables")
            for disable in self.work_disables:
                ET.SubElement(work_disables, "li").text = disable
        
        # Convert to string and prettify
        xml_string = ET.tostring(root, encoding="unicode")
        pretty_xml = xml.dom.minidom.parseString(xml_string).toprettyxml(indent="  ")
        
        # Remove the first line containing the XML declaration
        return "\n".join(pretty_xml.split("\n")[1:])
        