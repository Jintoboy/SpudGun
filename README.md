# SpudGun
### Custom Projectile Ranged Weapon for Abiotic Factor

**SpudGun** is an **Abiotic Factor** content mod generated from the official "Projectile Ranged Weapon" mod template. It introduces a craftable potato launcher with custom physical projectiles, ammunition items, and crafting recipes.

---

## 1. Mod Overview

- **Plugin Mount Point**: `/SpudGunLsjct/`
- **Mod Prefix**: **`NYYR5`**
- **Category**: Content-only UGC Plugin (`NoCode: true`)
- **Compatibility**: Singleplayer, Co-op Host/Client, Dedicated Server

---

## 2. Included Assets & Architecture

| Asset | Type / Class | Row Handle ID / Asset Path | Purpose |
| :--- | :--- | :--- | :--- |
| **Weapon Blueprint** | `Abiotic_Weapon_Gun_ParentBP` | `/SpudGunLsjct/Blueprints/Weapon_SpudGun` | Held weapon actor with muzzle socket and fire logic |
| **Projectile Blueprint** | `AbioticProjectile_ParentBP` | `/SpudGunLsjct/Blueprints/Projectile_SpudGun` | Physics projectile actor simulating potato trajectory & impact |
| **Weapon Item Data** | `ItemModRowAsset` | `NYYR5_SpudGun` (`ItemTable_Weapons`) | Durability, magazine size, ammo type linkage, stats |
| **Ammo Item Data** | `ItemModRowAsset` | `NYYR5_ammo_SpudGun` (`ItemTable_Pickups`) | Ammunition inventory item, stack sizes, icon |
| **Projectile Data** | `ProjectileModRowAsset` | `NYYR5_projectile_SpudGun` (`DT_Projectiles`) | Speed, gravity scale, damage value, damage type |
| **Weapon Recipe** | `RecipeModRowAsset` | `NYYR5_recipe_SpudGun` (`DT_Recipes`) | Crafting requirements and bench unlock for weapon |
| **Ammo Recipe** | `RecipeModRowAsset` | `NYYR5_recipe_ammo_SpudGun` (`DT_Recipes`) | Crafting requirements for ammo |

---

## 3. Play-In-Editor (PIE) Testing

While testing in the Mod Editor, press **`\` (Backslash)** to open the Developer Game Command Menu:
- **`SpawnItem`** $\rightarrow$ `NYYR5_SpudGun` (Spawns weapon into player inventory)
- **`SpawnItem`** $\rightarrow$ `NYYR5_ammo_SpudGun` (Spawns ammunition into player inventory)
- **`UnlockAllRecipes`** (Unlocks workbench recipes to verify crafting progression)

---

## 4. Packaging & Publishing

Packaging runs through the Mod Editor's official **Mod.io / "Upload Mod"** tool:
- Select **Mod Root Directory (`ModRootDir`)**: `C:\Users\vczle\Documents\Abiotic Factor Mods\SpudGun\SpudGunLsjct`
- Select **Platform**: `Windows`
- Set **Version** and **Changelog**, then click **Upload Mod File**.
