import random


def use_potion(player, potion):
    if player.max_health - player.health <= potion.value:
        player.health = player.max_health
    else:
        player.health += potion.value


def regenerate_energy(player, reg_value):
    if player.max_energy - player.energy <= reg_value:
        player.energy = player.max_energy
    else:
        player.energy += reg_value


def calculate_attack(damage1, damage2, critical_attack, attack_speed, is_critical):
    critical_attack_chance = random.random()
    if critical_attack_chance < critical_attack:
        attack = int(random.randint(damage1, damage2) * attack_speed) * 2
        is_critical = True
    else:
        attack = int(random.randint(damage1, damage2) * attack_speed)
    return attack, is_critical


def calculate_block(block, is_attack_blocked):
    block_chance = random.random()
    if block_chance < block:
        is_attack_blocked = True
    return is_attack_blocked


def calculate_dodge(dodge, is_attack_dodged):
    dodge_chance = random.random()
    if dodge_chance < dodge:
        is_attack_dodged = True
    return is_attack_dodged


def enemy_attacks(enemy, player, is_critical_taken, is_attack_taken_blocked, is_attack_taken_dodged, enemy_rests, attack_taken):
    if enemy.energy <= 0:
        enemy_rests = True
        enemy.energy += 10
    else:
        attack_taken, is_critical_taken = calculate_attack(enemy.damage1, enemy.damage2, enemy.critical_attack, enemy.attack_speed, is_critical_taken)
        if player.block > 0:
            is_attack_taken_blocked = calculate_block(player.block, is_attack_taken_blocked)
        if player.dodge > 0:
            is_attack_taken_dodged = calculate_dodge(player.block, is_attack_taken_blocked)
        if not (is_attack_taken_blocked or is_attack_taken_dodged):
            player.health -= attack_taken
        enemy.energy -= 10
    return attack_taken, is_critical_taken, is_attack_taken_blocked, is_attack_taken_dodged, enemy_rests
