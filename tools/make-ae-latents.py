"""Train the 2-D-bottleneck MNIST autoencoder behind lecture 7's latent-space
figures, and save everything those figures need to assets/data/ae-mnist-latents.npz.

Run from the repo root:  python3 tools/make-ae-latents.py
Deterministic (seeded); ~1 minute on CPU. MNIST comes via sklearn's fetch_openml
(cached in ~/scikit_learn_data after the first download).
"""
import numpy as np
import torch
import torch.nn as nn
from sklearn.datasets import fetch_openml

SEED = 0
torch.manual_seed(SEED)
np.random.seed(SEED)

print("Fetching MNIST ...")
X, y = fetch_openml("mnist_784", version=1, as_frame=False, return_X_y=True)
X = (X / 255.0).astype(np.float32)
y = y.astype(np.uint8)
X_train, y_train = X[:60_000], y[:60_000]
X_test, y_test = X[60_000:], y[60_000:]


class AE(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(784, 128), nn.ReLU(),
            nn.Linear(128, 32), nn.ReLU(),
            nn.Linear(32, 2),
        )
        self.decoder = nn.Sequential(
            nn.Linear(2, 32), nn.ReLU(),
            nn.Linear(32, 128), nn.ReLU(),
            nn.Linear(128, 784), nn.Sigmoid(),
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))


model = AE()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.MSELoss()
Xt = torch.from_numpy(X_train)
EPOCHS, BATCH = 10, 256

for epoch in range(EPOCHS):
    perm = torch.randperm(len(Xt))
    total = 0.0
    for i in range(0, len(Xt), BATCH):
        xb = Xt[perm[i:i + BATCH]]
        loss = loss_fn(model(xb), xb)
        opt.zero_grad()
        loss.backward()
        opt.step()
        total += loss.item() * len(xb)
    print(f"epoch {epoch + 1:2d}/{EPOCHS}  train MSE {total / len(Xt):.4f}")

model.eval()
with torch.no_grad():
    z_test = model.encoder(torch.from_numpy(X_test)).numpy()
    z_train = model.encoder(Xt).numpy()
    test_mse = loss_fn(model(torch.from_numpy(X_test)), torch.from_numpy(X_test)).item()
print(f"test MSE {test_mse:.4f}")

# Showcase points for the "decode the gaps" slide -----------------------------
# 1) a cluster point: the latent-space medoid of one digit class
digit = 1
zc = z_train[y_train == digit]
med = np.median(zc, axis=0)
z_cluster = zc[np.argmin(np.linalg.norm(zc - med, axis=1))]

# 2) a gap point: the grid point inside the occupied bounding box that is
#    furthest from every training latent (restricted to the central region so
#    we land between clusters, not outside the whole cloud)
lo, hi = np.percentile(z_train, 2, axis=0), np.percentile(z_train, 98, axis=0)
gx, gy = np.meshgrid(np.linspace(lo[0], hi[0], 120), np.linspace(lo[1], hi[1], 120))
grid = np.stack([gx.ravel(), gy.ravel()], axis=1).astype(np.float32)
d = np.full(len(grid), np.inf)
for i in range(0, len(z_train), 5000):  # chunked nearest-neighbour distance
    chunk = z_train[i:i + 5000]
    d = np.minimum(d, ((grid[:, None, :] - chunk[None, :, :]) ** 2).sum(-1).min(1))
z_gap = grid[np.argmax(d)]
print(f"cluster point (digit {digit}): {z_cluster}, gap point: {z_gap}")

with torch.no_grad():
    img_cluster = model.decoder(torch.from_numpy(z_cluster[None])).numpy().reshape(28, 28)
    img_gap = model.decoder(torch.from_numpy(z_gap[None])).numpy().reshape(28, 28)

out = "assets/data/ae-mnist-latents.npz"
np.savez_compressed(
    out,
    z_test=z_test.astype(np.float32), y_test=y_test,
    z_cluster=z_cluster, z_gap=z_gap,
    img_cluster=img_cluster.astype(np.float32), img_gap=img_gap.astype(np.float32),
    cluster_digit=np.array(digit), test_mse=np.array(test_mse),
)
print(f"saved {out}")
