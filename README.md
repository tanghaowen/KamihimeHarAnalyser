# KamihimeHarAnalyser
神姫プロジェクトの戦闘データ分析ツール/The Battle Data Analyser of Kamihime Project

ダウン‐ロード：
https://github.com/kisaragiHiyo/KamihimeHarAnalyser/releases
![image](11.jpg)
<hr>
このツール、何に使う？
 このツールは、楽に大量なデータを分析するために、作ったプログラムである。

<br>


使い方：

１．
  バトルが始まったら、F12ボタンを押して、ブラウザーの開発者ツールを呼び出す。
  ![image](1.jpg)
  
  <br>
<br>

  
  
２．
  NetworkとXHRを押して
  
  ![image](1.jpg)
  <br>
<br>

  
  
  
３．
  その後、ゲームに戻して、適当に戦闘を行う。バトルとともに、たくさんのデータは自動的に記録される。
  バトルが終わったら、記録されたアイテムに右クリックして、Save as HAR with content を選択して、名をてけて全てのデータを保存する。
  
  ![image](2.jpg)
  <br>
<br>

  
  
  
４．
  その後、ダウン‐ロードしたプログラムで、下の図のように保存したharファイルを開ける。
<br>
<br>
  
  
  ![image](3.jpg)
  
<br>
<br>
  
  
    
５．
   完成
<br>
<br>
   
   
  ![image](4.jpg)
 
<hr>
Tips:
 
 保存したHARファイルは全てのデータを含めているので、もし一気に複数のバトルを記録するなら、HARファイルのサイズは非常に大きくなり、分析のスピードも遅くなる。
 そのため、左上のこのボタンを活用してください。
  ![image](5.jpg)
 このボタンで開発者ツールに記録された全てのデータを削除できる。このボタンを使い、複数のバトルに区切りをつけ、一つ一つのHARファイルに保存できる。

