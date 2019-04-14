import vk_api
import time
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy2

session = vk_api.VkApi(token = '9d5ac8f3b2b65e0fc08201dd428907e4ec9d01e9c33243e148c364c26495bf907a025b6cc1a2ddc2e904d')
vk = session.get_api()

offset = 0
c = 0

nltk.download('stopwords')
download_stopwords = stopwords.words('russian')
morph = pymorphy2.MorphAnalyzer()
signs = ['!','\"',';',':','(',')','?','.','>','\'',',','#','+','=']
gaycheck = ['ё','й','ц','у','к','е','н','г','ш','щ','з','х','ъ','ф','ы','в','а','п','р','о','л','д','ж','э','я','ч','с','м','и','т',
            'ь','б','ю','q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x',
            'c','v','b','n','m']
result = {}
kill_me = []

file = open("kek.txt", "w")
for i in range(0, 2):
    data = vk.wall.get(domain = 'dtf',count=100, offset=offset, filter = 'owner')
    offset += 100
    for item in data['items']:
        comment = vk.wall.getComments(owner_id=item['from_id'], post_id=item['id'], count = 100)
        c += 1
        print(c)
        for ite in comment['items']:
            try:
                sentence = ite['text']
                for letter in sentence:
                    if letter in signs:
                        sentence = sentence.replace(letter, '')
                tokens = word_tokenize(sentence)

                check = []
                for token in tokens:
                    check.append(token)
                    for letter in token:
                        if letter.lower() not in gaycheck:
                            check.remove(token)
                            break
                    if token in download_stopwords:
                        check.remove(token)
                tokens.clear()
                for token in check:
                    tokens.append(token)

                for token in tokens:
                    parse = morph.parse(token)[0]
                    if morph.parse(token)[0].normal_form in kill_me:
                        result[token] += 1
                    else:
                        result[token] = 1
                        kill_me.append(morph.parse(token)[0].normal_form)
            except KeyError:
                continue
            except ValueError:
                continue

        for it in comment['items']:
            comm = vk.wall.getComments(owner_id=item['from_id'], post_id=item['id'], comment_id = it['id'], thread_items_count=10)
            for ite in comm['items']:
                try:
                    sentence = ite['text']
                    for letter in sentence:
                        if letter in signs:
                            sentence = sentence.replace(letter, '')
                    tokens = word_tokenize(sentence)

                    check = []
                    for token in tokens:
                        check.append(token)
                        for letter in token:
                            if letter.lower() not in gaycheck:
                                check.remove(token)
                                break
                        if token in download_stopwords:
                            check.remove(token)
                    tokens.clear()
                    for token in check:
                        tokens.append(token)

                    for token in tokens:
                        parse = morph.parse(token)[0]
                        if morph.parse(token)[0].normal_form in kill_me:
                            result[token] += 1
                        else:
                            result[token] = 1
                            kill_me.append(morph.parse(token)[0].normal_form)
                except KeyError:
                    continue
                except ValueError:
                    continue
                except IndexError:
                    continue
    time.sleep(15)
list_result = []
for k in result:
    list_result.append(result[k])
list_result = sorted(list_result, reverse=True)
checklist = []
for i in list_result:
    if i not in checklist:
        checklist.append(i)
for i in checklist:
        for key in result:
            file.write(str(key)+' '*(25-len(str(key)))+str(i)+'\n')
file.close()