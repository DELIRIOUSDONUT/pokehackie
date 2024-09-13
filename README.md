# README

## Setting up local PS server
1) Open command prompt
2) Use one of "pip install poke-env" or "python -m pip install poke-env" or "py -m pip install poke-env"
3) Copy-paste the next three lines:

git clone https://github.com/smogon/pokemon-showdown.git
cd pokemon-showdown
npm install

4) Use "copy config\config-example.js config\config.js" for Windows, "cp config/config-example.js config/config.js" for Linux based systems
5) Start local host with "node pokemon-showdown start --no-security"

## Validating teams

This can be done on either local or official PS servers

1) Click on Teambuilder
2) Select New Team
3) Click on the Format dropdown box and select [Gen 3] OU under the Past Gens OU column
4) Click on Add Pokemon
5) Proceed to add your Pokemons and select their items, ability, moves and EVs (we will be capping this)
6) Once you're done adding Pokemons, go back to the team section and click on Validate. This will tell if you if your team is valid. If not, it will tell you what to change to validate it.
7) Once validated, click on the Import/Export button at the top and save the output in a team.txt file. This will be your team we'll use for bot simulations.

## How to write a bot
