#!/usr/bin/env python
# coding: utf-8

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

# # 数据准备

# In[27]:


import pandas as pd
import seaborn as sns
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['simhei']
mpl.rcParams['axes.unicode_minus'] = False  


# In[28]:


df = pd.read_excel(r'C:\Users\MrChan\Desktop\酷狗音乐Top500排行榜数据采集+分析\酷狗音乐Top500排行榜.xlsx')
df


# In[29]:


df.info()


# # 描述性统计

# In[30]:


df.describe()


# # 可视化分析

# ## 歌曲时长分布情况

# In[31]:


plt.figure(figsize=(10, 6))
df['时长'] = df['时长'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]))  
plt.hist(df['时长'], bins=30, color='skyblue', edgecolor='black')
plt.title('歌曲时长分布')
plt.xlabel('时长（秒）')
plt.ylabel('歌曲数量')
plt.show()


# ## 歌曲数量排名前10的歌手

# In[32]:


plt.figure(figsize=(10, 5))
top_artists = df['歌手'].value_counts().head(10)
sns.barplot(x=top_artists.values, y=top_artists.index)
plt.title('排名前10位歌手')
plt.xlabel('歌曲数量')
plt.ylabel('歌手')
plt.show()


# ## 排名和时长的分布情况

# In[33]:


plt.figure(figsize=(10, 5))
sns.boxplot(data=df[['排名', '时长']])
plt.title('排名和时长箱型图')
plt.show()


# ## 排名区间内的前十歌手分布

# In[34]:


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


# ## 各歌手歌曲时长分布情况(前10位)

# In[35]:


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


# ## 歌曲词云图

# In[39]:


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


# In[ ]:





# In[ ]:




