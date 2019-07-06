# 概要
このソフトウェア群は、実際の運転台部品で鉄道模型をリアルに制御するシミュレータシステムです。

# 起動方法
- 進行方向を前進に合わせる
- ブレーキハンドルを手前いっぱいにする
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
- `python3 main.py brake mascon controller` で単体起動試験をする
- udevでデバイスファイルを割り当てる。 `sudo cp udev_rules/* /etc/udev/rules.d/`
- コンピュータを再起動する
- ターミナルを開いて `cd NController`
- `python3 BrakeReader.py` ブレーキ動作試験
- `python3 MasconReader.py` マスコン動作試験
- `python3 Controller.py` コントローラ動作試験

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

# オープンソースライセンス
MIT License
Copyright 2019 mipsparc

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
