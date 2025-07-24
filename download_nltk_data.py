import nltk

def setup():
    """下载必要的NLTK数据"""
    print("正在下载NLTK数据...")
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    print("NLTK数据下载完成！")

if __name__ == "__main__":
    setup()
