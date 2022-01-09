A small handy application for installing mods from steam workshop

## Installing
```
> pip install git+https://github.com/AshenHermit/steam-workshop-mods-installer.git
or download repo and run
> python setup.py install
```

## Usage
This will download archive with mod and unpack it into a working directory and also will write config file.
```
> smod install "https://steamcommunity.com/sharedfiles/filedetails/?id=2590814089" "2499635888" "https://steamcommunity.com/sharedfiles/filedetails/?id=2553733512"
```
This will update mods registered in config file
```
> smod update
```
This will print some info about mods
```
> smod log

registered 3 mods:
    <Mod 2590814089 - "AoM zed animation" for game "Project Zomboid" - 23.28 Mb>
    <Mod 2499635888 - "Afraid Of Monsters Zombies" for game "Project Zomboid" - 4.72 Mb>
    <Mod 2553733512 - "Soul Filcher's Turning Time" for game "Project Zomboid" - 0.36 Mb>

```