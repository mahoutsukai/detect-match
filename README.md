# detect-match

Based on Tomohiro Okazaki's "STUDY" video work with matches, this model is intended to enable instance detection of matches.

![image](https://github.com/mahoutsukai/detect-match/assets/1216152/cc4dd9cc-7552-4da2-b54e-c2c0fda99e30)

---

## Model 
detect-match-model
https://www.dropbox.com/sh/8uhz7hv9nu1a39k/AAAc165m3FT2RhQdKaD-Hok4a?dl=0

---

## Prediction Match
```zsh
python prediction_match.py --grandchild_directory_name 'name_of_grandchild_directory' --directory_path "/path/to/parent/images/directory/"
```

## Training Match
```zsh
python train_match.py
```


---
### このリポジトリについて


これは、深層学習を用いた画像認識技術のひとつ、インスタンスセグメンテーションで 「マッチ (match)」 を探索することに特化したモデルを作成するプロジェクトです。
第25回 亀倉雄策賞 受賞記念「岡崎智弘 個展 STUDY」で展示された「Matches Pond」から派生した成果物として生まれました。

インスタンスセグメンテーションやセマンティックセグメンテーションの分野では、2022年1月に論文発表された Meta 社が開発する「Detic」が2万種類の物体がアノーテーションフリーに検出ができることで有名ですが、 既存のクラスに「マッチ (match)」が存在しないために、「マッチ」の探索ができませんでした。

このリポジトリに格納するモデルは、岡崎智弘が日々生み出すスタディの群れ (Matches)をトレーニングセットとして用い、 **マッチのみを探索することに特化したモデル** を作成することを目的としています。

岡崎智弘が日々生み出す膨大な量のマッチの映像を構成する画像は数万点におよびますが、ここでは有効な画像 38,890点から、さらに各動画から1,2枚程度に限定し、モデルの学習に用いていきます。

岡崎智弘が生み出す画像のほうが主体のため、一定の学習後は、過学習に至ることが予想されます。
また、トレーニング用のデータには、 outside inside のデータ、スタディの群れ (Matches)の画像は、基本的に「室内のみ」のため、ある状況の偏在することになります。

**オーバーフィッティング (overfitting) を目的としたモデルです。一般的な使用ではご留意ください。**

---

### 「Matches Pond」とは

第25回 亀倉雄策賞 受賞記念「岡崎智弘 個展 STUDY」で展示された「Matches Pond」は、 映像のためのアプリケーションです。
スタディの群れ (Matches) の動画群を再構成する試みをしています。

コマ撮りのスタイルで撮影されるスタディの群れ (Matches) の動画 (画像) は、ある一定の状況下で撮影されることからコンピュータービジョンとの相性が良いと考えています。
比較的均質な映像用の写真データを用いることで、コンピュータービジョンのためのモデルを学習させています。

映像でときどき現れる "枠 (rect)" は、各画像に対してセマンティックセグメンテーションを実行し、検出できたセグメントマスク(要素)です。
前述のとおり、既存の "match"の検出は不可能ですが、検出結果には "match" であるはずのものに対し、 "toothpick", "chopstick", "pencil" などと認識されクラスが付与されていました。
それぞれの手、指との関係から近似した状況と判断されたものに対して、それらのクラスが付与されていると考えられます。

人間の目は優秀です。目で見た状況や、ものの輪郭や重なりは意識せずとも認知できるものですが、この「Matches Pond」では受動的にフィードバックされることから、 「人間とコンピュータの知覚の不一致」からの違和感と、「岡崎さんが撮影しているものとは何だろうか?」を感じてもらえたらと考えています。

- このアプリケーションでは、有効な撮影画像データ 38,890点を利用して作成しています。



---
## About this repository


This is a project to create a model specialized in searching for "matches.
It is derived from "Matches Pond," which was exhibited at "Tomohiro Okazaki's STUDY," the 25th Yusaku Kamekura Award Commemorative Exhibition.

In the field of semantic segmentation, "Detic," developed by Meta and published in January 2022, is famous for its ability to detect 20,000 object types without annotation. The model stored in this repository is the Oka model, which is a model of the Oka model.

The model in this repository aims to create a model specialized to search only for **matches**, using the swarm of studies (Matches) that Tomohiro Okazaki produces every day as a training set.

The images that make up the vast amount of matches produced by Tomohiro Okazaki on a daily basis number in the tens of thousands, but here we will limit the number of images to about 1 or 2 from each video from the 38,890 available images, and use them to train the model.

After a certain amount of training, over-training is expected.
Also, the data for training will be ubiquitous in certain situations, since the outside inside data, the images of the study flock (Matches), are essentially "indoors only."

**This model is intended for overfitting. Please note that this model is intended for general use.**

---

## What is "Matches Pond"?

Matches Pond", exhibited at the 25th Yusaku Kamekura Award winning commemorative "Tomohiro Okazaki Solo Exhibition STUDY", is an application for visual images.
It is an attempt to reconstruct a group of moving images of a group of studies (Matches).

We believe that Matches, which are shot in a frame-by-frame style, are compatible with computer vision because they are shot under certain conditions.
By using relatively homogeneous photographic data for the videos, we train models for computer vision.

The "rect" that sometimes appears in the video are segment masks (elements) that can be detected by performing semantic segmentation on each image.
As mentioned above, it is impossible to detect existing "matches," but the detection results showed that the "matches" were recognized as "toothpick," "chopstick," "pencil," etc. and assigned a class to them.
It is thought that these classes are assigned to objects that are judged to be in a similar situation based on their relationship to the respective hands and fingers.

The human eye is excellent. We are able to perceive the situation we see with our eyes and the contours and overlaps of objects without being conscious of it, but the "Matches Pond" provides passive feedback, which we hope will give the viewer a sense of discomfort from the "discrepancy between human and computer perception" and a sense of "what is it that Okazaki-san is shooting? We hope that the user will feel the discomfort from the "discrepancy between human and computer perception" and wonder "what is Okazaki-san shooting?

- This application was created using 38,890 valid images.




