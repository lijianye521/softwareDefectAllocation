

# 跑别人老项目的工作日志

## 1安装环境

使用conda安装python3.5.3 和tensorflow1.1。虽然已经停止维护了这几个，但是应通过conda-forge来下也是可以的。

下面是我的conda的bug环境下的包信息。

> certifi                   2018.8.24             py35_1001    conda-forge
> numpy                     1.18.5                   pypi_0    pypi
> pip                       20.3.4             pyhd8ed1ab_0    conda-forge
> protobuf                  3.19.6                   pypi_0    pypi
> python                    3.5.3                         3    conda-forge
> setuptools                40.4.3                   py35_0    conda-forge
> six                       1.16.0                   pypi_0    pypi
> tensorflow                1.1.0                    pypi_0    pypi
> ucrt                      10.0.22621.0         h57928b3_0    conda-forge
> vc                        14.3                hcf57466_18    conda-forge
> vc14_runtime              14.38.33130         h82b7239_18    conda-forge
> vs2015_runtime            14.38.33130         hcb4865c_18    conda-forge
> werkzeug                  1.0.1                    pypi_0    pypi
> wheel                     0.37.1             pyhd8ed1ab_0    conda-forge
> wincertstore              0.2             pyhd8ed1ab_1009    conda-forge

## 2 分析代码结构

![image-20240307102006801](./assets/image-20240307102006801.png)

他那不可多得的readme

> # TextCNN
>
> 使用CNN进行文本分类，工具为TensorFlow
>
> for i in range(1, 11):
> t = np.loadtxt('class_'+str(i)+'.csv', delimiter=',',dtype=str)
> classes.append(t)
> Eclipse文件分析
> 每个训练集要预测的类别数目
> [259, 571, 873, 1137, 1436, 1692, 1921, 2122, 2310, 2499]
> 每个文件的句子长度
> 194, 217, 220, 222, 222, 225, 229, 231, 234, 236
>
> Mozzila文件分析

这个文件结构应该是bug_dealing是做bug信息预处理的

cnn才是真正他的模块，但是有点乱，不知道哪个才是最终的。这个人的这个代码也是参考的，在它结果csv里面又说

### 2.1 他的引用

![image-20240307154435613](./assets/image-20240307154435613.png)

很好 竟然这个人的代码也是参考了别人的，那我们先瞅瞅这个被参考的项目

https://github.com/yoonkim/CNN_sentence

> ## Convolutional Neural Networks for Sentence Classification
>
> 
>
> Code for the paper [Convolutional Neural Networks for Sentence Classification](http://arxiv.org/abs/1408.5882) (EMNLP 2014).
>
> Runs the model on Pang and Lee's movie review dataset (MR in the paper). Please cite the original paper when using the data.
>
> ### Requirements
>
> 
>
> Code is written in Python (2.7) and requires Theano (0.7).
>
> Using the pre-trained `word2vec` vectors will also require downloading the binary file from https://code.google.com/p/word2vec/
>
> ### Data Preprocessing
>
> 
>
> To process the raw data, run
>
> ```
> python process_data.py path
> ```
>
> 
>
> where path points to the word2vec binary file (i.e. `GoogleNews-vectors-negative300.bin` file). This will create a pickle object called `mr.p` in the same folder, which contains the dataset in the right format.
>
> Note: This will create the dataset with different fold-assignments than was used in the paper. You should still be getting a CV score of >81% with CNN-nonstatic model, though.
>
> ### Running the models (CPU)
>
> 
>
> Example commands:
>
> ```
> THEANO_FLAGS=mode=FAST_RUN,device=cpu,floatX=float32 python conv_net_sentence.py -nonstatic -rand
> THEANO_FLAGS=mode=FAST_RUN,device=cpu,floatX=float32 python conv_net_sentence.py -static -word2vec
> THEANO_FLAGS=mode=FAST_RUN,device=cpu,floatX=float32 python conv_net_sentence.py -nonstatic -word2vec
> ```
>
> 
>
> This will run the CNN-rand, CNN-static, and CNN-nonstatic models respectively in the paper.
>
> ### Using the GPU
>
> 
>
> GPU will result in a good 10x to 20x speed-up, so it is highly recommended. To use the GPU, simply change `device=cpu` to `device=gpu` (or whichever gpu you are using). For example:
>
> ```
> THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python conv_net_sentence.py -nonstatic -word2vec
> ```
>
> 
>
> ### Example output
>
> 
>
> CPU output:
>
> ```
> epoch: 1, training time: 219.72 secs, train perf: 81.79 %, val perf: 79.26 %
> epoch: 2, training time: 219.55 secs, train perf: 82.64 %, val perf: 76.84 %
> epoch: 3, training time: 219.54 secs, train perf: 92.06 %, val perf: 80.95 %
> ```
>
> 
>
> GPU output:
>
> ```
> epoch: 1, training time: 16.49 secs, train perf: 81.80 %, val perf: 78.32 %
> epoch: 2, training time: 16.12 secs, train perf: 82.53 %, val perf: 76.74 %
> epoch: 3, training time: 16.16 secs, train perf: 91.87 %, val perf: 81.37 %
> ```
>
> 
>
> ### Other Implementations
>
> 
>
> #### TensorFlow
>
> 
>
> [Denny Britz](http://www.wildml.com/) has an implementation of the model in TensorFlow:
>
> https://github.com/dennybritz/cnn-text-classification-tf
>
> He also wrote a [nice tutorial](http://www.wildml.com/2015/12/implementing-a-cnn-for-text-classification-in-tensorflow) on it, as well as a general tutorial on [CNNs for NLP](http://www.wildml.com/2015/11/understanding-convolutional-neural-networks-for-nlp).
>
> #### Torch
>
> 
>
> [HarvardNLP](http://harvardnlp.github.io/) group has an implementation in Torch.
>
> https://github.com/harvardnlp/sent-conv-torch
>
> ### Hyperparameters
>
> 
>
> At the time of my original experiments I did not have access to a GPU so I could not run a lot of different experiments. Hence the paper is missing a lot of things like ablation studies and variance in performance, and some of the conclusions were premature (e.g. regularization does not always seem to help).
>
> Ye Zhang has written a [very nice paper](http://arxiv.org/abs/1510.03820) doing an extensive analysis of model variants (e.g. filter widths, k-max pooling, word2vec vs Glove, etc.) and their effect on performance.

看起来他借鉴的这个项目是关于句子分类的这么一个cnn，运行的话只需要，然后 采用的好像是

```shell
python process_data.py path
```

好家伙，竟然是套娃，这个代码是一篇文献的示例代码  （14年纽约大学的一个论文 Convolutional Neural Networks for Sentence Classification）

### 2.2 他引用的引用

https://arxiv.org/pdf/1408.5882v2.pdf

没时间看了，我直接把它喂给了gpt，分析了一下论文结构。

> 这段代码是一个使用TensorFlow框架实现的基于卷积神经网络(CNN)的文本分类示例，目的是对DBpedia数据库中的文本数据进行分类。代码分为几个主要部分，包括数据准备、模型定义、模型训练和评估等。下面是对代码各部分的简要解释：
>
> 1. **数据准备**：使用DBpedia数据集作为训练和测试数据。DBpedia是一个从Wikipedia提取的结构化的内容数据库。代码中通过`tf.contrib.learn.datasets.load_dataset`函数加载数据，然后使用`pandas`库进行数据的预处理。
>
> 2. **词嵌入**：文本数据首先通过词嵌入（embedding）转换成向量形式，这里提供了几种词嵌入方式，包括随机初始化词向量、使用预训练的Word2Vec模型等。词嵌入可以帮助模型理解单词之间的语义关系。
>
> 3. **模型构建**：定义了一个基于CNN的文本分类模型。模型中使用了多个卷积层（convolutional layer）和池化层（pooling layer）来提取文本特征，然后通过全连接层（fully connected layer）进行分类。模型中还包括了dropout和L2正则化来防止过拟合。
>
> 4. **训练和评估**：模型使用`tf.estimator.Estimator`进行训练和评估。通过`train`方法进行模型训练，使用`evaluate`方法对模型进行评估，包括准确度（accuracy）、召回率（recall）、精确度（precision）等指标。
>
> 整体上，这段代码展示了如何使用TensorFlow框架和CNN模型来处理文本分类问题，从数据准备到模型训练和评估，提供了一个完整的实现流程。

### 2.3数据集信息分析

刚开始会发现他的数据集好像和真正引用的不一样，确实是这样，但是想到了他有对数据的预处理。所以一切就豁然开朗。

![image-20240307104813744](.//assets/image-20240307104813744.png)



#### 2.3.1预处理文件结构

```python
bug_sorted_raw.to_csv(data_dir + 'raw/sorted_summary_description.csv', columns=['description', 'summary'], header=False, index=False)
bug_sorted_raw.to_csv(data_dir + 'raw/sorted_bug_id_date_who.csv', columns=['when', 'bug_id', 'who'], index=False)
```

对于缺陷报告中的描述和总结 放在了**summary_description.csv**

对于缺陷报告中bug时间，bugid和bug分配的人用的是**sorted_bug_id_date_who.csv**



然后这个人在cnn/data_helpers.py文件中，对分开的11个文件部分进行了处理，但是需要改一下文件目录的路径，不知道为何文件目录路径与之前的不统一。

#### 2.3.2他的数据预处理



```python
data_files = ['../data/data_by_ocean/eclipse/raw/0_summary_description.csv',
              '../data/data_by_ocean/eclipse/raw/1_summary_description.csv',
              '../data/data_by_ocean/eclipse/raw/2_summary_description.csv',
              '../data/data_by_ocean/eclipse/raw/3_summary_description.csv',
              '../data/data_by_ocean/eclipse/raw/4_summary_description.csv',
              '../data/data_by_ocean/eclipse/raw/5_summary_description.csv',
              '../data/data_by_ocean/eclipse/raw/6_summary_description.csv',
              '../data/data_by_ocean/eclipse/raw/7_summary_description.csv',
              '../data/data_by_ocean/eclipse/raw/8_summary_description.csv']
labels_files = ['../data/data_by_ocean/eclipse/raw/0_bug_id_date_who.csv',
                '../data/data_by_ocean/eclipse/raw/1_bug_id_date_who.csv',
                '../data/data_by_ocean/eclipse/raw/2_bug_id_date_who.csv',
                '../data/data_by_ocean/eclipse/raw/3_bug_id_date_who.csv',
                '../data/data_by_ocean/eclipse/raw/4_bug_id_date_who.csv',
                '../data/data_by_ocean/eclipse/raw/5_bug_id_date_who.csv',
                '../data/data_by_ocean/eclipse/raw/6_bug_id_date_who.csv',
                '../data/data_by_ocean/eclipse/raw/7_bug_id_date_who.csv',
                '../data/data_by_ocean/eclipse/raw/8_bug_id_date_who.csv']
test_data_files = ['../data/data_by_ocean/eclipse/raw/9_summary_description.csv',
                   '../data/data_by_ocean/eclipse/raw/10_summary_description.csv']
test_labels_files = ['../data/data_by_ocean/eclipse/raw/9_bug_id_date_who.csv',
                     '../data/data_by_ocean/eclipse/raw/10_bug_id_date_who.csv']
```

1. **数据文件 (`data_files`)** 和 **标签文件 (`labels_files`)**：这些文件分别存放在`../data/data_by_ocean/eclipse/raw/`目录下，其中数据文件包含了0到8的`summary_description`，标签文件包含了相对应的`bug_id_date_who`信息。这意味着数据文件可能包含有关eclipse项目中某些问题的描述性摘要，而标签文件可能包含与这些问题相关的具体标签信息，如bug的ID、日期和责任人。
2. **测试数据文件 (`test_data_files`)** 和 **测试标签文件 (`test_labels_files`)**：这些文件同样存放在`../data/data_by_ocean/eclipse/raw/`目录下，但是编号为9和10，指定为测试用途。这表明这部分数据可能用于验证或测试模型的性能。

```python
data = []
for data_file in data_files:
    with open(data_file, 'r', encoding='latin-1') as f:
        data.extend([s.strip() for s in f.readlines()])
        data = [clean_str(s) for s in data]
print('train data length: %d' % len(data))
```

> 1. 初始化一个空列表 `data`，用于存储从文件中读取的数据。
> 2. 遍历文件名列表 `data_files`，每次循环处理一个数据文件。
> 3. 使用 `with open(data_file, 'r', encoding='latin-1')` 打开当前的数据文件。这里指定了文件的编码为 'latin-1'，这意味着假定文件中的文本是按照拉丁-1编码存储的。
> 4. 使用 `f.readlines()` 读取文件的所有行，然后通过列表推导式 `[s.strip() for s in f.readlines()]` 去除每行文本首尾的空白字符（包括空格、制表符、换行符等）。
> 5. 通过扩展列表方法 `data.extend([...])`，将处理后的文本行添加到之前初始化的 `data` 列表中。
> 6. 然后，列表推导式 `[clean_str(s) for s in data]` 被用来对 `data` 列表中的每个字符串应用 `clean_str` 函数进行清理。这个步骤的具体作用取决于 `clean_str` 函数的实现，通常是进行如去除或替换特殊字符、统一字符大小写等文本预处理任务。
> 7. 最后，使用 `print` 函数打印出处理后的数据总量，即 `data` 列表的长度。

**目前一切经过我的改写以及路径改写一切顺利，直到遇到了一个问题**

```python
data = pd.read_csv("../data/data_by_ocean/eclipse/sort-text-id.csv", encoding='latin-1')
```

问题代码地址

[DeepTriage/src/cnn/data_helpers.ipynb at master · huazhisong/DeepTriage (github.com)](https://github.com/huazhisong/DeepTriage/blob/master/src/cnn/data_helpers.ipynb)

> [!Caution]
>
> 这个sort-text-id文件 ，我翻遍了所有的预处理python文件都没有这个东西的名字，也就是作者没有给。也不知道是不是原来那个bug_raw.csv变得

我的推测

以这个人的明明规则来看 sort-text-id 看起来是一个有bug id 并有一个description的那么一个，再结合后面的这个代码

```python
x = data.text
y = data.fixer
```

可以得知，x列应该是一段问题描述文本，而y列应该是这个问题或者说这个bug的修复者。

也就是说这个sort-text-id.csv文件至少包含两列，一列是text列，应该是bug描述，另一列是fixer，是bug修复者。

再结合这个data_helper.ipynb的上下文，我觉得这个x列就是文本数据，很可能就是之前的data，而y列就是标签数据，也就是x列是summary_desciption  而y列是bug_id_who这个样子。

### 拟定使用后序处理方案

1. 直接自我生成一个sort-text-id文件，然后继续顺着他的处理历程走一遍。可以通过调用bug-raw.csv文件夹把他们调用出来然后把summary或者description列作为text列，who列作为fixer列。
2. 这个人对源数据的数据处理代码还是不错的，反正数据预处理已经处理的差不多了，他还把文件分成了11份，也方便做测试和训练集。复杂的bug_raw.csv文件也已经搞好了，我就学习一下他后序训练的逻辑，直接使用他的数据集，然后自己编写一个更强大的网络或者调用预训练模型来训练这个数据集。

目前大概是这个样子。