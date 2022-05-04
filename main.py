import sys
import csv
import requests
import random
import discord

def create_image(request):
    response = requests.get(request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


def sites_import(sites):
    with open('requests.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            sites.append([row[0], row[1]])


sites = []
sites_import(sites)
random.seed(1453461)
test = sites.copy()
random.shuffle(test)
for i in range(len(test)):
    variants = sites.copy()
    del variants[variants.index(test[i])]
    first = random.choice(variants)
    del variants[variants.index(first)]
    second = random.choice(variants)
    del variants[variants.index(second)]
    test[i] = [test[i][0], [test[i][1], first[1], second[1]]]
session = {}
leader_board = {}

TOKEN = "OTcxMzMzODI3NTQ2OTcyMjEx.YnI_Hg.e_xSOMmwZgqkDH0YzYQJVPqMb1Y"
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    global session, right
    global leader_board, max_round
    author = str(message.author)
    if message.author == client.user:
        return
    word = message.content
    if word == '/start':
        session[author] = [0, 0]

        author = str(message.author)
        await message.channel.send(str(session[author][1] + 1) + ')')
        await message.channel.send(test[session[author][1]][0])
        vrs = test[session[author][1]][1].copy()
        right = vrs[0]
        random.shuffle(vrs)
        for i in range(3):
            await message.channel.send(f'   {i + 1}: {vrs[i]}')
        right = vrs.index(right)

    if word == '/help':
        await message.channel.send('Команды:\n' +
                                   '    /start - начало теста\n' +
                                   '    /stop - конец теста\n' +
                                   '    /help - помощь\n' +
                                   '    /leaderboard - таблица лидеров\n')

    if word == '/stop':
        author = str(message.author)
        if author in session.keys():
            del session[author]
            await message.channel.send('Тест окончен')

    if word == '/leaderboard':
        if leader_board:
            await message.channel.send('Таблица лидеров:')
            for name in sorted(sorted(leader_board.keys()), key=lambda x: leader_board[x]):
                await message.channel.send(f'{name}: {leader_board[name]}')
        else:
            await message.channel.send('Таблица лидеров пуста')

    if author in session.keys():
        author = str(message.author)
        if word in ['1', '2', '3']:
            vrs = test[session[author][1]][1].copy()
            if int(word) - 1 == right:
                session[author][0] += 1
                await message.channel.send('Правильно')
            else:
                await message.channel.send('Неправильно')
            session[author][1] += 1
            if session[author][1] >= len(test):
                await message.channel.send('Ваш счет:' + str(session[author][0]))
                if message.author in leader_board.keys():
                    if leader_board[author] < session[author][0]:
                        leader_board[author] = session[author][0]
                else:
                    leader_board[author] = session[author][0]
            else:

                await message.channel.send(str(session[author][1] + 1) + ')')
                await message.channel.send(test[session[author][1]][0])
                vrs = test[session[author][1]][1].copy()
                right = vrs[0]
                random.shuffle(vrs)
                for i in range(3):
                    await message.channel.send(f'   {i + 1}: {vrs[i]}')
                right = vrs.index(right)



client.run(TOKEN)
