import torch.nn as nn
import torch.fft as fft
import torch

class ARGCCascade(nn.Module):
    def __init__(self):
        super(ARGCCascade, self).__init__()
        self.local_var_conv = nn.Conv2d(1, 1, kernel_size=3, padding=1)
        self.global_mean_conv = nn.Conv2d(1, 1, kernel_size=1)
        self.blur_feature_enhancer_conv1 = nn.Conv2d(1, 1, kernel_size=3, padding=1)
        self.blur_feature_enhancer_conv2 = nn.Conv2d(1, 1, kernel_size=3, padding=1)
        self.sigmoid = nn.Sigmoid()
        self.alpha = nn.Parameter(torch.tensor(1.0))
        self.beta = nn.Parameter(torch.tensor(1.0))

    def forward(self, x):
        import torchvision
        # torchvision.utils.save_image(x, '/home/agou/vv/Medsegdiff/1.png')
        # Decompose RGB channels and compute FFT
        R, G, B = x[:, 0, :, :], x[:, 1, :, :], x[:, 2, :, :]
        F_spec_R = fft.fftn(R)
        F_spec_G = fft.fftn(G)
        F_spec_B = fft.fftn(B)
        
        # Convert complex tensors to float tensors (using magnitude)
        F_spec_R_mag = torch.abs(F_spec_R)
        F_spec_G_mag = torch.abs(F_spec_G)
        F_spec_B_mag = torch.abs(F_spec_B)

        # Compute local variance and global mean for each channel
        local_var_R = self.local_var_conv(F_spec_R_mag.unsqueeze(1)).squeeze(1)
        local_var_G = self.local_var_conv(F_spec_G_mag.unsqueeze(1)).squeeze(1)
        local_var_B = self.local_var_conv(F_spec_B_mag.unsqueeze(1)).squeeze(1)

        global_mean_R = self.global_mean_conv(F_spec_R_mag.unsqueeze(1)).squeeze(1)
        global_mean_G = self.global_mean_conv(F_spec_G_mag.unsqueeze(1)).squeeze(1)
        global_mean_B = self.global_mean_conv(F_spec_B_mag.unsqueeze(1)).squeeze(1)

        # Compute weights for each channel
        weight_R = self.sigmoid(self.alpha * local_var_R + self.beta * global_mean_R)
        weight_G = self.sigmoid(self.alpha * local_var_G + self.beta * global_mean_G)
        weight_B = self.sigmoid(self.alpha * local_var_B + self.beta * global_mean_B)

        # Fuse spectral features with computed weights
        F_fused = weight_R * F_spec_R_mag + weight_G * F_spec_G_mag + weight_B * F_spec_B_mag
        # print(F_fused.shape)
        # print(F_fused)
        # Enhance blur features
        F_enhanced = self.blur_feature_enhancer_conv1(F_fused.unsqueeze(1))
        # print("conv:",F_enhanced.shape)
        # print("conv:",F_enhanced)
        
        G_Br = self.blur_feature_enhancer_conv2(F_fused.unsqueeze(1))
        # print(G_Br.shape)
        # print(G_Br)
        F_enhanced = (F_enhanced * G_Br).squeeze(1)
        # print(F_enhanced.shape)
        # print(F_enhanced)
        # Inverse FFT to get back to spatial domain
        x_bi = fft.ifftn(F_enhanced)
        x_bi_real = x_bi.real
        x_bi_normalized = (x_bi_real - x_bi_real.min()) / (x_bi_real.max() - x_bi_real.min())
        # torchvision.utils.save_image(x_bi_normalized+x, '/home/agou/vv/Medsegdiff/2.png')
        # print(x_bi_normalized.shape)
        x_bi_normalized = x_bi_normalized.unsqueeze(1)
        # print(x.shape)
        # torchvision.utils.save_image(x_bi_normalized+x, '/home/agou/vv/Medsegdiff/2.png')
        return x_bi_normalized+x