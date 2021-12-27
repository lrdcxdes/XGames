from json import loads, dumps
import requests
import subprocess
import os


class Games:
    def __init__(self):
        self.path = os.getenv('TEMP') + '\\XGames\\'
        try:
            os.makedirs(self.path)
        except Exception as e:
            print(e)
        try:
            subprocess.call(['attrib', '-h', '.games.json'])
            self.file = open('.games.json', 'r').read()
            subprocess.call(['attrib', '+h', '.games.json'])
        except Exception as e:
            print(e)
            open('.games.json', 'w').write('[]')
            subprocess.call(['attrib', '+h', '.games.json'])
            self.file = open('.games.json', 'r').read()
        self.json = loads(self.file)
        self.games = [Game(self, i) for i in self.json]

    def add_game(self, game, filename):
        if game.game_name in [i.name for i in self.games]:
            index = [i.name for i in self.games].index(game.game_name)
            img = self.games[index].img
            game_dict = {'name': game.game_name, 'path': filename, 'installed': False, 'img': img}
            self.games[index] = Game(self, game_dict)
            self.json[index] = game_dict
            json = dumps(self.json, sort_keys=True, indent=4)
            subprocess.call(['attrib', '-h', '.games.json'])
            open('.games.json', 'w').write(json)
            subprocess.call(['attrib', '+h', '.games.json'])
            return

        game_dict = {'name': game.game_name, 'path': filename, 'installed': False}

        name = game.game_name
        name = name.replace(' ', '_').replace('\'', '')
        name = name.replace('.', '_').replace('/', '_')
        name = name.replace('\\', '_')

        url = self.path + name + '.'
        url = url.replace('\\', '/')

        if '.jpg' in game.game.img:
            url += 'jpg'
        elif '.jpeg' in game.game.img:
            url += 'jpeg'
        else:
            url += 'png'

        game_dict['img'] = url

        if not os.path.isfile(url):
            open(url, 'wb').write(requests.get(game.game.img).content)

        self.json.append(game_dict)

        json = dumps(self.json, sort_keys=True, indent=4)

        subprocess.call(['attrib', '-h', '.games.json'])
        open('.games.json', 'w').write(json)
        subprocess.call(['attrib', '+h', '.games.json'])

    def reload(self):
        try:
            os.makedirs(self.path)
        except Exception as e:
            print(e)
        try:
            subprocess.call(['attrib', '-h', '.games.json'])
            self.file = open('.games.json', 'r').read()
            subprocess.call(['attrib', '+h', '.games.json'])
        except Exception as e:
            print(e)
            open('.games.json', 'w').write('[]')
            subprocess.call(['attrib', '+h', '.games.json'])
            self.file = open('.games.json', 'r').read()
        self.json = loads(self.file)
        self.games = [Game(self, i) for i in self.json]
        return self


class Game:
    def __init__(self, games, source):
        self.games = games
        self.source = source
        self.name = self.source.get('name')
        self.path = self.source.get('path')
        self.img = self.source.get('img')
        self.installed = bool(self.source.get('installed'))
        self.exe = self.source.get('exe')

    def remove(self):
        self.games.games.remove(self)
        self.games.json.remove(self.source)
        json = dumps(self.games.json, sort_keys=True, indent=4)
        subprocess.call(['attrib', '-h', '.games.json'])
        open('.games.json', 'w').write(json)
        subprocess.call(['attrib', '+h', '.games.json'])
        return self.games.reload()

    def update_game(self):
        index = [i.name for i in self.games.games].index(self.name)
        game_dict = {'name': self.name, 'path': self.path, 'installed': self.installed, 'img': self.img}
        if self.exe:
            game_dict['exe'] = self.exe
        self.games.games[index] = Game(self.games, game_dict)
        self.games.json[index] = game_dict
        json = dumps(self.games.json, sort_keys=True, indent=4)
        subprocess.call(['attrib', '-h', '.games.json'])
        open('.games.json', 'w').write(json)
        subprocess.call(['attrib', '+h', '.games.json'])
        return self.games.reload()
