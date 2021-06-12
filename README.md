# 動作風景(YouTube)
[![](https://img.youtube.com/vi/OERTGuoC9UQ/0.jpg)](https://www.youtube.com/watch?v=OERTGuoC9UQ)

# 概要
- このソフトウェア群は、実物部品を使ったDE15運転台をリアルに制御するシミュレータシステムです。
- DesktopStation様のDSAir2などを使用して、DCC・アナログ鉄道模型を制御することもできます。

# 起動方法
- メニューからターミナルエミュレータを起動
- コマンドを入力 `cd DE15` Enterキーを押す(フォルダ移動)
- コマンドを入力 `python3 main.py` Enterキーを押す(起動)

`log/12345.txt` などにエラーログが記載されているので、動作に違和感を感じたら最も数字が大きいファイル(最新)を確認する

# 終了方法
- ターミナル画面でCtrlキーを押しながらcキーを押す

# 新しいUbuntu系Linux搭載コンピュータで動かす環境構築方法例
- `sudo apt install python3 python3-serial git python3-pip`
- `pip3 install pygame`
- `git clone git@github.com:mipsparc/DE15.git`
- `cd DE15`
- `python3 main.py hid mascon controller` で単体起動試験をする
- udevでデバイスファイルを割り当てる。 `sudo cp udev_rules/* /etc/udev/rules.d/`
- コンピュータを再起動する
- ターミナルを開いて `cd DE15`

# 音声に関するライセンスについて
音声(soundディレクトリ)内の音声は、別の用途での利用は禁止とさせていただきます。
ただし、例外的に許諾できる場合もありますので、ご相談ください。
