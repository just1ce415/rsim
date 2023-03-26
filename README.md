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

- Account for human factor (to account for that in some way, please, use realistic rotations).

- Account for ping.

- Account for any king of spatial data.

- Account for poorly configured rotation.

- Account for defensive utilities such as damage reduction and resistance to interruption, which is impossible to evaluate in "non-spatial dummy" setup.

- 1-piece sets are neglected.

### Important: CAVEATS

- Shield strength does not reduce damage taken by shield, but rather increases its HP (while in game it's opposite).

- Some character skills effeciency of which is depend on spatial data (e.g. Yaoyao elemetal skill) has special `uptime` parameter in order to account for that.

- Code allows user to use skills and bursts even duraing cooldown or without enough energy, because rotation cannot be changed in the code by design (to account for that, please, write realistic rotations).

- Simulator actually runs two simulations: test one (where data about damage distribution and energy requirements is collected) and main one.

- Character animations are coded in such way that it's assumed they are cancelled every time, when it's possible and optimal. In order chain of actions make feel to be less mechanic, character waits some time after performing action during after-animation.

- Enemies are just dummies who does NOT attack and stay in one place.

- For multitarget case, it's assumed, that enemies are close enough in order for quadratic scaling to work completely.
