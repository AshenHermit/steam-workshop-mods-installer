A small handy application for installing mods from steam workshop.  
Without authorization and api keys (instead it uses [this](https://steamworkshopdownloader.io/) downloader under the hood).

### What can do
* install, update, remove, print mods
* check missing files

## Installing
```
> pip install git+https://github.com/AshenHermit/steam-workshop-mods-installer.git
or download repo and run
> python setup.py install
```

## Usage
This will download archive with mod and unpack it into a working directory and also will write config file:
```
> smod install 2499635888 https://steamcommunity.com/sharedfiles/filedetails/?id=2590814089

fetching mod "2499635888"...
downloading "2499635888_afraid_of_monsters_zombies.raw.download.zip"...
100%|████████████████████████████████████████████████████████████████████████████| 4.73M/4.73M [00:00<00:00, 7.04MiB/s]
unpacking...
ssuucceessffuullyy installed <Mod 2499635888 - "Afraid Of Monsters Zombies" for game "Project Zomboid" - 4.72 Mb>

fetching mod "https://steamcommunity.com/sharedfiles/filedetails/?id=2590814089"...
downloading "2590814089_aom_zed_animation.raw.download.zip"...
100%|████████████████████████████████████████████████████████████████████████████| 23.3M/23.3M [00:02<00:00, 8.80MiB/s]
unpacking...
ssuucceessffuullyy installed <Mod 2590814089 - "AoM zed animation" for game "Project Zomboid" - 23.28 Mb>
```

This will update mods registered in config file:
```
> smod update
...
```

This will remove mods files and folders:
```
> smod remove 2553733512

removing <Mod 2553733512 - "Soul Filcher's Turning Time" for game "Project Zomboid" - 0.36 Mb>...
100%|████████████████████████████████████████████████████████████████████| 20/20 [00:00<00:00, 1539.45it/s, poster.png]
removed.
```

You can also remove all registered mods with:
```
> smod remove-all
...
```

This will print some info about mods:
```
> smod log

registered 3 mods:
    <Mod 2590814089 - "AoM zed animation" for game "Project Zomboid" - 23.28 Mb>
    <Mod 2499635888 - "Afraid Of Monsters Zombies" for game "Project Zomboid" - 4.72 Mb>
    <Mod 2553733512 - "Soul Filcher's Turning Time" for game "Project Zomboid" - 0.36 Mb>

```