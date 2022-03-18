from dezero import Layer
from dezero import utils
import dezero.functions as F 
import dezero.layers as L 

class Model(Layer):
    def plot(self, *inputs, to_file='model.png'):
        y = self.forward(*inputs)
        return utils.plot_dot_graph(y, verbose=True, to_file=to_file)

class MLP(Model):
    def __init__(self, fc_out_sizes, activation=F.sigmoid):
        super().__init__()
        self.activation = activation
        self.layers = []

        for i, out_size in enumerate(fc_out_sizes):
            layer = L.Linear(out_size)
            setattr(self, 'l'+str(i), layer)
            self.layers.append(layer)

    def forward(self, x):
        for l in self.layers[:-1]:
            x = self.activation(l(x))
        return self.layers[-1](x)

class VGG16(Model):
    WEIGHT_PATH = 'https://github.com/koki0702/dezero-models/releases/download/v0.1/vgg16.npz'

    def __init__(self, pretrained=False):
        super().__init__()
        if pretrained:
            weights_path = utils.get_file(VGG16.WEIGHT_PATH)
            self.load_weights(weights_path)

        self.conv1_1 = L.Conv2d(64, kernel_size = 3, stride = 1, pad = 1)
        self.conv1_2 = L.Conv2d(64, kernel_size = 3, stride = 1, pad = 1)
        self.conv2_1 = L.Conv2d(128, kernel_size = 3, stride = 1, pad = 1)
        self.conv2_2 = L.Conv2d(128, kernel_size = 3, stride = 1, pad = 1)
        self.conv3_1 = L.Conv2d(256, kernel_size = 3, stride = 1, pad = 1)
        self.conv3_2 = L.Conv2d(256, kernel_size = 3, stride = 1, pad = 1)
        self.conv3_3 = L.Conv2d(256, kernel_size = 3, stride = 1, pad = 1)
        self.conv4_1 = L.Conv2d(512, kernel_size = 3, stride = 1, pad = 1)
        self.conv4_2 = L.Conv2d(512, kernel_size = 3, stride = 1, pad = 1)
        self.conv4_3 = L.Conv2d(512, kernel_size = 3, stride = 1, pad = 1)
        self.conv5_1 = L.Conv2d(512, kernel_size = 3, stride = 1, pad = 1)
        self.conv5_2 = L.Conv2d(512, kernel_size = 3, stride = 1, pad = 1)
        self.conv5_3 = L.Conv2d(512, kernel_size = 3, stride = 1, pad = 1)
        self.fc6 = L.Linear(4096)
        self.fc7 = L.Linear(4096)
        self.fc8 = L.Linear(1000)

    def forward(self,x):
        x = F.relu(self.conv1_1(x))
        x = F.relu(self.conv1_2(x))
        x = F.C.pooling(x,2,2)
        x = F.relu(self.conv2_1(x))
        x = F.relu(self.conv2_2(x))
        x = F.C.pooling(x,2,2)
        x = F.relu(self.conv3_1(x))
        x = F.relu(self.conv3_2(x))
        x = F.relu(self.conv3_3(x))
        x = F.C.pooling(x,2,2)
        x = F.relu(self.conv4_1(x))
        x = F.relu(self.conv4_2(x))
        x = F.relu(self.conv4_3(x))
        x = F.C.pooling(x,2,2)
        x = F.relu(self.conv5_1(x))
        x = F.relu(self.conv5_2(x))
        x = F.relu(self.conv5_3(x)) 
        x = F.C.pooling(x,2,2)
        x = F.reshape(x, (x.shape[0],-1))
        x = F.dropout(F.relu(self.fc6(x)))
        x = F.dropout(F.relu(self.fc7(x)))
        x = self.fc8(x)
        return x 