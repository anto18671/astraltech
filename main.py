from modules.utils import write_xml_file, generate_mod_metadata, generate_about_xml, generate_language_keys
from modules.backstory import Backstory
from modules.bionics import Bionic
from modules.addons import Addon
from modules.stats import Stat
import shutil
import os

# Define a list of Astraltech-inspired backstories
adult_backstories = [
    Backstory(
        slot="Adulthood",
        title="Astraltech Salvager",
        def_name="AST_Salvager",
        title_short="Salvager",
        base_desc="[PAWN_nameDef] made a living salvaging parts from destroyed ships, many of which were rumored to contain traces of Astraltech technology. Though [PAWN_nameDef] could never fully verify their origin, the strange, advanced components were unlike anything [PAWN_nameDef] had ever seen, and their value on the black market was undeniable.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Crafting": 8, "Intellectual": 4, "Shooting": 3},
        work_disables=["Social"]
    ),
    Backstory(
        slot="Adulthood",
        title="Bionic Research Assistant",
        def_name="AST_ResearchAssistant",
        title_short="Research Assistant",
        base_desc="[PAWN_nameDef] worked in a clandestine lab dedicated to reverse-engineering advanced technology, some of which was whispered to be based on Astraltech. Though the inner workings of these mysterious devices were closely guarded, [PAWN_nameDef] became adept at piecing together their basic functions, always aware that there was more beneath the surface.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Intellectual": 6, "Medicine": 5, "Crafting": 3},
    ),
    Backstory(
        slot="Adulthood",
        title="Corporate Security Guard",
        def_name="AST_CorpSecurity",
        title_short="Security Guard",
        base_desc="Hired to guard a highly secretive facility believed to be researching technology inspired by Astraltech, [PAWN_nameDef] had no access to the advanced tech but heard countless rumors of its incredible power. [PAWN_nameDef] trained extensively, knowing that failure to protect the site could have dire consequences.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Shooting": 7, "Melee": 5, "Social": 2},
    ),
    Backstory(
        slot="Adulthood",
        title="Bionic Sales Representative",
        def_name="AST_SalesRep",
        title_short="Sales Rep",
        base_desc="[PAWN_nameDef] sold products that incorporated speculative technology inspired by Astraltech. Though [PAWN_nameDef] never fully understood the mechanics of the devices, the allure of Astraltech legends made every sale easier.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Social": 8, "Artistic": 4, "Intellectual": 2}
    ),
    Backstory(
        slot="Adulthood",
        title="Astraltech Artifact Dealer",
        def_name="AST_ArtifactDealer",
        title_short="Artifact Dealer",
        base_desc="[PAWN_nameDef] traded in rare, mysterious objects believed to be connected to Astraltech. While many of these items' origins were dubious, their extraordinary craftsmanship and rumored abilities attracted wealthy buyers from all over the galaxy.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Social": 7, "Crafting": 4, "Intellectual": 4},
        work_disables=["Caring"]
    ),
    Backstory(
        slot="Adulthood",
        title="Astraltech Cleanup Crew",
        def_name="AST_CleanupCrew",
        title_short="Cleaner",
        base_desc="[PAWN_nameDef] worked on cleanup crews following skirmishes involving advanced technology that many believed to be of Astraltech origin. [PAWN_nameDef] had seen the aftermath of battles involving such tech firsthand, but was never allowed to inspect the wreckage closely.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Construction": 6, "Shooting": 4, "Melee": 2},
        work_disables=["Social"]
    ),
    Backstory(
        slot="Adulthood",
        title="Bionic Conspiracy Theorist",
        def_name="AST_ConspiracyTheorist",
        title_short="Theorist",
        base_desc="Convinced that Astraltech was pulling the strings behind major world events, [PAWN_nameDef] spent years gathering information and spreading conspiracy theories. Though lacking hard evidence, [PAWN_nameDef] became adept at connecting dots where few others dared look.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Intellectual": 7, "Social": 5, "Artistic": 2},
    ),
    Backstory(
        slot="Adulthood",
        title="Underground Mechanic",
        def_name="AST_UndergroundMechanic",
        title_short="Mechanic",
        base_desc="[PAWN_nameDef] ran a secret workshop specializing in modifying and repairing black market bionics. Much of the tech [PAWN_nameDef] worked on was rumored to be derived from Astraltech, though [PAWN_nameDef] never saw definitive proof.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Crafting": 8, "Intellectual": 3, "Construction": 3}
    ),
    Backstory(
        slot="Adulthood",
        title="Military Analyst",
        def_name="AST_MilitaryAnalyst",
        title_short="Analyst",
        base_desc="[PAWN_nameDef] studied combat footage of battles where highly advanced bionic soldiers were used, some claiming they were equipped with Astraltech-enhanced weaponry. [PAWN_nameDef] became an expert in predicting the future of warfare, though [PAWN_nameDef] had no direct combat experience.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Intellectual": 7, "Shooting": 4, "Social": 3}
    ),
    Backstory(
        slot="Adulthood",
        title="Bionic Trial Participant",
        def_name="AST_TrialParticipant",
        title_short="Trial Participant",
        base_desc="[PAWN_nameDef] participated in human trials for experimental bionics, which were rumored to incorporate technology inspired by Astraltech. Though the trials were shrouded in secrecy, [PAWN_nameDef] experienced firsthand the power and potential of these devices.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Medicine": 5, "Intellectual": 4, "Crafting": 2},
    ),
    Backstory(
        slot="Adulthood",
        title="Bionic Instructor",
        def_name="AST_BionicInstructor",
        title_short="Instructor",
        base_desc="[PAWN_nameDef] taught bionics engineering at a technical school, though much of the curriculum was based on theoretical knowledge derived from rumors about Astraltech. [PAWN_nameDef] was highly skilled but had never worked with authentic Astraltech devices.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Intellectual": 8, "Social": 5, "Crafting": 3},
    ),
    Backstory(
        slot="Adulthood",
        title="Smuggler's Scout",
        def_name="AST_SmugglersScout",
        title_short="Scout",
        base_desc="[PAWN_nameDef] worked for a smuggling ring dealing in illicit bionics, many of which were rumored to have Astraltech origins. [PAWN_nameDef] scouted routes and helped avoid detection, always aware that the stakes were high when dealing with such high-value tech.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Shooting": 5, "Melee": 4, "Social": 3},
        work_disables=["Caring"]
    ),
    Backstory(
        slot="Adulthood",
        title="Astraltech Bounty Hunter",
        def_name="AST_BountyHunter",
        title_short="Bounty Hunter",
        base_desc="[PAWN_nameDef] made a living hunting down criminals who dealt in stolen bionics, including those suspected of originating from Astraltech. [PAWN_nameDef] relied on a mix of combat skills and knowledge of underground markets to track targets.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Shooting": 6, "Melee": 5, "Social": 3},
    ),
    Backstory(
        slot="Adulthood",
        title="Astraltech Test Engineer",
        def_name="AST_TestEngineer",
        title_short="Test Engineer",
        base_desc="[PAWN_nameDef] tested prototype bionics, some of which were rumored to be based on Astraltech technology. Though these devices often malfunctioned or fell short of expectations, [PAWN_nameDef] became adept at identifying weaknesses in design.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Crafting": 7, "Intellectual": 4, "Medicine": 3},
    ),
    Backstory(
        slot="Adulthood",
        title="Astraltech Black Market Surgeon",
        def_name="AST_BlackMarketSurgeon",
        title_short="Surgeon",
        base_desc="[PAWN_nameDef] performed illegal bionic surgeries in underground clinics. [PAWN_nameDef] became highly skilled at installing and repairing black-market bionics, including those rumored to have Astraltech origins.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Medicine": 9, "Crafting": 4, "Social": 2},
    ),
    Backstory(
        slot="Adulthood",
        title="Astraltech Hacker",
        def_name="AST_Hacker",
        title_short="Hacker",
        base_desc="[PAWN_nameDef] specialized in breaching highly secure systems, often believed to contain data on Astraltech technology. While never confirmed, [PAWN_nameDef]'s work pushed the boundaries of what was thought possible with conventional tech.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Intellectual": 8, "Crafting": 5, "Social": 2},
    )
]

# Define a list of Astraltech-inspired child backstories
child_backstories = [
    Backstory(
        slot="Childhood",
        title="Astraltech Warehouse Child",
        def_name="AST_WarehouseChild",
        title_short="Warehouse Worker",
        base_desc="Growing up in a factory district where Astraltech parts were stored and shipped, [PAWN_nameDef] often snuck into crates and learned a lot about the tech through observation.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Crafting": 3, "Intellectual": 1},
    ),
    Backstory(
        slot="Childhood",
        title="Bionic Trader's Assistant",
        def_name="AST_TraderAssistant",
        title_short="Trader's Assistant",
        base_desc="[PAWN_nameDef] grew up assisting a traveling merchant who dealt in tech goods, including parts rumored to come from Astraltech. [PAWN_nameDef] learned how to identify valuable items and haggle effectively.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Social": 3, "Crafting": 2},
    ),
    Backstory(
        slot="Childhood",
        title="Astraltech Refugee",
        def_name="AST_RefugeeChild",
        title_short="Refugee",
        base_desc="Forced to flee home when Astraltech weapons were deployed in a nearby conflict, [PAWN_nameDef] learned resilience and became adept at surviving under harsh conditions.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Melee": 2, "Shooting": 1},
    ),
    Backstory(
        slot="Childhood",
        title="Astraltech Junkyard Scavenger",
        def_name="AST_JunkyardScavenger",
        title_short="Scavenger",
        base_desc="Growing up in a junkyard filled with discarded tech, including remnants of Astraltech products, [PAWN_nameDef] spent days sifting through debris, finding useful parts to sell.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Crafting": 4, "Intellectual": 2},
    ),
    Backstory(
        slot="Childhood",
        title="Bionic Research Intern",
        def_name="AST_ResearchIntern",
        title_short="Intern",
        base_desc="[PAWN_nameDef] was an intern at a laboratory researching Astraltech-inspired bionics. Although young, [PAWN_nameDef] was exposed to complex theories and was tasked with minor technical responsibilities.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Intellectual": 3, "Crafting": 2},
    ),
    Backstory(
        slot="Childhood",
        title="Astraltech War Orphan",
        def_name="AST_WarOrphan",
        title_short="Orphan",
        base_desc="[PAWN_nameDef]'s parents were killed in a battle involving Astraltech forces. Orphaned at a young age, [PAWN_nameDef] grew up in a war-torn environment, developing a strong sense of survival.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Melee": 2, "Shooting": 2},
    ),
    Backstory(
        slot="Childhood",
        title="Bionic Scrap Dealer's Kid",
        def_name="AST_ScrapDealersKid",
        title_short="Scrap Dealer's Kid",
        base_desc="Growing up in a family scrap business that often dealt in old bionic parts, [PAWN_nameDef] learned how to identify useful components and repair basic machinery.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Crafting": 3, "Social": 1},
    ),
    Backstory(
        slot="Childhood",
        title="Astraltech Technician's Child",
        def_name="AST_TechnicianChild",
        title_short="Technician's Child",
        base_desc="The child of a technician who worked on non-classified Astraltech technologies, [PAWN_nameDef] often watched their parent at work and learned a few things about machines.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Crafting": 3, "Intellectual": 2},
    ),
    Backstory(
        slot="Childhood",
        title="Astraltech Museum Curator's Child",
        def_name="AST_MuseumCuratorsChild",
        title_short="Curator's Child",
        base_desc="Raised in an academic environment, [PAWN_nameDef]'s parent was a curator at a museum displaying historical technology, including artifacts believed to come from Astraltech.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Intellectual": 4, "Artistic": 2},
    ),
    Backstory(
        slot="Childhood",
        title="Astraltech Freelancer's Apprentice",
        def_name="AST_FreelancersApprentice",
        title_short="Apprentice",
        base_desc="[PAWN_nameDef] was apprenticed to a freelancer who worked on projects involving tech inspired by Astraltech. [PAWN_nameDef] picked up practical skills and a love of tinkering.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Crafting": 3, "Medicine": 1},
    ),
    Backstory(
        slot="Childhood",
        title="Astraltech Salvage Kid",
        def_name="AST_SalvageKid",
        title_short="Salvage Kid",
        base_desc="[PAWN_nameDef] grew up in a salvage community where Astraltech debris was highly prized. [PAWN_nameDef] learned early on how to find value in scraps and became resourceful in survival.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Crafting": 4, "Shooting": 2},
    ),
    Backstory(
        slot="Childhood",
        title="Astraltech Collector's Heir",
        def_name="AST_CollectorsHeir",
        title_short="Collector's Heir",
        base_desc="[PAWN_nameDef] was born into wealth as the child of a collector obsessed with Astraltech relics. Their upbringing was filled with stories of legendary bionics and forbidden tech.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Social": 3, "Intellectual": 3},
    ),
    Backstory(
        slot="Childhood",
        title="Astraltech Robotics Enthusiast",
        def_name="AST_RoboticsEnthusiast",
        title_short="Robotics Enthusiast",
        base_desc="[PAWN_nameDef] grew up fascinated by robots built with Astraltech parts. [PAWN_nameDef] spent hours tinkering with machines, learning as much as possible from old manuals and scavenged parts.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Crafting": 3, "Intellectual": 3},
    ),
    Backstory(
        slot="Childhood",
        title="Astraltech Street Urchin",
        def_name="AST_StreetUrchin",
        title_short="Street Urchin",
        base_desc="[PAWN_nameDef] grew up on the streets, surviving by stealing and selling Astraltech scraps. [PAWN_nameDef] became adept at evading the law and using the tech to their advantage.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Social": 2, "Melee": 3},
    ),
    Backstory(
        slot="Childhood",
        title="Astraltech Experimental Subject",
        def_name="AST_ExperimentalSubject",
        title_short="Experimental Subject",
        base_desc="[PAWN_nameDef] was taken in by an experimental lab as a child and subjected to minor tests involving Astraltech prototypes. The experience left [PAWN_nameDef] with a deep curiosity about technology and its limits.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Intellectual": 3, "Crafting": 1},
    ),
    Backstory(
        slot="Childhood",
        title="Astraltech Bionic Prodigy",
        def_name="AST_BionicProdigy",
        title_short="Bionic Prodigy",
        base_desc="[PAWN_nameDef] displayed an exceptional aptitude for understanding complex machines at a young age. [PAWN_nameDef] often helped older engineers with repairs and tinkered with basic bionic devices.",
        spawn_categories=["Astraltech Impacted"],
        skill_gains={"Crafting": 4, "Intellectual": 3},
    )
]
        
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
            Stat("ArmorRating_Sharp", 0.1, stat_type='stat', mod_type='offset'),
            Stat("ArmorRating_Blunt", 0.2, stat_type='stat', mod_type='offset'),
            Stat("PawnBeauty", 4.0, stat_type='stat', mod_type='offset'),
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
            Stat("Consciousness", 4.5, stat_type='capacity', mod_type='offset'),
            Stat("Sight", 0.75, stat_type='capacity', mod_type='offset'),
            Stat("Hearing", 0.75, stat_type='capacity', mod_type='offset'),
            Stat("Manipulation", 0.2, stat_type='capacity', mod_type='offset'),
            Stat("MeleeHitChance", 0.75, stat_type='stat', mod_type='offset'),
            Stat("ShootingAccuracyPawn", 1.25, stat_type='stat', mod_type='offset'),
            Stat("GlobalLearningFactor", 3.0, stat_type='stat', mod_type='offset'),
            Stat("MedicalOperationSpeed", 0.2, stat_type='stat', mod_type='offset'),
            Stat("MedicalTendSpeed", 0.2, stat_type='stat', mod_type='offset'),
            Stat("MedicalTendQuality", 0.6, stat_type='stat', mod_type='offset'),
            Stat("MedicalSurgerySuccessChance", 0.6, stat_type='stat', mod_type='offset'),
            Stat("MeditationFocusGain", 0.8, stat_type='stat', mod_type='offset'),
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
                    Stat("Consciousness", 0.75, stat_type='capacity', mod_type='offset'),
                    Stat("WorkSpeedGlobal", 0.1, stat_type='stat', mod_type='offset'),
                    Stat("GlobalLearningFactor", 1.0, stat_type='stat', mod_type='offset'),
                    Stat("ResearchSpeed", 1.0, stat_type='stat', mod_type='offset'),
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
                    Stat("Consciousness", 0.5, stat_type='capacity', mod_type='offset'),
                    Stat("WorkSpeedGlobal", 0.1, stat_type='stat', mod_type='offset'),
                    Stat("Manipulation", 0.1, stat_type='capacity', mod_type='offset'),
                    Stat("GlobalLearningFactor", 0.2, stat_type='stat', mod_type='offset'),
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
                    Stat("Consciousness", 0.5, stat_type='capacity', mod_type='offset'),
                    Stat("GlobalLearningFactor", 0.5, stat_type='stat', mod_type='offset'),
                    Stat("WorkSpeedGlobal", 0.1, stat_type='stat', mod_type='offset'),
                    Stat("MeleeHitChance", 0.4, stat_type='stat', mod_type='offset'),
                    Stat("ShootingAccuracyPawn", 0.25, stat_type='stat', mod_type='offset'),
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
            Stat("Sight", 1.75, stat_type='capacity', mod_type='offset'),
            Stat("ShootingAccuracyPawn", 1.0, stat_type='stat', mod_type='offset'),
            Stat("Manipulation", 0.1, stat_type='capacity', mod_type='offset'),
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
                    Stat("Sight", 0.5, stat_type='capacity', mod_type='offset'),
                    Stat("ShootingAccuracyPawn", 0.4, stat_type='stat', mod_type='offset'),
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
                    Stat("Sight", 0.5, stat_type='capacity', mod_type='offset'),
                    Stat("MeleeHitChance", 0.8, stat_type='stat', mod_type='offset'),
                    Stat("Manipulation", 0.1, stat_type='capacity', mod_type='offset'),
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
            Stat("Hearing", 1.75, stat_type='capacity', mod_type='offset'),
            Stat("ShootingAccuracyPawn", 0.2, stat_type='stat', mod_type='offset'),
            Stat("NegotiationAbility", 0.2, stat_type='stat', mod_type='offset'),
            Stat("SocialImpact", 0.1, stat_type='stat', mod_type='offset'),
            Stat("MeleeHitChance", 0.1, stat_type='stat', mod_type='offset'),
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
                    Stat("Hearing", 0.4, stat_type='capacity', mod_type='offset'),
                    Stat("ShootingAccuracyPawn", 0.1, stat_type='stat', mod_type='offset'),
                    Stat("MeleeHitChance", 0.1, stat_type='stat', mod_type='offset'),
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
                    Stat("Hearing", 0.2, stat_type='capacity', mod_type='offset'),
                    Stat("MeleeHitChance", 0.1, stat_type='stat', mod_type='offset'),
                    Stat("ShootingAccuracyPawn", 0.1, stat_type='stat', mod_type='offset'),
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
                    Stat("Hearing", 0.2, stat_type='capacity', mod_type='offset'),
                    Stat("Sight", 0.1, stat_type='capacity', mod_type='offset'),
                    Stat("MeleeDodgeChance", 0.1, stat_type='stat', mod_type='offset'),
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
            Stat("SocialImpact", 0.25, stat_type='stat', mod_type='offset'),
            Stat("FoodPoisonChance", -0.5, stat_type='stat', mod_type='offset'),
            Stat("Breathing", 0.25, stat_type='capacity', mod_type='offset'),
        ]
    ),
    Bionic(
        bionic_name="Astraltech Jaw",
        label="Astraltech Jaw",
        description=(
            "The Astraltech Jaw is a pinnacle of oral enhancement, granting its user unparalleled speech capabilities. "
            "It provides flawless articulation in any language, enhanced persuasive abilities."
        ),
        part_efficiency=1.25,
        market_value=20800,
        mass=0.8,
        body_part="Jaw",
        additional_stats=[
            Stat("PawnBeauty", 1.0, stat_type='stat', mod_type='offset'),
            Stat("SocialImpact", 0.25, stat_type='stat', mod_type='offset'),
            Stat("NegotiationAbility", 0.25, stat_type='stat', mod_type='offset'),
            Stat("TradePriceImprovement", 0.1, stat_type='stat', mod_type='offset'),
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
            Stat("ArmorRating_Sharp", 0.1, stat_type='stat', mod_type='offset'),
            Stat("Manipulation", 0.1, stat_type='capacity', mod_type='offset'),
            Stat("MeleeDodgeChance", 0.2, stat_type='stat', mod_type='offset'),
            Stat("Breathing", 0.25, stat_type='capacity', mod_type='offset'),
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
            Stat("Manipulation", 1.0, stat_type='capacity', mod_type='offset'),
            Stat("WorkSpeedGlobal", 0.2, stat_type='stat', mod_type='offset'),
            Stat("ShootingAccuracyPawn", 0.6, stat_type='stat', mod_type='offset'),
            Stat("MedicalOperationSpeed", 0.3, stat_type='stat', mod_type='offset'),
            Stat("MedicalTendSpeed", 0.3, stat_type='stat', mod_type='offset'),
            Stat("MedicalTendQuality", 0.3, stat_type='stat', mod_type='offset'),
            Stat("MedicalSurgerySuccessChance", 0.3, stat_type='stat', mod_type='offset'),
            Stat("MeleeHitChance", 0.5, stat_type='stat', mod_type='offset'),
            Stat("ConstructionSpeed", 0.25, stat_type='stat', mod_type='offset'),
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
                    Stat("Manipulation", 0.3, stat_type='capacity', mod_type='offset'),
                    Stat("MeleeDPS", 0.2, stat_type='stat', mod_type='offset'),
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
            Stat("Moving", 0.6, stat_type='capacity', mod_type='offset'),
            Stat("Manipulation", 0.4, stat_type='capacity', mod_type='offset'),
            Stat("MeleeDodgeChance", 1.0, stat_type='stat', mod_type='offset'),
            Stat("Consciousness", 0.2, stat_type='capacity', mod_type='offset'),
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
                    Stat("Manipulation", 0.1, stat_type='capacity', mod_type='offset'),
                    Stat("PawnBeauty", 1.0, stat_type='stat', mod_type='offset'),
                    Stat("SocialImpact", 0.25, stat_type='stat', mod_type='offset'),
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
                    Stat("Manipulation", 0.1, stat_type='capacity', mod_type='offset'),
                    Stat("ShootingAccuracyPawn", 0.5, stat_type='stat', mod_type='offset'),
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
                    Stat("Moving", 0.2, stat_type='capacity', mod_type='offset'),
                    Stat("MeleeDodgeChance", 0.5, stat_type='stat', mod_type='offset'),
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
        market_value=22600,
        mass=5,
        body_part="Ribcage",
        additional_stats=[
            Stat("ArmorRating_Blunt", 0.2, stat_type='stat', mod_type='offset'),
            Stat("Breathing", 0.5, stat_type='capacity', mod_type='offset'),
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
            Stat("ArmorRating_Sharp", 0.1, stat_type='stat', mod_type='offset'),
            Stat("ArmorRating_Blunt", 0.2, stat_type='stat', mod_type='offset'),
            Stat("BloodPumping", 0.2, stat_type='capacity', mod_type='offset'),
            Stat("Moving", 0.4, stat_type='capacity', mod_type='offset'),
            Stat("Manipulation", 0.25, stat_type='capacity', mod_type='offset'),
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
                    Stat("ArmorRating_Sharp", 0.2, stat_type='stat', mod_type='offset'),
                    Stat("ArmorRating_Blunt", 0.2, stat_type='stat', mod_type='offset'),
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
                    Stat("Moving", 0.25, stat_type='capacity', mod_type='offset'),
                    Stat("Manipulation", 0.25, stat_type='capacity', mod_type='offset'),
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
                    Stat("ArmorRating_Blunt", 0.2, stat_type='stat', mod_type='offset'),
                    Stat("MeleeDPS", 0.1, stat_type='stat', mod_type='offset'),
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
                    Stat("Moving", 0.2, stat_type='capacity', mod_type='offset'),
                    Stat("Consciousness", 0.1, stat_type='capacity', mod_type='offset'),
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
                    Stat("ArmorRating_Sharp", 0.1, stat_type='stat', mod_type='offset'),
                    Stat("ArmorRating_Blunt", 0.1, stat_type='stat', mod_type='offset'),
                    Stat("MeleeDPS", 0.1, stat_type='stat', mod_type='offset'),
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
                    Stat("PawnBeauty", 2.0, stat_type='stat', mod_type='offset'),
                    Stat("SocialImpact", 0.3, stat_type='stat', mod_type='offset'),
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
                    Stat("ArmorRating_Sharp", 0.1, stat_type='stat', mod_type='offset'),
                    Stat("PawnBeauty", 2.0, stat_type='stat', mod_type='offset'),
                    Stat("SocialImpact", 0.3, stat_type='stat', mod_type='offset'),
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
            Stat("BloodPumping", 1.5, stat_type='capacity', mod_type='offset'),
            Stat("Moving", 0.2, stat_type='capacity', mod_type='offset'),
            Stat("Consciousness", 0.2, stat_type='capacity', mod_type='offset'),
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
                    Stat("BloodPumping", 0.25, stat_type='capacity', mod_type='offset'),
                    Stat("Moving", 0.3, stat_type='capacity', mod_type='offset'),
                    Stat("Consciousness", 0.1, stat_type='capacity', mod_type='offset'),
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
            Stat("Breathing", 1.5, stat_type='capacity', mod_type='offset'),
            Stat("BloodPumping", 0.1, stat_type='capacity', mod_type='offset'),
            Stat("Moving", 0.5, stat_type='capacity', mod_type='offset'),
            Stat("Consciousness", 0.05, stat_type='capacity', mod_type='offset'),
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
            Stat("BloodFiltration", 1.0, stat_type='capacity', mod_type='offset'),
            Stat("Consciousness", 0.05, stat_type='capacity', mod_type='offset'),
            Stat("Breathing", 0.2, stat_type='capacity', mod_type='offset'),
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
            Stat("BloodFiltration", 2.25, stat_type='capacity', mod_type='offset'),
            Stat("Consciousness", 0.1, stat_type='capacity', mod_type='offset'),
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
            Stat("MaxNutrition", 0.5, stat_type='stat', mod_type='offset'),
            Stat("Consciousness", 0.05, stat_type='capacity', mod_type='offset'),
        ],
        compatible_addons=[
            Addon(
                addon_name="AstraltechMetabolicOptimizer",
                label="Astraltech Metabolic Optimizer",
                description=(
                    "The Astraltech Metabolic Optimizer pushes the stomach's capabilities to near-magical levels. "
                    "This addon allows the user to extract maximum energy from minimal food, virtually eliminating fatigue and granting seemingly limitless endurance."
                ),
                market_value=18800,
                additional_stats=[
                    Stat("BloodFiltration", 0.5, stat_type='capacity', mod_type='offset'),
                    Stat("Consciousness", 0.05, stat_type='capacity', mod_type='offset'),
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
            Stat("Moving", 0.25, stat_type='capacity', mod_type='offset'),
            Stat("MeleeHitChance", 0.25, stat_type='stat', mod_type='offset'),
            Stat("MeleeDodgeChance", 0.2, stat_type='stat', mod_type='offset'),
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
            Stat("Moving", 0.8, stat_type='capacity', mod_type='offset'),
            Stat("MeleeDodgeChance", 0.2, stat_type='stat', mod_type='offset'),
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
                    Stat("Moving", 0.25, stat_type='capacity', mod_type='offset'),
                    Stat("MeleeDodgeChance", 0.1, stat_type='stat', mod_type='offset'),
                ]
            ),
        ]
    ),
]

# Creating multiple Bionic and Addon objects
if __name__ == "__main__":
    # Check if the folder exists, then delete it
    if os.path.exists("Astraltech/"):
        shutil.rmtree("Astraltech/")

    # Generate mod structure and files
    write_xml_file("About/PublishedFileId.xml", generate_mod_metadata())
    write_xml_file("About/About.xml", generate_about_xml())
    write_xml_file("Languages/English/Keyed/Astraltech_Keys.xml", generate_language_keys())
    
    # Initialize counters
    adult_backstory_count = 0
    child_backstory_count = 0
    
    # Generate XML content for adult backstories
    adult_xml_content = '<?xml version="1.0" encoding="utf-8"?>\n<Defs>\n'
    for backstory in adult_backstories:
        adult_backstory_count += 1
        adult_xml_content += backstory.generate_xml() + "\n"
    adult_xml_content += "</Defs>"
    
    # Write the adult backstories to a separate XML file
    write_xml_file("Defs/AstraltechAdultBackstories.xml", adult_xml_content)

    # Generate XML content for child backstories
    child_xml_content = '<?xml version="1.0" encoding="utf-8"?>\n<Defs>\n'
    for backstory in child_backstories:
        child_backstory_count += 1
        child_xml_content += backstory.generate_xml() + "\n"
    child_xml_content += "</Defs>"
    
    # Write the child backstories to a separate XML file
    write_xml_file("Defs/AstraltechChildBackstories.xml", child_xml_content)
    
    # Print the number of backstories
    print(f"Generated successfully {adult_backstory_count} adult backstories and {child_backstory_count} child backstories.")

    # Initialize counters
    bionics_count = 0
    addons_count = 0

    # Generate ThingDefs for bionics and addons
    bionics_xml = '<?xml version="1.0" encoding="utf-8" ?>\n<Defs>\n'
    addons_xml = '<?xml version="1.0" encoding="utf-8" ?>\n<Defs>\n'
    bionics_surgery_xml = '<?xml version="1.0" encoding="utf-8" ?>\n<Defs>\n'
    addons_surgery_xml = '<?xml version="1.0" encoding="utf-8" ?>\n<Defs>\n'
    bionics_hediffs_xml = '<?xml version="1.0" encoding="utf-8" ?>\n<Defs>\n'
    addons_hediffs_xml = '<?xml version="1.0" encoding="utf-8" ?>\n<Defs>\n'

    # Generate XML content for bionics and addons
    for bionic in bionics_list:
        bionics_xml += bionic.generate_thingdef()
        bionics_surgery_xml += bionic.generate_surgery_instruction()
        bionics_hediffs_xml += bionic.generate_hediffdef()
        bionics_count += 1
        for addon in bionic.compatible_addons:
            addons_xml += addon.generate_thingdef()
            addons_surgery_xml += addon.generate_surgery_instruction()
            addons_hediffs_xml += addon.generate_hediffdef()
            addons_count += 1

    # Close the XML content
    bionics_xml += "</Defs>"
    addons_xml += "</Defs>"
    bionics_surgery_xml += "</Defs>"
    addons_surgery_xml += "</Defs>"
    bionics_hediffs_xml += "</Defs>"
    addons_hediffs_xml += "</Defs>"

    # Write the bionics and addons to separate XML files
    write_xml_file("Defs/ThingDefs_AstraltechBionics.xml", bionics_xml)
    write_xml_file("Defs/ThingDefs_AstraltechAddons.xml", addons_xml)
    write_xml_file("Defs/SurgeryInstructions_AstraltechBionics.xml", bionics_surgery_xml)
    write_xml_file("Defs/SurgeryInstructions_AstraltechAddons.xml", addons_surgery_xml)
    write_xml_file("Defs/HediffDefs_AstraltechBionics.xml", bionics_hediffs_xml)
    write_xml_file("Defs/HediffDefs_AstraltechAddons.xml", addons_hediffs_xml)

    # Copy the texture files
    bionics_texture_source = "assets/astral_bionics.png"
    bionics_texture_destination = "Astraltech/Textures/Things/Item/Health/AstralBionics.png"
    addons_texture_source = "assets/astral_addons.png"
    addons_texture_destination = "Astraltech/Textures/Things/Item/Health/AstralAddons.png"

    # Ensure the destination directories exist
    os.makedirs(os.path.dirname(bionics_texture_destination), exist_ok=True)
    os.makedirs(os.path.dirname(addons_texture_destination), exist_ok=True)

    # Copy the texture files
    shutil.copy2(bionics_texture_source, bionics_texture_destination)
    shutil.copy2(addons_texture_source, addons_texture_destination)

    # Copy the Steam Workshop image
    steam_image_source = "assets/steam.png"
    steam_image_destination = "Astraltech/About/Preview.png"
    shutil.copy2(steam_image_source, steam_image_destination)

    print(f"Astraltech Bionic Implants mod generated successfully with {bionics_count} bionics and {addons_count} addons.")
    print("Texture files and Steam assets copied successfully.")
    