# 概要
このソフトウェア群は、実際の運転台部品で鉄道模型をリアルに制御するシミュレータシステムです。(WIP)

# 起動方法
- メニューからターミナルエミュレータを起動
- コマンドを入力 `cd NController` Enterキーを押す(フォルダ移動)
- コマンドを入力 `python3 main.py` Enterキーを押す(起動)

`log/12345.txt` などにエラーログが記載されているので、動作に違和感を感じたら最も数字が大きいファイル(最新)を確認する

# 終了方法
- ターミナル画面でCtrlキーを押しながらcキーを押す

# 新しいUbuntu系Linux搭載コンピュータで動かす環境構築
- `sudo apt install python3 python3-serial git python3-pip`
- `pip3 install pygame`
- `git clone git@github.com:mipsparc/NController.git`
- `cd NController`
- `python3 main.py hid mascon controller` で単体起動試験をする
- udevでデバイスファイルを割り当てる。 `sudo cp udev_rules/* /etc/udev/rules.d/`
- コンピュータを再起動する
- ターミナルを開いて `cd NController`
- `python3 BrakeReader.py` ブレーキ動作試験
- `python3 MasconReader.py` マスコン動作試験

# 構成
## MasconReader
主幹制御器に取り付けたPICマイコンからUART通信で送信されたノッチ情報をUSB-UARTを通して取得する

## DE10
日本国有鉄道DE10形液体式ディーゼル機関車の加速度に近い加減速を計算して、リアルタイムでの実物をシミュレートする

## Sounder
音の鳴動を制御する。soundディレクトリ内に実際の音がある

## SoundManager
Sounderを制御する

## DSair2_v1
渡された速度に基づいてコマンドステーション DSair2に走行指令をする(DC/DCC)

## BrakeReader
ブレーキ装置の状態とブレーキ角を読み込む

## main
すべてを統括する

