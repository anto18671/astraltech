VALID_STATS = [
    'WorkSpeedGlobal', 'ShootingAccuracyPawn', 'MeleeHitChance', 'MoveSpeed', 'AimingDelayFactor',
    'PainShockThreshold', 'GlobalLearningFactor', 'MedicalTendSpeed',
    'MedicalTendQuality', 'MedicalSurgerySuccessChance', 'ResearchSpeedFactor', 'SocialImpact',
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

VALID_CAPACITIES = [
    'Consciousness', 'Sight', 'Hearing', 'Moving', 'Manipulation', 'Talking', 'Eating', 'Breathing',
    'BloodPumping', 'BloodFiltration', 'Metabolism', 'Immunity'
]

class Stat:
    def __init__(self, name, value, stat_type='stat', mod_type='factor'):
        self.name = name
        self.value = value
        self.stat_type = stat_type
        self.mod_type = mod_type

