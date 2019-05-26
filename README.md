# 概要
このソフトウェア群は、鉄道模型を実際の運転台部品で制御し、実物の音が同時に鳴るシステムです。

# 起動方法
- メニューからターミナルを起動
- コマンドを入力 cd NController
- Enterキーを押す(フォルダを移動するコマンド)
- コマンドを入力 python3 NControl.py
- Enterキーを押す

# 終了方法
- ターミナル画面でCtrlキーを押しながらcキーを押す

# 新しいUbuntu系Linux搭載コンピュータで動かす環境構築
- sudo apt install python3 python3-pygame python3-serial git
- git clone git@github.com:mipsparc/NController.git
- python3 NControl.py brake mascon controller で単体起動試験をする
- udevの設定をして、デバイスに読み書き権限があるようにする。/dev/mascon, /dev/brake, /dev/controller に各デバイスを割り当てる
- コンピュータを再起動する
- screenコマンドなどで各デバイスの動作を確認する

# 構成
## MasconReader
主幹制御器に取り付けたPICマイコンからUART通信で送信されたノッチ情報をUSB-UARTを通して取得する

## DE10
日本国有鉄道DE10形液体式ディーゼル機関車の加速度に近い加減速を計算して、リアルタイムでの実物をシミュレートする

## Sounder
音の鳴動を制御する。soundディレクトリ内に実際の音がある

## SoundManager
Sounderを制御する

## Controller
渡された出力レベルに基づいて自作のPIC製PWM鉄道模型コントローラを制御する

## BrakeReader
ブレーキ統合ユニットからブレーキハンドルの角度と各種ボタン操作を受け取って、速度計に速度情報を渡す

## NControl
すべてを統括する
