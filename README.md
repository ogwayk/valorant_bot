# valorant_bot
- Discord上で作動する、Valorantの個人のストア情報を取得して返してくれるBot
- メンション+登録でDMが届き、そこにユーザー名とパスワードを入力することで登録が完了する
- 登録した情報は暗号化したうえでスプレッドシートに保存
- 登録したあとはメンションを飛ばすことでその日のストア情報を取得してきてくれる
- 取得に用いるAPIはこちらのものを拝借
  - https://github.com/HeyM1ke/ValorantClientAPI
- ナイトマーケット開催時はメンション+ナイトなどのコマンドでナイトマーケット情報が得られる
- Heroku上で動く
