# このスキルについて
- 参加メンバーがほぼ固定されている会議で今回だれが議事録取るんだっけ？を教えてくれるスキル
- もし今回当番の人が不在だった場合はその次の当番を教える。
- 会議じゃなくても当番制があり、ほぼ固定メンバーが参加するイベントなどで使えそう。
- 社内向けスキルのため公開はしていない。
- [The Alexa Skills Kit SDK for Python](https://github.com/alexa/alexa-skills-kit-sdk-for-python)で開発。

# 主要なインテント解説
## DecidePICIntent
- 前回の議事録担当をもとに今回の担当をセットするインテント
- 議事録当番になりうるメンバー全員をスロットへ追加する。
- 議事録担当するメンバーのタプルを作成しておいて、スロットに入った前回の当番のインデックス番号を1加えることで今回の当番をセットする。
- 議事録書いた人はどなたですか？と聞くと本人が「わたしです」と答えそうなので、「お名前は？」と聞くことでスロットに定義した名前にマッチさせてこのインテントが呼び出されるようにした。

## AMAZON.YesIntent
- 「今回は○○さんです。いらっしゃいますか？」→「はい」で呼び出されるインテント
- ビルトインインテントへ「います」「いますよ」などを追加。
- 議事録当番が決定するとセッションが終わる。


## AMAZON.NoIntent
- 「今回は○○さんです。いらっしゃいますか？」→「いいえ」で呼び出されるインテント
- ビルトインインテントへ「いません」「休みです」「出張です」などを追加。
- 欠席者のタプルインデックス番号へ1加算して次の担当を伝える。
- その人が参加していればAMAZON.YesIntentへ飛んでセッション終了。
- 決まるまでタプルの担当者が順次読み上げられる。


# メモなど
- 会議参加者は毎回固定なので全員を登録したスロットを作成した。
- 苗字または名前で呼ばれることもあるメンバーがいることもあるので呼び方の「ゆれ」を吸収する。
- 欠席で当番をスキップする場合があるため、参加者ごとに議事録を何回書いた書いていないというステートをDynamoDBで管理しようと思ったが、複雑になるのでやめておいた。
- 例えば当番の田中さんが欠席した場合、次回の会議で「田中さんの前はだれ？」と確認できるインテントがあってもよいかもしれない。
