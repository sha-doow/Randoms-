{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyN0ZRpOC9L6Y5onZc0gxWIW",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/sha-doow/ML/blob/main/Transformer.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "xXQ0CohKVoFm",
        "outputId": "eab7de6f-cdeb-48a2-ca9c-7369bdfd2e4a"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "--2024-06-21 00:56:55--  https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt\n",
            "Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.108.133, 185.199.109.133, 185.199.110.133, ...\n",
            "Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.108.133|:443... connected.\n",
            "HTTP request sent, awaiting response... 200 OK\n",
            "Length: 1115394 (1.1M) [text/plain]\n",
            "Saving to: ‘input.txt’\n",
            "\n",
            "input.txt           100%[===================>]   1.06M  --.-KB/s    in 0.04s   \n",
            "\n",
            "2024-06-21 00:56:56 (29.1 MB/s) - ‘input.txt’ saved [1115394/1115394]\n",
            "\n"
          ]
        }
      ],
      "source": [
        "# We always start with a dataset to train on. Let's download the tiny shakespeare dataset\n",
        "!wget https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# read it in to inspect it\n",
        "with open('input.txt', 'r', encoding='utf-8') as f:\n",
        "    text = f.read()"
      ],
      "metadata": {
        "id": "-_z6wUedVrxa"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "print(\"length of dataset in characters: \", len(text))"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "LJRbMqXFVuSj",
        "outputId": "9732d5f4-7f09-4d66-b01a-83bc4b0e06b1"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "length of dataset in characters:  1115394\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# let's look at the first 1000 characters\n",
        "print(text[:1000])"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "8f_3W_xaVxXE",
        "outputId": "9a062555-78f6-4313-b38d-9e4aef5480ee"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "First Citizen:\n",
            "Before we proceed any further, hear me speak.\n",
            "\n",
            "All:\n",
            "Speak, speak.\n",
            "\n",
            "First Citizen:\n",
            "You are all resolved rather to die than to famish?\n",
            "\n",
            "All:\n",
            "Resolved. resolved.\n",
            "\n",
            "First Citizen:\n",
            "First, you know Caius Marcius is chief enemy to the people.\n",
            "\n",
            "All:\n",
            "We know't, we know't.\n",
            "\n",
            "First Citizen:\n",
            "Let us kill him, and we'll have corn at our own price.\n",
            "Is't a verdict?\n",
            "\n",
            "All:\n",
            "No more talking on't; let it be done: away, away!\n",
            "\n",
            "Second Citizen:\n",
            "One word, good citizens.\n",
            "\n",
            "First Citizen:\n",
            "We are accounted poor citizens, the patricians good.\n",
            "What authority surfeits on would relieve us: if they\n",
            "would yield us but the superfluity, while it were\n",
            "wholesome, we might guess they relieved us humanely;\n",
            "but they think we are too dear: the leanness that\n",
            "afflicts us, the object of our misery, is as an\n",
            "inventory to particularise their abundance; our\n",
            "sufferance is a gain to them Let us revenge this with\n",
            "our pikes, ere we become rakes: for the gods know I\n",
            "speak this in hunger for bread, not in thirst for revenge.\n",
            "\n",
            "\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# here are all the unique characters that occur in this text\n",
        "chars = sorted(list(set(text)))\n",
        "vocab_size = len(chars)\n",
        "print(''.join(chars))\n",
        "print(vocab_size)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "46ssgnFyVzLA",
        "outputId": "16a70253-ebbc-4e00-ff8f-f03f8fba4ccb"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            " !$&',-.3:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\n",
            "65\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# create a mapping from characters to integers\n",
        "stoi = { ch:i for i,ch in enumerate(chars) }\n",
        "itos = { i:ch for i,ch in enumerate(chars) }\n",
        "encode = lambda s: [stoi[c] for c in s] # encoder: take a string, output a list of integers\n",
        "decode = lambda l: ''.join([itos[i] for i in l]) # decoder: take a list of integers, output a string\n",
        "\n",
        "print(encode(\"olamide\"))\n",
        "print(decode(encode(\"olamide\")))"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "sihT_3e4V1tw",
        "outputId": "dd467824-4c06-4132-c972-779e26f41ac1"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "[53, 50, 39, 51, 47, 42, 43]\n",
            "olamide\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# let's now encode the entire text dataset and store it into a torch.Tensor\n",
        "import torch # we use PyTorch: https://pytorch.org\n",
        "data = torch.tensor(encode(text), dtype=torch.long)\n",
        "print(data.shape, data.dtype)\n",
        "print(data[:1000]) # the 1000 characters we looked at earier will to the GPT look like this"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "N0oXvrRMV6DX",
        "outputId": "14c11b03-f37c-4489-cdfb-eb9e5d103a36"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "torch.Size([1115394]) torch.int64\n",
            "tensor([18, 47, 56, 57, 58,  1, 15, 47, 58, 47, 64, 43, 52, 10,  0, 14, 43, 44,\n",
            "        53, 56, 43,  1, 61, 43,  1, 54, 56, 53, 41, 43, 43, 42,  1, 39, 52, 63,\n",
            "         1, 44, 59, 56, 58, 46, 43, 56,  6,  1, 46, 43, 39, 56,  1, 51, 43,  1,\n",
            "        57, 54, 43, 39, 49,  8,  0,  0, 13, 50, 50, 10,  0, 31, 54, 43, 39, 49,\n",
            "         6,  1, 57, 54, 43, 39, 49,  8,  0,  0, 18, 47, 56, 57, 58,  1, 15, 47,\n",
            "        58, 47, 64, 43, 52, 10,  0, 37, 53, 59,  1, 39, 56, 43,  1, 39, 50, 50,\n",
            "         1, 56, 43, 57, 53, 50, 60, 43, 42,  1, 56, 39, 58, 46, 43, 56,  1, 58,\n",
            "        53,  1, 42, 47, 43,  1, 58, 46, 39, 52,  1, 58, 53,  1, 44, 39, 51, 47,\n",
            "        57, 46, 12,  0,  0, 13, 50, 50, 10,  0, 30, 43, 57, 53, 50, 60, 43, 42,\n",
            "         8,  1, 56, 43, 57, 53, 50, 60, 43, 42,  8,  0,  0, 18, 47, 56, 57, 58,\n",
            "         1, 15, 47, 58, 47, 64, 43, 52, 10,  0, 18, 47, 56, 57, 58,  6,  1, 63,\n",
            "        53, 59,  1, 49, 52, 53, 61,  1, 15, 39, 47, 59, 57,  1, 25, 39, 56, 41,\n",
            "        47, 59, 57,  1, 47, 57,  1, 41, 46, 47, 43, 44,  1, 43, 52, 43, 51, 63,\n",
            "         1, 58, 53,  1, 58, 46, 43,  1, 54, 43, 53, 54, 50, 43,  8,  0,  0, 13,\n",
            "        50, 50, 10,  0, 35, 43,  1, 49, 52, 53, 61,  5, 58,  6,  1, 61, 43,  1,\n",
            "        49, 52, 53, 61,  5, 58,  8,  0,  0, 18, 47, 56, 57, 58,  1, 15, 47, 58,\n",
            "        47, 64, 43, 52, 10,  0, 24, 43, 58,  1, 59, 57,  1, 49, 47, 50, 50,  1,\n",
            "        46, 47, 51,  6,  1, 39, 52, 42,  1, 61, 43,  5, 50, 50,  1, 46, 39, 60,\n",
            "        43,  1, 41, 53, 56, 52,  1, 39, 58,  1, 53, 59, 56,  1, 53, 61, 52,  1,\n",
            "        54, 56, 47, 41, 43,  8,  0, 21, 57,  5, 58,  1, 39,  1, 60, 43, 56, 42,\n",
            "        47, 41, 58, 12,  0,  0, 13, 50, 50, 10,  0, 26, 53,  1, 51, 53, 56, 43,\n",
            "         1, 58, 39, 50, 49, 47, 52, 45,  1, 53, 52,  5, 58, 11,  1, 50, 43, 58,\n",
            "         1, 47, 58,  1, 40, 43,  1, 42, 53, 52, 43, 10,  1, 39, 61, 39, 63,  6,\n",
            "         1, 39, 61, 39, 63,  2,  0,  0, 31, 43, 41, 53, 52, 42,  1, 15, 47, 58,\n",
            "        47, 64, 43, 52, 10,  0, 27, 52, 43,  1, 61, 53, 56, 42,  6,  1, 45, 53,\n",
            "        53, 42,  1, 41, 47, 58, 47, 64, 43, 52, 57,  8,  0,  0, 18, 47, 56, 57,\n",
            "        58,  1, 15, 47, 58, 47, 64, 43, 52, 10,  0, 35, 43,  1, 39, 56, 43,  1,\n",
            "        39, 41, 41, 53, 59, 52, 58, 43, 42,  1, 54, 53, 53, 56,  1, 41, 47, 58,\n",
            "        47, 64, 43, 52, 57,  6,  1, 58, 46, 43,  1, 54, 39, 58, 56, 47, 41, 47,\n",
            "        39, 52, 57,  1, 45, 53, 53, 42,  8,  0, 35, 46, 39, 58,  1, 39, 59, 58,\n",
            "        46, 53, 56, 47, 58, 63,  1, 57, 59, 56, 44, 43, 47, 58, 57,  1, 53, 52,\n",
            "         1, 61, 53, 59, 50, 42,  1, 56, 43, 50, 47, 43, 60, 43,  1, 59, 57, 10,\n",
            "         1, 47, 44,  1, 58, 46, 43, 63,  0, 61, 53, 59, 50, 42,  1, 63, 47, 43,\n",
            "        50, 42,  1, 59, 57,  1, 40, 59, 58,  1, 58, 46, 43,  1, 57, 59, 54, 43,\n",
            "        56, 44, 50, 59, 47, 58, 63,  6,  1, 61, 46, 47, 50, 43,  1, 47, 58,  1,\n",
            "        61, 43, 56, 43,  0, 61, 46, 53, 50, 43, 57, 53, 51, 43,  6,  1, 61, 43,\n",
            "         1, 51, 47, 45, 46, 58,  1, 45, 59, 43, 57, 57,  1, 58, 46, 43, 63,  1,\n",
            "        56, 43, 50, 47, 43, 60, 43, 42,  1, 59, 57,  1, 46, 59, 51, 39, 52, 43,\n",
            "        50, 63, 11,  0, 40, 59, 58,  1, 58, 46, 43, 63,  1, 58, 46, 47, 52, 49,\n",
            "         1, 61, 43,  1, 39, 56, 43,  1, 58, 53, 53,  1, 42, 43, 39, 56, 10,  1,\n",
            "        58, 46, 43,  1, 50, 43, 39, 52, 52, 43, 57, 57,  1, 58, 46, 39, 58,  0,\n",
            "        39, 44, 44, 50, 47, 41, 58, 57,  1, 59, 57,  6,  1, 58, 46, 43,  1, 53,\n",
            "        40, 48, 43, 41, 58,  1, 53, 44,  1, 53, 59, 56,  1, 51, 47, 57, 43, 56,\n",
            "        63,  6,  1, 47, 57,  1, 39, 57,  1, 39, 52,  0, 47, 52, 60, 43, 52, 58,\n",
            "        53, 56, 63,  1, 58, 53,  1, 54, 39, 56, 58, 47, 41, 59, 50, 39, 56, 47,\n",
            "        57, 43,  1, 58, 46, 43, 47, 56,  1, 39, 40, 59, 52, 42, 39, 52, 41, 43,\n",
            "        11,  1, 53, 59, 56,  0, 57, 59, 44, 44, 43, 56, 39, 52, 41, 43,  1, 47,\n",
            "        57,  1, 39,  1, 45, 39, 47, 52,  1, 58, 53,  1, 58, 46, 43, 51,  1, 24,\n",
            "        43, 58,  1, 59, 57,  1, 56, 43, 60, 43, 52, 45, 43,  1, 58, 46, 47, 57,\n",
            "         1, 61, 47, 58, 46,  0, 53, 59, 56,  1, 54, 47, 49, 43, 57,  6,  1, 43,\n",
            "        56, 43,  1, 61, 43,  1, 40, 43, 41, 53, 51, 43,  1, 56, 39, 49, 43, 57,\n",
            "        10,  1, 44, 53, 56,  1, 58, 46, 43,  1, 45, 53, 42, 57,  1, 49, 52, 53,\n",
            "        61,  1, 21,  0, 57, 54, 43, 39, 49,  1, 58, 46, 47, 57,  1, 47, 52,  1,\n",
            "        46, 59, 52, 45, 43, 56,  1, 44, 53, 56,  1, 40, 56, 43, 39, 42,  6,  1,\n",
            "        52, 53, 58,  1, 47, 52,  1, 58, 46, 47, 56, 57, 58,  1, 44, 53, 56,  1,\n",
            "        56, 43, 60, 43, 52, 45, 43,  8,  0,  0])\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Let's now split up the data into train and validation sets\n",
        "n = int(0.9*len(data)) # first 90% will be train, rest val\n",
        "train_data = data[:n]\n",
        "val_data = data[n:]"
      ],
      "metadata": {
        "id": "7Trju7LyV-fe"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "block_size = 8\n",
        "train_data[:block_size+1]"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "IiAxLTgdWOCF",
        "outputId": "d5f65627-8ed0-4767-c49b-d5c41d34b588"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "tensor([18, 47, 56, 57, 58,  1, 15, 47, 58])"
            ]
          },
          "metadata": {},
          "execution_count": 10
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "x = train_data[:block_size]\n",
        "y = train_data[1:block_size+1]\n",
        "for t in range(block_size):\n",
        "    context = x[:t+1]\n",
        "    target = y[t]\n",
        "    print(f\"when input is {context} the target: {target}\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "6cHcJ7ohWPt1",
        "outputId": "f10fc1bb-7ead-44e7-fe55-c6199b38bfe9"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "when input is tensor([18]) the target: 47\n",
            "when input is tensor([18, 47]) the target: 56\n",
            "when input is tensor([18, 47, 56]) the target: 57\n",
            "when input is tensor([18, 47, 56, 57]) the target: 58\n",
            "when input is tensor([18, 47, 56, 57, 58]) the target: 1\n",
            "when input is tensor([18, 47, 56, 57, 58,  1]) the target: 15\n",
            "when input is tensor([18, 47, 56, 57, 58,  1, 15]) the target: 47\n",
            "when input is tensor([18, 47, 56, 57, 58,  1, 15, 47]) the target: 58\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "torch.manual_seed(1337)\n",
        "batch_size = 4 # how many independent sequences will we process in parallel?\n",
        "block_size = 8 # what is the maximum context length for predictions?\n",
        "\n",
        "def get_batch(split):\n",
        "    # generate a small batch of data of inputs x and targets y\n",
        "    data = train_data if split == 'train' else val_data\n",
        "    ix = torch.randint(len(data) - block_size, (batch_size,))\n",
        "    x = torch.stack([data[i:i+block_size] for i in ix])\n",
        "    y = torch.stack([data[i+1:i+block_size+1] for i in ix])\n",
        "    return x, y\n",
        "\n",
        "xb, yb = get_batch('train')\n",
        "print('inputs:')\n",
        "print(xb.shape)\n",
        "print(xb)\n",
        "print('targets:')\n",
        "print(yb.shape)\n",
        "print(yb)\n",
        "\n",
        "print('----')\n",
        "\n",
        "for b in range(batch_size): # batch dimension\n",
        "    for t in range(block_size): # time dimension\n",
        "        context = xb[b, :t+1]\n",
        "        target = yb[b,t]\n",
        "        print(f\"when input is {context.tolist()} the target: {target}\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "UiamVP9pWRft",
        "outputId": "16b5be66-0166-4484-e95b-af5b0fb008fc"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "inputs:\n",
            "torch.Size([4, 8])\n",
            "tensor([[24, 43, 58,  5, 57,  1, 46, 43],\n",
            "        [44, 53, 56,  1, 58, 46, 39, 58],\n",
            "        [52, 58,  1, 58, 46, 39, 58,  1],\n",
            "        [25, 17, 27, 10,  0, 21,  1, 54]])\n",
            "targets:\n",
            "torch.Size([4, 8])\n",
            "tensor([[43, 58,  5, 57,  1, 46, 43, 39],\n",
            "        [53, 56,  1, 58, 46, 39, 58,  1],\n",
            "        [58,  1, 58, 46, 39, 58,  1, 46],\n",
            "        [17, 27, 10,  0, 21,  1, 54, 39]])\n",
            "----\n",
            "when input is [24] the target: 43\n",
            "when input is [24, 43] the target: 58\n",
            "when input is [24, 43, 58] the target: 5\n",
            "when input is [24, 43, 58, 5] the target: 57\n",
            "when input is [24, 43, 58, 5, 57] the target: 1\n",
            "when input is [24, 43, 58, 5, 57, 1] the target: 46\n",
            "when input is [24, 43, 58, 5, 57, 1, 46] the target: 43\n",
            "when input is [24, 43, 58, 5, 57, 1, 46, 43] the target: 39\n",
            "when input is [44] the target: 53\n",
            "when input is [44, 53] the target: 56\n",
            "when input is [44, 53, 56] the target: 1\n",
            "when input is [44, 53, 56, 1] the target: 58\n",
            "when input is [44, 53, 56, 1, 58] the target: 46\n",
            "when input is [44, 53, 56, 1, 58, 46] the target: 39\n",
            "when input is [44, 53, 56, 1, 58, 46, 39] the target: 58\n",
            "when input is [44, 53, 56, 1, 58, 46, 39, 58] the target: 1\n",
            "when input is [52] the target: 58\n",
            "when input is [52, 58] the target: 1\n",
            "when input is [52, 58, 1] the target: 58\n",
            "when input is [52, 58, 1, 58] the target: 46\n",
            "when input is [52, 58, 1, 58, 46] the target: 39\n",
            "when input is [52, 58, 1, 58, 46, 39] the target: 58\n",
            "when input is [52, 58, 1, 58, 46, 39, 58] the target: 1\n",
            "when input is [52, 58, 1, 58, 46, 39, 58, 1] the target: 46\n",
            "when input is [25] the target: 17\n",
            "when input is [25, 17] the target: 27\n",
            "when input is [25, 17, 27] the target: 10\n",
            "when input is [25, 17, 27, 10] the target: 0\n",
            "when input is [25, 17, 27, 10, 0] the target: 21\n",
            "when input is [25, 17, 27, 10, 0, 21] the target: 1\n",
            "when input is [25, 17, 27, 10, 0, 21, 1] the target: 54\n",
            "when input is [25, 17, 27, 10, 0, 21, 1, 54] the target: 39\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "print(xb) # our input to the transformer"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "5dVHPD2CWXUl",
        "outputId": "8b55d566-d65a-4fa6-a7fa-8dee0d057a13"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "tensor([[24, 43, 58,  5, 57,  1, 46, 43],\n",
            "        [44, 53, 56,  1, 58, 46, 39, 58],\n",
            "        [52, 58,  1, 58, 46, 39, 58,  1],\n",
            "        [25, 17, 27, 10,  0, 21,  1, 54]])\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import torch\n",
        "import torch.nn as nn\n",
        "from torch.nn import functional as F\n",
        "torch.manual_seed(1337)\n",
        "\n",
        "class BigramLanguageModel(nn.Module):\n",
        "\n",
        "    def __init__(self, vocab_size):\n",
        "        super().__init__()\n",
        "        # each token directly reads off the logits for the next token from a lookup table\n",
        "        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)\n",
        "\n",
        "    def forward(self, idx, targets=None):\n",
        "\n",
        "        # idx and targets are both (B,T) tensor of integers\n",
        "        logits = self.token_embedding_table(idx) # (B,T,C)\n",
        "\n",
        "        if targets is None:\n",
        "            loss = None\n",
        "        else:\n",
        "            B, T, C = logits.shape\n",
        "            logits = logits.view(B*T, C)\n",
        "            targets = targets.view(B*T)\n",
        "            loss = F.cross_entropy(logits, targets)\n",
        "\n",
        "        return logits, loss\n",
        "\n",
        "    def generate(self, idx, max_new_tokens):\n",
        "        # idx is (B, T) array of indices in the current context\n",
        "        for _ in range(max_new_tokens):\n",
        "            # get the predictions\n",
        "            logits, loss = self(idx)\n",
        "            # focus only on the last time step\n",
        "            logits = logits[:, -1, :] # becomes (B, C)\n",
        "            # apply softmax to get probabilities\n",
        "            probs = F.softmax(logits, dim=-1) # (B, C)\n",
        "            # sample from the distribution\n",
        "            idx_next = torch.multinomial(probs, num_samples=1) # (B, 1)\n",
        "            # append sampled index to the running sequence\n",
        "            idx = torch.cat((idx, idx_next), dim=1) # (B, T+1)\n",
        "        return idx\n",
        "\n",
        "m = BigramLanguageModel(vocab_size)\n",
        "logits, loss = m(xb, yb)\n",
        "print(logits.shape)\n",
        "print(loss)\n",
        "\n",
        "print(decode(m.generate(idx = torch.zeros((1, 1), dtype=torch.long), max_new_tokens=100)[0].tolist()))\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "9xWwhewIWcnG",
        "outputId": "8bd22506-dede-4d9f-a20b-519e9d09feb3"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "torch.Size([32, 65])\n",
            "tensor(4.8786, grad_fn=<NllLossBackward0>)\n",
            "\n",
            "Sr?qP-QWktXoL&jLDJgOLVz'RIoDqHdhsV&vLLxatjscMpwLERSPyao.qfzs$Ys$zF-w,;eEkzxjgCKFChs!iWW.ObzDnxA Ms$3\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# create a PyTorch optimizer\n",
        "optimizer = torch.optim.AdamW(m.parameters(), lr=1e-3)"
      ],
      "metadata": {
        "id": "MnaqAx1AWfOD"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "batch_size = 32\n",
        "for steps in range(100): # increase number of steps for good results...\n",
        "\n",
        "    # sample a batch of data\n",
        "    xb, yb = get_batch('train')\n",
        "\n",
        "    # evaluate the loss\n",
        "    logits, loss = m(xb, yb)\n",
        "    optimizer.zero_grad(set_to_none=True)\n",
        "    loss.backward()\n",
        "    optimizer.step()\n",
        "\n",
        "print(loss.item())\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "cPKFFqmiWrLu",
        "outputId": "8f3a0b05-9309-4ab3-9fa6-84d158068c5f"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "2.503154754638672\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "print(decode(m.generate(idx = torch.zeros((1, 1), dtype=torch.long), max_new_tokens=500)[0].tolist()))"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "cpZl3lNbWtig",
        "outputId": "8f836cfb-692f-4ecd-f2c6-10e425b3eb8a"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "O,\n",
            "\n",
            "Whest bend\n",
            "\n",
            "JUn\n",
            "\n",
            "Ther,\n",
            "Whonowd.\n",
            "CHENemangr, f\n",
            "QUKICLY howo as.\n",
            "SBELIDulothelis\n",
            "thond d r, y tt poscee te y alea hid;\n",
            "GHERungu nto't mir, o, I hesavinde ng;\n",
            "CENCENGBut ave d.\n",
            "PUS:\n",
            "If t tof theleale thin n iteanderin yindorenod or.\n",
            "Ark ars athawor od?\n",
            "QUp.\n",
            "'s ble younod anauik, tins pe hicht Me, noke bo hathipalobl, coure bor ayo rce,\n",
            "\n",
            "Wh myafase ben l y' theceas listtousthadassod mof nerer\n",
            "\n",
            "TYoveve he anince jor hy s alll'\n",
            "Myshe,\n",
            "Twopak,\n",
            "Th a otonfodg w thanomye are\n",
            "Hafrere:\n",
            "the st thore?\n",
            "TUC\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# toy example illustrating how matrix multiplication can be used for a \"weighted aggregation\"\n",
        "torch.manual_seed(42)\n",
        "a = torch.tril(torch.ones(3, 3))\n",
        "a = a / torch.sum(a, 1, keepdim=True)\n",
        "b = torch.randint(0,10,(3,2)).float()\n",
        "c = a @ b\n",
        "print('a=')\n",
        "print(a)\n",
        "print('--')\n",
        "print('b=')\n",
        "print(b)\n",
        "print('--')\n",
        "print('c=')\n",
        "print(c)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "OfyShA-fW0RL",
        "outputId": "0145bed2-0642-43d3-b7bb-055ba10f16aa"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "a=\n",
            "tensor([[1.0000, 0.0000, 0.0000],\n",
            "        [0.5000, 0.5000, 0.0000],\n",
            "        [0.3333, 0.3333, 0.3333]])\n",
            "--\n",
            "b=\n",
            "tensor([[2., 7.],\n",
            "        [6., 4.],\n",
            "        [6., 5.]])\n",
            "--\n",
            "c=\n",
            "tensor([[2.0000, 7.0000],\n",
            "        [4.0000, 5.5000],\n",
            "        [4.6667, 5.3333]])\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# consider the following toy example:\n",
        "\n",
        "torch.manual_seed(1337)\n",
        "B,T,C = 4,8,2 # batch, time, channels\n",
        "x = torch.randn(B,T,C)\n",
        "x.shape"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "HPF5yFa9W3d1",
        "outputId": "59a5f2c1-c863-4f6b-d2aa-e7ca827ba580"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "torch.Size([4, 8, 2])"
            ]
          },
          "metadata": {},
          "execution_count": 24
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# We want x[b,t] = mean_{i<=t} x[b,i]\n",
        "xbow = torch.zeros((B,T,C))\n",
        "for b in range(B):\n",
        "    for t in range(T):\n",
        "        xprev = x[b,:t+1] # (t,C)\n",
        "        xbow[b,t] = torch.mean(xprev, 0)\n"
      ],
      "metadata": {
        "id": "FJKf2WIXW5ql"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# version 2: using matrix multiply for a weighted aggregation\n",
        "wei = torch.tril(torch.ones(T, T))\n",
        "wei = wei / wei.sum(1, keepdim=True)\n",
        "xbow2 = wei @ x # (B, T, T) @ (B, T, C) ----> (B, T, C)\n",
        "torch.allclose(xbow, xbow2)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "fGJSpxUKW8zi",
        "outputId": "070a08e7-4425-404a-8908-ef912ee1d24d"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "False"
            ]
          },
          "metadata": {},
          "execution_count": 26
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# version 3: use Softmax\n",
        "tril = torch.tril(torch.ones(T, T))\n",
        "wei = torch.zeros((T,T))\n",
        "wei = wei.masked_fill(tril == 0, float('-inf'))\n",
        "wei = F.softmax(wei, dim=-1)\n",
        "xbow3 = wei @ x\n",
        "torch.allclose(xbow, xbow3)\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "yBIfZtb-XANL",
        "outputId": "eb614d9d-81da-4d2a-b1b0-8d6775a02ea3"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "False"
            ]
          },
          "metadata": {},
          "execution_count": 27
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# version 4: self-attention!\n",
        "torch.manual_seed(1337)\n",
        "B,T,C = 4,8,32 # batch, time, channels\n",
        "x = torch.randn(B,T,C)\n",
        "\n",
        "# let's see a single Head perform self-attention\n",
        "head_size = 16\n",
        "key = nn.Linear(C, head_size, bias=False)\n",
        "query = nn.Linear(C, head_size, bias=False)\n",
        "value = nn.Linear(C, head_size, bias=False)\n",
        "k = key(x)   # (B, T, 16)\n",
        "q = query(x) # (B, T, 16)\n",
        "wei =  q @ k.transpose(-2, -1) # (B, T, 16) @ (B, 16, T) ---> (B, T, T)\n",
        "\n",
        "tril = torch.tril(torch.ones(T, T))\n",
        "#wei = torch.zeros((T,T))\n",
        "wei = wei.masked_fill(tril == 0, float('-inf'))\n",
        "wei = F.softmax(wei, dim=-1)\n",
        "\n",
        "v = value(x)\n",
        "out = wei @ v\n",
        "#out = wei @ x\n",
        "\n",
        "out.shape"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "ZNnwmClAXFep",
        "outputId": "b8fb3f50-0fc9-4341-e142-a8434169bb07"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "torch.Size([4, 8, 16])"
            ]
          },
          "metadata": {},
          "execution_count": 28
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "wei[0]"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "0quvD6K6XKse",
        "outputId": "40452437-1305-4da6-c485-04828e47bf34"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "tensor([[1.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],\n",
              "        [0.1574, 0.8426, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],\n",
              "        [0.2088, 0.1646, 0.6266, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],\n",
              "        [0.5792, 0.1187, 0.1889, 0.1131, 0.0000, 0.0000, 0.0000, 0.0000],\n",
              "        [0.0294, 0.1052, 0.0469, 0.0276, 0.7909, 0.0000, 0.0000, 0.0000],\n",
              "        [0.0176, 0.2689, 0.0215, 0.0089, 0.6812, 0.0019, 0.0000, 0.0000],\n",
              "        [0.1691, 0.4066, 0.0438, 0.0416, 0.1048, 0.2012, 0.0329, 0.0000],\n",
              "        [0.0210, 0.0843, 0.0555, 0.2297, 0.0573, 0.0709, 0.2423, 0.2391]],\n",
              "       grad_fn=<SelectBackward0>)"
            ]
          },
          "metadata": {},
          "execution_count": 29
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "k = torch.randn(B,T,head_size)\n",
        "q = torch.randn(B,T,head_size)\n",
        "wei = q @ k.transpose(-2, -1) * head_size**-0.5"
      ],
      "metadata": {
        "id": "YP6LQSHAXNkz"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "k.var()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "pBBW9kOtXThP",
        "outputId": "743272fd-08ef-455a-8eb2-669da9eba4d9"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "tensor(1.0449)"
            ]
          },
          "metadata": {},
          "execution_count": 31
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "q.var()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "LIwzcqVnXVvG",
        "outputId": "1339475d-fed0-4472-e4ff-9990ea675dc6"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "tensor(1.0700)"
            ]
          },
          "metadata": {},
          "execution_count": 32
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "wei.var()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "cKdJvGmcXXpK",
        "outputId": "a074bb83-bf51-40f4-92f1-3cb47174ad65"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "tensor(1.0918)"
            ]
          },
          "metadata": {},
          "execution_count": 33
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "torch.softmax(torch.tensor([0.1, -0.2, 0.3, -0.2, 0.5]), dim=-1)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "YgM_2VpDXZS5",
        "outputId": "cde9b10c-b75c-4167-a587-ddffa969982e"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "tensor([0.1925, 0.1426, 0.2351, 0.1426, 0.2872])"
            ]
          },
          "metadata": {},
          "execution_count": 34
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "torch.softmax(torch.tensor([0.1, -0.2, 0.3, -0.2, 0.5])*8, dim=-1) # gets too peaky, converges to one-hot"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "oGT6pK88Xxn1",
        "outputId": "4e9aeed4-b873-47e2-99fb-559397a57167"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "tensor([0.0326, 0.0030, 0.1615, 0.0030, 0.8000])"
            ]
          },
          "metadata": {},
          "execution_count": 35
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "class LayerNorm1d: # (used to be BatchNorm1d)\n",
        "\n",
        "  def __init__(self, dim, eps=1e-5, momentum=0.1):\n",
        "    self.eps = eps\n",
        "    self.gamma = torch.ones(dim)\n",
        "    self.beta = torch.zeros(dim)\n",
        "\n",
        "  def __call__(self, x):\n",
        "    # calculate the forward pass\n",
        "    xmean = x.mean(1, keepdim=True) # batch mean\n",
        "    xvar = x.var(1, keepdim=True) # batch variance\n",
        "    xhat = (x - xmean) / torch.sqrt(xvar + self.eps) # normalize to unit variance\n",
        "    self.out = self.gamma * xhat + self.beta\n",
        "    return self.out\n",
        "\n",
        "  def parameters(self):\n",
        "    return [self.gamma, self.beta]\n",
        "\n",
        "torch.manual_seed(1337)\n",
        "module = LayerNorm1d(100)\n",
        "x = torch.randn(32, 100) # batch size 32 of 100-dimensional vectors\n",
        "x = module(x)\n",
        "x.shape"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "4JxHQwOqX55t",
        "outputId": "29e160bf-c9e6-4c5e-ca98-90f284a787af"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "torch.Size([32, 100])"
            ]
          },
          "metadata": {},
          "execution_count": 36
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "x[:,0].mean(), x[:,0].std() # mean,std of one feature across all batch inputs"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "tC1eK05rX8Kj",
        "outputId": "66ca6ca3-c52a-4c10-f20e-e014a3244ba0"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(tensor(0.1469), tensor(0.8803))"
            ]
          },
          "metadata": {},
          "execution_count": 37
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "x[0,:].mean(), x[0,:].std() # mean,std of a single input from the batch, of its features"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "KtdXz_LUX_Cl",
        "outputId": "220007d1-321c-46ce-a4ad-1f7b8a346e4b"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(tensor(-9.5367e-09), tensor(1.0000))"
            ]
          },
          "metadata": {},
          "execution_count": 38
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import torch\n",
        "import torch.nn as nn\n",
        "from torch.nn import functional as F\n",
        "\n",
        "# hyperparameters\n",
        "batch_size = 16 # how many independent sequences will we process in parallel?\n",
        "block_size = 32 # what is the maximum context length for predictions?\n",
        "max_iters = 5000\n",
        "eval_interval = 100\n",
        "learning_rate = 1e-3\n",
        "device = 'cuda' if torch.cuda.is_available() else 'cpu'\n",
        "eval_iters = 200\n",
        "n_embd = 64\n",
        "n_head = 4\n",
        "n_layer = 4\n",
        "dropout = 0.0\n",
        "# ------------\n",
        "\n",
        "torch.manual_seed(1337)\n",
        "\n",
        "# wget https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt\n",
        "with open('input.txt', 'r', encoding='utf-8') as f:\n",
        "    text = f.read()\n",
        "\n",
        "# here are all the unique characters that occur in this text\n",
        "chars = sorted(list(set(text)))\n",
        "vocab_size = len(chars)\n",
        "# create a mapping from characters to integers\n",
        "stoi = { ch:i for i,ch in enumerate(chars) }\n",
        "itos = { i:ch for i,ch in enumerate(chars) }\n",
        "encode = lambda s: [stoi[c] for c in s] # encoder: take a string, output a list of integers\n",
        "decode = lambda l: ''.join([itos[i] for i in l]) # decoder: take a list of integers, output a string\n",
        "\n",
        "# Train and test splits\n",
        "data = torch.tensor(encode(text), dtype=torch.long)\n",
        "n = int(0.9*len(data)) # first 90% will be train, rest val\n",
        "train_data = data[:n]\n",
        "val_data = data[n:]\n",
        "\n",
        "# data loading\n",
        "def get_batch(split):\n",
        "    # generate a small batch of data of inputs x and targets y\n",
        "    data = train_data if split == 'train' else val_data\n",
        "    ix = torch.randint(len(data) - block_size, (batch_size,))\n",
        "    x = torch.stack([data[i:i+block_size] for i in ix])\n",
        "    y = torch.stack([data[i+1:i+block_size+1] for i in ix])\n",
        "    x, y = x.to(device), y.to(device)\n",
        "    return x, y\n",
        "\n",
        "@torch.no_grad()\n",
        "def estimate_loss():\n",
        "    out = {}\n",
        "    model.eval()\n",
        "    for split in ['train', 'val']:\n",
        "        losses = torch.zeros(eval_iters)\n",
        "        for k in range(eval_iters):\n",
        "            X, Y = get_batch(split)\n",
        "            logits, loss = model(X, Y)\n",
        "            losses[k] = loss.item()\n",
        "        out[split] = losses.mean()\n",
        "    model.train()\n",
        "    return out\n",
        "\n",
        "class Head(nn.Module):\n",
        "    \"\"\" one head of self-attention \"\"\"\n",
        "\n",
        "    def __init__(self, head_size):\n",
        "        super().__init__()\n",
        "        self.key = nn.Linear(n_embd, head_size, bias=False)\n",
        "        self.query = nn.Linear(n_embd, head_size, bias=False)\n",
        "        self.value = nn.Linear(n_embd, head_size, bias=False)\n",
        "        self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))\n",
        "\n",
        "        self.dropout = nn.Dropout(dropout)\n",
        "\n",
        "    def forward(self, x):\n",
        "        B,T,C = x.shape\n",
        "        k = self.key(x)   # (B,T,C)\n",
        "        q = self.query(x) # (B,T,C)\n",
        "        # compute attention scores (\"affinities\")\n",
        "        wei = q @ k.transpose(-2,-1) * C**-0.5 # (B, T, C) @ (B, C, T) -> (B, T, T)\n",
        "        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf')) # (B, T, T)\n",
        "        wei = F.softmax(wei, dim=-1) # (B, T, T)\n",
        "        wei = self.dropout(wei)\n",
        "        # perform the weighted aggregation of the values\n",
        "        v = self.value(x) # (B,T,C)\n",
        "        out = wei @ v # (B, T, T) @ (B, T, C) -> (B, T, C)\n",
        "        return out\n",
        "\n",
        "class MultiHeadAttention(nn.Module):\n",
        "    \"\"\" multiple heads of self-attention in parallel \"\"\"\n",
        "\n",
        "    def __init__(self, num_heads, head_size):\n",
        "        super().__init__()\n",
        "        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])\n",
        "        self.proj = nn.Linear(n_embd, n_embd)\n",
        "        self.dropout = nn.Dropout(dropout)\n",
        "\n",
        "    def forward(self, x):\n",
        "        out = torch.cat([h(x) for h in self.heads], dim=-1)\n",
        "        out = self.dropout(self.proj(out))\n",
        "        return out\n",
        "\n",
        "class FeedFoward(nn.Module):\n",
        "    \"\"\" a simple linear layer followed by a non-linearity \"\"\"\n",
        "\n",
        "    def __init__(self, n_embd):\n",
        "        super().__init__()\n",
        "        self.net = nn.Sequential(\n",
        "            nn.Linear(n_embd, 4 * n_embd),\n",
        "            nn.ReLU(),\n",
        "            nn.Linear(4 * n_embd, n_embd),\n",
        "            nn.Dropout(dropout),\n",
        "        )\n",
        "\n",
        "    def forward(self, x):\n",
        "        return self.net(x)\n",
        "\n",
        "class Block(nn.Module):\n",
        "    \"\"\" Transformer block: communication followed by computation \"\"\"\n",
        "\n",
        "    def __init__(self, n_embd, n_head):\n",
        "        # n_embd: embedding dimension, n_head: the number of heads we'd like\n",
        "        super().__init__()\n",
        "        head_size = n_embd // n_head\n",
        "        self.sa = MultiHeadAttention(n_head, head_size)\n",
        "        self.ffwd = FeedFoward(n_embd)\n",
        "        self.ln1 = nn.LayerNorm(n_embd)\n",
        "        self.ln2 = nn.LayerNorm(n_embd)\n",
        "\n",
        "    def forward(self, x):\n",
        "        x = x + self.sa(self.ln1(x))\n",
        "        x = x + self.ffwd(self.ln2(x))\n",
        "        return x\n",
        "\n",
        "# super simple bigram model\n",
        "class BigramLanguageModel(nn.Module):\n",
        "\n",
        "    def __init__(self):\n",
        "        super().__init__()\n",
        "        # each token directly reads off the logits for the next token from a lookup table\n",
        "        self.token_embedding_table = nn.Embedding(vocab_size, n_embd)\n",
        "        self.position_embedding_table = nn.Embedding(block_size, n_embd)\n",
        "        self.blocks = nn.Sequential(*[Block(n_embd, n_head=n_head) for _ in range(n_layer)])\n",
        "        self.ln_f = nn.LayerNorm(n_embd) # final layer norm\n",
        "        self.lm_head = nn.Linear(n_embd, vocab_size)\n",
        "\n",
        "    def forward(self, idx, targets=None):\n",
        "        B, T = idx.shape\n",
        "\n",
        "        # idx and targets are both (B,T) tensor of integers\n",
        "        tok_emb = self.token_embedding_table(idx) # (B,T,C)\n",
        "        pos_emb = self.position_embedding_table(torch.arange(T, device=device)) # (T,C)\n",
        "        x = tok_emb + pos_emb # (B,T,C)\n",
        "        x = self.blocks(x) # (B,T,C)\n",
        "        x = self.ln_f(x) # (B,T,C)\n",
        "        logits = self.lm_head(x) # (B,T,vocab_size)\n",
        "\n",
        "        if targets is None:\n",
        "            loss = None\n",
        "        else:\n",
        "            B, T, C = logits.shape\n",
        "            logits = logits.view(B*T, C)\n",
        "            targets = targets.view(B*T)\n",
        "            loss = F.cross_entropy(logits, targets)\n",
        "\n",
        "        return logits, loss\n",
        "\n",
        "    def generate(self, idx, max_new_tokens):\n",
        "        # idx is (B, T) array of indices in the current context\n",
        "        for _ in range(max_new_tokens):\n",
        "            # crop idx to the last block_size tokens\n",
        "            idx_cond = idx[:, -block_size:]\n",
        "            # get the predictions\n",
        "            logits, loss = self(idx_cond)\n",
        "            # focus only on the last time step\n",
        "            logits = logits[:, -1, :] # becomes (B, C)\n",
        "            # apply softmax to get probabilities\n",
        "            probs = F.softmax(logits, dim=-1) # (B, C)\n",
        "            # sample from the distribution\n",
        "            idx_next = torch.multinomial(probs, num_samples=1) # (B, 1)\n",
        "            # append sampled index to the running sequence\n",
        "            idx = torch.cat((idx, idx_next), dim=1) # (B, T+1)\n",
        "        return idx\n",
        "\n",
        "model = BigramLanguageModel()\n",
        "m = model.to(device)\n",
        "# print the number of parameters in the model\n",
        "print(sum(p.numel() for p in m.parameters())/1e6, 'M parameters')\n",
        "\n",
        "# create a PyTorch optimizer\n",
        "optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)\n",
        "\n",
        "for iter in range(max_iters):\n",
        "\n",
        "    # every once in a while evaluate the loss on train and val sets\n",
        "    if iter % eval_interval == 0 or iter == max_iters - 1:\n",
        "        losses = estimate_loss()\n",
        "        print(f\"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}\")\n",
        "\n",
        "    # sample a batch of data\n",
        "    xb, yb = get_batch('train')\n",
        "\n",
        "    # evaluate the loss\n",
        "    logits, loss = model(xb, yb)\n",
        "    optimizer.zero_grad(set_to_none=True)\n",
        "    loss.backward()\n",
        "    optimizer.step()\n",
        "\n",
        "# generate from the model\n",
        "context = torch.zeros((1, 1), dtype=torch.long, device=device)\n",
        "print(decode(m.generate(context, max_new_tokens=2000)[0].tolist()))\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "GKxBmWlPYBCw",
        "outputId": "5a893471-14b2-4542-c5e1-f0c852eb7147"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "0.209729 M parameters\n",
            "step 0: train loss 4.4116, val loss 4.4022\n",
            "step 100: train loss 2.6568, val loss 2.6670\n",
            "step 200: train loss 2.5090, val loss 2.5059\n",
            "step 300: train loss 2.4196, val loss 2.4338\n",
            "step 400: train loss 2.3504, val loss 2.3566\n",
            "step 500: train loss 2.2965, val loss 2.3129\n",
            "step 600: train loss 2.2410, val loss 2.2500\n",
            "step 700: train loss 2.2057, val loss 2.2191\n",
            "step 800: train loss 2.1633, val loss 2.1864\n",
            "step 900: train loss 2.1244, val loss 2.1510\n",
            "step 1000: train loss 2.1038, val loss 2.1308\n",
            "step 1100: train loss 2.0707, val loss 2.1197\n",
            "step 1200: train loss 2.0377, val loss 2.0800\n",
            "step 1300: train loss 2.0268, val loss 2.0650\n",
            "step 1400: train loss 1.9918, val loss 2.0356\n",
            "step 1500: train loss 1.9697, val loss 2.0293\n",
            "step 1600: train loss 1.9645, val loss 2.0499\n",
            "step 1700: train loss 1.9404, val loss 2.0129\n",
            "step 1800: train loss 1.9095, val loss 1.9951\n",
            "step 1900: train loss 1.9067, val loss 1.9855\n",
            "step 2000: train loss 1.8854, val loss 1.9948\n",
            "step 2100: train loss 1.8727, val loss 1.9766\n",
            "step 2200: train loss 1.8597, val loss 1.9631\n",
            "step 2300: train loss 1.8530, val loss 1.9516\n",
            "step 2400: train loss 1.8428, val loss 1.9464\n",
            "step 2500: train loss 1.8161, val loss 1.9424\n",
            "step 2600: train loss 1.8283, val loss 1.9406\n",
            "step 2700: train loss 1.8101, val loss 1.9322\n",
            "step 2800: train loss 1.8050, val loss 1.9233\n",
            "step 2900: train loss 1.8033, val loss 1.9289\n",
            "step 3000: train loss 1.7955, val loss 1.9216\n",
            "step 3100: train loss 1.7697, val loss 1.9184\n",
            "step 3200: train loss 1.7541, val loss 1.9088\n",
            "step 3300: train loss 1.7567, val loss 1.9034\n",
            "step 3400: train loss 1.7573, val loss 1.9000\n",
            "step 3500: train loss 1.7398, val loss 1.8925\n",
            "step 3600: train loss 1.7270, val loss 1.8869\n",
            "step 3700: train loss 1.7283, val loss 1.8814\n",
            "step 3800: train loss 1.7210, val loss 1.8918\n",
            "step 3900: train loss 1.7219, val loss 1.8732\n",
            "step 4000: train loss 1.7146, val loss 1.8576\n",
            "step 4100: train loss 1.7136, val loss 1.8720\n",
            "step 4200: train loss 1.7060, val loss 1.8653\n",
            "step 4300: train loss 1.7032, val loss 1.8499\n",
            "step 4400: train loss 1.7057, val loss 1.8656\n",
            "step 4500: train loss 1.6907, val loss 1.8477\n",
            "step 4600: train loss 1.6878, val loss 1.8371\n",
            "step 4700: train loss 1.6808, val loss 1.8415\n",
            "step 4800: train loss 1.6689, val loss 1.8457\n",
            "step 4900: train loss 1.6716, val loss 1.8415\n",
            "step 4999: train loss 1.6658, val loss 1.8275\n",
            "\n",
            "ROTCUMER:\n",
            "Tyburforth, bloody,\n",
            "WhIs migute: you duke I use list. WIthon of where's grande will! savist tought!\n",
            "Why room upwor alond, liegle. I hone, Iell thou sudd have then strue thus mind,\n",
            "His by blow, Virdom tow, glingien, yithre spees ssince them Those not.\n",
            "\n",
            "LUCIO:\n",
            "Look,----\n",
            "But thou sging them this my freceimmsed,\n",
            "By thou sovor conursion that thou sade but grove\n",
            "the tage encond:\n",
            "It will Rament me; an your touther,\n",
            "And havis like to-does, and little spright.\n",
            "\n",
            "GLOUCESTER:\n",
            "Rewards thou for Panfessira's bigguards such ways!\n",
            "What curfort his\n",
            "will havolss you, as I have the cervirs arled,\n",
            "Dear my love and pitace unto duly son.\n",
            "\n",
            "Secome:\n",
            "Offolk, even thy whose my late all that you by jotly us belies!\n",
            "Lord, we a-montencry! I\n",
            "\n",
            "SLARNE:\n",
            "Day, mave from out prrive And orculing\n",
            "What confess, temimelyour and stropt;\n",
            "Secumfospet the gatieus I'll that confence-sting,\n",
            "But; man't, Rolget\n",
            "would garnion'd live in which, you, prothre?\n",
            "\n",
            "CORIOLANUS:\n",
            "What bonum stravoing, not out be seemmed with\n",
            "That the boly noll to.\n",
            "Bently, which in on my not tomberven why, fortune,\n",
            "And that wark you, banot thus orl'ld groves viles.\n",
            "\n",
            "PUMNIUS:\n",
            "It thou addow less, proth-straing.\n",
            "Mutwing your contrant stomfe, whom they\n",
            "is by this famestle; and of the loves my not Mercarcious to the stord; thesoo, in thus my nome are:\n",
            "Will fuch, have there enplience your gone, ho's,\n",
            "And gentleman, my beged lind to be am\n",
            "in That ant:\n",
            "In I sugner murded! I play's,\n",
            "If not sume the confity will reasur slord:\n",
            "That get because at that his say\n",
            "and to beepts guarst you lom if then.\n",
            "\n",
            "MENEN MARGARUS:\n",
            "I but aftelence! made yoour never.\n",
            "\n",
            "KING RICHARD II:\n",
            "Who too near?\n",
            "\n",
            "LORDIUS:\n",
            "Or as madaw brird, tou thee?\n",
            "\n",
            "Sirightly the haste's beforempt.\n",
            "\n",
            "First:\n",
            "Is though.\n",
            "Fell, whose toes with requmpts, up I make\n",
            "Here figUS verean that I will, by the wateon.\n",
            "\n",
            "MOWIDIUS:\n",
            "How, while, more is in meep.\n",
            "twan be the fless this countrens platcar merperter sure make Giventled,\n",
            "At not your must to reason togs,\n",
            "And what you gue;--\n",
            "\n",
            "RUKE ESFiren; gravent,\n",
            "Apol\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "69lZUOmwYI1s"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}