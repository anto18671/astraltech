import os

def write_xml_file(filename, content):
    relative_path = f"Astraltech/{filename}"
    os.makedirs(os.path.dirname(relative_path), exist_ok=True)
    with open(relative_path, "w", encoding='utf-8') as file:
        file.write(content)
    print(f"{relative_path} generated successfully.")

def generate_mod_metadata():
    return (
        """<?xml version="1.0" encoding="utf-8" ?>\n"""
        "<ModMetaData>\n"
        "\t<name>Astraltech Bionic Implants</name>\n"
        "\t<author>Anthony Therrien</author>\n"
        "\t<description>Adds new advanced bionic implants to RimWorld, pushing the boundaries of human enhancement with the mysterious Astraltech technology.</description>\n"
        "\t<packageId>AnthonyTherrien.AstraltechBionics</packageId>\n"
        "\t<supportedVersions>\n"
        "\t\t<li>1.5</li>\n"
        "\t</supportedVersions>\n"
        "</ModMetaData>"
    )

def generate_about_xml():
    return (
        """<?xml version="1.0" encoding="utf-8"?>\n"""
        "<ModMetaData>\n"
        "\t<name>Astraltech Bionic Implants</name>\n"
        "\t<author>Anthony Therrien</author>\n"
        "\t<url></url>\n"
        "\t<description>Astraltech Bionic Implants introduces a new tier of advanced bionics to RimWorld. These implants, developed by a mysterious faction from beyond known space, offer unprecedented enhancements to human capabilities. Each Astraltech implant pushes the boundaries of what's possible, granting users abilities that border on the supernatural. Upgrade your colonists with these cutting-edge implants and experience a new level of power in the RimWorld universe.</description>\n"
        "\t<packageId>AnthonyTherrien.AstraltechBionics</packageId>\n"
        "\t<supportedVersions>\n"
        "\t\t<li>1.5</li>\n"
        "\t</supportedVersions>\n"
        "</ModMetaData>"
    )

def generate_language_keys():
    return (
        """<?xml version="1.0" encoding="utf-8" ?>\n"""
        "<LanguageData>\n"
        "\t<AstraltechDescription>Astraltech is the next leap in bionic technology, far beyond even the mysterious Archotech devices. Developed in secret by an advanced faction from beyond the known stars, these implants were created for only the most elite individuals. They are not only functional but also imbued with seemingly supernatural capabilities that push the very limits of physical performance. No one knows the full extent of their capabilities, but their power is unmistakable.</AstraltechDescription>\n"
        "</LanguageData>"
    )