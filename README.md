# 随机数后处理算法仿真研究
## 算法
Reversed XOR

Reversed XOR + mLSB

### Differentiation
选取两路独立同分布的做差，可以使得分布关于0对称（i.i.d随机变量X、Y的分布关于0对称）。向右移128即可使得得到的分布关于128对称。这样的话第八位的bias就会为0。

## 性能指标
### Bias
我们要生成均匀分布的8位数序列，那么每个位都应该服从$p=0.5$的伯努利分布。我们定义一个位$x_i$的bias为$\bar x_i$偏离$0.5$的程度，也就是$Bias(x_i) = |\bar x_i - 0.5|$。

## 实验
### 使用NumPy生成的高斯噪声测试不同的算法
下面是不同情况下的测试结果，可以看到，当分布参数$\mu$不为128时，高位有比较大的bias，而当$\mu$正好为128时，高位的bias很小，而其他位的bias比较大。

$\text{Gaussian distribution}, \mu=90, \sigma=30$:
![](/imgs/Bias_1M_gaussian_90_30_(1).png)

$\text{Gaussian distribution}, \mu=120, \sigma=40$:
![](/imgs/Bias_1M_gaussian_120_40_(1).png)

$\text{Gaussian distribution}, \mu=128, \sigma=40$:
![](/imgs/Bias_1M_gaussian_128_40_(1).png)


**结论**：可以看到，Reversed XOR确实改善了不同位的bias不均衡的问题，但是取mLSB似乎不论m为多少时都对bias没有太大的影响。另外，Reversed XOR对于bias没有明显的降低。
