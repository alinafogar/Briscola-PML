# Briscola-PML

The project focuses on Bayesian opponent modelling in two-player Briscola.

The idea is that we observe how an opponent plays, we assume that their
style can be represented by a latent parameter vector `theta`, and we try to
infer a posterior distribution over that vector. Once we have this posterior,
we can use it to predict future opponent moves.

We are not trying to build a complete Briscola-playing agent. Our focus is the
inference problem: the opponent has a hidden hand, we only see public
information and played cards and we want to understand whether we can recover
an interpretable playing style from partial observations.

Detailed notes on the theory behind our approach can be found in
[theory.md](theory.md).

## What We Have Built

At the moment, the project includes:

- a two-player Briscola simulator with scoring, trick resolution, and draw
  order;
- a public game state and player-specific views;
- synthetic opponents that choose cards with a softmax model based on `theta`;
- two feature sets, `core` and `interaction`, with profile-specific synthetic
  theta vectors;
- synthetic data collection from simulated games;
- a sequential hand belief that is updated across the moves of the same game;
- mean-field Gaussian variational inference for `theta`;
- validation scripts for theta recovery and test posterior prediction;
- comparison scripts to test different feature sets, opponent profiles, and
  random seeds.


## Feature Sets

We have two feature sets: `core` uses direct card and
current-trick features; `interaction` keeps only context-dependent terms based
on game progress and the current trick.

### `core`

```text
is_trump
points_normalized
wins_current_trick
lowest_card_in_suit
```

Current `core` theta vectors:

| Profile | `theta` |
|---|---|
| `aggressive` | `(0.4, 1.4, 2.2, -0.2)` |
| `conservative` | `(-1.8, -1.1, 0.7, 1.2)` |
| `greedy_points` | `(0.1, 3.0, 0.4, -0.2)` |

### `interaction`

```text
trump_progress
points_progress
trump_on_table_points
greedy_take
```

This set keeps only context-dependent interaction terms: late-game trump use,
late-game point use, trump use when points are already on the table, and taking
a point-bearing trick.

Current `interaction` theta vectors:

| Profile | `theta` |
|---|---|
| `aggressive` | `(-1.0, -1.5, 2.0, 3.0)` |
| `conservative` | `(1.5, 1.5, -0.5, -1.0)` |
| `greedy_points` | `(-0.1, -2.0, 0.5, 1.0)` |

The profiles are hand-written and used only to generate controlled synthetic
data where the true parameters are known.

## Repository Layout

```text
game/
  cards.py              Cards, suits, ranks, points, and Briscola strength.
  simulator.py          Two-player Briscola engine and public state.

opponents/
  features.py           Feature extraction for candidate moves.
  models.py             Random and theta-softmax synthetic opponents.

experiments/
  episode_collection.py Synthetic game collection.
  validation.py         Recovery, prediction, and validation helpers.

inference/
  beliefs.py            Compatible hidden-hand enumeration.
  vi.py                 Sequential likelihood and variational inference.

theory.md               Detailed model notes.
run_experiment.py       Single validation runs and comparison grids.
test.py                 Core project tests.
```

## Run One Validation

This command runs one synthetic experiment with the default feature set:

```bash
python3 run_experiment.py single \
  --num-games 50 \
  --feature-set core \
  --profile aggressive \
  --opponent-temperature 1.0 \
  --vi-steps 150 \
  --elbo-samples 2 \
  --posterior-samples 50 \
  --output artifacts/validation_report.json
```

The report tells us:

- the true synthetic `theta`;
- the posterior mean and standard deviation learned by VI;
- the per-feature error and L2 recovery error;
- the ELBO trajectory;
- test posterior predictive log-likelihood against a zero-theta baseline.

Useful flags:

- `--opponent-temperature` controls how deterministic the synthetic opponent's
  softmax policy is. Lower values make the opponent follow its preferences more
  sharply.
- `--prior-std` changes the width of the Gaussian prior over `theta`.
- `--vi-steps` controls how long we optimize the variational posterior.
- `--posterior-samples` controls how many theta samples from `q(theta)` we use
  for test posterior prediction.

Validation uses a fixed game-level 75/25 train/test split, which keeps all
moves from one game in the same partition and avoids leakage between train and
test data. The Adam learning rate is fixed at `0.03`.

## Run A Comparison

This repeats the same validation pipeline across feature sets, profiles, and
seeds:

```bash
python3 run_experiment.py compare \
  --feature-sets core interaction \
  --profiles aggressive conservative greedy_points \
  --seeds 0 1 2 \
  --num-games 20 \
  --opponent-temperature 1.0 \
  --vi-steps 150 \
  --posterior-samples 20 \
  --jobs 4
```

The `compare` command does not use a different inference method. Each run
follows the same sequential VI pipeline as `single`; the command only repeats
that pipeline over several configurations and summarizes the results.

Outputs are written under `artifacts/comparison/`. The run CSV is written
incrementally, so it is possible to inspect partial results while a larger comparison is
still running.

## Dependencies

Install the project dependencies with:

```bash
pip install -r requirements.txt
```
