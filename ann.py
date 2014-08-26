# import
from PIL import Image
import os
import random

# constants
katakana = ['a', 'i', 'u', 'e', 'o',
            'ka', 'ki', 'ku', 'ke', 'ko',
            'sa', 'shi', 'su', 'se', 'so',
            'ta', 'chi', 'tsu', 'te', 'to',
            'na', 'ni', 'nu', 'ne', 'no',
            'ha', 'hi', 'fu', 'he', 'ho',
            'ma', 'mi', 'mu', 'me', 'mo',
            'ya', 'yu', 'yo',
            'ra', 'ri', 'ru', 're', 'ro',
            'wa', 'wo', 'n']

# variables
base = "data\\"
dirs = ["computer (gray)\\", "natural (good)\\"]

# learning rate decreases over time
a = 2.0

# classes
class ANN:
    def __init__(self):
        """3 layer network - input (16 x 16 image), hidden, and output (kana)"""
        self.arch = [256, 256, 46]
        self.inter = [[] for a in self.arch]
    def train(self, itr):
        """neural network training - reads input data, randomizes weight matrix, then iteratively trains itself"""
        self.read()
        self.rand()
        self.iterate(itr)
        
    def iterate(self, itr):
        """iteratively train for itr rounds"""
        for i in range(itr):
            print("Iteration: " + str(i + 1))
            for data in self.input:
                error = 0
                for kana, ans in zip(data, [[0 if m != k else 1 for m in range(len(katakana))] for k in range(len(katakana))]):
                    self.foreprop(permute(kana))
                    delta = [a - b for a, b in zip(ans, self.output)]
                    global a
                    a = 1 / (i + 1)
                    error += sum([d * d / 2 for d in delta])
                    self.backprop(delta)
                print(" Total error: " + str(error)[0:6])
    def read(self):
        """get image data, return: [[[ 0 - 255 | pixel] | kana] | dataset]"""
        print("reading input data")
        self.input = []
        for d in dirs:
            for f in os.listdir(base + d):
                kanadata = []
                for k in katakana:
                    img = Image.open(base + d + f + "\\" + k + "_norm.png")
                    kanadata.append(self.parse(img))
                self.input.append(kanadata)
        #return self.input
    def parse(self, img):
        """process image, return flat list of pixel values"""
        img = img.convert("RGBA").convert("LA")
        return [255 - img.getpixel((x, y))[0] for y in range(img.size[1]) for x in range(img.size[0])]
    def rand(self):
        """generate matrix of randomized weights, return: [[[weight] | neuron] | layer]"""
        print("randomizing weights")
        self.weights = [[[(0.5 - random.random()) for j in range(self.arch[l + 1])] for i in range(self.arch[l])] for l in range(len(self.arch) - 1)]
        #return self.weights
    def foreprop(self, data):
        """forward propogation, keep intermediate results, returns results as list"""
        self.output = [self.act(i - 100) for i in data]
        self.inter[0] = self.output
        for l in range(len(self.arch) - 1):
            self.output = [self.act(sum([self.output[i] * self.weights[l][i][j] for i in range(self.arch[l])])) for j in range(self.arch[l + 1])]
            self.inter[l + 1] = self.output
        #return self.output
    def act(self, x):
        """activation function (logistic), returns: 1 / (1 + e ^ -x)"""
        return 1 / (1 + 2.7182818284 ** -x)
    def backprop(self, delta):
        """back propogation, update weights"""
        for l in range(len(self.arch) - 2, -1, -1):
            delta = [d * a * (1 - a) for a, d in zip(self.inter[l], delta)]
            self.weights[l], delta = (
                [[self.weights[l][i][j] + a * delta[j] * self.inter[l][i] for j in range(self.arch[l + 1])] for i in range(self.arch[l])], 
                [sum([delta[k] * self.weights[l][i][k] for k in range(self.arch[l + 1])]) for i in range(self.arch[l])])
        #return self.weights
    def classify(self, kana):
        """classify kana, given data, based on forward propogation results"""
        self.foreprop(kana)
        results = list(zip(self.output, [i for i in range(0, len(katakana))]))
        results.sort()
        results.reverse()
        classes = list(map(lambda x : x[1], results))[0 : 5]
        print(", ".join([katakana[c] + " (" + str(self.output[c] * 100)[0:4] + "%)" for c in classes]))
        return classes
    def output(self):
        """print model data in text format"""
        print("Arch: " + ", ".join([str(a) for a in self.arch]))
        for i, weight in zip(list(range(len(self.weights))), self.weights):
            print("\nLayer " + str(i + 1) + " \n")
            for neuron in weight:
                print(neuron)
    def load(self, model):
        """load model from textual data"""
        text = open("model\\" + model + ".txt")
        layer = -1
        while(text.readable()):
            line = text.readline()
            if "Arch:" in line:
                self.arch = [int(a) for a in line[6:-1].split(", ")]
                self.weights = [[] for a in range(len(self.arch) - 1)]
            elif "Layer" in line:
                layer = int(line[6:-1])
            elif (len(line) > 1 and layer != -1):
                self.weights[layer - 1].append([float(w) for w in line.strip("[] \n").split(",")])
            elif line == "":
                return

def edge(sums):
    """calculates number of pixels on edge of image w/ empty space"""
    for i in range(16):
        if sums[i] > 300:
            return i
    return 0

def trans(kana):
    """50% chance of applying translational permutation to kana"""
    if (random.random() < 0.5):
        return kana

    xmin = edge([sum([kana[y][x] for y in range(16)]) for x in range(16)])
    xmax = edge([sum([kana[y][15 - x] for y in range(16)]) for x in range(16)])
    ymin = edge([sum([kana[y][x] for x in range(16)]) for y in range(16)])
    ymax = edge([sum([kana[15 - y][x] for x in range(16)]) for y in range(16)])
    
    dx = random.randint(-xmin, xmax)
    dy = random.randint(-ymin, ymax)

    return [[kana[y + dy][x + dx] if 0 <= y + dy < 16 and 0 <= x + dx < 16 else 0 for x in range(16)] for y in range(16)]

def permute(kana):
    """randomly permute kana matrix"""
    grid = [[kana[j * 16 + i] for i in range(16)] for j in range(16)]
    grid = trans(grid)
    return [grid[i][j] for i in range(16) for j in range(16)]

def test():
    ann.classify(ann.parse(Image.open("test.png")))

def classify_test(dataset):
    for i in range(len(katakana)):
        print("classifying: " + katakana[i])
        ann.classify(ann.input[dataset][i])

if __name__ == "__main__":
    ann = ANN()
    ann.train(30)
