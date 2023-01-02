def use_potion(player, potion):
    if player.max_health - player.health <= potion.value:
        player.health = player.max_health
    else:
        player.health += potion.value