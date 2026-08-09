"""Train the small 2-D-latent MNIST VAE behind lecture 7's interpolation strip
("Walking the latent space") and save the decoded frames to
assets/data/vae-mnist-interp.npz.

Run from the repo root:  python3 tools/make-vae-interp.py
Deterministic (seeded); a few minutes on CPU. MNIST comes via sklearn's
fetch_openml (cached), as in tools/make-ae-latents.py.
"""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.datasets import fetch_openml

SEED = 0
torch.manual_seed(SEED)
np.random.seed(SEED)

print("Fetching MNIST ...")
X, y = fetch_openml("mnist_784", version=1, as_frame=False, return_X_y=True)
X = (X / 255.0).astype(np.float32)
y = y.astype(np.uint8)
X_train = X[:60_000]
X_test, y_test = X[60_000:], y[60_000:]


class VAE(nn.Module):
    def __init__(self, d_latent=2):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(784, 256), nn.ReLU(),
                                 nn.Linear(256, 128), nn.ReLU())
        self.mu = nn.Linear(128, d_latent)
        self.logvar = nn.Linear(128, d_latent)
        self.dec = nn.Sequential(
            nn.Linear(d_latent, 128), nn.ReLU(),
            nn.Linear(128, 256), nn.ReLU(),
            nn.Linear(256, 784), nn.Sigmoid(),
        )

    def forward(self, x):
        h = self.enc(x)
        mu, logvar = self.mu(h), self.logvar(h)
        z = mu + torch.exp(0.5 * logvar) * torch.randn_like(mu)
        return self.dec(z), mu, logvar


model = VAE()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
Xt = torch.from_numpy(X_train)
EPOCHS, BATCH = 20, 256

for epoch in range(EPOCHS):
    perm = torch.randperm(len(Xt))
    total = 0.0
    for i in range(0, len(Xt), BATCH):
        xb = Xt[perm[i:i + BATCH]]
        xhat, mu, logvar = model(xb)
        recon = F.binary_cross_entropy(xhat, xb, reduction="sum") / len(xb)
        kl = -0.5 * torch.sum(1 + logvar - mu**2 - logvar.exp()) / len(xb)
        loss = recon + kl
        opt.zero_grad()
        loss.backward()
        opt.step()
        total += loss.item() * len(xb)
    print(f"epoch {epoch + 1:2d}/{EPOCHS}  loss/example {total / len(Xt):.1f}")

model.eval()
with torch.no_grad():
    h = model.enc(torch.from_numpy(X_test))
    mu_test = model.mu(h).numpy()

# Endpoints: the latent-space medoid exemplar of each class, so both are
# real test images with typical codes.
def medoid_index(digit):
    idx = np.where(y_test == digit)[0]
    mus = mu_test[idx]
    med = np.median(mus, axis=0)
    return idx[np.argmin(np.linalg.norm(mus - med, axis=1))]

iA, iB = medoid_index(3), medoid_index(8)
zA, zB = mu_test[iA], mu_test[iB]
print(f"3 exemplar #{iA} at z={np.round(zA, 2)}, 8 exemplar #{iB} at z={np.round(zB, 2)}")

ts = np.linspace(0, 1, 9).astype(np.float32)
z_path = np.stack([(1 - t) * zA + t * zB for t in ts])
with torch.no_grad():
    frames = model.dec(torch.from_numpy(z_path)).numpy().reshape(-1, 28, 28)

out = "assets/data/vae-mnist-interp.npz"
np.savez_compressed(
    out,
    frames=frames.astype(np.float32), ts=ts,
    zA=zA, zB=zB,
    imgA=X_test[iA].reshape(28, 28), imgB=X_test[iB].reshape(28, 28),
)
print(f"saved {out}")
