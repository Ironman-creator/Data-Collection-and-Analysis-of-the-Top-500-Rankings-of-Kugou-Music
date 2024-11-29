
# # 目录
# 
# - [数据准备](#数据准备)
# - [描述性统计](#描述性统计)
# - [可视化分析](#可视化分析)
#     - [歌曲时长分布情况](#歌曲时长分布情况)
#     - [歌曲数量排名前10的歌手](#歌曲数量排名前10的歌手)
#     - [排名和时长的分布情况](#排名和时长的分布情况)
#     - [排名区间内的前十歌手分布](#排名区间内的前十歌手分布)
#     - [各歌手歌曲时长分布情况(前10位)](#各歌手歌曲时长分布情况(前10位))
#     - [歌曲词云图](#歌曲词云图)


# 一、导入必要的库并设置中文字体显示
# pandas（pd）：用于数据读取、处理和分析。
# seaborn（sns）：基于matplotlib的高级数据可视化库，能创建更美观、更具信息性的统计图表。
# numpy（np）：用于数值计算，在数据处理和一些可视化操作中可能会用到。
# PIL（from PIL import Image）：Python
# Imaging
# Library，用于处理图像相关的操作，虽然在这段代码中未详细体现其图像处理功能，但在生成词云图时可能会涉及到一些底层的图像相关设置。
# matplotlib.pyplot（plt）：用于创建各种静态、动态、交互式的可视化图表。
# WordCloud：用于生成词云图，以直观展示文本数据中词语的出现频率等信息。
import pandas as pd
import seaborn as sns
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['simhei']
mpl.rcParams['axes.unicode_minus'] = False  


# 二、数据读取与初步查看
# 首先使用pandas的read_excel函数从指定路径读取一个 Excel 文件（酷狗音乐 Top500 排行榜数据），并将数据存储在一个名为df的DataFrame对象中。
# 然后通过df.info()查看数据框的基本信息，包括列名、数据类型、非空值数量等，有助于了解数据的整体结构和完整性。
# 接着使用df.describe()对数据框中的数值型列进行描述性统计分析，如计算均值、标准差、最小值、最大值、四分位数等，以便快速了解数据的分布特征。
df = pd.read_excel(r'C:\Users\MrChan\Desktop\酷狗音乐Top500排行榜数据采集+分析\酷狗音乐Top500排行榜.xlsx')
df.info()
df.describe()


# 三、可视化分析 - 歌曲时长分布情况
# 首先创建一个新的matplotlib图形对象，并设置图形的大小为宽度 10 英寸、高度 6 英寸（plt.figure(figsize=(10, 6))）。
# 然后对数据框df中的时长列进行数据转换，将原本以分:秒格式表示的时长字符串转换为以秒为单位的整数。通过apply方法结合一个匿名函数（lambda函数）实现，先将时长字符串按:分割，然后将分钟数乘以 60 再加上秒数得到总秒数。
# 接着使用plt.hist函数绘制直方图，以展示歌曲时长的分布情况。bins=30指定了将数据划分为 30 个区间来统计每个区间内歌曲的数量，color='skyblue'设置了直方图的填充颜色，edgecolor='black'设置了直方图边框的颜色。
# 最后设置图表的标题（plt.title）、x 轴标签（plt.xlabel）和 y 轴标签（plt.ylabel），并通过plt.show()显示绘制好的图表。
plt.figure(figsize=(10, 6))
df['时长'] = df['时长'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]))  
plt.hist(df['时长'], bins=30, color='skyblue', edgecolor='black')
plt.title('歌曲时长分布')
plt.xlabel('时长（秒）')
plt.ylabel('歌曲数量')
plt.show()


# 四、可视化分析 - 歌曲数量排名前 10 的歌手
# 同样先创建一个大小为宽度 10 英寸、高度 5 英寸的matplotlib图形对象。
# 通过df['歌手'].value_counts().head(10)统计数据框中每个歌手出现的次数（即演唱歌曲的数量），并取前 10 名歌手，将结果存储在top_artists中。
# 使用seaborn的barplot函数绘制柱状图，其中x轴为歌手演唱歌曲的数量（top_artists.values），y轴为歌手名字（top_artists.index），这样可以直观地展示出排名前 10 的歌手及其演唱歌曲的数量。
# 设置图表的标题、x 轴标签和 y 轴标签，最后通过plt.show()显示图表。
plt.figure(figsize=(10, 5))
top_artists = df['歌手'].value_counts().head(10)
sns.barplot(x=top_artists.values, y=top_artists.index)
plt.title('排名前10位歌手')
plt.xlabel('歌曲数量')
plt.ylabel('歌手')
plt.show()

# 五、可视化分析 - 排名和时长的分布情况
# 创建一个宽度 10 英寸、高度 5 英寸的matplotlib图形对象。
# 使用seaborn的boxplot函数绘制箱型图，用于展示数据框df中排名和时长这两个变量的分布情况。箱型图可以直观地显示出数据的中位数、四分位数、异常值等信息。
# 设置图表的标题，然后通过plt.show()显示图表。
plt.figure(figsize=(10, 5))
sns.boxplot(data=df[['排名', '时长']])
plt.title('排名和时长箱型图')
plt.show()


# 六、可视化分析 - 排名区间内的前十歌手分布
# 首先使用pd.cut函数对数据框df中的排名列进行分组操作，根据指定的区间（bins）将排名划分为不同的组，并为每个组赋予对应的标签（labels），如Top 10、11-20等，将分组结果存储在新创建的Rank Group列中。
# 通过df['歌手'].value_counts().head(10)获取演唱歌曲数量排名前 10 的歌手，然后使用df[df['歌手'].isin(top_artists.index)]筛选出数据框中属于这前 10 名歌手的数据，存储在df_top_artists中。
# 创建一个宽度 10 英寸、高度 5 英寸的matplotlib图形对象，然后使用seaborn的countplot函数绘制计数图，以展示在不同排名区间内前 10 名歌手的歌曲数量分布情况。x轴为排名区间（Rank Group），hue为歌手，通过不同颜色区分不同歌手在各个排名区间内的歌曲数量。
# 设置图表的标题、x 轴标签和 y 轴标签，并通过plt.legend设置图例的标题以及其在图形中的位置（通过bbox_to_anchor和loc参数），最后通过plt.show()显示图表。
df['Rank Group'] = pd.cut(df['排名'], bins=[0, 10, 20, 30, 40, 500], labels=['Top 10', '11-20', '21-30', '31-40', '41+'])

top_artists = df['歌手'].value_counts().head(10)
df_top_artists = df[df['歌手'].isin(top_artists.index)]

plt.figure(figsize=(10, 5))
sns.countplot(x='Rank Group', hue='歌手', data=df_top_artists)
plt.title('排名区间内的歌手分布（前10位歌手）')
plt.xlabel('排名区间')
plt.ylabel('歌曲数量')
plt.legend(title='歌手', bbox_to_anchor=(1.05, 1), loc=2)
plt.show()


# 七、可视化分析 - 各歌手歌曲时长分布情况 (前 10 位)
# 首先通过df['歌手'].value_counts().head(10).index获取演唱歌曲数量排名前 10 的歌手的名字索引，然后使用df[df['歌手'].isin(top_artists.index)]筛选出数据框中属于这前 10 名歌手的数据，存储在filtered_df中。
# 使用seaborn的color_palette函数获取一个指定颜色方案（husl）的调色板，颜色数量与排名前 10 的歌手数量相同，将其存储在palette_colors中。
# 创建一个宽度 12 英寸、高度 6 英寸的matplotlib图形对象，然后使用seaborn的violinplot函数绘制小提琴图，以展示排名前 10 的歌手的歌曲时长分布情况。x轴为歌手，y轴为时长（以秒为单位），inner="quartile"指定了小提琴图内部的显示方式为四分位数，hue='歌手'通过不同颜色区分不同歌手的歌曲时长分布，palette=palette_colors使用之前获取的调色板设置颜色，legend=False表示不显示图例（因为通过颜色区分歌手已经很清晰）。
# 设置图表的标题、x 轴标签和 y 轴标签，并通过plt.xticks(rotation=90)将 x 轴标签旋转 90 度以便更好地显示，最后通过plt.show()显示图表。
top_artists = df['歌手'].value_counts().head(10).index
filtered_df = df[df['歌手'].isin(top_artists)]
palette_colors = sns.color_palette('husl', len(top_artists))
plt.figure(figsize=(12, 6))
sns.violinplot(
    x='歌手', 
    y='时长', 
    data=filtered_df, 
    inner="quartile",
    hue='歌手',  
    palette=palette_colors,  
    legend=False  
)
plt.title('各歌手歌曲时长分布')
plt.xlabel('歌手')
plt.ylabel('时长（秒）')
plt.xticks(rotation=90)
plt.show()


# 八、可视化分析 - 歌曲词云图
# 首先导入相关库用于生成词云图。
# 将数据框df中的歌曲列的值转换为列表（song_names = df['歌曲'].tolist()），然后通过join函数将列表中的歌曲名称连接成一个字符串（text = ' '.join(song_names)），作为生成词云图的文本数据。
# 指定词云图的字体路径为simhei.ttf，设置背景颜色为白色，宽度为 800 像素，高度为 400 像素，然后使用WordCloud类的generate方法根据提供的文本数据生成词云图，将结果存储在wordcloud中。
# 创建一个宽度 10 英寸、高度 5 英寸的matplotlib图形对象，然后通过plt.imshow显示词云图，interpolation='bilinear'指定了图像显示的插值方式，plt.axis('off')关闭坐标轴显示，最后通过plt.show()显示图表。
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image
font_path =r'C:/Windows/Fonts/msyh.ttc'
song_names = df['歌曲'].tolist()
text = ' '.join(song_names)
font_path = 'simhei.ttf'  
wordcloud = WordCloud(
    font_path=font_path,  
    background_color='white',
    width=800,
    height=400
).generate(text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  
plt.show()











