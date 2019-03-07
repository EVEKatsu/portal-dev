## What is it?
This website will report the news of Japanese EVE Online players.

## License
evekatsu.github.io is licensed under the The Unlicense, see LICENSE.

## Contacts
* Omochin
    * GitHub: @Omochin
    * [Twitter](https://twitter.com/omochin4eve): @omochin4eve
    * Email: omochin7@gmail.com

## Launch local develop environment

please copy evekatsu.env.example to evekatsu.env and set twitter api key and secrets.

### Windows

if you are Microsoft Windows user, use [vagrant](https://www.vagrantup.com/) and [Oracle VirtualBox](https://www.virtualbox.org/).

you can use docker in VirtualBox.
source code are placed at /app in virtual machine.

and read below Linux or MacOS section.

### Linux or MacOS

install [docker](https://www.docker.com/) and [docker compose](https://docs.docker.com/compose/)

```
docker-compose up
```

more information, read Vagrantfile and dockerfiles/*, docker-compose.yml.

### 「俺は日本人だ」 ― "for Japanese developer"

まず、TwitterAPIのキーとシークレットをevekatsu.envに保存してください。
evekatsu.env.exampleをコピーすると良いです。

dockerとdocker-composeを使っていぶかつをローカルで起動できます。
WindowsユーザはVagrantfileを用意してるので、それを使ってください。
(仮想マシンの/app以下に丸々ファイルが入っています。)

後の詳しいことはVagrantfileやdockerfilesフォルダ以下、docker-compose.ymlを読んでください。

## CCP Copyright Notice
EVE Online, the EVE logo, EVE and all associated logos and designs are the intellectual property of CCP hf. All artwork, screenshots, characters, vehicles, storylines, world facts or other recognizable features of the intellectual property relating to these trademarks are likewise the intellectual property of CCP hf. EVE Online and the EVE logo are the registered trademarks of CCP hf. All rights are reserved worldwide. All other trademarks are the property of their respective owners. CCP hf. has granted permission to evekatsu.github.io to use EVE Online and all associated logos and designs for promotional and information purposes on its website but does not endorse, and is not in any way affiliated with, evekatsu.github.io. CCP is in no way responsible for the content on or functioning of this program, nor can it be liable for any damage arising from the use of this program.
