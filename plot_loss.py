import os
import json
import matplotlib.pyplot as plt
import numpy as np

def smooth_curve(data, smoothing_factor=0.8):
    smoothed = []
    for i, point in enumerate(data):
        if i == 0:
            smoothed.append(point)
        else:
            smoothed.append(smoothed[-1] * smoothing_factor + point * (1 - smoothing_factor))
    return smoothed

def plot_loss_curves(json_folder, smoothing_factor=0.8):
    # 获取文件夹中所有的 JSON 文件
    json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]

    plt.figure(figsize=(10, 6))  # 设置图形大小

    for json_file in json_files:
        # 打开并读取每个 JSON 文件
        with open(os.path.join(json_folder, json_file), 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 提取 loss 和 epoch 数据
        epochs = []
        losses = []
        for entry in data.get('log_history', []):
            if 'loss' in entry:
                epochs.append(entry['epoch'])
                losses.append(entry['loss'])

        # 如果有 loss 数据，进行平滑处理
        if losses:
            smoothed_losses = smooth_curve(losses, smoothing_factor)
            # 绘制平滑后的 loss 曲线
            plt.plot(epochs, smoothed_losses, label=json_file)

    # 添加图例、标题和标签
    plt.legend()
    plt.title('Loss Curves Comparison (Smoothed)')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')

    # 显示图形
    plt.grid(True)
    plt.show()

# 调用函数并传入存放 JSON 文件的文件夹路径
plot_loss_curves('dataset/train/loss', smoothing_factor=0.9)
