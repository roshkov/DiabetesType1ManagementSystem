# POEDSS

## Configuration
For Docker-From-Docker to work correctly, you must enable "Terminal > Inherit Env" inside VSCode. This enables the dev container to collect the repo's directory from the host into an environmental variable for use with docker inside the container.

### Windows
For use in windows, I suggest you clone this repo into the Windows Subsystem for Linux (WSL2). This gives docker an easier time figuring out exactly where your project folder is when it needs to mount.
To clone the repo into WSL2, open up the WSL2 terminal, this brings you to your home directory under WSL2. [Create an ssh key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) as such 
```
ssh-keygen -t ed25519 -C "your_email@example.com"
```

let it save into the default folder, give it no passphrase.
Type in this command: 
```
eval "$(ssh-agent -s)"
```
and then type this 
```
ssh-add ~/.ssh/id_xxxxx
```
where the x's correspond to the id that was just created.

Now type in
```
cat ~/.ssh/id_xxxxx.pub
```
again where the x's correspond to the id, and copy the output and add this to your githubs ssh keys.

Now finally type in
```
git clone git@github.com:tina5kova/POEDSS.git 
```
This shall clone it into a folder named ` POEDSS `

  When opening VSCode to find the folder location, select "Open Folder" and into the top bar type in "//wsl$/" and find the folder from there. It is usually in /Ubuntu-xxxx/home/USERNAME/" to where you have cloned the repo.

## Running

`make up-camunda` runs the containers: Siddhi, Camunda + Database. 
`poetry run poedss [speed]` runs the python command to stream the data. 
`make down-camunda` brings down the docker containers.

``` 
$ make up-camunda
$ poetry run poedss [speed]
$ make down-camunda
$ sudo docker logs services_siddhi_1 -f
```

## Useful for developing

Rebuilding external api-endpoint and connecting to logs
```
$ make rebuild-logs-external
```

Rebuilding Siddhi and connecting to logs right away
```
$ make restart-logs-siddhi
```