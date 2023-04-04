# Rsim

## (rotation simulator for Genshin Impact)

## THIS SOFTWARE IS NOT FINISHED

### Important message

#### This software is open-source and provided "as is" (check licence). Before making any conclusions regarding its functions, limitations, etc., please, make sure you have read README.md

### What rsim CAN do

- Accounts for weapons, talents, artifacts, constallations, etc., etc. - any factors like stats, resonances, uptimes, downtimes, character states, events that should be considered when calculating damage.

- Specifically, account for elemental application ICD, elemental gauge interactions (weapon gauge included), simultaneous reaction priority, reaction ICD.

- Accounts for healing and shielding considering any factors that should be considered.

- Accounts for hitlag extension (and thus animation duration).

- Has ability to simulate single target as well as multitarget scenarios to account for quadratic and pseudo-quadratic scaling.

- Has ability to generate artifact substats based on the amount of required Energy Recharge and stat value (check documentation).

- Accounts for character that lose HP naturally (Xiao burst, Dehya A1).

### What rsim CANNOT do

- Account for human factor (except all the actions (e.g. jump, dash, elemental skill, N2) have 10 frames added to account for human error, to further account for that in some way, please, use realistic rotations).

- Account for ping (it's always 20ms, never changes)

- Account for any kind of spatial data.

- Account for poise.

- Account for poorly configured rotation.

- Account for defensive utilities such as damage reduction and resistance to interruption, which is impossible to evaluate in "non-spatial dummy" setup.

- 1-piece sets are neglected.

### Important: CAVEATS

- Shield strength does not reduce damage taken by shield, but rather increases its HP (while in game it's opposite).

- Some character skills effeciency of which is depend on spatial data (e.g. Yaoyao elemetal skill) has special `uptime` parameter in order to account for that.

- Code allows user to use bursts without enough energy for ER optimization and because rotation cannot be changed in the code by design (to account for that, please, write realistic rotations).

- Simulator actually runs two simulations: a test one (where data about damage distribution and energy requirements is collected) and a main one.

- Character animations are coded in such way that it's assumed they are cancelled every time, when it's possible and optimal.

- Enemies are just dummies who does NOT attack and stay in one place.

- For multitarget case, it's assumed, that enemies are close enough in order for quadratic scaling to work completely. However, application of some character's skills may benefit from enemies being not too close from each other (e.g. Yaoyao), therefore such skills can be configured to apply element in single target.

- Burning swirl and frozen swirl are considered pyro swirl and cryo swirl respectively.

- When character tries to use charged attack/dash with not enough stamina, he just waits till it regenerates; by analogy, when character tries to use skill/burst while on cooldown, he just waits till it passes.
