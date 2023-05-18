# TSR Dataset Data Augmentation
TSR数据集数据增强共包含两个文件：1.0TSR-DataAugmentation和1.1TSR-DataAugmentation。都具备批量生成图片，批量重写label file的功能。两者主要思路一致，1.0TSR-DataAugmentation是将一张图上所有的标注标志替换为同一个类别的标志marks，即数据增强后一张图上所有标志都为同一个。

1.1TSR-DataAugmentation是进一步升级，不同于前者全部替换，后者是根据原图上的类别，判断是粘贴原类别的marks还是根据规则替换为别的类别的marks，详见论文。两者代码上最大的区别在于重写label file的方式，后者是先将.txt的文件读入为numpy矩阵，更改后，再将矩阵写入.txt文件中。

需要用到的标志marks，详见链接https://www.kaggle.com/datasets/braunge/tt100k-marks。

其余用到的路径，基于自己实际情况进行更改。

1.0TSR-DataAugmentation是基于Version 3数据集进行使用。链接中数据集是使用TSR数据集数据增强后的数据集。
Version 3数据集：https://www.kaggle.com/datasets/braunge/tt100k-reconfigure/versions/2

1.1TSR-DataAugmentation是基于Version 4数据集进行使用。链接中数据集是使用TSR数据集数据增强后的数据集。
Version 4数据集：https://www.kaggle.com/datasets/braunge/tt100k

如需使用自己定义的数据集，更改labels = []。
