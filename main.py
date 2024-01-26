from flask import Flask, render_template, request
from collections import Counter
import matplotlib.pyplot as plt
app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


def saving_form():
    answer = ""
    for i in range(1, 15):
        try:
            answer += request.args['a'+str(i)].strip().lower() + "\t"
        except Exception as e:
            answer += "\t"
            with open("problems.txt", "a", encoding="utf-8") as f:
                f.write(str(e)+"\n")
    with open("answers.tsv", "a", encoding="utf-8") as f:
        f.write(answer[:len(answer)-1]+"\n")


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/thanks')
def thanks():
    saving_form()
    return render_template('thanks.html')


@app.route('/statistics')
def statistics():
    with open("answers.tsv", "r", encoding="utf-8") as f:
        info = f.read()
    participants = info[:len(info)-1].split("\n")
    total = len(participants)
    all_answers = []
    for i in participants:
        all_answers.append(i.split("\t"))
    age = []
    for i in range(len(participants)):
        if len(all_answers[i][0]) != 0:
            age.append(int(all_answers[i][0]))
    rus = 0
    bulg = 0
    for i in range(len(participants)):
        if all_answers[i][1] == "yes":
            rus += 1
        if all_answers[i][2] == "yes":
            bulg += 1
    a = []
    for j in range(4, 14):
        b = []
        for i in range(len(participants)):
            if len(all_answers[i][j]) != 0:
                b.append(all_answers[i][j])
        a.append(b)
    print(a)
    test_quest = []
    for j in range(5):
        test_quest.extend(a[j])
    test_count = Counter(test_quest)
    rus_test_count = dict()
    rus_test_count["дательный падеж"] = test_count["dat"]
    rus_test_count["использование для"] = test_count["for"]
    rus_test_count["оба варианта"] = test_count["both"]
    rus_test_count["ни один из вариантов"] = test_count["none"]
    open_quest = []
    for j in range(5, 10):
        if len(list(Counter(a[j]))) != 0:
            open_quest.append(list(Counter(a[j]))[0])
        else:
            open_quest.append("")
    a6, a7, a8, a9, a10 = open_quest
    overall_answers = test_quest.copy()
    for t in a[5]:
        if t == "профессору":
            overall_answers.append("dat")
        elif t == "для профессора":
            overall_answers.append("for")
    for t in a[6]+a[8]:
        if t == "ему":
            overall_answers.append("dat")
        elif t == "для него":
            overall_answers.append("for")
    for t in a[7]+a[9]:
        if t == "мне":
            overall_answers.append("dat")
        elif t == "для меня":
            overall_answers.append("for")
    overall_count = Counter(overall_answers)
    plt.rcParams["font.family"] = "Georgia"
    fig, ax = plt.subplots()
    ax.pie(x=[overall_count["dat"], overall_count["for"]], labels=["дательный падеж", "использование для"],
           autopct='%1.2f%%', textprops={'fontsize': 14}, colors=['#005AFA', 'violet'])
    plt.savefig('static/chart.png', transparent=True, dpi=400)
    return render_template('statistics.html', total=total, min=min(age), max=max(age), rus=round(rus/total, 3),
                           bulg=round(bulg/total, 3), test_count=rus_test_count, a6=a6, a7=a7, a8=a8.capitalize(),
                           a9=a9.capitalize(), a10=a10.capitalize(), chart='chart.png')


if __name__ == '__main__':
    app.run()
