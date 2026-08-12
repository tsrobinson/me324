# ME324 · Midterm assessment — A language model for Parliament

**Due Tuesday 18 August 2026, 09:00 (Moodle). 25% of your final mark. Individual work.**

## The task

In Lab 8 you built a character-level language-model pipeline and ran a bigram through it, on Shakespeare; in Lab 5 you built and trained feedforward networks in PyTorch. This weekend I would like you to put the two together on a different corpus -- about 2.1 million characters of debate from the House of Commons in July 2026.

Build the best character-level language model you can, using only the tools from weeks 1 and 2, following the constraints detailed below. Then run two controlled assessments on it, and write a short discussion of what your model has and hasn't learned.

You should expect the whole exercise to take around six hours.

## What you're given

The starter notebook (`midterm-starter.ipynb`) contains, already working:

- The corpus download and a look at the data
- The Lab 8 pipeline (`build_char_pipeline`)
- A training loop (`train_model_tracked`) —- identical to the labs' `train_model` except it also records the loss history
- A `plot_histories` helper to plot those losses
- The Lab 8 bigram model to use as your baseline
- `count_params`, which counts every trainable parameter, biases included
- A **checkpoint save cell** and a **verify cell**. The verify cell runs the same automated checks we will run on every submission, so if it passes for you, it will run on our testing setup too.

## The rules

1. **Architectures from weeks 1 and 2 only.** Character embeddings and feedforward layers are all you need -- an embedding table feeding a small network over a window of characters. You may use recurrent networks (`nn.RNN`/`nn.GRU`/`nn.LSTM`) following from Thursday's lecture, but they are not required. You should not use attention, transformer blocks, pretrained weights, or any form of external data
2. Token prediction must be at the **character-level, using the given pipeline.** Do not modify `build_char_pipeline`. You may change the *arguments* you call it with (`block_size`, `batch_size`, seed) but you may not change the tokeniser or the train/validation split
3. **Your model may contain up to 500,000 parameters but no more.** You should validate by using the `count_params(model)` template we provide, and note that biases are included in this count.
4. **Your code must run.** Before submitting, do Runtime → Restart and run all, and check it completes on a free Colab GPU runtime in under 20 minutes. Do not clear the outputs — your saved outputs are what we mark!
5. AI assistants are allowed and expected (see below), and you may talk generally with your classmates, but please do not share code, notebooks, or your experimentation.
6. **Be ready to talk it through.** During week 3 labs the teaching team may ask you to explain any cell of your submission -- why it is there, what it does, what happens if it changes. This is routine, not an accusation. If you can't explain your own notebook, that will be reflected in the mark.

## Part A — Building a model (35 marks)

Design and train your model.

- Write a model class that follows the labs' pipeline and setup: `forward(idx, targets)` returns `(logits, loss)`, and `generate(idx, max_new_tokens)` extends a context. You may reuse anything you yourself built in Labs 5 and 8. One practical requirement: your final hyperparameters must be set as constructor defaults, so `MyLanguageModel(vocab_size)` rebuilds your trained model.
- Train it with `train_model_tracked` but choose your own hyperparameters.
- **Threshold:** your model's validation loss must beat the bigram baseline you trained in Section 2 by at least 0.1. Once you pass that threshold, your mark will not continue to increase.
- Report: final train and validation loss, per-character perplexity (e^loss, as in Lecture 8), the parameter count, and a 400-character sample.
- Save your checkpoint with the provided notebook cell and confirm the verify cell passes. You need to submit your `.pt` file.
- In ~150 words: justify your design. Why this architecture, why these sizes, and what you spent your 500k parameters on.

Full marks look like: a working model within the rules, a clear margin over the baseline, and a justification that argues from things we've covered — not "an LLM suggested these settings".

## Part B — Experimenting on your model (35 marks)

Pick **two** of the following hyperparameters:

1. **Context length** — `block_size` (Lecture 8): a wider window gives the model more to condition on, but in a fixed-window model it also grows the input layer, so it costs parameters. Does the trade buy you anything?
2. **Capacity** — hidden size, embedding size, or number of layers (depth vs width)
3. **Learning rate** — value or schedule (Lecture 4)
4. **Regularisation** — dropout or weight decay (Lecture 5)
5. **Batch size** (Lectures 4–5)
6. **Training length** — train much longer, and decide from the curves when you *should* have stopped (Lecture 5)

For each chosen option:

- **State your hypothesis.** One or two sentences noting what you expect to happen to the validation loss and why. Write this before you run the experiments: a specific but *wrong* hypothesis can score full marks still.
- **Run a comparison.** Change the value of your lever but keep everything else fixed.
- **Plot the resulting curves.** Use `plot_histories` to plot the runs against each other.
- **Interpret.** 150–250 words. What happened, was your hypothesis right, and what in the curves tells you. Refer to your actual numbers.

## Part C — Discussing your model (25 marks)

Complete three short answers, ~200 words each, in the marked cells. All three must be grounded in *your* results — quote your own numbers and samples.

1. **Diagnose your final model** using the Lecture 5 taxonomy: underfitting, overfitting, or about right — argue from your train/validation curves. Then say what you would try first with ten times the compute, and why that and not something else.
2. **Read your model's output.** Take two or three generated samples. What has the model genuinely learned about parliamentary English — structure, register, names, procedure? What does it consistently get wrong, and which limitation from the lectures explains that failure?
3. **The data.** Your training data is real MPs' words, scraped from the public record (it is published under the Open Parliament Licence, which permits this). Give one reason this use is clearly legitimate, and one genuine concern that would apply to training on scraped text in general. We return to this properly in Lecture 12.

## Appendix — AI use, reporting and reproducibility (5 marks)

Fill in the appendix at the bottom of the notebook:

- **Tools.** Which AI assistants you used and for what (writing code, debugging, explaining, drafting prose). "None" is an acceptable answer, but won't score you more points!
- **One correction.** Paste one exchange where an assistant's suggestion was wrong, or didn't fit the rules or the budget, and explain how you caught and fixed it. If you never had to correct anything, pick one substantial piece of assistant-written code and explain how you satisfied yourself it was right.
- **Declaration.** You can explain every line you submitted.

The remaining reporting marks are for the basics: the notebook runs top-to-bottom, outputs are saved, seeds are set where the starter sets them, and your prose lives in the marked cells.

## Marking 

Remember: assistants are good at writing training loops and bad at knowing which experiment is worth running on *your* loss curves. So our marks will emphasise the judgements you make. Generic prose that could have been written without running your notebook will score worse, whereas short, specific claims tied to your own numbers will score well.

**What we check automatically.** We will reload your checkpoint and re-evaluate your notebook on our own testing platform, i.e. we will recount the parameters, screen for banned `nn.` modules, rebuild your model from your class, and recompute your validation loss on the same split. This is exactly what the verify cell does, so there should be no surprises, but it means the numbers in your notebook must be the numbers your checkpoint produces. A reported loss that doesn't match the reloaded model will result in a mark deduction.

## Submission

Two files, uploaded to Moodle by **09:00, Tuesday 18 August**:

- `ME324-midterm-<candidate-number>.ipynb` — outputs saved, from a fresh top-to-bottom run;
- `ME324-midterm-<candidate-number>.pt` — the checkpoint the notebook saves (download it from Colab's file browser).

## The data

`hansard-2026.txt`: every attributed speech from five sitting days of the House of Commons (9–16 July 2026), formatted exactly like the labs' Shakespeare file — speaker name, colon, speech. Contains Parliamentary information licensed under the Open Parliament Licence v3.0, via TheyWorkForYou.
