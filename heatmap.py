import numpy as np
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.autograd as autograd
import matplotlib.pyplot as plt

# 使用双线性插值调整大小
interp = nn.Upsample(size=(256, 256), mode='bilinear', align_corners=False)

def normalize_tensor(tensor):
    min_val = tensor.min()
    max_val = tensor.max()
    normalized_tensor = (tensor - min_val) / (max_val - min_val)
    return normalized_tensor

def visualize_heatmap(pred, feature_map, name):
    # pred = F.softmax(pred, dim=1)
    # pred = normalize_tensor(pred)
    # pred = torch.sigmoid(pred)
    x_comp = 39
    y_comp = 39
    pred = pred[:, 0, x_comp, y_comp]
    
    feature = feature_map
    feature_grad = autograd.grad(pred, feature, allow_unused=True, retain_graph=True)[0]
    grads = feature_grad  # 获取梯度
    pooled_grads = torch.nn.functional.adaptive_avg_pool2d(grads, (1, 1))
    # 此处batch size默认为1，所以去掉了第0维（batch size维）
    pooled_grads = pooled_grads[0]
    feature = feature[0]
    # print("pooled_grads:", pooled_grads.shape)
    # print("feature:", feature.shape)
    # feature.shape[0]是指定层feature的通道数
    for i in range(feature.shape[0]):
        feature[i, ...] *= pooled_grads[i, ...]
    heatmap = feature.detach().cpu().numpy()
    heatmap = np.mean(heatmap, axis=0)
    heatmap1 = np.maximum(heatmap, 0)
    heatmap1 /= np.max(heatmap1)
    
    heatmap1 = cv2.resize(heatmap1, (256, 256))
    # heatmap[heatmap < 0.7] = 0
    heatmap1 = np.uint8(255 * heatmap1)
    heatmap1 = cv2.applyColorMap(heatmap1, cv2.COLORMAP_JET)
    heatmap1 = heatmap1[:, :, (2, 1, 0)]

    # fig = plt.figure()
    # 转换为RGB格式
    # heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

    # 保存热力图为 PDF 文件
    plt.figure()
    plt.imshow(heatmap1)
    # plt.imshow(heatmap)
    plt.axis('off')
    plt.savefig(name, bbox_inches='tight', pad_inches=0)
    plt.close()
